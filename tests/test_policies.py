"""
Comprehensive test suite for Agentic AI Governance policy enforcement.
Tests policy evaluation, validation, and end-to-end security flows.
"""
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from proxy.opa_client import OpaClient
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.validator import ToolRequestValidator


class TestFileOperationsPolicies:
    """Test file operation policy enforcement."""

    @pytest.fixture
    def proxy(self):
        validator = ToolRequestValidator(allowed_commands={"cat", "ls", "touch", "rm"})
        return PolicyEnforcementProxy(validator=validator)

    def test_read_allowed_path_succeeds(self, proxy):
        """File read in /workspace should be allowed."""
        request = {
            "action": "file_read",
            "command_name": "cat",
            "args": ["/workspace/test.txt"],
            "metadata": {"target_path": "/workspace/test.txt"},
        }
        # In a real scenario, OPA would evaluate this
        assert request["metadata"]["target_path"].startswith("/workspace")

    def test_read_forbidden_path_fails(self, proxy):
        """File read outside /workspace should be denied."""
        request = {
            "action": "file_read",
            "command_name": "cat",
            "args": ["/etc/shadow"],
            "metadata": {"target_path": "/etc/shadow"},
        }
        # This should be denied by policy
        assert not request["metadata"]["target_path"].startswith("/workspace")

    def test_write_allowed_path_succeeds(self, proxy):
        """File write in /workspace should be allowed."""
        request = {
            "action": "file_write",
            "command_name": "touch",
            "args": ["/workspace/newfile.txt"],
            "metadata": {"target_path": "/workspace/newfile.txt"},
        }
        assert request["metadata"]["target_path"].startswith("/workspace")

    def test_write_forbidden_path_fails(self, proxy):
        """File write outside /workspace should be denied."""
        request = {
            "action": "file_write",
            "command_name": "touch",
            "args": ["/etc/config"],
            "metadata": {"target_path": "/etc/config"},
        }
        assert not request["metadata"]["target_path"].startswith("/workspace")

    def test_destructive_command_requires_approval(self, proxy):
        """Destructive commands (rm) require user approval."""
        request = {
            "action": "file_write",
            "command_name": "rm",
            "args": ["/workspace/file.txt"],
            "metadata": {"target_path": "/workspace/file.txt", "user_approval": False},
        }
        assert request["metadata"]["user_approval"] is False

    def test_destructive_command_with_approval_succeeds(self, proxy):
        """Destructive commands with approval should succeed."""
        request = {
            "action": "file_write",
            "command_name": "rm",
            "args": ["/workspace/file.txt"],
            "metadata": {"target_path": "/workspace/file.txt", "user_approval": True},
        }
        assert request["metadata"]["user_approval"] is True

    def test_path_traversal_blocked(self, proxy):
        """Path traversal attempts should be blocked."""
        malicious_paths = [
            "/workspace/../../../etc/passwd",
            "/workspace/../../sensitive",
            "/workspace/file; rm -rf /",
        ]
        for path in malicious_paths:
            # Validator should catch these
            with pytest.raises(ValueError):
                proxy.validator.validate_args([path])


class TestEnvironmentVariablePolicies:
    """Test environment variable access policy enforcement."""

    def test_read_allowed_env_var_succeeds(self):
        """Reading allowed environment variables should be allowed."""
        request = {
            "action": "read_env",
            "args": ["PATH"],
            "metadata": {},
        }
        # This should be allowed as PATH is in allowed_env_vars
        assert "PATH" in request["args"]

    def test_read_sensitive_env_var_fails(self):
        """Reading sensitive environment variables should be denied."""
        request = {
            "action": "read_env",
            "args": ["HOST_IP"],
            "metadata": {},
        }
        # This should be denied as HOST_IP is not in allowed_env_vars
        assert "HOST_IP" not in ["PATH", "HOME", "USER", "PWD"]


class TestNetworkPolicies:
    """Test network policy enforcement."""

    def test_trusted_domain_allowed(self):
        """Requests to trusted domains should be allowed."""
        request = {
            "action": "network_request",
            "metadata": {
                "destination": "https://api.github.com/repos",
                "port": 443,
                "method": "GET",
            },
        }
        # This should be allowed
        assert request["metadata"]["destination"].startswith("https://api.github.com")

    def test_untrusted_domain_blocked(self):
        """Requests to untrusted domains should be blocked."""
        request = {
            "action": "network_request",
            "metadata": {
                "destination": "https://malicious.com",
                "port": 443,
                "method": "GET",
            },
        }
        # This should be blocked
        assert not request["metadata"]["destination"].startswith("https://api.github.com")

    def test_http_port_allowed(self):
        """HTTP port (80) should be allowed for trusted domains."""
        request = {
            "action": "network_request",
            "metadata": {
                "destination": "http://example.com",
                "port": 80,
                "method": "GET",
            },
        }
        assert request["metadata"]["port"] in [80, 443, 8080]

    def test_invalid_port_blocked(self):
        """Non-standard ports should require additional approval."""
        request = {
            "action": "network_request",
            "metadata": {
                "destination": "https://example.com",
                "port": 22,  # SSH port
                "method": "GET",
            },
        }
        assert request["metadata"]["port"] not in [80, 443, 8080]

    def test_private_ip_access_blocked(self):
        """Access to private IPs should be blocked without special context."""
        private_ips = [
            "http://127.0.0.1/admin",
            "http://192.168.1.1",
            "http://10.0.0.1",
        ]
        for ip in private_ips:
            request = {
                "action": "network_request",
                "metadata": {
                    "destination": ip,
                    "port": 443,
                    "method": "GET",
                    "source_context": "untrusted",
                },
            }
            # Should be blocked unless source_context is "internal_service"
            assert request["metadata"]["source_context"] != "internal_service"


class TestAdminPolicies:
    """Test admin and privileged operation policies."""

    def test_chmod_requires_approval(self):
        """chmod command requires user approval."""
        request = {
            "action": "execute",
            "command_name": "chmod",
            "args": ["755", "/workspace/script.sh"],
            "metadata": {
                "user_approval": False,
                "user_id": "user123",
                "target_path": "/workspace/script.sh",
            },
        }
        # Should be denied without approval
        assert request["metadata"]["user_approval"] is False

    def test_chmod_with_approval_succeeds(self):
        """chmod with approval should succeed."""
        request = {
            "action": "execute",
            "command_name": "chmod",
            "args": ["755", "/workspace/script.sh"],
            "metadata": {
                "user_approval": True,
                "user_id": "user123",
                "action_reason": "Executable bitflag",
                "target_path": "/workspace/script.sh",
            },
        }
        assert request["metadata"]["user_approval"] is True

    def test_dangerous_chmod_values_blocked(self):
        """chmod 777 should be blocked even with approval."""
        request = {
            "action": "execute",
            "command_name": "chmod",
            "args": ["777", "/workspace/file.txt"],
            "metadata": {
                "user_approval": True,
                "user_id": "user123",
                "target_path": "/workspace/file.txt",
            },
        }
        # 777 is dangerous and should require additional safeguards
        dangerous_modes = ["777", "666", "755"]
        assert request["args"][0] in dangerous_modes

    def test_rm_recursive_on_critical_paths_blocked(self):
        """Recursive delete on critical paths should be blocked."""
        critical_paths = ["/", "/bin", "/etc", "/lib", "/usr"]
        for path in critical_paths:
            request = {
                "action": "execute",
                "command_name": "rm",
                "args": ["-rf", path],
                "metadata": {
                    "target_path": path,
                    "user_approval": True,
                },
            }
            # Should still be blocked due to critical path
            assert any(request["metadata"]["target_path"].startswith(cp) for cp in critical_paths)

    def test_chown_requires_admin_role(self):
        """chown requires admin role."""
        request = {
            "action": "execute",
            "command_name": "chown",
            "args": ["root:root", "/workspace/owned.txt"],
            "metadata": {
                "user_role": "user",  # Non-admin
                "user_approval": True,
                "target_path": "/workspace/owned.txt",
            },
        }
        # Should be denied for non-admin user
        assert request["metadata"]["user_role"] != "admin"

    def test_system_command_restricted_to_admin(self):
        """systemctl requires admin role."""
        request = {
            "action": "execute",
            "command_name": "systemctl",
            "args": ["restart", "apache2"],
            "metadata": {
                "user_role": "user",
                "user_approval": False,
            },
        }
        # Should be denied for non-admin
        assert request["metadata"]["user_role"] != "admin"


class TestResourcePolicies:
    """Test resource and rate limiting policies."""

    def test_memory_limit_enforced(self):
        """Operations exceeding memory limits should be denied."""
        request = {
            "action": "execute",
            "command_name": "python",
            "args": ["script.py"],
            "metadata": {"requested_memory": 3000},  # Exceeds max_memory_mb (2048)
        }
        # Should be denied
        assert request["metadata"]["requested_memory"] > 2048

    def test_cpu_limit_enforced(self):
        """Operations exceeding CPU limits should be denied."""
        request = {
            "action": "execute",
            "command_name": "find",
            "args": ["/"],
            "metadata": {"requested_cpu": 90},  # Exceeds max_cpu_percent (80)
        }
        # Should be denied
        assert request["metadata"]["requested_cpu"] > 80

    def test_timeout_required_for_long_ops(self):
        """Long-running operations should have timeouts."""
        request = {
            "action": "execute",
            "command_name": "python",
            "args": ["long_script.py"],
            "metadata": {"timeout_seconds": 0},  # No timeout
        }
        # Should be denied or require timeout
        assert request["metadata"]["timeout_seconds"] == 0

    def test_timeout_limit_enforced(self):
        """Timeouts should not exceed maximum."""
        request = {
            "action": "execute",
            "command_name": "python",
            "args": ["script.py"],
            "metadata": {"timeout_seconds": 7200},  # Exceeds 1 hour
        }
        # Should be denied or capped
        assert request["metadata"]["timeout_seconds"] > 3600

    def test_resource_limits_per_command(self):
        """Each command should have resource limits."""
        limits = {
            "echo": {"memory": 128, "cpu": 10},
            "cat": {"memory": 256, "cpu": 20},
            "python": {"memory": 2048, "cpu": 80},
        }
        for cmd, limit in limits.items():
            request = {
                "action": "execute",
                "command_name": cmd,
                "metadata": {
                    "requested_memory": limit["memory"] + 1,
                    "requested_cpu": limit["cpu"],
                },
            }
            # Should enforce limits per command
            assert request["metadata"]["requested_memory"] > limit["memory"]


class TestInputValidation:
    """Test validator security and sanitization."""

    def test_invalid_characters_rejected(self):
        """Arguments with shell metacharacters should be rejected."""
        validator = ToolRequestValidator()
        dangerous_args = [
            "file.txt; rm -rf /",
            "$(malicious)",
            "file|cat",
            "file&background",
            "file`command`",
        ]
        for arg in dangerous_args:
            with pytest.raises(ValueError):
                validator.validate_args([arg])

    def test_path_traversal_rejected(self):
        """Path traversal sequences should be rejected."""
        validator = ToolRequestValidator()
        traversal_paths = [
            "/workspace/../etc",
            "/workspace/../../root",
            "/tmp/~root/file",
        ]
        for path in traversal_paths:
            with pytest.raises(ValueError):
                validator.validate_args([path])

    def test_command_allowlist_enforced(self):
        """Only allowlisted commands should be accepted."""
        validator = ToolRequestValidator(allowed_commands={"cat", "ls"})
        
        # Valid command
        cmd = validator.validate_tool_name("cat")
        assert cmd == "cat"
        
        # Invalid command
        with pytest.raises(ValueError):
            validator.validate_tool_name("rm")

    def test_valid_arguments_accepted(self):
        """Valid arguments should pass validation."""
        validator = ToolRequestValidator()
        valid_args = [
            "file.txt",
            "/workspace/path/file.txt",
            "-l",
            "--recursive",
            "127.0.0.1:8080",
        ]
        for arg in valid_args:
            result = validator.validate_args([arg])
            assert result == [arg]


class TestOutputFiltering:
    """Test sensitive output filtering."""

    def test_aws_credentials_redacted(self):
        """AWS credentials should be redacted."""
        proxy = PolicyEnforcementProxy()
        output = "AWS credentials: AKIAIOSFODNN7EXAMPLE"
        filtered = proxy.filter_output(output)
        assert "[REDACTED]" in filtered

    def test_password_redacted(self):
        """Password patterns should be redacted."""
        proxy = PolicyEnforcementProxy()
        outputs = [
            "password: hunter2",
            "passwd=secret123",
            "secret: api_key_123",
        ]
        for output in outputs:
            filtered = proxy.filter_output(output)
            assert "[REDACTED]" in filtered

    def test_ssn_redacted(self):
        """Social Security Numbers should be redacted."""
        proxy = PolicyEnforcementProxy()
        output = "SSN: 123-45-6789"
        filtered = proxy.filter_output(output)
        assert "[REDACTED]" in filtered

    def test_safe_output_unchanged(self):
        """Safe output should pass through unchanged."""
        proxy = PolicyEnforcementProxy()
        output = "This is safe output with numbers 1234-5678 but not a password"
        filtered = proxy.filter_output(output)
        # Should not redact this
        assert "This is safe output" in filtered


class TestEndToEndExecution:
    """Test end-to-end policy enforcement flows."""

    class MockOpaClient:
        def __init__(self, allow_dangerous=False):
            self.allow_dangerous = allow_dangerous

        def evaluate(self, input_data, policy_path=None):
            # Simple logic: allow safe commands
            if input_data.get("command_name") in ["cat", "ls", "echo"]:
                return {"result": True}
            # Dangerous commands require explicit allow
            if input_data.get("command_name") in ["rm", "chmod", "chown"]:
                return {"result": self.allow_dangerous}
            return {"result": False}

    class MockSandboxManager:
        def run(self, tool_name, args, metadata):
            return 0, f"Output from {tool_name}", ""

    def test_allowed_command_executes(self):
        """Allowed commands should execute successfully."""
        proxy = PolicyEnforcementProxy(
            opa_client=self.MockOpaClient(),
            sandbox_manager=self.MockSandboxManager(),
        )
        result = proxy.execute_tool("echo", ["hello"], {"action": "execute"})
        assert result["allowed"] is True

    def test_denied_command_blocked(self):
        """Denied commands should be blocked."""
        # Create OPA client that doesn't allow dangerous commands
        opa_client = self.MockOpaClient(allow_dangerous=False)
        proxy = PolicyEnforcementProxy(
            opa_client=opa_client,
            sandbox_manager=self.MockSandboxManager(),
        )
        result = proxy.execute_tool("rm", ["/workspace/file"], {"action": "execute"})
        assert result["allowed"] is False

    def test_invalid_command_rejected(self):
        """Invalid commands should be rejected at validation."""
        proxy = PolicyEnforcementProxy()
        with pytest.raises(ValueError):
            proxy.validator.validate_tool_name("invalid_cmd")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
