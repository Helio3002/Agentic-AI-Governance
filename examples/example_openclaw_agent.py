#!/usr/bin/env python3
"""
OpenClaw Agent Integration with Agentic AI Governance

This template shows how to integrate OpenClaw with the secure proxy.
Replace the direct tool executions in your OpenClaw agent with proxy calls.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient
from sandbox_manager.docker_sandbox import DockerSandboxManager


class OpenClawAgent:
    """OpenClaw Agent with secure tool execution."""

    def __init__(self):
        workspace_dir = Path(__file__).resolve().parents[1] / "workspace"
        workspace_dir.mkdir(parents=True, exist_ok=True)

        try:
            sandbox = DockerSandboxManager(workspace_dir=workspace_dir)
            opa_client = OpaClient(opa_url="")  # Use local OPA if available
            self.proxy = PolicyEnforcementProxy(opa_client=opa_client, sandbox_manager=sandbox)
            print("🔒 OpenClaw Agent secured with Agentic AI Governance")
            self.ready = True
        except Exception as e:
            print(f"⚠️  Proxy setup failed: {e}")
            print("💡 Install Docker and OPA, then restart")
            self.proxy = None
            self.ready = False

    def execute_tool(self, tool_name: str, args: list = None, metadata: dict = None) -> dict:
        """
        Secure tool execution method.
        Replace your OpenClaw tool calls with this.
        """
        if not self.ready:
            return {"error": "Proxy not ready", "allowed": False}

        if args is None:
            args = []
        if metadata is None:
            metadata = {"source": "openclaw_agent", "action": "execute"}

        print(f"🔧 OpenClaw executing: {tool_name} {' '.join(args)}")

        # This is the key integration point
        result = self.proxy.execute_tool(tool_name, args, metadata)

        if not result.get("allowed", False):
            print(f"❌ Denied: {result.get('reason', 'Policy violation')}")
        else:
            print(f"✅ Executed successfully")

        return result

    # Example OpenClaw tool methods - adapt these to your actual tools

    def list_directory(self, path: str = "/workspace") -> dict:
        """List directory contents."""
        return self.execute_tool("ls", ["-la", path], {"description": f"List {path}"})

    def read_file(self, file_path: str) -> dict:
        """Read file content."""
        return self.execute_tool("cat", [file_path], {"description": f"Read {file_path}"})

    def search_files(self, pattern: str, directory: str = "/workspace") -> dict:
        """Find files matching pattern."""
        return self.execute_tool("find", [directory, "-name", pattern], {"description": f"Find {pattern} in {directory}"})

    def run_command(self, command: str, args: list = None) -> dict:
        """Run a custom command."""
        if args is None:
            args = []
        return self.execute_tool(command, args, {"description": f"Run {command}"})


# Example usage
if __name__ == "__main__":
    agent = OpenClawAgent()

    # Test the integration
    print("\n🚀 Testing OpenClaw Integration")
    print("=" * 40)

    # Example 1: List directory
    result = agent.list_directory()
    print("List result:", result)

    # Example 2: Read file
    result = agent.read_file("GUIDE.md")
    print("Read result:", result)

    # Example 3: Search files
    result = agent.search_files("*.md")
    print("Search result:", result)