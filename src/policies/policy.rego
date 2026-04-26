package policy

default allow = false

# SECURITY NOTE: Default-deny ensures that any action not explicitly allowed is blocked.

allowed_network_destinations = {
    "https://example.com",
    "https://api.trusted.ai",
}

destructive_commands = {"rm", "chmod", "chown", "mv", "rmdir", "dd"}

write_path_allowed(path) {
    startswith(path, "/workspace")
}

network_allowed(destination) {
    destination == allowed_network_destinations[_]
}

is_destructive {
    input.command_name == cmd
    destructive_commands[cmd]
}

denied[msg] {
    input.action == "execute"
    some i
    flag := input.args[i]
    write_path_flag(flag)
    path := input.args[i+1]
    not write_path_allowed(path)
    msg = sprintf("write access denied outside /workspace: %s", [path])
}

denied[msg] {
    input.metadata.action == "network"
    not network_allowed(input.metadata.destination)
    msg = sprintf("network destination denied: %s", [input.metadata.destination])
}

allow {
    input.action == "execute"
    not denied[_]
    not is_destructive
}

allow {
    input.action == "execute"
    not denied[_]
    is_destructive
    input.metadata.user_approval == true
}

write_path_flag(flag) {
    flag == "-o"
    flag == "--output"
}
