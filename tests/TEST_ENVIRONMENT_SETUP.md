# Test Environment Setup Guide

This guide will help you set up a complete test environment for testing Agentic AI Governance policies and the policy enforcement proxy.

## Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
python3 -m pip install -U pip
python3 -m pip install -e .[dev]

# Install OPA (Open Policy Agent)
# macOS
brew install opa

# Linux
curl https://openpolicyagent.org/downloads/latest/opa_linux_x86_64 -o opa
chmod +x opa
sudo mv opa /usr/local/bin/
```

### 2. Create Workspace Directory

```bash
mkdir -p workspace
```

## Environment Setup Options

### Option 1: Minimal Testing (No OPA Server)

For basic unit tests without running an actual OPA server:

```bash
# Run tests with mock OPA client
pytest tests/test_policies.py -v

# Run specific test class
pytest tests/test_policies.py::TestFileOperationsPolicies -v

# Run with coverage
pytest tests/test_policies.py --cov=src --cov-report=html
```

### Option 2: Local OPA Server Testing

For integration testing with a running OPA server:

#### Terminal 1: Start OPA Server

```bash
# Start OPA with the main policy
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# OPA will be available at http://localhost:8181
# Test the server health:
curl http://localhost:8181/health
```

#### Terminal 2: Run Integration Tests

```bash
# Run all tests
pytest tests/ -v

# Run with detailed logging
pytest tests/ -v -s

# Run only integration tests
pytest tests/test_integration.py -v
```

### Option 3: Docker-Based Test Environment

Use Docker for isolated, reproducible testing:

```bash
# Build test environment
docker-compose up -d

# Run tests inside container
docker-compose exec ai-governance pytest tests/ -v

# View logs
docker-compose logs -f opa
```

See `docker-compose.yml` for the full setup.

## Test Organization

```
tests/
├── conftest.py              # Pytest configuration and shared fixtures
├── test_policies.py         # Comprehensive policy tests
├── test_fixtures.py         # Mock clients and test data generators
├── test_integration.py      # End-to-end integration tests (if OPA is running)
├── test_validator.py        # Input validation tests
├── test_policy_enforcement_proxy.py  # Proxy behavior tests
└── fixtures/
    ├── sample_payloads.json # Sample request payloads
    ├── audit_logs.json      # Sample audit logs
    └── policies/            # Policy files for testing
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# File operations policies
pytest tests/test_policies.py::TestFileOperationsPolicies -v

# Network policies
pytest tests/test_policies.py::TestNetworkPolicies -v

# Admin policies
pytest tests/test_policies.py::TestAdminPolicies -v

# Resource policies
pytest tests/test_policies.py::TestResourcePolicies -v

# Input validation
pytest tests/test_policies.py::TestInputValidation -v

# Output filtering
pytest tests/test_policies.py::TestOutputFiltering -v

# End-to-end execution
pytest tests/test_policies.py::TestEndToEndExecution -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Run Tests with Markers

```bash
# Run only unit tests
pytest tests/ -m unit -v

# Run only integration tests (requires OPA server)
pytest tests/ -m integration -v

# Run except slow tests
pytest tests/ -m "not slow" -v
```

## Debugging Tests

### Enable Verbose Output

```bash
pytest tests/test_policies.py -v -s
```

### Run Single Test

```bash
pytest tests/test_policies.py::TestFileOperationsPolicies::test_read_allowed_path_succeeds -v
```

### Use PDB for Debugging

```bash
pytest tests/test_policies.py --pdb
```

### Generate JUnit XML Report

```bash
pytest tests/ --junit-xml=test_report.xml
```

## Testing Policies

### Test a Specific Policy Module

```bash
# Test file operations policy
opa eval -d src/policies/file_operations.rego 'data.policy.file_operations'

# Test network policy
opa eval -d src/policies/network_policies.rego 'data.policy.network_policies'

# Test admin policy
opa eval -d src/policies/admin_policies.rego 'data.policy.admin_policies'
```

### Test Policy with Sample Data

```bash
# Create a test request
cat > /tmp/test_request.json << 'EOF'
{
  "command_name": "cat",
  "action": "execute",
  "args": ["/workspace/test.txt"],
  "metadata": {
    "target_path": "/workspace/test.txt",
    "user_id": "user123"
  }
}
EOF

# Evaluate policy against request
opa eval -d src/policies/policy.rego -i /tmp/test_request.json 'data.policy.allow'
```

## Test Fixtures

The test suite includes fixtures in `tests/test_fixtures.py`:

### MockOpaClient

Mock OPA client for testing without a real OPA server:

```python
from tests.test_fixtures import MockOpaClient

# Allow all commands by default
mock_client = MockOpaClient(allow_by_default=True)

# Allow specific commands
mock_client = MockOpaClient(custom_rules={"safe_commands": True})
```

### MockSandboxManager

Mock sandbox for testing command execution:

```python
from tests.test_fixtures import MockSandboxManager

# Use default mock responses
mock_sandbox = MockSandboxManager()

# Define custom responses
custom_outputs = {
    "echo": (0, "mocked output", ""),
    "cat": (0, "file content", ""),
}
mock_sandbox = MockSandboxManager(mock_outputs=custom_outputs)
```

### TestDataGenerator

Generate test data:

```python
from tests.test_fixtures import TestDataGenerator

# Generate file read request
read_req = TestDataGenerator.file_read_request("/workspace/file.txt")

# Generate network request
net_req = TestDataGenerator.network_request("https://api.github.com")

# Generate privileged execute request
priv_req = TestDataGenerator.privileged_execute_request("chmod", ["755", "/workspace/script.sh"])
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Policies

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install -U pip
          python -m pip install -e .[dev]
      - name: Run tests
        run: pytest tests/ -v --cov=src
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### OPA Server Connection Issues

```bash
# Check OPA is running
curl http://localhost:8181/health

# View OPA logs
# Check /tmp/opa_output.log or terminal output
```

### Test Import Errors

```bash
# Verify PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Verify conftest.py is loading paths correctly
pytest tests/ -v --co  # Show all collected tests
```

### Policy Evaluation Failures

```bash
# Validate policy syntax
opa check src/policies/policy.rego

# Test policy evaluation locally
opa eval -d src/policies/policy.rego 'data.policy'
```

## Performance Testing

### Profile Policy Evaluation

```bash
pytest tests/test_policies.py --profile
```

### Load Test Policy Server

```bash
# Use Apache Bench or similar
ab -n 1000 -c 10 http://localhost:8181/v1/data/policy/allow
```

## Sample Test Scenarios

### Scenario 1: File Access Control

```python
# Allowed: /workspace files
assert policy_allows_read("/workspace/config.json")
assert policy_allows_write("/workspace/output.txt")

# Denied: system files
assert not policy_allows_read("/etc/passwd")
assert not policy_allows_write("/root/.ssh/id_rsa")
```

### Scenario 2: Network Access Control

```python
# Allowed: trusted domains
assert policy_allows_network("https://api.github.com/repos")

# Denied: untrusted domains
assert not policy_allows_network("https://malicious.com")
assert not policy_allows_network("http://192.168.1.1")
```

### Scenario 3: Privileged Operations

```python
# Denied: without approval
assert not policy_allows_execute("rm", ["/workspace/file"], approval=False)

# Allowed: with approval
assert policy_allows_execute("rm", ["/workspace/file"], approval=True)

# Denied: even with approval (critical path)
assert not policy_allows_execute("rm", ["-rf", "/"], approval=True)
```

## Next Steps

1. Run `pytest tests/ -v` to execute all tests
2. Check coverage with `pytest tests/ --cov=src`
3. Add new tests in `tests/test_policies.py` for new policy rules
4. Create integration tests in `tests/test_integration.py` for end-to-end flows
5. Set up CI/CD pipeline for continuous testing

For more information, see the main [README.md](../README.md).
