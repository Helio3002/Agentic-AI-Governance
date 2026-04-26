# 📚 Complete Guide: Agentic AI Governance

**Table of Contents**
- [What Is This Tool?](#what-is-this-tool)
- [Why Do You Need It?](#why-do-you-need-it)
- [How Does It Work?](#how-does-it-work)
- [Prerequisites](#prerequisites)
- [Step-by-Step Installation](#step-by-step-installation)
- [Configuration Guide](#configuration-guide)
- [Using the Tool](#using-the-tool)
- [Examples](#examples)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## What Is This Tool?

**Agentic AI Governance** is a security framework that acts as a **protective layer** between your AI agents (like ChatGPT plugins or autonomous systems) and sensitive operations on your computer.

### In Simple Terms:
Think of it as a **security guard for AI agents**. When an AI agent wants to:
- Read or delete files
- Access the internet
- Run commands on your computer
- Use significant computing resources

...this tool **checks if it's safe** before letting it happen.

---

## Why Do You Need It?

### Real-World Scenario:
You're using an autonomous AI agent to help manage your files and systems. Without this tool:
- ❌ The agent could accidentally delete important files
- ❌ The agent could connect to malicious websites
- ❌ The agent could consume all your computer's memory
- ❌ You'd have no record of what the agent did

### With This Tool:
- ✅ Only safe operations are allowed
- ✅ All actions are logged for audit trails
- ✅ Resource limits prevent system overload
- ✅ Sensitive data is automatically redacted
- ✅ You maintain full control

---

## How Does It Work?

### Visual Overview:
```
┌─────────────────────┐
│   Your AI Agent     │
│  (e.g., ChatGPT)    │
└──────────┬──────────┘
           │ "Can I delete this file?"
           ▼
┌─────────────────────────────────────────┐
│     Policy Enforcement Proxy            │
│  (This is the security guard)           │
├─────────────────────────────────────────┤
│ 1. VALIDATE: Is the request legitimate? │
│ 2. CHECK POLICY: Is it in the rulebook? │
│ 3. AUTHORIZE: Does user approve it?     │
│ 4. EXECUTE: Run in secure sandbox       │
│ 5. FILTER: Hide sensitive info          │
│ 6. AUDIT: Log everything                │
└──────────┬───────────────────────────────┘
           │ "Yes, but only in /workspace"
           ▼
┌─────────────────────┐
│  Secure Execution   │
│   (Docker Box)      │
└─────────────────────┘
```

### 5 Key Components:

#### 1. **Input Validator**
- Checks the request format
- Prevents injection attacks
- Ensures arguments are safe

#### 2. **Policy Engine (OPA)**
- Reads your security rules
- Makes decisions (Allow/Deny)
- Uses default-deny (safer approach)

#### 3. **Docker Sandbox**
- Runs operations in isolation
- Limits resource usage
- Contains damage if something goes wrong

#### 4. **Output Filter**
- Removes passwords
- Hides API keys
- Blocks sensitive data

#### 5. **Audit Logger**
- Records every request
- Tracks decisions
- Creates compliance reports

---

## Prerequisites

Before you can use this tool, you need to install a few things. Don't worry—they're free and easy to install!

### Requirements Checklist:

| Component | Version | What It Is | Why You Need It |
|-----------|---------|-----------|-----------------|
| **Python** | 3.11+ | Programming language | Core requirement |
| **Docker** | Latest | Container platform | Sandbox isolation |
| **OPA** | Latest | Policy engine | Rule evaluation |
| **Git** | Any | Version control | Download code |

### Installation Time: 15-30 minutes

---

## Step-by-Step Installation

### Step 1️⃣: Check Your Python Version

Open your terminal/command prompt and run:

**macOS/Linux:**
```bash
python3 --version
```

**Windows (PowerShell):**
```powershell
python --version
```

**Expected Output:**
```
Python 3.11.0  (or higher like 3.12, 3.13)
```

✅ If you see 3.11 or higher, go to **Step 2**
❌ If it's lower or missing, install Python from [python.org](https://www.python.org/downloads/)

---

### Step 2️⃣: Download the Tool

Choose one way to get the code:

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/Helio3002/Agentic-AI-Governance.git
cd Agentic-AI-Governance
```

**Option B: Manual Download**
1. Go to [GitHub Repository](https://github.com/Helio3002/Agentic-AI-Governance)
2. Click **"Code"** → **"Download ZIP"**
3. Extract the ZIP file
4. Open terminal in the extracted folder

---

### Step 3️⃣: Install Docker

Docker is a container platform that isolates operations safely.

**macOS:**
```bash
# Install via Homebrew (easier)
brew install docker

# Or download Docker Desktop from:
# https://www.docker.com/products/docker-desktop
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER  # Run without sudo
newgrp docker  # Activate group changes
```

**Windows:**
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Install and restart your computer
3. Verify: `docker --version` in PowerShell

---

### Step 4️⃣: Install OPA (Open Policy Agent)

OPA is the "brain" that makes security decisions.

**macOS:**
```bash
brew install opa
```

**Linux:**
```bash
# Download the latest version
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_x86_64
chmod +x opa
sudo mv opa /usr/local/bin/
```

**Windows (PowerShell):**
```powershell
# Download and save to Program Files
$url = "https://openpolicyagent.org/downloads/latest/opa_windows_x86_64.exe"
Invoke-WebRequest -Uri $url -OutFile "C:\Program Files\opa.exe"
```

**Verify Installation:**
```bash
opa --version
# Should show: OPA 0.x.x
```

---

### Step 5️⃣: Create Project Directories

```bash
# Navigate to the project folder
cd Agentic-AI-Governance

# Create workspace directory (where files will be stored)
mkdir -p workspace

# Verify it was created
ls -la workspace
```

---

### Step 6️⃣: Install Python Dependencies

The project needs some Python libraries. Install them all at once:

```bash
# Upgrade pip (Python package manager)
python3 -m pip install --upgrade pip

# Install the project and dev tools
python3 -m pip install -e .[dev]
```

**What's happening:**
- `pip install` = Install packages
- `-e` = Install in edit mode (for development)
- `.[dev]` = Install the project + development tools

**Expected output:**
```
Successfully installed [list of packages]
```

---

### Step 7️⃣: Verify Installation

Run this verification script:

```bash
# Check all components
python3 -c "print('✓ Python installed'); import sys; print(f'  Version: {sys.version}')"
docker --version
opa --version
python3 -m pytest --version
```

**Expected Output:**
```
✓ Python installed
  Version: Python 3.12.1
Docker version 24.0.0
OPA 0.48.0
pytest 9.0.0
```

✅ **Congratulations!** You're all set up. Move to **Configuration Guide**.

---

## Configuration Guide

Now that you have everything installed, let's configure it for your needs.

### Basic Configuration (5 minutes)

#### 1. **Choose Which Commands Are Allowed**

Edit `src/proxy/validator.py`:

```python
DEFAULT_ALLOWED_COMMANDS = {
    "cat",        # Read files
    "ls",         # List files
    "echo",       # Print text
    "grep",       # Search in files
    "python",     # Run Python scripts
    # Add more commands as needed
}
```

**Common Commands to Consider:**
- Safe: `cat`, `ls`, `find`, `grep`, `echo`, `curl`
- Dangerous: `rm`, `dd`, `chmod`, `chown`
- Very Dangerous: Commands that modify the system

**How to Add a Command:**
```python
DEFAULT_ALLOWED_COMMANDS = {
    # ... existing commands ...
    "my-new-command",  # Add here
}
```

---

#### 2. **Set Allowed File Paths**

Edit `src/policies/file_operations.rego`:

```rego
allowed_read_paths = {
    "/workspace",           # Your working directory
    "/tmp",                 # Temporary files
    "/etc/hostname",        # System info (read-only)
}

allowed_write_paths = {
    "/workspace",           # Only write here
}
```

**What This Means:**
- Read from: Multiple safe locations
- Write to: Only `/workspace` (to prevent accidents)

**How to Add a Path:**
```rego
allowed_read_paths = {
    "/workspace",
    "/tmp",
    "/home/documents",     # Add here
}
```

---

#### 3. **Configure Network Access**

Edit `src/policies/network_policies.rego`:

```rego
allowed_domains = {
    "https://api.github.com",
    "https://api.openai.com",
    "https://example.com",
}

allowed_ports = {
    80,      # HTTP
    443,     # HTTPS
    8080,    # Common alternative
}
```

**How to Add a Domain:**
```rego
allowed_domains = {
    "https://api.github.com",
    "https://api.openai.com",
    "https://my-api.example.com",  # Add here
}
```

---

#### 4. **Set Resource Limits**

Edit `src/policies/resource_policies.rego`:

```rego
max_memory_mb = 2048      # 2 GB maximum
max_cpu_percent = 80      # Don't exceed 80% CPU
max_disk_gb = 10          # Limit disk space
```

**Understanding Limits:**
- If agent exceeds these, operation is blocked
- Prevents runaway processes
- Protects system stability

**Examples:**
```rego
max_memory_mb = 1024      # More restrictive (1 GB)
max_memory_mb = 4096      # More permissive (4 GB)
```

---

### Advanced Configuration (Optional)

#### Custom Policy Rules

Create new rules in policy files. Example:

```rego
# In file_operations.rego
# Block access to sensitive paths
deny_sensitive_paths {
    input.metadata.target_path
    contains_sensitive_path(input.metadata.target_path)
}

contains_sensitive_path(path) {
    sensitive = [".env", ".ssh", ".git", ".aws"]
    some s
    s := sensitive[_]
    contains(path, s)
}
```

---

## Using the Tool

### Basic Workflow

#### Step 1: Start OPA Server

In terminal 1, start the policy engine:

```bash
opa run --server --set=decision_logs.console=true src/policies/policy.rego
```

**What You'll See:**
```
Starting OPA server...
Listening on http://127.0.0.1:8181
Ready for policy decisions
```

✅ Leave this running

---

#### Step 2: Run Your Application

In terminal 2, run your AI agent or application:

```python
# Example: Python script
python3 src/main.py

# Or with Docker:
docker-compose up
```

---

#### Step 3: Check the Results

View the output and audit logs:

**In OPA Terminal:** See policy decisions in real-time
```
Policy Decision: ALLOW - File read from /workspace
Policy Decision: DENY - Network connection to untrusted.com
```

**In Application Terminal:** See results returned to agent

---

### Practical Example: Using with Your Application

**Scenario: Your AI agent wants to do this:**
```
1. Read a file from /workspace
2. Process it with Python
3. Save results back to /workspace
```

**What Happens:**

```bash
# AI Agent requests:
{
  "action": "file_read",
  "command": "cat",
  "args": ["/workspace/data.txt"],
  "metadata": {"user_id": "agent123"}
}

# System processes:
✓ Step 1: Validator checks format → OK
✓ Step 2: Policy checks path → /workspace allowed → OK
✓ Step 3: Docker executes safely → OK
✓ Step 4: Filter sensitive data → None found → OK
✓ Step 5: Return result to agent

# Result returned:
{
  "exit_code": 0,
  "stdout": "File contents here",
  "stderr": ""
}
```

---

### Running Tests to Verify

Before using in production, verify everything works:

```bash
# Run all tests (no setup needed)
pytest tests/test_policies.py -v

# Run specific test
pytest tests/test_policies.py::TestFileOperationsPolicies -v

# Run integration tests (requires OPA running)
pytest tests/test_integration.py -v
```

**Expected Output:**
```
test_read_allowed_path_succeeds ................ PASSED
test_read_forbidden_path_fails ................. PASSED
test_network_allowed .......................... PASSED
...
====== 34 passed in 0.15s ======
```

✅ All tests pass = System is ready

---

## Examples

### Example 1: Simple File Reading

**Goal:** Have your AI agent read a file safely

**Python Code:**
```python
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient
from sandbox_manager.docker_sandbox import DockerSandboxManager

# Initialize components
sandbox = DockerSandboxManager()
opa_client = OpaClient()
proxy = PolicyEnforcementProxy(opa_client=opa_client, sandbox_manager=sandbox)

# Execute a safe operation
result = proxy.execute_tool(
    tool_name="cat",
    args=["/workspace/documents.txt"],
    metadata={
        "user_id": "user123",
        "action": "execute",
        "user_approval": False
    }
)

# Check result
if result["allowed"]:
    print("File contents:", result["stdout"])
else:
    print("Operation blocked:", result["reason"])
```

**What Happens:**
1. Request is validated ✓
2. Policy checks if `/workspace` is allowed ✓
3. Docker runs `cat` safely ✓
4. Output is filtered ✓
5. Result returned ✓

**Output:**
```
File contents: [Your file data here]
```

---

### Example 2: Blocked Dangerous Operation

**Goal:** Prevent unauthorized file deletion

**Python Code:**
```python
# Try to delete a file without approval
result = proxy.execute_tool(
    tool_name="rm",
    args=["/workspace/important-file.txt"],
    metadata={
        "user_id": "user123",
        "action": "execute",
        "user_approval": False  # ← No approval
    }
)

# What Happens:
# 1. Validator checks format ✓
# 2. Policy sees destructive command 'rm' ✓
# 3. Policy sees user_approval = False ✓
# 4. Policy DENIES ✗
```

**Output:**
```python
{
    'allowed': False,
    'reason': 'Policy denied execution. Destructive command requires approval.'
}
```

✅ File is protected

---

### Example 3: Approved Privileged Operation

**Goal:** Allow admin to delete a file when necessary

**Python Code:**
```python
# Same operation BUT with approval
result = proxy.execute_tool(
    tool_name="rm",
    args=["/workspace/temp-file.txt"],
    metadata={
        "user_id": "admin123",
        "user_role": "admin",
        "action": "execute",
        "user_approval": True,  # ← Approval granted
        "action_reason": "Cleanup temporary files"
    }
)
```

**Output:**
```python
{
    'allowed': True,
    'exit_code': 0,
    'stdout': '',
    'stderr': ''
}
```

✅ File deleted safely with audit trail

---

### Example 4: Network Access Control

**Goal:** Allow API calls to trusted services only

**Python Code:**
```python
# Call trusted API
result = proxy.execute_tool(
    tool_name="curl",
    args=["https://api.github.com/user/repos"],
    metadata={
        "user_id": "user123",
        "destination": "https://api.github.com/user/repos",
        "method": "GET",
        "port": 443
    }
)

# This works ✓ because api.github.com is in allowed_domains

# Try untrusted domain
result = proxy.execute_tool(
    tool_name="curl",
    args=["https://malicious.com/steal-data"],
    metadata={
        "user_id": "user123",
        "destination": "https://malicious.com/steal-data",
        "method": "GET",
        "port": 443
    }
)

# This fails ✗ because malicious.com is NOT in allowed_domains
```

---

### Example 5: Resource Limit Protection

**Goal:** Prevent resource-hungry operations from crashing system

**Python Code:**
```python
# Request with excessive memory
result = proxy.execute_tool(
    tool_name="python",
    args=["memory_intensive.py"],
    metadata={
        "user_id": "user123",
        "requested_memory": 5000,  # 5 GB (exceeds 2GB limit)
        "timeout_seconds": 300
    }
)

# Result: DENIED because memory exceeds limit
```

**Output:**
```python
{
    'allowed': False,
    'reason': 'Policy denied execution. Memory request exceeds limit.'
}
```

---

## Advanced Features

### Auto-Audit Logging

All operations are automatically logged:

```json
{
  "timestamp": "2024-04-26T10:30:45Z",
  "request_id": "req-12345",
  "user_id": "user123",
  "action": "file_read",
  "resource": "/workspace/data.txt",
  "decision": "ALLOW",
  "reason": "Path allowed and user authorized",
  "duration_ms": 125
}
```

**View Logs:**
```bash
# In terminal running OPA
# Logs appear in real-time

# Or save to file
opa run --server src/policies/policy.rego > audit.log &
```

---

### Output Filtering (Automatic)

Sensitive data is automatically removed:

**Example Input from Agent:**
```
Command output: password=mysecretpass123
AWS_KEY=AKIAIOSFODNN7EXAMPLE
SSN=123-45-6789
```

**What Agent Receives:**
```
Command output: password=[REDACTED]
AWS_KEY=[REDACTED]
SSN=[REDACTED]
```

✅ Secrets are never exposed to your AI agent

---

### Custom Approval Workflow

**Step 1: User requests operation**
```python
result = proxy.execute_tool(
    tool_name="rm",
    args=["/workspace/old-file.txt"],
    metadata={
        "user_id": "user123",
        "user_approval": False,  # Not approved yet
        "action_reason": "User requested cleanup"
    }
)
# Result: DENIED
```

**Step 2: Admin reviews request**
```
Admin sees in audit log:
- FILE: /workspace/old-file.txt
- REASON: User requested cleanup
- RISK: Low
- RECOMMENDATION: Safe to approve
```

**Step 3: Approve and execute**
```python
result = proxy.execute_tool(
    tool_name="rm",
    args=["/workspace/old-file.txt"],
    metadata={
        "user_id": "user123",
        "user_approval": True,  # Now approved by admin
        "action_reason": "Admin approved cleanup",
        "audit_id": "audit-12345"
    }
)
# Result: ALLOWED and EXECUTED
```

---

### Integration with AI Frameworks

#### LangChain Integration

```python
from langchain.tools import Tool
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

# Create policy-protected tool
def safe_file_read(path: str) -> str:
    proxy = PolicyEnforcementProxy()
    result = proxy.execute_tool(
        "cat",
        [path],
        {"source": "langchain"}
    )
    return result.get("stdout", "")

# Use in LangChain
read_tool = Tool(
    name="ReadFile",
    func=safe_file_read,
    description="Read a file safely"
)

agent.tools.append(read_tool)
```

#### OpenAI Functions

```python
from openai import OpenAI
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

client = OpenAI()
proxy = PolicyEnforcementProxy()

# Define protected functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_workspace_file",
            "description": "Read file from workspace",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                }
            }
        }
    }
]

# When GPT calls the function, route through proxy
def handle_function_call(name, args):
    if name == "read_workspace_file":
        result = proxy.execute_tool(
            "cat",
            [f"/workspace/{args['filename']}"],
            {"source": "openai-gpt"}
        )
        return result["stdout"]
```

---

## Troubleshooting

### Problem 1: OPA Server Won't Start

**Error Message:**
```
Error: Address already in use
```

**Solution:**
```bash
# Find process using port 8181
lsof -i :8181

# Kill the process
kill -9 <PID>

# Or use different port
opa run --server --addr localhost:8182 src/policies/policy.rego
```

---

### Problem 2: Docker Not Running

**Error Message:**
```
Cannot connect to Docker daemon
```

**Solution:**

**macOS:**
```bash
# Start Docker Desktop from Applications
# Or command line:
open -a Docker
```

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker  # Auto-start on boot
```

**Windows:**
```powershell
# Start Docker Desktop from Start Menu
# Or ensure it's running in taskbar
```

---

### Problem 3: Tests Failing

**Error Message:**
```
FAILED tests/test_policies.py - ModuleNotFoundError: No module named 'proxy'
```

**Solution:**
```bash
# Reinstall in edit mode
python3 -m pip install -e .[dev]

# Clear cache
rm -rf .pytest_cache __pycache__

# Run tests again
pytest tests/test_policies.py -v
```

---

### Problem 4: Permission Denied on Linux

**Error Message:**
```
Got permission denied while trying to connect to Docker daemon
```

**Solution:**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Activate new group
newgrp docker

# Verify
docker ps
```

---

### Problem 5: Command Not in Allowlist

**Error Message:**
```
ValueError: Tool is not in the allowlist: my-command
```

**Solution:**

Edit `src/proxy/validator.py`:

```python
DEFAULT_ALLOWED_COMMANDS = {
    # ... existing commands ...
    "my-command",  # Add here
}
```

Then restart the service.

---

### Problem 6: Policy Decision Different Than Expected

**Debugging:**

```bash
# Create test request
cat > /tmp/test.json << 'EOF'
{
  "command_name": "cat",
  "action": "execute",
  "args": ["/workspace/file.txt"],
  "metadata": {"target_path": "/workspace/file.txt"}
}
EOF

# Evaluate policy manually
opa eval -d src/policies/policy.rego -i /tmp/test.json 'data.policy.allow'

# Check policy file syntax
opa check src/policies/policy.rego
```

---

## FAQ

### Q1: Is This Only for Linux?

**A:** No! It works on:
- ✅ macOS (Intel and Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)
- ✅ Windows (with WSL2 or native Docker)

---

### Q2: Can I Use This Without Docker?

**A:** Partially. Docker provides security isolation, but you can try without it for development:

```python
# Use local execution instead
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

proxy = PolicyEnforcementProxy()  # Uses local execution by default
```

**Warning:** ⚠️ Less secure. Docker recommended for production.

---

### Q3: How Do I Know What Decisions OPA Is Making?

**A:** Check the logs in real-time:

```bash
# Terminal 1: Start OPA with debug output
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# You'll see every decision:
# Policy Decision: ALLOW - file_read from /workspace
# Policy Decision: DENY - network to blacklisted.com
```

---

### Q4: Can I Use This with Multiple AI Agents?

**A:** Yes! The proxy handles concurrent requests:

```python
# Multiple agents can call simultaneously
# Each gets their own isolated sandbox
# All decisions logged separately
```

**Example:**
```python
# Agent 1
proxy.execute_tool("cat", ["/workspace/file1.txt"])

# Agent 2 (simultaneously)
proxy.execute_tool("echo", ["hello"])

# Agent 3 (simultaneously)
proxy.execute_tool("grep", ["pattern", "/workspace/file3.txt"])

# All execute safely in parallel
```

---

### Q5: What If I Need More Resources Than the Limits?

**A:** Adjust limits in `src/policies/resource_policies.rego`:

```rego
# Before (restrictive)
max_memory_mb = 2048
max_cpu_percent = 80

# After (more permissive)
max_memory_mb = 8192     # 8 GB
max_cpu_percent = 95     # Nearly full CPU
```

⚠️ Warning: Higher limits = More risk

---

### Q6: How Do I Add New Security Rules?

**A:** Create rules in Rego language:

```rego
# Example: Block operations at night
deny_night_operations {
    input.action == "execute"
    input.metadata.timestamp
    hour := time.now_ns() / 3600000000000 % 24
    hour >= 22  # After 10 PM
    hour <= 6   # Before 6 AM
}
```

Then test it:
```bash
pytest tests/test_policies.py -v
```

---

### Q7: Can I Integrate This with Existing Tools?

**A:** Yes! It's designed for integration:

- ✅ LangChain agents
- ✅ OpenAI Function Calling
- ✅ LLamaIndex tools
- ✅ Hugging Face transformers
- ✅ Custom Python applications
- ✅ Kubernetes deployments

See **Advanced Features** section for examples.

---

### Q8: What About Compliance and Audit?

**A:** Full audit support:

```bash
# All operations logged:
# - Who did it
# - What did they do
# - When they did it
# - Was it allowed/blocked
# - Why that decision

# Export logs for compliance:
opa run --server src/policies/policy.rego > audit_$(date +%Y%m%d).log &
```

Perfect for SOC 2, ISO 27001, etc.

---

### Q9: Is This Production Ready?

**A:** Yes! Features:

- ✅ Default-deny security model
- ✅ Comprehensive policy engine
- ✅ Automatic audit logging
- ✅ Resource limits
- ✅ Tested thoroughly
- ✅ Enterprise-grade controls

Recommended for production after:
1. Running tests (pytest)
2. Customizing policies
3. Reviewing audit logs
4. Testing with your agent

---

### Q10: Can I Get Help?

**A:** Yes! Resources:

1. **Documentation:** Read policy READMEs
2. **Tests:** Look at test examples
3. **GitHub:** Report issues
4. **Logs:** Check OPA console output for clues

---

## Quick Cheat Sheet

### One-Liners

```bash
# Start fresh
cd Agentic-AI-Governance
mkdir -p workspace

# Install
python3 -m pip install -e .[dev]

# Start OPA
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# Start app (new terminal)
python3 src/main.py

# Run tests
pytest tests/test_policies.py -v

# View coverage
pytest tests/ --cov=src --cov-report=html

# Use Docker
docker-compose up

# Check OPA health
curl http://localhost:8181/health
```

---

## Getting Started (TL;DR)

1. Install: `bash scripts/quick_start.sh`
2. Configure: Edit policy files
3. Test: `pytest tests/test_policies.py -v`
4. Start: `opa run --server src/policies/policy.rego`
5. Use: Call `proxy.execute_tool()`
6. Monitor: Check OPA logs

---

**🎉 You're Ready!**

You now have everything you need to use Agentic AI Governance. Start with examples, customize policies for your use case, and monitor your AI agents safely!

For detailed information, see:
- [src/policies/README.md](src/policies/README.md) - Policy details
- [TEST_ENVIRONMENT_SETUP.md](TEST_ENVIRONMENT_SETUP.md) - Testing guide
- Test files - Working examples
