# Multi-Layered Policy Enforcement Framework for Secure Agentic AI Execution

Secure-by-design mediation layer that proxies all autonomous agent tool calls through OPA policy evaluation and a hardened Docker sandbox.

## Structure

- `src/proxy`: Policy enforcement and tool mediation logic
- `src/policies`: Rego policy definitions with default-deny controls
- `src/sandbox_manager`: Container sandbox orchestration for isolated execution
- `tests`: Unit tests for validation, sandbox behavior, and policy integration

## How it works

1. The autonomous agent sends a tool request to `PolicyEnforcementProxy`.
2. `ToolRequestValidator` sanitizes the command name and arguments using an allowlist.
3. `OpaClient` evaluates the structured request against `src/policies/policy.rego`.
4. If the policy allows execution, `DockerSandboxManager` runs the command in a hardened container.
5. The proxy filters output for secrets/PII and returns only safe results to the agent.

## Environment setup

These steps create a secure local environment for the tool.

1. Install Python 3.11 or newer.
2. Install Docker and ensure the daemon is running.
3. Install OPA from https://www.openpolicyagent.org/
4. Create the workspace directory used by sandboxed execution:

```bash
mkdir -p workspace
```

5. Install project dependencies:

```bash
python3 -m pip install -U pip
python3 -m pip install -e .[dev]
```

6. Start OPA with the current policy file:

```bash
opa run --server --set=decision_logs.console=true src/policies/policy.rego
```

7. Run the example proxy integration:

```bash
python src/main.py
```

## Production Readiness

This framework enforces:

- Deterministic policy decisions through OPA
- Default-deny execution for all agent tool calls
- Least privilege sandboxing for host access
- Sensitive output filtering before returning results to the agent
- Structured JSON audit logs for requests, decisions, and results

## Setup

1. Install dependencies for local development:

```bash
python3 -m pip install -U pip
python3 -m pip install -e .[dev]
```

2. Start OPA with the policy package:

```bash
opa run --server --set=decision_logs.console=true src/policies/policy.rego
```

3. Run the integration example:

```bash
python src/main.py
```

## Updating `policy.rego`

When changing policy rules, keep the following production controls in mind:

- Maintain `default allow = false` so every request is denied unless explicitly permitted.
- Keep the file write rule restricted to `/workspace` and avoid broad path grants.
- Only add trusted URLs to `allowed_network_destinations` and avoid wildcard or open host matching.
- Preserve the destructive command list and require `metadata.user_approval == true` for commands like `rm`, `chmod`, `chown`, `mv`, `rmdir`, and `dd`.
- Add any new command-specific validation rules in Rego rather than trusting agent-provided arguments.
- Log denials and decisions through OPA so audit evidence can be captured from the policy layer.

### How to test policy changes

1. Update `src/policies/policy.rego`.
2. Start or restart OPA with the policy file:

```bash
opa run --server --set=decision_logs.console=true src/policies/policy.rego
```

3. Use the sample integration or call OPA directly to validate behavior:

```bash
curl --header "Content-Type: application/json" \
  --data '{"input": {"tool":"echo","action":"execute","args":["hello"],"metadata":{"action":"execute"}}}' \
  http://localhost:8181/v1/data/policy/allow
```

4. Confirm the response is `true` only for allowed requests and `false` for denied requests.

5. Run unit tests after policy changes to ensure no behavior regressions:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -q
```

## Notes

- All tool calls must be routed through `PolicyEnforcementProxy`.
- The agent never invokes tools directly; it only submits requests to the proxy.
- Docker must be installed and running for sandboxed execution.
