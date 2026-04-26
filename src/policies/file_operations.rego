package policy.file_operations

# File operations policy module
# Restricts file operations to safe directories and prevents dangerous patterns

import data.policy

allowed_read_paths = {
    "/workspace",
    "/tmp",
    "/etc/hostname",
    "/etc/timezone",
}

allowed_write_paths = {
    "/workspace",
}

destructive_write_commands = {"rm", "rmdir", "dd"}
safe_read_commands = {"cat", "ls", "find", "grep", "wc"}
write_commands = {"touch", "mkdir", "cp"}

# Allow safe read operations on permitted paths
allow_file_read {
    input.action == "file_read"
    input.command_name == cmd
    safe_read_commands[cmd]
    input.metadata.target_path != ""
    path_allowed_for_read(input.metadata.target_path)
}

# Allow safe write operations on permitted paths (non-destructive)
allow_file_write {
    input.action == "file_write"
    input.command_name == cmd
    write_commands[cmd]
    not cmd in destructive_write_commands
    input.metadata.target_path != ""
    path_allowed_for_write(input.metadata.target_path)
}

# Deny destructive writes unless explicitly approved
deny_unsafe_delete {
    input.action == "file_write"
    input.command_name == cmd
    cmd in destructive_write_commands
    input.metadata.user_approval != true
}

# Check if path is allowed for reading
path_allowed_for_read(path) {
    some allowed_path
    allowed_path := allowed_read_paths[_]
    regex.match(sprintf("^%s(/.*)?$", [regex.quote(allowed_path)]), path)
}

# Check if path is allowed for writing
path_allowed_for_write(path) {
    some allowed_path
    allowed_path := allowed_write_paths[_]
    regex.match(sprintf("^%s(/.*)?$", [regex.quote(allowed_path)]), path)
}

# Deny access outside allowed paths
deny_path_traversal {
    input.metadata.target_path
    not path_allowed_for_read(input.metadata.target_path)
    not path_allowed_for_write(input.metadata.target_path)
}

# Block suspicious patterns
deny_suspicious_patterns {
    input.metadata.target_path
    regex.match(".*[;|&$`].*", input.metadata.target_path)
}
