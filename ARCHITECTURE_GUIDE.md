# 📊 Architecture and System Overview

Visual guides to understand how Agentic AI Governance works.

---

## 🏗️ System Architecture

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                      Your AI Application                          │
│            (ChatGPT, LangChain, AutoGPT, Custom Agent)            │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                    Tool Execution Request
                    (e.g., "delete file.txt")
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                  Agentic AI Governance System                     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  1. Input Validator                                         │ │
│  │  - Check format: Is request valid?                          │ │
│  │  - Allowed commands: Is tool in allowlist?                  │ │
│  │  - Sanitize arguments: Safe arguments?                      │ │
│  │  - Block injection: No shell manipulation?                  │ │
│  └────────────────────────┬────────────────────────────────────┘ │
│                           │                                       │
│  ✓ Valid / ✗ Invalid      │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  2. Policy Decision Engine (OPA)                            │ │
│  │  - Read security rules                                      │ │
│  │  - Evaluate request against policies                        │ │
│  │  - Make Allow/Deny decision                                 │ │
│  │  - Log decision for audit                                   │ │
│  └────────────────────────┬────────────────────────────────────┘ │
│                           │                                       │
│  ✓ Allowed / ✗ Denied     │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  3. Sandbox Executor (Docker)                               │ │
│  │  - Run in isolated container                                │ │
│  │  - Set resource limits                                      │ │
│  │  - Prevent damage to host system                            │ │
│  │  - Capture output                                           │ │
│  └────────────────────────┬────────────────────────────────────┘ │
│                           │                                       │
│  ✓ Success / ✗ Error      │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  4. Output Filter                                           │ │
│  │  - Remove passwords: [REDACTED]                             │ │
│  │  - Hide API keys: [REDACTED]                                │ │
│  │  - Block SSN/credit cards: [REDACTED]                       │ │
│  │  - Return clean output                                      │ │
│  └────────────────────────┬────────────────────────────────────┘ │
│                           │                                       │
│  Filtered Result          │                                       │
│                           ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  5. Audit Logger                                            │ │
│  │  - Who did it: user_id                                      │ │
│  │  - What they did: action                                    │ │
│  │  - When they did it: timestamp                              │ │
│  │  - Was it allowed: decision                                 │ │
│  │  - Why: reason                                              │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                      Safe Result Returned
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Your AI Application                          │
│                  (Receives safe results only)                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Security Layers

Each layer provides protection:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: VALIDATION                                         │
│  ├─ Format validation (request must be well-formed)         │
│  ├─ Command allowlist (only safe commands)                  │
│  ├─ Argument validation (no injection attacks)              │
│  └─ Path validation (no traversal attacks)                  │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ If any check fails → DENY
                           │
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: POLICY ENFORCEMENT                                │
│  ├─ File access policies (allowed paths)                    │
│  ├─ Network policies (trusted domains)                      │
│  ├─ Admin policies (approval requirements)                  │
│  └─ Resource policies (memory/CPU limits)                   │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ If policy denies → DENY
                           │
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: ISOLATION                                          │
│  ├─ Docker container (separate from host)                   │
│  ├─ Resource quotas (memory/CPU/timeout)                    │
│  ├─ File system isolation (only /workspace)                 │
│  └─ Network isolation (only allowed domains)                │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ If process escapes → killed
                           │
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: OUTPUT PROTECTION                                 │
│  ├─ Credential redaction (passwords, keys)                  │
│  ├─ PII masking (SSN, credit cards)                         │
│  ├─ Pattern matching (sensitive data types)                 │
│  └─ Safe return (only sanitized data)                       │
└─────────────────────────────────────────────────────────────┘
                           ▲
                           │ If sensitive data → REDACTED
                           │
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: AUDIT                                              │
│  ├─ Immutable logs (what happened)                          │
│  ├─ Compliance records (audit trail)                        │
│  ├─ Security monitoring (detect attacks)                    │
│  └─ Evidence preservation (SOC 2, ISO 27001)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Request Flow Diagram

Step-by-step what happens when your AI agent requests an operation:

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: AI Agent Makes Request                              │
├─────────────────────────────────────────────────────────────┤
│ Example:                                                     │
│ {                                                            │
│   "command": "rm",                                           │
│   "args": ["/workspace/temp.txt"],                           │
│   "user_id": "agent123"                                      │
│ }                                                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Validate Input                                      │
├─────────────────────────────────────────────────────────────┤
│ Check: Is "rm" in allowed commands? → YES ✓                 │
│ Check: Is path valid? → YES ✓                               │
│ Check: Are arguments safe? → YES ✓                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Check Policies                                      │
├─────────────────────────────────────────────────────────────┤
│ Question 1: Is "rm" a destructive command?                  │
│ Answer: YES                                                 │
│                                                             │
│ Question 2: Does user have approval?                        │
│ Answer: checking metadata...                                │
│ Answer: NO → POLICY DENIES ✗                                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Decision                                            │
├─────────────────────────────────────────────────────────────┤
│ DECISION: DENY                                              │
│ REASON: Destructive command requires user approval          │
│ AUDIT_ID: audit-12345                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Return Result                                       │
├─────────────────────────────────────────────────────────────┤
│ {                                                            │
│   "allowed": false,                                          │
│   "reason": "Destructive command requires approval",         │
│   "audit_id": "audit-12345"                                 │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
```

### Alternative: When Approved

```
┌─────────────────────────────────────────────────────────────┐
│ Step 3b: Check Policies (WITH APPROVAL)                     │
├─────────────────────────────────────────────────────────────┤
│ Question 1: Is "rm" a destructive command?                  │
│ Answer: YES                                                 │
│                                                             │
│ Question 2: Does user have approval?                        │
│ Answer: checking metadata...                                │
│ Answer: YES ✓                                               │
│                                                             │
│ Question 3: Is path allowed for write?                      │
│ Answer: /workspace allowed ✓                                │
│                                                             │
│ Question 4: Does request match other policies?              │
│ Answer: Everything checks out ✓                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4b: Decision (WITH APPROVAL)                           │
├─────────────────────────────────────────────────────────────┤
│ DECISION: ALLOW ✓                                           │
│ ACTION: Execute in Docker sandbox                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5b: Execute Safely                                     │
├─────────────────────────────────────────────────────────────┤
│ ✓ Start Docker container                                    │
│ ✓ Run: rm /workspace/temp.txt                               │
│ ✓ Capture output: (file deleted)                            │
│ ✓ Stop container                                            │
│ ✓ Filter output: No sensitive data                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Return Safe Result                                  │
├─────────────────────────────────────────────────────────────┤
│ {                                                            │
│   "allowed": true,                                           │
│   "exit_code": 0,                                            │
│   "stdout": "",                                              │
│   "stderr": "",                                              │
│   "audit_id": "audit-12346"                                 │
│ }                                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 File System Isolation

How files are protected:

```
Host System                          Docker Sandbox
──────────────────────────────────────────────────────

/home              ─────┐
  /user                 │
    /.ssh               ├─ NOT VISIBLE
    /.env               │
    /secret_files   ─────

/etc               ─────┐
  /passwd               ├─ NOT VISIBLE
  /shadow               │
  /config           ─────

/workspace         ─────────► /workspace (MOUNTED)
  /data.txt             │  (Read/Write allowed)
  /output.txt           │
                    ─────

Agent sees:          ONLY: /workspace/
Cannot see:          /.ssh, /etc, /home, etc.
Cannot write to:     Anywhere except /workspace
```

---

## 🌐 Network Isolation

How network access is controlled:

```
Docker Container                    External Networks

Agent inside container              Internet
wants to connect to...              ──────

1. https://api.github.com  ──────► ✓ ALLOWED (in allowlist)
                                   Response returned

2. https://malicious.com   ──────► ✗ BLOCKED (not in allowlist)
                                   Connection denied

3. http://localhost:9999   ──────► ✗ BLOCKED (private IP)
                                   Connection denied

4. https://api.openai.com  ──────► ✓ ALLOWED (in allowlist)
                                   Response returned
```

---

## 💾 Resource Management

How resources are limited:

```
Container Resource Limits:

┌─────────────────────────────────────────────────────┐
│ Memory Usage                                        │
├──────────────────┬──────────────────────────────────┤
│ Limit: 2048 MB   │ ████████████████░░░░░░           │
│ Current: 1200 MB │ (58% used, 848 MB available)     │
└──────────────────┴──────────────────────────────────┘

If execution tries to use MORE than 2048 MB:
→ Container killed immediately
→ Operation fails safely
→ Host system protected


┌─────────────────────────────────────────────────────┐
│ CPU Usage                                           │
├──────────────────┬──────────────────────────────────┤
│ Limit: 80%       │ ███████████░░░░░░░░░░░░░░░░     │
│ Current: 35%     │ (35% used)                       │
└──────────────────┴──────────────────────────────────┘

If execution tries to use MORE than 80%:
→ Process throttled or killed
→ System stays responsive


┌─────────────────────────────────────────────────────┐
│ Execution Time                                      │
├──────────────────┬──────────────────────────────────┤
│ Limit: 300 sec   │ ███████████░░░░░░░░░░░░░░░░     │
│ Elapsed: 127 sec │ (42% of timeout)                 │
└──────────────────┴──────────────────────────────────┘

If execution takes LONGER than 300 seconds:
→ Process terminated
→ Results returned with timeout message
```

---

## 🔐 Data Protection

How sensitive data is protected:

```
Agent's Output                    After Filtering

password=mysecret123     ────►  password=[REDACTED]
AWS_KEY=AKIA...          ────►  AWS_KEY=[REDACTED]
SSN=123-45-6789          ────►  SSN=[REDACTED]
api_key=sk_test_abc      ────►  api_key=[REDACTED]
name=John                ────►  name=John (safe)
count=42                 ────►  count=42 (safe)

Rules:
✓ Passwords: Looking for "password=***"
✓ AWS Keys: Looking for "AKIA***"
✓ SSN: Looking for "###-##-####"
✓ API Keys: Looking for "sk_***"
✓ Safe Text: Numbers, names, regular output
```

---

## 📊 Policy Decision Tree

How policies are evaluated:

```
Request comes in
│
├─ Is format valid?
│  ├─ YES ──────────────────┐
│  └─ NO ──► DENY       
│
├─ Is command allowlisted?
│  ├─ YES ──────────────────┐
│  └─ NO ──► DENY        
│
├─ Are arguments safe?
│  ├─ YES ──────────────────┐
│  └─ NO ──► DENY        
│
├─ Is this a file operation?
│  ├─ NO ──► CONTINUE   
│  └─ YES ──────────────────┐
│     ├─ Is path allowed?
│     │  ├─ YES ──────────────────┐
│     │  └─ NO ──► DENY         
│     │
│     └─ Is it destructive?
│        ├─ YES ──────────────────┐
│        │  ├─ Is approved?
│        │  │  ├─ YES ──────────────────┐
│        │  │  └─ NO ──► DENY         
│        │  └─ YES ──► CHECK RESOURCES
│        └─ NO ──► CHECK RESOURCES
│
├─ Is this a network operation?
│  ├─ NO ──► CONTINUE   
│  └─ YES ──────────────────┐
│     ├─ Is domain trusted?
│     │  ├─ YES ──────────────────┐
│     │  └─ NO ──► DENY         
│     │
│     └─ Is port allowed?
│        ├─ YES ──────────────────┐
│        └─ NO ──► DENY      
│
├─ CHECK RESOURCES
│  ├─ Memory OK?
│  │  ├─ YES ──────────────────┐
│  │  └─ NO ──► DENY         
│  │
│  ├─ CPU OK?
│  │  ├─ YES ──────────────────┐
│  │  └─ NO ──► DENY         
│  │
│  └─ Timeout valid?
│     ├─ YES ──────────────────┐
│     └─ NO ──► DENY      
│
└─ ✓ ALL CHECKS PASS ──► ALLOW
```

---

## 🔄 Audit Log Format

What gets recorded:

```json
{
  "timestamp": "2024-04-26T10:30:45.123Z",
  "request_id": "req-12345",
  "user_id": "user123",
  "user_role": "admin",
  "action": "file_delete",
  "resource": "/workspace/temp.txt",
  "metadata": {
    "source": "my-app",
    "reason": "cleanup",
    "user_approval": true
  },
  "decision": "ALLOW",
  "reason": "Destructive command with admin approval",
  "components_checked": [
    "validator",
    "file_policy",
    "admin_policy",
    "resource_policy"
  ],
  "execution": {
    "exit_code": 0,
    "duration_ms": 125,
    "sandbox": "docker-container-123"
  },
  "security": {
    "output_filtered": false,
    "sensitive_data_detected": false,
    "resource_limits_ok": true
  }
}
```

---

## 🎯 Decision Matrix

Quick reference for allowed operations:

| Operation | File | Network | Destructive | Requires | Result |
|-----------|------|---------|-------------|----------|--------|
| `cat /workspace/file` | ✓ | - | ✗ | None | ALLOW |
| `rm /workspace/file` | ✓ | - | ✓ | Approval | ALLOW if approved |
| `curl https://api.github.com` | - | ✓ | ✗ | None | ALLOW |
| `curl https://evil.com` | - | ✗ | ✗ | - | DENY |
| `cat /etc/passwd` | ✗ | - | ✗ | - | DENY |
| `chmod 777 /workspace/file` | ✓ | - | ✓ | Approval | ALLOW if approved |
| Any operation for 10000 seconds | - | - | - | Timeout | DENY (exceeds limit) |
| Process using 5GB RAM | - | - | - | - | KILL (exceeds limit) |

---

## 🔗 Component Relationships

How components work together:

```
┌──────────────────────────────────────────────────────────┐
│                  PolicyEnforcementProxy                   │
│                  (Main coordinator)                       │
└──────────────────────┬───────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
   ┌────────┐    ┌──────────┐  ┌──────────┐  ┌──────────┐
   │Validator│    │OpaClient │  │DockerMgr │  │OutputMgr │
   ├────────┤    ├──────────┤  ├──────────┤  ├──────────┤
   │• Check  │    │• Execute │  │• Run cmd │  │• Redact  │
   │  format │    │  policy  │  │  safely  │  │  secrets │
   │• Whitelist│   │• Decide  │  │• Isolate │  │• Filter  │
   │  commands│   │  Allow   │  │• Limit   │  │  data    │
   │• Validate│   │  Deny    │  │  resources│  │          │
   │  args    │    │          │  │          │  │          │
   └────────┘    └──────────┘  └──────────┘  └──────────┘
        │              │              │              │
        └──────────────┼──────────────┴──────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  Audit Logger        │
            ├──────────────────────┤
            │• Record all requests │
            │• Track decisions     │
            │• Store audit trail   │
            │• Enable compliance   │
            └──────────────────────┘
```

---

## 🚀 Deployment Scenarios

### Scenario 1: Local Development
```
Your Laptop
├─ Python (Interpreter)
├─ OPA (Policy Engine)
├─ Docker (Isolated Execution)
└─ Your AI Agent
```

### Scenario 2: Docker Container
```
Single Docker Container
├─ Python Application
├─ OPA Server
└─ Nested Docker (for running commands)
```

### Scenario 3: Kubernetes
```
Kubernetes Cluster
├─ Pod 1: OPA Server
├─ Pod 2: Proxy + Agent
├─ Pod 3: Monitoring/Logging
└─ Persistent Volume: Audit Logs
```

---

## 📈 Performance Characteristics

Typical performance metrics:

```
Operation                Time    Memory   CPU Usage
────────────────────────────────────────────────────
Validate request         2ms     1MB      <1%
OPA policy decision      5ms     5MB      1-2%
Docker execution         varies  varies   varies
Output filtering         1ms     2MB      <1%
Audit logging           1ms     1MB      <1%
────────────────────────────────────────────────────
Total overhead          ~9ms    ~9MB     ~1-2%
(excluding actual command execution)
```

---

This visual guide helps you understand:
- ✅ How the system works
- ✅ How requests flow through
- ✅ How security is enforced
- ✅ How data is protected
- ✅ How decisions are made
- ✅ How components interact

For detailed documentation, see [GUIDE.md](GUIDE.md)
