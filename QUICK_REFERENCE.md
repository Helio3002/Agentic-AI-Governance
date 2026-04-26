# 🚀 Quick Reference Guide

## One-Liners

```bash
# Install everything
python3 -m pip install -e .[dev]

# Run all tests (no OPA required)
pytest tests/test_policies.py -v

# Run tests with coverage
pytest tests/ --cov=src --cov-report=html && open htmlcov/index.html

# Run integration tests (OPA server required)
opa run --server --set=decision_logs.console=true src/policies/policy.rego &
pytest tests/test_integration.py -v

# Test a specific policy module
pytest tests/test_policies.py::TestFileOperationsPolicies -v

# Run in Docker
docker-compose up

# Validate OPA policy syntax
opa check src/policies/policy.rego

# Test policy evaluation locally
opa eval -d src/policies/policy.rego -i test_data.json 'data.policy.allow'

# Generate test report
pytest tests/ --junit-xml=report.xml
```

---

## Test Categories

### By Policy Domain
```bash
pytest tests/test_policies.py::TestFileOperationsPolicies -v          # File access
pytest tests/test_policies.py::TestNetworkPolicies -v                 # Network access
pytest tests/test_policies.py::TestAdminPolicies -v                   # Privileged ops
pytest tests/test_policies.py::TestResourcePolicies -v                # Resource limits
```

### By Feature
```bash
pytest tests/test_policies.py::TestInputValidation -v                 # Validation
pytest tests/test_policies.py::TestOutputFiltering -v                 # Output filtering
pytest tests/test_policies.py::TestEndToEndExecution -v               # End-to-end
```

### Integration Tests
```bash
pytest tests/test_integration.py -v                                    # All integration tests
pytest tests/test_integration.py::TestOpaIntegration -v                # OPA integration
pytest tests/test_integration.py::TestAuditLogging -v                  # Audit logging
```

---

## File Reference

### Policies
| File | Purpose |
|------|---------|
| `policy.rego` | Main policy, default-deny model |
| `file_operations.rego` | File system access control |
| `network_policies.rego` | Network access control |
| `admin_policies.rego` | Privileged operations |
| `resource_policies.rego` | Resource & rate limits |

### Tests
| File | Tests | Focus |
|------|-------|-------|
| `test_policies.py` | 34 | Core functionality |
| `test_integration.py` | 15 | OPA server integration |
| `test_fixtures.py` | Helpers | Mock clients & data |
| `conftest.py` | Fixtures | Shared test setup |

### Documentation
| File | Purpose |
|------|---------|
| `TEST_ENVIRONMENT_SETUP.md` | Complete setup guide |
| `src/policies/README.md` | Policy architecture |
| `POLICIES_AND_TESTS_SUMMARY.md` | Overview & status |

---

## Common Tasks

### Add a New Test
```python
def test_my_new_feature(self):
    """Test description."""
    request = TestDataGenerator.file_read_request("/workspace/file.txt")
    assert request["metadata"]["target_path"].startswith("/workspace")
```

### Modify a Policy
```bash
1. vim src/policies/your_policy.rego
2. opa check src/policies/your_policy.rego
3. pytest tests/test_policies.py -v
```

### Debug a Failing Test
```bash
pytest tests/test_policies.py::TestClass::test_name -v -s --pdb
```

### View Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Configuration

### Allowed Commands
Edit `src/proxy/validator.py` - DEFAULT_ALLOWED_COMMANDS

### Allowed Domains
Edit `src/policies/network_policies.rego` - allowed_domains

### Allowed Paths
Edit `src/policies/file_operations.rego`:
- `allowed_read_paths`
- `allowed_write_paths`

### Resource Limits
Edit `src/policies/resource_policies.rego`:
- `max_memory_mb` (default: 2048)
- `max_cpu_percent` (default: 80)
- `max_disk_gb` (default: 10)

---

## Test Data

### Generate Requests
```python
from tests.test_fixtures import TestDataGenerator

gen = TestDataGenerator()
file_req = gen.file_read_request("/workspace/file.txt")
net_req = gen.network_request("https://api.github.com")
exec_req = gen.execute_request("echo", ["hello"])
priv_req = gen.privileged_execute_request("chmod", ["755", "script.sh"])
```

### Sample Payloads
```python
from tests.fixtures import SAMPLE_PAYLOADS

payload = SAMPLE_PAYLOADS["safe_file_read"]
payload = SAMPLE_PAYLOADS["destructive_with_approval"]
payload = SAMPLE_PAYLOADS["trusted_api_call"]
```

---

## Environment Setup

### Local Development
```bash
# Requires: Python 3.11+, OPA (optional)
python3 -m pip install -e .[dev]
pytest tests/test_policies.py -v
```

### With OPA Server
```bash
# Terminal 1: Start OPA
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# Terminal 2: Run tests
pytest tests/test_integration.py -v
```

### Docker
```bash
docker-compose up     # Run all tests in container
```

---

## Troubleshooting

### OPA Server Not Responding
```bash
# Check if running
curl http://localhost:8181/health

# Restart
pkill opa
opa run --server src/policies/policy.rego
```

### Import Errors
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/
```

### Policy Syntax Error
```bash
opa check src/policies/policy.rego
opa eval -d src/policies/policy.rego 'data.policy'
```

### Test Collection Issues
```bash
pytest tests/ --collect-only  # See what tests are found
```

---

## Performance Tips

1. Run unit tests only (no OPA server needed): `pytest tests/test_policies.py -v`
2. Use `-x` to stop on first failure: `pytest -x`
3. Run specific test class: `pytest tests/test_policies.py::TestInputValidation`
4. Parallel execution: `pytest -n auto` (requires pytest-xdist)

---

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run tests
  run: |
    python -m pip install -e .[dev]
    pytest tests/ --junit-xml=report.xml --cov=src
```

### Docker
```bash
docker-compose up --abort-on-container-exit
```

### Pre-commit Hook
```bash
#!/bin/bash
pytest tests/test_policies.py -v --tb=short
```

---

## Status Dashboard

```
Policies:        5 files ✅
Tests:          34 unit + 15 integration ✅
Documentation:  3 comprehensive guides ✅
Fixtures:       Mock clients, sample data ✅
Automation:     Docker, quick_start.sh ✅
```

---

**Last Updated**: April 2026  
**Status**: Production Ready  
**All Tests**: ✅ PASSING
