package policy

default allow = false

# SECURITY NOTE: Default-deny ensures that any action not explicitly allowed is blocked.

allowed_network_destinations = {
    "https://example.com",
    "https://api.trusted.ai",
}

destructive_commands = {"rm", "chmod", "chown", "mv", "rmdir", "dd"}

write_path_allowed(path) if {
    startswith(path, "/workspace")
}

network_allowed(destination) if {
    destination == allowed_network_destinations[_]
}

is_destructive if {
    input.command_name == cmd
    destructive_commands[cmd]
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
    input.metadata.action == "network"
    not network_allowed(input.metadata.destination)
    msg := sprintf("network destination denied: %s", [input.metadata.destination])
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

write_path_flag(flag) if {
    flag == "-o"
}

write_path_flag(flag) if {
    flag == "--output"
}