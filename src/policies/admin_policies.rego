package policy.admin_policies

# Admin and privileged operations policies
# Enforces strict controls on system-level operations

# Privileged operations that require explicit approval
privileged_commands = {
    "chmod",
    "chown",
    "dd",
    "mv",
    "rmdir",
    "rm",
}

# System-level operations
system_commands = {
    "systemctl",
    "service",
    "usermod",
    "groupadd",
}

# Allow privileged commands only with user approval and audit context
allow_privileged_operation {
    input.action == "execute"
    input.command_name == cmd
    cmd in privileged_commands
    input.metadata.user_approval == true
    input.metadata.user_id != ""
    input.metadata.action_reason != ""
}

# Deny privileged commands without approval
deny_privileged_without_approval {
    input.action == "execute"
    input.command_name == cmd
    cmd in privileged_commands
    input.metadata.user_approval != true
}

# Restrict system commands to admin-only contexts
allow_system_command {
    input.action == "execute"
    input.command_name == cmd
    cmd in system_commands
    input.metadata.user_role == "admin"
    input.metadata.user_approval == true
}

# Safeguard specific dangerous patterns with chmod
deny_chmod_abuse {
    input.action == "execute"
    input.command_name == "chmod"
    some i
    arg := input.args[i]
    (arg == "777" ; arg == "666" ; arg == "777" ; arg == "755")
    not input.metadata.user_approval
}

# Prevent rm -rf on system critical paths
deny_recursive_delete_critical {
    input.action == "execute"
    input.command_name == "rm"
    some i
    arg := input.args[i]
    arg == "-rf"
    contains_critical_path(input.metadata.target_path)
}

# Critical paths that should never be recursively deleted
critical_paths = {
    "/",
    "/bin",
    "/etc",
    "/lib",
    "/usr",
    "/var",
    "/sys",
    "/proc",
    "/dev",
    "/boot",
    "/root",
}

contains_critical_path(path) {
    some critical
    critical := critical_paths[_]
    startswith(path, critical)
}

# Log all privileged operations for audit
deny_unaudited_privileged {
    input.action == "execute"
    input.command_name == cmd
    cmd in privileged_commands
    input.metadata.audit_id == ""
}
