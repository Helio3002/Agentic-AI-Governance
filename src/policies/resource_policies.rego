package policy.resource_policies

# Resource and rate limiting policies
# Prevents abuse and ensures fair usage

# Rate limiting windows (requests per hour)
rate_limits = {
    "api_calls": 1000,
    "file_operations": 500,
    "network_requests": 100,
    "execute": 50,
}

# Resource constraints
max_memory_mb = 2048
max_cpu_percent = 80
max_disk_gb = 10

# Resource limits per operation type
resource_limits = {
    "echo": {"memory": 128, "cpu": 10},
    "cat": {"memory": 256, "cpu": 20},
    "grep": {"memory": 512, "cpu": 30},
    "find": {"memory": 512, "cpu": 40},
    "curl": {"memory": 1024, "cpu": 50},
    "python": {"memory": 2048, "cpu": 80},
}

# Check rate limit for operation
rate_limit_exceeded {
    input.action == "execute"
    operation_rate_count := get_operation_count(input.command_name)
    limit := rate_limits[input.action]
    operation_rate_count > limit
}

# Mock function to get operation count (would be backed by real state)
get_operation_count(cmd) = 0 {
    true
}

# Check resource constraints
allow_resource_operation {
    input.action == "execute"
    cmd_resource_limits := resource_limits[input.command_name]
    cmd_resource_limits != null
    requested_memory := input.metadata.requested_memory
    requested_memory <= cmd_resource_limits.memory
    requested_cpu := input.metadata.requested_cpu
    requested_cpu <= cmd_resource_limits.cpu
}

allow_resource_operation {
    input.action == "execute"
    not resource_limits[input.command_name]  # Allow commands without specific limits
}

# Deny operations that exceed memory
deny_high_memory {
    input.action == "execute"
    input.metadata.requested_memory > max_memory_mb
}

# Deny operations that need excessive CPU
deny_high_cpu {
    input.action == "execute"
    input.metadata.requested_cpu > max_cpu_percent
}

# Timeout protection for long-running operations
allow_with_timeout {
    input.action == "execute"
    input.metadata.timeout_seconds > 0
    input.metadata.timeout_seconds <= 3600  # Max 1 hour
}

# Prevent infinite loops or hanging processes
deny_infinite_operations {
    input.action == "execute"
    input.metadata.timeout_seconds == 0
    input.command_name in ["python", "bash", "sh"]
}

default_timeout = 300  # 5 minutes default
