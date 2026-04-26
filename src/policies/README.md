# Agentic AI Governance Policies

This directory contains OPA (Open Policy Agent) policies that enforce security controls for AI agent tool execution. Policies are written in Rego and provide deterministic decision-making for all sensitive operations.

## Policy Architecture

The policy framework is organized into modular components:

### 1. **policy.rego** - Main Policy
The primary policy file that implements default-deny security and handles:
- Command execution validation
- Network access controls  
- File operation restrictions
- Destructive command approval requirements

### 2. **file_operations.rego** - File System Access
Controls file read/write operations with:
- Allowed paths for reading (`/workspace`, `/tmp`, `/etc/hostname`, etc.)
- Allowed paths for writing (`/workspace` only)
- Path traversal prevention
- Dangerous command restrictions (`rm`, `rmdir`, `dd`)

### 3. **network_policies.rego** - Network Access
Manages external network communications:
- Allowlisted domains (`https://api.github.com`, `https://api.openai.com`, etc.)
- Allowed ports (80, 443, 8080)
- Private IP access prevention
- DNS rebinding attack prevention

### 4. **admin_policies.rego** - Privileged Operations
Enforces strict controls on privileged commands:
- User approval requirements for dangerous operations
- Role-based access control (admin-only commands)
- Protection against chmod/chown abuse
- Critical path deletion prevention
- Audit logging requirements

### 5. **resource_policies.rego** - Resource Limits
Prevents resource exhaustion and abuse:
- Memory limits per operation (max 2048 MB)
- CPU limits (max 80%)
- Timeout requirements for long-running ops
- Rate limiting for different operation types
- Command-specific resource constraints

## Policy Evaluation Flow

```
Request → Validator → OPA Policy Engine → Decision (Allow/Deny)
                         ↓
                    Policy Modules
                         ↓
                   Decision Logs & Audit
```

## Default-Deny Security Model

All policies follow a **default-deny** principle:
- Every action is blocked unless explicitly allowed
- Rules must pass ALL deny conditions and match at least one allow condition
- Absence of a rule acts as an implicit denial

Example:
```rego
default allow = false  # Everything denied by default

allow {
    input.action == "execute"
    input.command_name in safe_commands
    not denied[_]
}
```

## Policy Authoring Guidelines

### Adding a New Policy Rule

1. **Define the rule clearly**
   ```rego
   allow {
       input.action == "new_action"
       condition_1
       condition_2
       not denied[_]
   }
   ```

2. **Add corresponding deny rules**
   ```rego
   denied[msg] {
       input.action == "new_action"
       unsafe_condition
       msg = sprintf("Action denied: %s", [reason])
   }
   ```

3. **Test the rule**
   ```bash
   opa eval -d src/policies/policy.rego -i test_data.json 'data.policy.allow'
   ```

### Best Practices

- **Explicit Allowlists**: Use allowlists (`allowed_commands`, `allowed_domains`) rather than denylists
- **Meaningful Denial Messages**: Provide clear reasons in denial messages
- **Input Validation**: Validate all inputs before making decisions
- **Logging**: Log all policy decisions for audit trails
- **Testing**: Write tests for both allow and deny scenarios
- **Documentation**: Comment non-obvious policy logic
- **Versioning**: Update version tags when changing policies

## Policy Configuration

### Allowed Commands

Default allowed commands (in `src/proxy/validator.py`):
```python
DEFAULT_ALLOWED_COMMANDS = {
    "cat", "chmod", "chown", "curl", "echo", "find", "grep",
    "ls", "mv", "python", "rm", "sed", "tar", "touch", "wc"
}
```

To modify:
1. Update `DEFAULT_ALLOWED_COMMANDS` in `validator.py`
2. Update policy rules in policy files
3. Test with `pytest tests/test_validator.py`

### Allowed Domains

Update in `src/policies/network_policies.rego`:
```rego
allowed_domains = {
    "https://api.github.com",
    "https://api.openai.com",
    "https://example.com",
    "https://api.trusted.ai",
}
```

### Allowed Paths

Update in `src/policies/file_operations.rego`:
```rego
allowed_read_paths = {
    "/workspace",
    "/tmp",
    "/etc/hostname",
}

allowed_write_paths = {
    "/workspace",
}
```

### Resource Limits

Update in `src/policies/resource_policies.rego`:
```rego
max_memory_mb = 2048
max_cpu_percent = 80
max_disk_gb = 10

resource_limits = {
    "python": {"memory": 2048, "cpu": 80},
    "curl": {"memory": 1024, "cpu": 50},
}
```

## Testing Policies

### Run Unit Tests

```bash
# Test all policies
pytest tests/test_policies.py -v

# Test specific policy module
pytest tests/test_policies.py::TestFileOperationsPolicies -v
pytest tests/test_policies.py::TestNetworkPolicies -v
pytest tests/test_policies.py::TestAdminPolicies -v
pytest tests/test_policies.py::TestResourcePolicies -v
```

### Test with OPA CLI

```bash
# Validate policy syntax
opa check src/policies/policy.rego

# Test policy evaluation locally
opa eval -d src/policies/policy.rego 'data.policy'

# Test with sample data
cat > /tmp/request.json << 'EOF'
{
  "command_name": "cat",
  "action": "execute",
  "args": ["/workspace/file.txt"],
  "metadata": {"target_path": "/workspace/file.txt"}
}
EOF

opa eval -d src/policies/policy.rego -i /tmp/request.json 'data.policy.allow'
```

### Integration Tests

```bash
# Start OPA server
opa run --server --set=decision_logs.console=true src/policies/policy.rego &

# Run integration tests
pytest tests/test_integration.py -v

# Kill OPA server
pkill opa
```

## Audit and Logging

All policy decisions are logged with:
- **Timestamp**: When the decision was made
- **Request**: Full request details
- **Decision**: Allow or Deny
- **Reason**: Why the decision was made
- **User**: User ID making the request
- **Audit ID**: Unique identifier for traceability

Example log entry:
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "request_id": "req-001",
  "action": "file_read",
  "command": "cat",
  "target": "/workspace/README.md",
  "user_id": "user123",
  "decision": "ALLOW",
  "reason": "Path allowed: /workspace"
}
```

View logs in OPA:
```bash
# OPA console logs (when running with --set=decision_logs.console=true)
opa run --server --set=decision_logs.console=true src/policies/policy.rego
```

## Production Readiness Checklist

- [ ] All policies have been reviewed for security
- [ ] Allowlists are conservative (minimum permissions)
- [ ] Testing covers both allow and deny scenarios
- [ ] Audit logging is configured
- [ ] Performance has been profiled
- [ ] Failover behavior is defined
- [ ] Regular policy audits are scheduled
- [ ] Documentation is up to date
- [ ] Version control is in place
- [ ] Monitoring and alerting are configured

## Troubleshooting

### Policy Not Working as Expected

1. **Check syntax**
   ```bash
   opa check src/policies/policy.rego
   ```

2. **Test isolated rule**
   ```bash
   opa eval -d src/policies/policy.rego 'data.policy.file_operations.allow_file_read'
   ```

3. **Debug with sample data**
   ```bash
   opa eval -d src/policies/policy.rego -i sample_request.json 'data.policy'
   ```

### Performance Issues

- Check policy complexity with `opa eval ... -explain full`
- Profile with `opa eval ... --metrics`
- Consider caching frequently evaluated policies

### Permission Denied Unexpectedly

1. Verify request structure matches policy expectations
2. Check all deny rules aren't matching
3. Verify allow rule conditions are met
4. Review audit logs for detailed denial reasons

## Policy Updates

### Making Policy Changes

1. **Create a branch**
   ```bash
   git checkout -b update-file-policy
   ```

2. **Modify policy files**
   ```bash
   vim src/policies/file_operations.rego
   ```

3. **Test thoroughly**
   ```bash
   pytest tests/test_policies.py -v
   ```

4. **Document changes**
   - Update this README
   - Add comments in policy file
   - Create changelog entry

5. **Create pull request**
   ```bash
   git push origin update-file-policy
   ```

6. **Review and merge**
   - Get security review
   - Verify tests pass
   - Merge to main

### Deployment

For production systems:
1. Blue-green deployment with old/new policies running
2. Monitor decision logs for anomalies
3. Gradual rollout with percentage-based routing
4. Rollback plan in case of issues

## References

- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)
- [Rego Language Guide](https://www.openpolicyagent.org/docs/latest/policy-language/)
- [OPA Best Practices](https://www.openpolicyagent.org/docs/latest/terraform/)
- [OWASP Security Guidelines](https://owasp.org/)

## Support

For issues or questions about policies:
1. Check existing issues in the repository
2. Review policy test cases in `tests/test_policies.py`
3. Consult the main README security section
4. Create a new issue with policy details
