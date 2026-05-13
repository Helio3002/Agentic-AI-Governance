package policy

import future.keywords.in

default allow = false

# SECURITY NOTE: Default-deny ensures that any action not explicitly allowed is blocked.

allowed_network_destinations = {
    "https://example.com",
    "https://api.trusted.ai",
    "https://api.github.com",
    "https://openai.com",
}

allowed_env_vars = {"PATH", "HOME", "USER", "PWD"}

sensitive_patterns = [
    "(?:AKIA|ASIA)[A-Z0-9]{16}",
    "(?:\\bpassword\\b|\\bpasswd\\b|\\bsecret\\b)\\s*[:=]\\s*\\S+",
    "\\b\\d{3}-\\d{2}-\\d{4}\\b",
]

destructive_commands = {"rm", "chmod", "chown", "mv", "rmdir", "dd"}

write_path_allowed(path) if {
    startswith(path, "/workspace")
}

network_allowed(destination) if startswith(destination, "https://api.github.com")
network_allowed(destination) if startswith(destination, "https://openai.com")
network_allowed(destination) if destination == "https://example.com"
network_allowed(destination) if destination == "https://api.trusted.ai"

is_destructive if {
    input.command_name == cmd
    destructive_commands[cmd]
}

contains_sensitive(content) if {
    some pat in sensitive_patterns
    regex.match(pat, content)
}

recursive_rm if {
    input.command_name == "rm"
    some i
    flag := input.args[i]
    flag == "-r"
}

recursive_rm if {
    input.command_name == "rm"
    some i
    flag := input.args[i]
    flag == "-rf"
}

recursive_rm if {
    input.command_name == "rm"
    some i
    flag := input.args[i]
    flag == "--recursive"
}

is_sensitive_env_var(var) if {
    not allowed_env_vars[var]
}

denied contains msg if {
    input.action == "execute"
    some i
    flag := input.args[i]
    write_path_flag(flag)
    path := input.args[i+1]
    not write_path_allowed(path)
    msg := sprintf("write access denied outside /workspace: %s", [path])
}

denied contains msg if {
    input.action == "network_request"
    not network_allowed(input.metadata.destination)
    msg := sprintf("network destination denied: %s", [input.metadata.destination])
}

denied contains msg if {
    input.action == "network_request"
    some idx
    argument := input.args[idx]
    contains_sensitive(argument)
    not network_allowed(input.metadata.destination)
    msg := sprintf("exfiltration of sensitive data to unauthorized destination denied: %s", [input.metadata.destination])
}

denied contains msg if {
    input.action == "file_write"
    recursive_rm
    not input.metadata.hitl_authorized
    msg := "recursive delete denied without HITL authorization"
}

denied contains msg if {
    input.action == "file_read"
    some i
    path := input.args[i]
    not startswith(path, "/workspace")
    not path in ["/etc/hostname", "/etc/timezone"]
    msg := sprintf("file read denied outside /workspace: %s", [path])
}

denied contains msg if {
    input.action == "read_env"
    some i
    var := input.args[i]
    is_sensitive_env_var(var)
    msg := sprintf("access to sensitive environment variable denied: %s", [var])
}

allow if {
    input.action == "execute"
    count(denied) == 0
    not is_destructive
}

allow if {
    input.action == "execute"
    count(denied) == 0
    is_destructive
    input.metadata.user_approval == true
}

allow if {
    input.action == "read_env"
    count(denied) == 0
}

allow if {
    input.action == "file_read"
    count(denied) == 0
}

allow if {
    input.action == "file_write"
    count(denied) == 0
    not is_destructive
}

allow if {
    input.action == "file_write"
    count(denied) == 0
    is_destructive
    not recursive_rm
    input.metadata.user_approval == true
}

allow if {
    input.action == "file_write"
    count(denied) == 0
    recursive_rm
    input.metadata.user_approval == true
    input.metadata.hitl_authorized == true
}

allow if {
    input.action == "network_request"
    count(denied) == 0
}

write_path_flag(flag) if {
    flag == "-o"
}

write_path_flag(flag) if {
    flag == "--output"
}