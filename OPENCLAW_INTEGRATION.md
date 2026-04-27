# OpenClaw Integration Usage Guide

## Quick Start

### Option 1: Run the Demo Script
```bash
# Navigate to repo root
cd /path/to/Agentic-AI-Governance

# Make script executable
chmod +x examples/setup_openclaw.sh

# Run the setup and demo
examples/setup_openclaw.sh
```

### Option 2: Manual Setup
```bash
# 1. Create workspace
mkdir -p workspace

# 2. In one terminal: Start OPA
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# 3. In another terminal: Run the integration
python3 examples/openclaw_integration.py
```

## Integration with Your OpenClaw Agent

### Step 1: Import the Integration Class
```python
from examples.openclaw_integration import OpenClawIntegration

# Initialize
agent = OpenClawIntegration(workspace_dir="/path/to/workspace")
```

### Step 2: Replace Direct Tool Calls
**Before** (direct execution - NOT SECURE):
```python
import subprocess
result = subprocess.run(["ls", "-la"], capture_output=True)
```

**After** (secure proxy):
```python
result = agent.execute("ls", ["-la"], "List current directory")
if result["allowed"]:
    print(result["stdout"])
else:
    print(f"Denied: {result['reason']}")
```

### Step 3: Use Pre-Built Tool Methods
The integration provides common tool wrappers:

```python
# List directory
result = agent.list_directory("/workspace")

# Read file
result = agent.read_file("config.txt")

# Search in file
result = agent.search_text("error", "log.txt")

# Find files
result = agent.find_files("*.txt")

# Count words
result = agent.word_count("document.txt")

# Get file info
result = agent.get_file_info("script.sh")

# Execute script
result = agent.execute_script("deploy.sh", ["production"])
```

### Step 4: Access Execution History
```python
# Print all executions
agent.print_execution_history()

# Export audit summary to JSON
agent.export_audit_summary("my_audit.json")
```

## Understanding the Response

Each `execute()` call returns a dictionary:

```python
{
    "allowed": True,           # Whether policy allowed it
    "exit_code": 0,           # Command exit code
    "stdout": "output...",    # Command output
    "stderr": ""              # Error output (if any)
}
```

Handle responses:
```python
result = agent.execute("command", ["arg"])

if result.get("allowed"):
    # Success - use the output
    output = result.get("stdout", "")
else:
    # Denied - handle gracefully
    error = result.get("reason", "Unknown reason")
    print(f"Command denied: {error}")
```

## Customizing for Your Agent

### Add Custom Tool Methods
```python
class MyOpenClawAgent(OpenClawIntegration):
    def my_custom_tool(self, param):
        """My custom secure tool."""
        return self.execute(
            "my_command",
            ["--param", param],
            f"Running my custom tool with {param}"
        )

# Use it
agent = MyOpenClawAgent()
result = agent.my_custom_tool("value")
```

### Modify Policies
Edit `src/policies/policy.rego` to allow/deny specific commands:

```rego
# Allow echo but deny rm
allow {
    input.tool == "echo"
}
```

## Monitoring & Audit Logs

### Real-time Audit Logs
```bash
tail -f logs/audit_log.jsonl
```

### View Execution History
```bash
python3 -c "import json; print(json.dumps(json.load(open('openclaw_audit_summary.json')), indent=2))"
```

### Parse Audit Logs
```python
import json
with open("logs/audit_log.jsonl") as f:
    for line in f:
        event = json.loads(line)
        print(f"{event['event']}: {event['payload']}")
```

## Troubleshooting

### Error: "Proxy not initialized"
- Ensure Docker is running: `docker ps`
- Ensure OPA server is running: `curl http://localhost:8181/v1/data/policy/allow`
- Check OPA started correctly

### Error: "Policy denied execution"
- Edit `src/policies/policy.rego` to allow the command
- Restart OPA server after policy changes

### Error: "File not found"
- Commands run in the workspace directory (`workspace/`)
- Use absolute paths or place files in workspace

### Error: Command exits with code 1 or 2
- This is normal - it means the command ran but failed
- Check `result["stderr"]` for the error message

## Example: Complete Integration

```python
from examples.openclaw_integration import OpenClawIntegration

def main():
    # Initialize
    agent = OpenClawIntegration()
    
    if not agent.ready:
        print("Failed to initialize")
        return
    
    # Execute secure commands
    files = agent.list_directory("/workspace")
    if files["allowed"]:
        print("Workspace contents:", files["stdout"])
    
    search = agent.search_text("error", "app.log")
    if search["allowed"]:
        print("Found errors:", search["stdout"])
    
    # Export audit trail
    agent.print_execution_history()
    agent.export_audit_summary("audit.json")

if __name__ == "__main__":
    main()
```

## Security Notes

✅ **Always use the proxy** for all external commands  
✅ **Check `allowed` field** before using command output  
✅ **Review audit logs** regularly  
✅ **Keep policies updated** as your agent evolves  
❌ **Never bypass the proxy** for "convenience"  
❌ **Never hardcode** sensitive paths or commands  

---

For more details, see [examples/README.md](README.md) and [../README.md](../README.md)
