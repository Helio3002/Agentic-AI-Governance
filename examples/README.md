# 🤖 AI Agent Integration Examples

This directory contains working examples showing how different AI agents can integrate with **Agentic AI Governance** for secure command execution.

## 📁 Examples Included

### 1. `example_ibm_agent.py`
**IBM AI Agent Integration**
- Shows how IBM AI agents can use the security proxy
- Demonstrates file analysis, directory listing, and text search
- Includes summary report generation

### 2. `example_openai_agent.py`
**OpenAI Agent Integration**
- Shows how OpenAI agents (or similar) can use function calling
- Demonstrates safe file operations through the proxy
- Includes OpenAI function schema for reference

### 3. `example_openclaw_agent.py`
**OpenClaw Agent Integration**
- Template for integrating OpenClaw with secure proxy
- Shows how to replace direct tool executions with proxy calls
- Includes example tool methods for common operations

## 🚀 Running the Examples

### Prerequisites
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or
   poetry install
   ```

2. **Start OPA server:**
   ```bash
   docker-compose up opa
   # or
   opa run --server --addr :8181
   ```

3. **Start Docker service** (for sandboxing)

### Run IBM Agent Example
```bash
python example_ibm_agent.py
```

### Run OpenClaw Integration Example
```bash
python openclaw_integration.py
```

This script demonstrates:
- Secure command execution through the proxy
- Common tool operations (list, read, search, etc.)
- Execution history and audit logging
- JSON export of audit summary

## 🔒 How It Works

### Security Proxy Integration
Both examples use the `PolicyEnforcementProxy` class:

```python
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

proxy = PolicyEnforcementProxy()

# Instead of: os.system("dangerous-command")
# Use:
result = proxy.execute_tool("safe-command", ["args"], {"source": "your_agent"})
```

### What Gets Protected
- ✅ **Command validation** - Only allowed commands execute
- ✅ **Path restrictions** - File access limited to safe directories
- ✅ **Network filtering** - Outbound connections controlled
- ✅ **Resource limits** - CPU/memory usage capped
- ✅ **Data sanitization** - Sensitive info redacted
- ✅ **Audit logging** - All actions recorded

## 🛠️ Integration for Your AI Agent

### For Any Python-Based Agent
```python
# 1. Import the proxy
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

# 2. Initialize
proxy = PolicyEnforcementProxy()

# 3. Replace direct calls with proxy calls
# BAD: subprocess.run(["rm", "-rf", "/"])
# GOOD:
result = proxy.execute_tool("rm", ["-rf", "/safe/path"], {"source": "my_agent"})
```

### For Non-Python Agents
Create a simple HTTP wrapper service:

```python
# http_wrapper.py
from flask import Flask, request, jsonify
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

app = Flask(__name__)
proxy = PolicyEnforcementProxy()

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    result = proxy.execute_tool(
        data['command'],
        data.get('args', []),
        data.get('metadata', {})
    )
    return jsonify(result)
```

Then your non-Python agent can make HTTP requests to this wrapper.

## 📋 Example Output

```
🚀 IBM AI Agent Example with Agentic AI Governance
============================================================
🤖 IBM AI Agent initialized with secure proxy

1️⃣ File Analysis Example:
📊 Analyzing file: GUIDE.md
Result: {
  "allowed": true,
  "exit_code": 0,
  "stdout": "1260 GUIDE.md\n",
  "stderr": ""
}

2️⃣ Directory Listing Example:
📁 Listing directory: /workspace
Result: {
  "allowed": true,
  "exit_code": 0,
  "stdout": "total 1234\ndrwxr-xr-x ... GUIDE.md\n...",
  "stderr": ""
}
```

## 🔧 Configuration

### Policy Configuration
Edit `src/policies/policy.rego` to customize:
- Allowed commands
- File paths
- Network domains
- Resource limits

### Docker Sandbox
The proxy uses Docker for command isolation. Configure in `docker-compose.yml`.

## 🚨 Security Notes

- **Default-deny policy**: Only explicitly allowed operations work
- **Input validation**: All arguments are sanitized
- **Output filtering**: Sensitive data is automatically redacted
- **Audit trail**: Every action is logged with context

## 📞 Support

- Check `TROUBLESHOOTING_GUIDE.md` for common issues
- Review `ARCHITECTURE_GUIDE.md` for technical details
- See `GUIDE.md` for complete setup instructions

---

**Ready to integrate your AI agent with secure command execution!** 🚀