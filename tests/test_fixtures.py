"""
Test fixtures and utilities for policy testing.
Provides mock clients, test data, and setup helpers.
"""
import json
from pathlib import Path
from typing import Any, Dict, List


class MockOpaClient:
    """Mock OPA client for testing without running an actual OPA server."""

    def __init__(self, allow_by_default: bool = False, custom_rules: Dict[str, bool] = None):
        self.allow_by_default = allow_by_default
        self.custom_rules = custom_rules or {}
        self.call_history: List[Dict[str, Any]] = []

    def evaluate(self, input_data: Dict[str, Any], policy_path: str = None) -> Dict[str, Any]:
        """Evaluate policy with simple rules for testing."""
        self.call_history.append({"input": input_data, "policy_path": policy_path})

        # Check custom rules first
        for rule_key, rule_result in self.custom_rules.items():
            if self._matches_rule(input_data, rule_key):
                return {"result": [{"expressions": [{"value": rule_result}]}]}

        # Default behavior
        return {"result": [{"expressions": [{"value": self.allow_by_default}]}]}

    def _matches_rule(self, input_data: Dict[str, Any], rule_key: str) -> bool:
        """Check if input matches a rule key."""
        if rule_key == "safe_commands":
            return input_data.get("command_name") in ["cat", "ls", "echo", "find"]
        if rule_key == "workspace_only_write":
            path = input_data.get("metadata", {}).get("target_path", "")
            return path.startswith("/workspace")
        if rule_key == "trusted_domains":
            domain = input_data.get("metadata", {}).get("destination", "")
            trusted = ["https://api.github.com", "https://example.com"]
            return any(domain.startswith(d) for d in trusted)
        return False


class MockSandboxManager:
    """Mock sandbox manager for testing tool execution."""

    def __init__(self, mock_outputs: Dict[str, tuple] = None):
        """
        Args:
            mock_outputs: Dict mapping tool_name to (exit_code, stdout, stderr)
        """
        self.mock_outputs = mock_outputs or {}
        self.execution_history: List[Dict[str, Any]] = []

    def run(self, tool_name: str, args: List[str], metadata: Dict[str, Any]) -> tuple:
        """Execute tool and return (exit_code, stdout, stderr)."""
        self.execution_history.append(
            {
                "tool": tool_name,
                "args": args,
                "metadata": metadata,
            }
        )

        if tool_name in self.mock_outputs:
            return self.mock_outputs[tool_name]

        # Default mock responses by tool
        if tool_name == "echo":
            return 0, f"echo: {' '.join(args)}", ""
        elif tool_name == "cat":
            return 0, f"content of {args[0] if args else 'file'}", ""
        elif tool_name == "ls":
            return 0, "file1.txt\nfile2.txt", ""
        elif tool_name in ["rm", "chmod", "chown"]:
            return 0, "", ""

        return 1, "", f"Command {tool_name} not found"


class TestDataGenerator:
    """Generate test data for policy testing."""

    @staticmethod
    def file_read_request(
        path: str,
        command: str = "cat",
        user_id: str = "user123",
        **metadata
    ) -> Dict[str, Any]:
        """Generate a file read request."""
        return {
            "action": "file_read",
            "command_name": command,
            "args": [path],
            "metadata": {
                "target_path": path,
                "user_id": user_id,
                **metadata,
            },
        }

    @staticmethod
    def file_write_request(
        path: str,
        command: str = "touch",
        user_id: str = "user123",
        user_approval: bool = False,
        **metadata
    ) -> Dict[str, Any]:
        """Generate a file write request."""
        return {
            "action": "file_write",
            "command_name": command,
            "args": [path],
            "metadata": {
                "target_path": path,
                "user_id": user_id,
                "user_approval": user_approval,
                **metadata,
            },
        }

    @staticmethod
    def network_request(
        destination: str,
        method: str = "GET",
        port: int = 443,
        **metadata
    ) -> Dict[str, Any]:
        """Generate a network request."""
        return {
            "action": "network_request",
            "command_name": "curl",
            "args": [destination],
            "metadata": {
                "destination": destination,
                "method": method,
                "port": port,
                **metadata,
            },
        }

    @staticmethod
    def execute_request(
        command: str,
        args: List[str] = None,
        user_id: str = "user123",
        user_approval: bool = False,
        **metadata
    ) -> Dict[str, Any]:
        """Generate an execute request."""
        return {
            "action": "execute",
            "command_name": command,
            "args": args or [],
            "metadata": {
                "user_id": user_id,
                "user_approval": user_approval,
                **metadata,
            },
        }

    @staticmethod
    def privileged_execute_request(
        command: str,
        args: List[str] = None,
        user_id: str = "admin123",
        user_role: str = "admin",
        user_approval: bool = True,
        action_reason: str = "Authorized operation",
        **metadata
    ) -> Dict[str, Any]:
        """Generate a privileged execute request."""
        return {
            "action": "execute",
            "command_name": command,
            "args": args or [],
            "metadata": {
                "user_id": user_id,
                "user_role": user_role,
                "user_approval": user_approval,
                "action_reason": action_reason,
                **metadata,
            },
        }


class PolicyTestHelper:
    """Helper functions for policy testing."""

    @staticmethod
    def load_policy_file(policy_path: str) -> str:
        """Load a Rego policy file."""
        path = Path(policy_path)
        if not path.exists():
            raise FileNotFoundError(f"Policy file not found: {policy_path}")
        return path.read_text()

    @staticmethod
    def validate_policy_syntax(policy_content: str) -> bool:
        """Basic syntax validation for Rego policies."""
        required_keywords = ["package"]
        return all(keyword in policy_content for keyword in required_keywords)

    @staticmethod
    def extract_policy_rules(policy_content: str) -> List[str]:
        """Extract rule names from Rego policy."""
        rules = []
        for line in policy_content.split("\n"):
            line = line.strip()
            if line.startswith("allow") or line.startswith("deny"):
                rule_name = line.split(" ")[0]
                if rule_name not in rules:
                    rules.append(rule_name)
        return rules

    @staticmethod
    def create_audit_log(request: Dict[str, Any], decision: bool, reason: str = "") -> Dict[str, Any]:
        """Create an audit log entry."""
        return {
            "timestamp": "2024-01-01T00:00:00Z",  # Would use real timestamp
            "request": request,
            "decision": decision,
            "reason": reason,
        }


# Test data constants
SAFE_WORKSPACE_PATH = "/workspace/safefile.txt"
UNSAFE_SYSTEM_PATH = "/etc/passwd"
TRUSTED_API = "https://api.github.com"
UNTRUSTED_DOMAIN = "https://malicious.com"

SAFE_COMMANDS = ["cat", "ls", "echo", "find", "grep"]
DANGEROUS_COMMANDS = ["rm", "chmod", "chown", "dd"]

APPROVED_USER_METADATA = {
    "user_id": "user123",
    "user_role": "admin",
    "user_approval": True,
    "action_reason": "Authorized operation",
}

UNAUTHORIZED_USER_METADATA = {
    "user_id": "user456",
    "user_role": "user",
    "user_approval": False,
}
