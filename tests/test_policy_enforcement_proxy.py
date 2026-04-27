import json
import tempfile
import unittest
from pathlib import Path

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

    def test_execute_tool_writes_audit_log_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            audit_path = Path(tmpdir) / "audit_log.jsonl"
            proxy = PolicyEnforcementProxy(
                opa_client=FakeOpaClient(),
                sandbox_manager=FakeSandboxManager(),
                audit_log_path=audit_path,
            )
            result = proxy.execute_tool("echo", ["test"], {"action": "execute"})
            self.assertTrue(result["allowed"])

            self.assertTrue(audit_path.exists())
            with audit_path.open("r", encoding="utf-8") as audit_file:
                lines = [json.loads(line) for line in audit_file if line.strip()]

            event_types = [line["event"] for line in lines]
            self.assertIn("policy_request", event_types)
            self.assertIn("policy_decision", event_types)
            self.assertIn("tool_result", event_types)

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
