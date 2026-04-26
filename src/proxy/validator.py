from __future__ import annotations

import re
from typing import Iterable, List

DEFAULT_ALLOWED_COMMANDS = {
    "cat",
    "chmod",
    "chown",
    "curl",
    "echo",
    "find",
    "grep",
    "ls",
    "mv",
    "python",
    "rm",
    "sed",
    "tar",
    "touch",
    "wc",
}

ARGUMENT_PATTERN = re.compile(r"^[A-Za-z0-9_./:-]+$")
FORBIDDEN_PATH_SEGMENTS = {"..", "~"}


class ToolRequestValidator:
    """Validates command and argument inputs for secure agent tooling.

    SECURITY NOTE: Prevents prompt injection and path traversal by enforcing
    strict, allowlisted request shapes.
    """

    def __init__(self, allowed_commands: Iterable[str] = DEFAULT_ALLOWED_COMMANDS) -> None:
        self.allowed_commands = set(allowed_commands)

    def validate_tool_name(self, tool_name: str) -> str:
        if not tool_name or not ARGUMENT_PATTERN.fullmatch(tool_name):
            raise ValueError(f"Invalid tool name: {tool_name}")
        if tool_name not in self.allowed_commands:
            raise ValueError(f"Tool is not in the allowlist: {tool_name}")
        return tool_name

    def validate_args(self, args: List[str]) -> List[str]:
        sanitized_args: List[str] = []
        for arg in args:
            if not arg or not ARGUMENT_PATTERN.fullmatch(arg):
                raise ValueError(f"Invalid argument: {arg}")
            if any(segment in arg for segment in FORBIDDEN_PATH_SEGMENTS):
                raise ValueError(f"Forbidden path segment in argument: {arg}")
            sanitized_args.append(arg)
        return sanitized_args
