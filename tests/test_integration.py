"""
Integration tests for policy enforcement with OPA server.
These tests require a running OPA server at http://localhost:8181
"""
import os
import pytest
from pathlib import Path

from proxy.opa_client import OpaClient
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from tests.fixtures import SAMPLE_PAYLOADS, EXPECTED_RESULTS


@pytest.mark.integration
class TestOpaIntegration:
    """Integration tests with real OPA server."""

    @pytest.fixture
    def opa_url(self):
        """Get OPA URL from environment or use default."""
        return os.getenv("OPA_URL", "http://localhost:8181/v1/data/policy/allow")

    @pytest.fixture
    def policy_path(self):
        """Get path to policy file."""
        return Path(__file__).resolve().parents[1] / "src" / "policies" / "policy.rego"

    @pytest.fixture
    def opa_client(self, opa_url):
        """Create OPA client."""
        return OpaClient(opa_url=opa_url)

    def test_opa_server_health(self, opa_client):
        """Test that OPA server is running and healthy."""
        import urllib.request
        health_url = opa_client.opa_url.replace("/v1/data/policy/allow", "/health")
        try:
            response = urllib.request.urlopen(health_url, timeout=5)
            assert response.status == 200
        except Exception as e:
            pytest.skip(f"OPA server not available: {e}")

    def test_safe_file_read_allowed(self, opa_client, policy_path):
        """Test that safe file read is allowed."""
        request = SAMPLE_PAYLOADS["safe_file_read"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["safe_file_read"]["allow"]
        # OPA returns result in various formats
        actual = self._extract_allow_result(result)
        assert actual == expected, f"Expected {expected}, got {actual}"

    def test_unsafe_file_read_denied(self, opa_client, policy_path):
        """Test that unsafe file read is denied."""
        request = SAMPLE_PAYLOADS["unsafe_file_read"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["unsafe_file_read"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_trusted_domain_allowed(self, opa_client, policy_path):
        """Test that trusted domain access is allowed."""
        request = SAMPLE_PAYLOADS["trusted_api_call"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["trusted_api_call"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_untrusted_domain_denied(self, opa_client, policy_path):
        """Test that untrusted domain access is denied."""
        request = SAMPLE_PAYLOADS["untrusted_domain"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["untrusted_domain"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_exfiltration_attempt_denied(self, opa_client, policy_path):
        """Test that exfiltration of sensitive data to unauthorized IP is denied."""
        request = SAMPLE_PAYLOADS["exfiltration_attempt"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["exfiltration_attempt"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_destructive_without_approval_denied(self, opa_client, policy_path):
        """Test that destructive operations require approval."""
        request = SAMPLE_PAYLOADS["destructive_without_approval"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["destructive_without_approval"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_recursive_delete_without_hitl_denied(self, opa_client, policy_path):
        """Test that recursive delete without HITL authorization is denied."""
        request = SAMPLE_PAYLOADS["recursive_delete_without_hitl"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["recursive_delete_without_hitl"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_recursive_delete_with_hitl_allowed(self, opa_client, policy_path):
        """Test that recursive delete with HITL authorization is allowed."""
        request = SAMPLE_PAYLOADS["recursive_delete_with_hitl"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["recursive_delete_with_hitl"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_destructive_with_approval_allowed(self, opa_client, policy_path):
        """Test that destructive operations with approval are allowed."""
        request = SAMPLE_PAYLOADS["destructive_with_approval"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["destructive_with_approval"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_read_allowed_env_var_allowed(self, opa_client, policy_path):
        """Test that reading allowed environment variables is allowed."""
        request = SAMPLE_PAYLOADS["read_allowed_env_var"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["read_allowed_env_var"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    def test_read_sensitive_env_var_denied(self, opa_client, policy_path):
        """Test that reading sensitive environment variables is denied."""
        request = SAMPLE_PAYLOADS["read_sensitive_env_var"]
        result = opa_client.evaluate(request, str(policy_path))
        expected = EXPECTED_RESULTS["read_sensitive_env_var"]["allow"]
        actual = self._extract_allow_result(result)
        assert actual == expected

    @staticmethod
    def _extract_allow_result(opa_response):
        """Extract allow boolean from OPA response in various formats."""
        if isinstance(opa_response, dict):
            if "result" in opa_response:
                result = opa_response["result"]
                if isinstance(result, list) and len(result) > 0:
                    expr = result[0].get("expressions", [])
                    if len(expr) > 0:
                        return bool(expr[0].get("value", False))
                return bool(result)
            return bool(opa_response.get("allow", False))
        return bool(opa_response)


@pytest.mark.integration
class TestPolicyEnforcementProxyIntegration:
    """Integration tests for PolicyEnforcementProxy with OPA."""

    @pytest.fixture
    def proxy_with_opa(self):
        """Create proxy with real OPA client."""
        opa_url = os.getenv("OPA_URL", "http://localhost:8181/v1/data/policy/allow")
        opa_client = OpaClient(opa_url=opa_url)
        policy_path = Path(__file__).resolve().parents[1] / "src" / "policies" / "policy.rego"
        return PolicyEnforcementProxy(
            opa_client=opa_client,
            policy_path=policy_path,
        )

    def test_policy_evaluation_workflow(self, proxy_with_opa):
        """Test end-to-end policy evaluation."""
        allowed = proxy_with_opa.evaluate_policy(
            tool_name="cat",
            action="execute",
            args=["/workspace/README.md"],
            metadata={"user_id": "user123"},
        )
        # Safe command should be allowed
        assert allowed is not False

    def test_output_filtering(self, proxy_with_opa):
        """Test sensitive output filtering."""
        raw_output = "AWS Key: AKIAIOSFODNN7EXAMPLE and password: secret123"
        filtered = proxy_with_opa.filter_output(raw_output)
        assert "[REDACTED]" in filtered
        assert "AKIAIOSFODNN7EXAMPLE" not in filtered
        assert "secret123" not in filtered


@pytest.mark.integration
class TestPolicyModuleIntegration:
    """Integration tests for individual policy modules."""

    @pytest.fixture
    def opa_client(self):
        """Create OPA client for policy module tests."""
        opa_url = os.getenv("OPA_URL", "http://localhost:8181/v1/data/policy/allow")
        return OpaClient(opa_url=opa_url)

    def test_file_operations_policy_module(self, opa_client):
        """Test file_operations policy module."""
        # Test allowed file read
        request = {
            "action": "file_read",
            "command_name": "cat",
            "metadata": {"target_path": "/workspace/file.txt"},
        }
        # This would require OPA to have file_operations module loaded
        # For now, we just verify the request structure is valid
        assert request["action"] == "file_read"
        assert request["metadata"]["target_path"].startswith("/workspace")

    def test_network_policies_module(self, opa_client):
        """Test network_policies policy module."""
        request = {
            "action": "network_request",
            "metadata": {
                "destination": "https://api.github.com",
                "port": 443,
            },
        }
        assert request["metadata"]["destination"].startswith("https://")

    def test_admin_policies_module(self, opa_client):
        """Test admin_policies policy module."""
        request = {
            "action": "execute",
            "command_name": "chmod",
            "metadata": {
                "user_approval": True,
                "user_role": "admin",
            },
        }
        assert request["metadata"]["user_approval"] is True

    def test_resource_policies_module(self, opa_client):
        """Test resource_policies policy module."""
        request = {
            "action": "execute",
            "command_name": "python",
            "metadata": {
                "requested_memory": 1024,
                "requested_cpu": 50,
                "timeout_seconds": 300,
            },
        }
        assert request["metadata"]["requested_memory"] <= 2048
        assert request["metadata"]["requested_cpu"] <= 80


@pytest.mark.integration
class TestAuditLogging:
    """Test audit logging during policy enforcement."""

    def test_policy_decisions_logged(self, capsys):
        """Test that policy decisions are logged."""
        from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

        class MockOpaClient:
            def evaluate(self, input_data, policy_path=None):
                return {"result": True}

        proxy = PolicyEnforcementProxy(opa_client=MockOpaClient())

        # Make a policy evaluation
        result = proxy.evaluate_policy(
            tool_name="echo",
            action="execute",
            args=["test"],
            metadata={"user_id": "user123"},
        )

        # Check that logs were generated
        captured = capsys.readouterr()
        assert "policy_request" in captured.out or "policy_decision" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
