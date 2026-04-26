#!/usr/bin/env python3
"""
Example: IBM AI Agent Integration with Agentic AI Governance

This example shows how an IBM AI agent (or any AI agent) can safely execute
system commands using the Policy Enforcement Proxy.
"""

import json
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy


class IBMAgentExample:
    """Example IBM AI Agent that uses secure command execution."""

    def __init__(self):
        try:
            self.proxy = PolicyEnforcementProxy()
            print("🤖 IBM AI Agent initialized with secure proxy")
            self.ready = True
        except Exception as e:
            print(f"⚠️  Warning: Proxy initialization failed: {e}")
            print("💡 To run fully: start OPA server and configure sandbox manager")
            self.proxy = None
            self.ready = False

    def analyze_file(self, file_path: str) -> dict:
        """Analyze a file safely using the proxy."""
        if not self.ready:
            return {"error": "Proxy not configured", "simulation": f"Would analyze {file_path}"}

        print(f"📊 Analyzing file: {file_path}")

        # Use proxy instead of direct system calls
        result = self.proxy.execute_tool(
            "wc",  # word count command
            ["-l", file_path],  # count lines
            {
                "source": "ibm_agent",
                "action": "analyze",
                "user_approval": False
            }
        )

        return result

    def list_directory(self, directory: str = "/workspace") -> dict:
        """List directory contents safely."""
        if not self.ready:
            return {"error": "Proxy not configured", "simulation": f"Would list {directory}"}

        print(f"📁 Listing directory: {directory}")

        result = self.proxy.execute_tool(
            "ls",
            ["-la", directory],
            {
                "source": "ibm_agent",
                "action": "list",
                "user_approval": False
            }
        )

        return result

    def search_text(self, pattern: str, file_path: str) -> dict:
        """Search for text in a file safely."""
        if not self.ready:
            return {"error": "Proxy not configured", "simulation": f"Would search '{pattern}' in {file_path}"}

        print(f"🔍 Searching for '{pattern}' in {file_path}")

        result = self.proxy.execute_tool(
            "grep",
            [pattern, file_path],
            {
                "source": "ibm_agent",
                "action": "search",
                "user_approval": False
            }
        )

        return result

    def create_summary_report(self) -> dict:
        """Create a summary report of workspace analysis."""
        if not self.ready:
            return {"error": "Proxy not configured", "simulation": "Would create summary report"}

        print("📋 Creating summary report")

        # Multiple safe operations
        results = {}

        # Count files
        file_count = self.proxy.execute_tool(
            "find",
            ["/workspace", "-type", "f", "-name", "*.md"],
            {"source": "ibm_agent", "action": "count"}
        )

        # Get disk usage
        disk_usage = self.proxy.execute_tool(
            "du",
            ["-sh", "/workspace"],
            {"source": "ibm_agent", "action": "usage"}
        )

        results["file_count"] = file_count
        results["disk_usage"] = disk_usage

        return results


def main():
    """Demonstrate IBM AI Agent with secure proxy."""
    print("🚀 IBM AI Agent Example with Agentic AI Governance")
    print("=" * 60)

    agent = IBMAgentExample()

    # Example 1: Analyze a file
    print("\n1️⃣ File Analysis Example:")
    result = agent.analyze_file("GUIDE.md")
    print(f"Result: {json.dumps(result, indent=2)}")

    # Example 2: List directory
    print("\n2️⃣ Directory Listing Example:")
    result = agent.list_directory()
    print(f"Result: {json.dumps(result, indent=2)}")

    # Example 3: Search text
    print("\n3️⃣ Text Search Example:")
    result = agent.search_text("AI", "GUIDE.md")
    print(f"Result: {json.dumps(result, indent=2)}")

    # Example 4: Summary report
    print("\n4️⃣ Summary Report Example:")
    result = agent.create_summary_report()
    print(f"Result: {json.dumps(result, indent=2)}")

    if agent.ready:
        print("\n✅ All operations completed safely through the proxy!")
    else:
        print("\n💡 This is a simulation - to run fully:")
        print("   1. Start OPA server: docker-compose up opa")
        print("   2. Configure sandbox manager")
        print("   3. Run again for real execution")


if __name__ == "__main__":
    main()