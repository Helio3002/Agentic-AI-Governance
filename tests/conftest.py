"""
Pytest configuration and shared fixtures.
"""
import sys
from pathlib import Path

import pytest

# Add src directory to path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))

from proxy.opa_client import OpaClient
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.validator import ToolRequestValidator


@pytest.fixture
def validator():
    """Fixture for ToolRequestValidator."""
    return ToolRequestValidator()


@pytest.fixture
def opa_client():
    """Fixture for OpaClient."""
    return OpaClient()


@pytest.fixture
def policy_proxy(validator, opa_client):
    """Fixture for PolicyEnforcementProxy."""
    return PolicyEnforcementProxy(
        opa_client=opa_client,
        validator=validator,
    )


@pytest.fixture
def mock_opa_client():
    """Fixture for MockOpaClient that simulates OPA responses."""
    class MockOpaClient:
        def evaluate(self, input_data, policy_path=None):
            # Simple policy logic for testing
            if input_data.get("action") == "execute":
                cmd = input_data.get("command_name", "")
                # Allow safe commands
                if cmd in ["cat", "ls", "echo", "find"]:
                    return {"result": [{"expressions": [{"value": True}]}]}
                # Require approval for dangerous commands
                if cmd in ["rm", "chmod", "chown"]:
                    has_approval = input_data.get("metadata", {}).get("user_approval", False)
                    return {"result": [{"expressions": [{"value": has_approval}]}]}
            return {"result": [{"expressions": [{"value": False}]}]}

    return MockOpaClient()


@pytest.fixture
def mock_sandbox_manager():
    """Fixture for MockSandboxManager that simulates sandbox execution."""
    class MockSandboxManager:
        def __init__(self):
            self.call_history = []

        def run(self, tool_name, args, metadata):
            self.call_history.append((tool_name, args, metadata))
            # Return different outputs based on tool
            if tool_name == "echo":
                return 0, " ".join(args), ""
            elif tool_name == "cat":
                return 0, f"contents of {args[0] if args else 'file'}", ""
            elif tool_name == "ls":
                return 0, "file1.txt\nfile2.txt\nfile3.txt", ""
            return 0, "", ""

    return MockSandboxManager()


@pytest.fixture
def sample_file_request():
    """Sample file access request for testing."""
    return {
        "action": "file_read",
        "command_name": "cat",
        "args": ["/workspace/test.txt"],
        "metadata": {
            "target_path": "/workspace/test.txt",
            "user_id": "user123",
        },
    }


@pytest.fixture
def sample_network_request():
    """Sample network request for testing."""
    return {
        "action": "network_request",
        "command_name": "curl",
        "args": ["https://api.github.com"],
        "metadata": {
            "destination": "https://api.github.com",
            "port": 443,
            "method": "GET",
            "user_id": "user123",
        },
    }


@pytest.fixture
def sample_execute_request():
    """Sample command execution request for testing."""
    return {
        "action": "execute",
        "command_name": "echo",
        "args": ["hello", "world"],
        "metadata": {
            "user_id": "user123",
            "user_approval": False,
        },
    }


# Pytest markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests requiring external services")
    config.addinivalue_line("markers", "slow: slow running tests")
    config.addinivalue_line("markers", "security: security-related tests")
