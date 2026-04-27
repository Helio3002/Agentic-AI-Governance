#!/usr/bin/env python3
"""
OpenClaw Agent Integration Script with Agentic AI Governance

This script demonstrates secure tool execution for OpenClaw agents.
It wraps the PolicyEnforcementProxy for seamless integration.

Usage:
    1. Start OPA: opa run --server --set=decision_logs.console=true src/policies/policy.rego
    2. Run this script: python examples/openclaw_integration.py
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient
from sandbox_manager.docker_sandbox import DockerSandboxManager


class OpenClawIntegration:
    """Secure integration layer for OpenClaw agents."""

    def __init__(self, workspace_dir: Optional[str] = None, opa_url: str = ""):
        """
        Initialize OpenClaw integration with secure proxy.

        Args:
            workspace_dir: Optional custom workspace directory
            opa_url: OPA server URL (empty string for local evaluation)
        """
        self.workspace_dir = Path(workspace_dir) if workspace_dir else Path.cwd() / "workspace"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        self.execution_history = []
        self.ready = False

        try:
            sandbox = DockerSandboxManager(workspace_dir=self.workspace_dir)
            opa_client = OpaClient(opa_url=opa_url)
            self.proxy = PolicyEnforcementProxy(
                opa_client=opa_client,
                sandbox_manager=sandbox
            )
            self.ready = True
            print("✅ OpenClaw secure proxy initialized")
        except Exception as e:
            print(f"❌ Failed to initialize proxy: {e}")
            print("📌 Ensure Docker is running and OPA server is available")
            self.proxy = None

    def execute(
        self,
        command: str,
        args: Optional[List[str]] = None,
        description: str = "",
        user_approval: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a command safely through the secure proxy.

        Args:
            command: Command to execute (e.g., 'ls', 'cat', 'grep')
            args: List of command arguments
            description: Human-readable description of the action
            user_approval: Whether user approved this action

        Returns:
            Dictionary with execution result
        """
        if not self.ready:
            return {
                "allowed": False,
                "error": "Proxy not initialized",
                "timestamp": datetime.now().isoformat()
            }

        if args is None:
            args = []

        # Build metadata for audit logging
        metadata = {
            "source": "openclaw_agent",
            "action": "execute",
            "description": description,
            "user_approval": user_approval,
            "timestamp": datetime.now().isoformat()
        }

        print(f"\n🔧 Executing: {command} {' '.join(args)}")
        if description:
            print(f"   📝 {description}")

        try:
            result = self.proxy.execute_tool(command, args, metadata)

            # Track execution
            self.execution_history.append({
                "command": command,
                "args": args,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

            # Print result
            if result.get("allowed"):
                print(f"   ✅ Success (exit code: {result.get('exit_code')})")
                if result.get("stdout"):
                    print(f"   Output: {result['stdout'][:100]}...")
            else:
                print(f"   ❌ Denied: {result.get('reason', 'Policy violation')}")

            return result

        except Exception as e:
            error_result = {
                "allowed": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.execution_history.append({
                "command": command,
                "args": args,
                "result": error_result,
                "timestamp": datetime.now().isoformat()
            })
            print(f"   ❌ Error: {e}")
            return error_result

    # Common tool wrappers for OpenClaw

    def list_directory(self, path: str = "/workspace") -> Dict[str, Any]:
        """List files and directories."""
        return self.execute(
            "ls",
            ["-la", path],
            f"List directory contents: {path}"
        )

    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read file content."""
        return self.execute(
            "cat",
            [file_path],
            f"Read file: {file_path}"
        )

    def write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Write content to a file."""
        temp_file = self.workspace_dir / Path(file_path).name
        temp_file.write_text(content)
        return self.execute(
            "cp",
            [str(temp_file), file_path],
            f"Write to file: {file_path}"
        )

    def search_text(self, pattern: str, file_path: str) -> Dict[str, Any]:
        """Search for text in a file."""
        return self.execute(
            "grep",
            ["-n", pattern, file_path],
            f"Search for '{pattern}' in {file_path}"
        )

    def find_files(self, pattern: str, directory: str = "/workspace") -> Dict[str, Any]:
        """Find files matching a pattern."""
        return self.execute(
            "find",
            [directory, "-name", pattern],
            f"Find files matching '{pattern}' in {directory}"
        )

    def execute_script(self, script_path: str, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute a shell script."""
        if args is None:
            args = []
        return self.execute(
            "bash",
            [script_path] + args,
            f"Execute script: {script_path}"
        )

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file metadata and information."""
        return self.execute(
            "stat",
            [file_path],
            f"Get file info: {file_path}"
        )

    def word_count(self, file_path: str) -> Dict[str, Any]:
        """Count lines, words, and characters in a file."""
        return self.execute(
            "wc",
            ["-l", "-w", "-c", file_path],
            f"Word count for: {file_path}"
        )

    def print_execution_history(self) -> None:
        """Print all executed commands and their results."""
        print("\n📋 Execution History")
        print("=" * 60)
        for i, entry in enumerate(self.execution_history, 1):
            allowed = entry["result"].get("allowed", False)
            status = "✅" if allowed else "❌"
            print(f"{i}. {status} {entry['command']} {' '.join(entry.get('args', []))}")
            print(f"   Time: {entry['timestamp']}")
            if not allowed:
                print(f"   Reason: {entry['result'].get('reason', 'Unknown')}")
        print("=" * 60)

    def export_audit_summary(self, output_file: str = "openclaw_audit_summary.json") -> None:
        """Export execution history to JSON file."""
        summary = {
            "total_executions": len(self.execution_history),
            "allowed_count": sum(1 for e in self.execution_history if e["result"].get("allowed")),
            "denied_count": sum(1 for e in self.execution_history if not e["result"].get("allowed")),
            "history": self.execution_history
        }
        with open(output_file, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Audit summary exported to {output_file}")


def run_demo():
    """Run demonstration of OpenClaw integration."""
    print("🚀 OpenClaw Integration Demo")
    print("=" * 60)

    # Initialize integration
    agent = OpenClawIntegration(workspace_dir=str(Path.cwd() / "workspace"))

    if not agent.ready:
        print("⚠️  Cannot run demo - proxy not ready")
        print("   Check that Docker is running and OPA server is started")
        return

    # Demo commands
    demo_commands = [
        ("list_directory", lambda: agent.list_directory("/workspace")),
        ("read_file", lambda: agent.read_file("GUIDE.md")),
        ("find_files", lambda: agent.find_files("*.md")),
        ("word_count", lambda: agent.word_count("GUIDE.md")),
        ("search_text", lambda: agent.search_text("secure", "GUIDE.md")),
    ]

    for i, (name, command_func) in enumerate(demo_commands, 1):
        print(f"\n{i}. Testing: {name}")
        try:
            result = command_func()
            if result.get("allowed"):
                print(f"   ✅ Command allowed")
                output = result.get("stdout", "")
                if len(output) > 200:
                    print(f"   Output (first 200 chars): {output[:200]}...")
                else:
                    print(f"   Output: {output}")
            else:
                print(f"   ❌ Command denied")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Print history
    agent.print_execution_history()

    # Export audit summary
    agent.export_audit_summary("openclaw_audit_summary.json")

    print("\n📝 Integration test completed!")
    print("📍 Check 'logs/audit_log.jsonl' for detailed audit logs")
    print("📍 Check 'openclaw_audit_summary.json' for execution summary")


if __name__ == "__main__":
    run_demo()
