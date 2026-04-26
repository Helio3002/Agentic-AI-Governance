package policy.network_policies

# Network policies module
# Controls external network access and API calls

allowed_domains = {
    "https://api.github.com",
    "https://api.openai.com",
    "https://example.com",
    "https://api.trusted.ai",
}

allowed_ports = {
    80,
    443,
    8080,
}

# Allow HTTP/HTTPS requests to trusted domains only
allow_network_request {
    input.action == "network_request"
    input.metadata.method in ["GET", "POST", "PUT", "DELETE", "PATCH"]
    domain_is_allowed(input.metadata.destination)
    port_is_allowed(input.metadata.port)
}

# Check if domain is in allowlist
domain_is_allowed(destination) {
    regex.match("^https?://", destination)
    some allowed_domain
    allowed_domain := allowed_domains[_]
    startswith(destination, allowed_domain)
}

# Check port is allowed
port_is_allowed(port) {
    port in allowed_ports
}

port_is_allowed(port) {
    port == 0  # Let system choose port
}

# Deny DNS rebinding attacks
deny_dns_rebind {
    input.action == "network_request"
    contains_private_ip(input.metadata.destination)
}

# Helper to detect private IPs
contains_private_ip(url) {
    regex.match("127\\.0\\.0\\.", url)
}

contains_private_ip(url) {
    regex.match("192\\.168\\.", url)
}

contains_private_ip(url) {
    regex.match("10\\.", url)
}

# Deny connections to localhost from untrusted contexts
deny_localhost_access {
    input.action == "network_request"
    regex.match("localhost|127\\.0\\.0\\.1", input.metadata.destination)
    input.metadata.source_context != "internal_service"
}
