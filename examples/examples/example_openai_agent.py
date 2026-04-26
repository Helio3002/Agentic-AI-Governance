#!/usr/bin/env python3
"""
Example: OpenAI Agent Integration with Agentic AI Governance

This example shows how an OpenAI agent (or similar) can safely execute
system commands using the Policy Enforcement Proxy with function calling.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy


class OpenAIAgentExample:
    """Example OpenAI Agent that uses secure command execution."""

    def __init__(self):
        try:
            self.proxy = PolicyEnforcementProxy()
            print("🤖 OpenAI Agent initialized with secure proxy")
            self.ready = True
        except Exception as e:
            print(f"⚠️  Warning: Proxy initialization failed: {e}")
            print("💡 To run fully: start OPA server and configure sandbox manager")
            self.proxy = None
            self.ready = False

    def execute_safe_command(self, command: str, args: list = None, description: str = "") -> Dict[str, Any]:
        """
        Function that can be called by OpenAI function calling.
        This is the main integration point for OpenAI agents.
        """
        if not self.ready:
            return {
                "error": "Proxy not configured",
                "simulation": f"Would execute: {command} {' '.join(args or [])}",
                "description": description
            }

        if args is None:
            args = []

        print(f"🔧 Executing safe command: {command} {' '.join(args)}")
        if description:
            print(f"📝 Description: {description}")

        # Call the secure proxy instead of direct execution
        result = self.proxy.execute_tool(
            command,
            args,
            {
                "source": "openai_agent",
                "action": "execute",
                "description": description,
                "user_approval": False
            }
        )

        return result

    def read_file_content(self, file_path: str) -> Dict[str, Any]:
        """OpenAI function: Read file content safely."""
        return self.execute_safe_command(
            "cat",
            [file_path],
            f"Reading content of {file_path}"
        )

    def list_files(self, directory: str = "/workspace") -> Dict[str, Any]:
        """OpenAI function: List directory contents safely."""
        return self.execute_safe_command(
            "ls",
            ["-la", directory],
            f"Listing contents of {directory}"
        )

    def find_files(self, pattern: str, directory: str = "/workspace") -> Dict[str, Any]:
        """OpenAI function: Find files matching a pattern."""
        return self.execute_safe_command(
            "find",
            [directory, "-name", pattern],
            f"Finding files matching '{pattern}' in {directory}"
        )

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """OpenAI function: Get detailed file information."""
        return self.execute_safe_command(
            "stat",
            [file_path],
            f"Getting information about {file_path}"
        )


# OpenAI Function Schema (for function calling)
OPENAI_FUNCTIONS = [
    {
        "name": "execute_safe_command",
        "description": "Execute a system command safely through security proxy",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute (e.g., 'ls', 'cat', 'find')"
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Command arguments as array of strings"
                },
                "description": {
                    "type": "string",
                    "description": "Description of what this command does"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "read_file_content",
        "description": "Read and return the content of a file safely",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "list_files",
        "description": "List files and directories in a given path",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list (defaults to /workspace)",
                    "default": "/workspace"
                }
            }
        }
    }
]


def simulate_openai_conversation():
    """Simulate how an OpenAI agent would use the secure proxy."""
    print("🚀 OpenAI Agent Simulation with Agentic AI Governance")
    print("=" * 60)

    agent = OpenAIAgentExample()

    # Simulate OpenAI function calls
    test_calls = [
        {
            "function": "list_files",
            "args": {},
            "description": "List workspace contents"
        },
        {
            "function": "read_file_content",
            "args": {"file_path": "GUIDE.md"},
            "description": "Read the main guide file"
        },
        {
            "function": "find_files",
            "args": {"pattern": "*.md", "directory": "/workspace"},
            "description": "Find all markdown files"
        },
        {
            "function": "execute_safe_command",
            "args": {
                "command": "wc",
                "args": ["-l", "GUIDE.md"],
                "description": "Count lines in guide file"
            },
            "description": "Execute word count command"
        }
    ]

    for i, call in enumerate(test_calls, 1):
        print(f"\n{i}️⃣ Simulating OpenAI function call: {call['function']}")
        print(f"   {call['description']}")

        try:
            if call["function"] == "list_files":
                result = agent.list_files(**call["args"])
            elif call["function"] == "read_file_content":
                result = agent.read_file_content(**call["args"])
            elif call["function"] == "find_files":
                result = agent.find_files(**call["args"])
            elif call["function"] == "execute_safe_command":
                result = agent.execute_safe_command(**call["args"])

            print(f"   ✅ Result: {json.dumps(result, indent=2)}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    if agent.ready:
        print("\n✅ All operations completed safely through the proxy!")
    else:
        print("\n💡 This is a simulation - to run fully:")
        print("   1. Start OPA server: docker-compose up opa")
        print("   2. Configure sandbox manager")
        print("   3. Run again for real execution")

    print("\n🎯 OpenAI Function Schema for Reference:")
    print(json.dumps(OPENAI_FUNCTIONS, indent=2))


def main():
    """Run the OpenAI agent example."""
    simulate_openai_conversation()


if __name__ == "__main__":
    main()