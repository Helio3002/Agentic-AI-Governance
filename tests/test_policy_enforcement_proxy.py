import unittest

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy


class FakeOpaClient:
    def evaluate(self, input_data, policy_path):
        return {"result": [{"expressions": [{"value": True}]}]}


class FakeSandboxManager:
    def run(self, tool_name, args, metadata):
        return 0, "safe output", ""


class PolicyEnforcementProxyTest(unittest.TestCase):
    def setUp(self):
        self.proxy = PolicyEnforcementProxy(
            opa_client=FakeOpaClient(),
            sandbox_manager=FakeSandboxManager(),
        )

    def test_sanitize_argument_rejects_invalid_chars(self):
        with self.assertRaises(ValueError):
            self.proxy.sanitize_argument("rm; echo malicious")

    def test_filter_output_redacts_secrets(self):
        raw = "my password: hunter2"
        filtered = self.proxy.filter_output(raw)
        self.assertIn("[REDACTED]", filtered)

    def test_execute_tool_returns_allowed_result(self):
        result = self.proxy.execute_tool("echo", ["test"], {"action": "execute"})
        self.assertTrue(result["allowed"])
        self.assertEqual(result["stdout"], "safe output")


if __name__ == "__main__":
    unittest.main()
