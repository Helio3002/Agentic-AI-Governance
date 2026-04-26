# 🔍 Troubleshooting & Advanced FAQ

Complete guide to solving problems and answering advanced questions.

---

## 🆘 Common Issues and Solutions

### Issue 1: Python Version Too Low

**Error:**
```
This project requires Python 3.11 or higher
You have Python 3.9.0
```

**Why it happens:**
- Your system has an older Python version
- Needed features are unavailable in older versions

**Solutions:**

**Option A: Update Python (Recommended)**
```bash
# macOS
brew upgrade python@3.11

# Linux
sudo apt update
sudo apt install python3.11

# Windows
# Download from https://www.python.org/downloads/
# OR use: choco install python311 (with Chocolatey)
```

**Option B: Use Virtual Environment**
```bash
# Install Python 3.11 separately
# Then create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

**Verify Fix:**
```bash
python3 --version
# Should show 3.11 or higher
```

---

### Issue 2: Docker Daemon Not Running

**Error:**
```
Cannot connect to Docker daemon at unix:///var/run/docker.sock
```

**Why it happens:**
- Docker service not started
- Docker Desktop not running (macOS/Windows)

**Solutions:**

**macOS:**
```bash
# Check if Docker is running
docker ps

# Start Docker Desktop
open -a Docker

# Wait 30 seconds for startup, then try again
docker ps
```

**Linux:**
```bash
# Check status
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Enable auto-start on boot
sudo systemctl enable docker

# Verify
sudo systemctl status docker
```

**Windows (PowerShell):**
```powershell
# Check status
docker ps

# Start Docker Desktop
# Open Start Menu → Docker Desktop → Run
# Or use:
Start-Service com.docker.service
```

**Alternative: Use WSL2 backend (Windows)**
```powershell
# In Docker Desktop Settings:
# 1. Go to Settings
# 2. Select "WSL 2" as backend
# 3. Click "Apply & Restart"
```

---

### Issue 3: OPA Binary Not Found

**Error:**
```
opa: command not found
```

**Why it happens:**
- OPA not installed
- OPA not in PATH
- Installation incomplete

**Solutions:**

**macOS:**
```bash
# Install via Homebrew
brew install opa

# Verify
opa --version

# Or manually download
curl -L -o /usr/local/bin/opa https://openpolicyagent.org/downloads/latest/opa_darwin_x86_64
chmod +x /usr/local/bin/opa
opa --version
```

**Linux:**
```bash
# Download
curl -L -o ~/opa https://openpolicyagent.org/downloads/latest/opa_linux_x86_64
chmod +x ~/opa

# Add to PATH
sudo mv ~/opa /usr/local/bin/

# Verify
which opa
opa --version
```

**Windows (PowerShell):**
```powershell
# Create directory
New-Item -ItemType Directory -Path "C:\Program Files\opa"

# Download
$url = "https://openpolicyagent.org/downloads/latest/opa_windows_x86_64.exe"
Invoke-WebRequest -Uri $url -OutFile "C:\Program Files\opa\opa.exe"

# Add to PATH (System Environment Variables)
$env:Path += ";C:\Program Files\opa"

# Verify
opa --version
```

---

### Issue 4: Port 8181 Already in Use

**Error:**
```
address already in use
dial tcp 127.0.0.1:8181: bind: address already in use
```

**Why it happens:**
- Another OPA instance running
- Another service using port 8181
- OPA didn't shut down cleanly

**Solutions:**

**Option A: Find and Kill Process**
```bash
# Find what's using port 8181
lsof -i :8181

# Kill process
kill -9 <PID>

# Or more aggressive
pkill -f "opa run"
```

**Windows (PowerShell):**
```powershell
# Find process using port 8181
Get-NetTCPConnection -LocalPort 8181

# Kill process
Stop-Process -Id <PID> -Force
```

**Option B: Use Different Port**
```bash
# Run OPA on different port
opa run --server --addr localhost:8182 src/policies/policy.rego

# Update code to use new port
# In your Python code:
OpaClient(opa_url="http://localhost:8182/v1/data/policy/allow")
```

**Option C: Check What's Running**
```bash
# See all listening ports
netstat -tuln | grep 8181

# Or
sudo lsof -i :8181 -n
```

---

### Issue 5: Module Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'proxy'
```

**Why it happens:**
- Project not installed correctly
- Not in project directory
- Python path not set

**Solutions:**

**Check Your Location:**
```bash
# Must be in project directory
pwd
# Should show: .../Agentic-AI-Governance

# Go to project directory
cd /path/to/Agentic-AI-Governance
```

**Reinstall Project:**
```bash
# Clear old installation
python3 -m pip uninstall agentic-ai-governance -y

# Reinstall in edit mode
python3 -m pip install -e .[dev]

# Verify
python3 -c "import proxy; print('OK')"
```

**Fix Python Path:**
```bash
# Add to your Python script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Then import
from proxy import PolicyEnforcementProxy
```

---

### Issue 6: Pytest Collection Errors

**Error:**
```
ERROR: not found: .../tests/test_policies.py
(no name 'test_policies.py' in module 'tests')
```

**Why it happens:**
- conftest.py not found
- Tests not in right location
- Import path issue

**Solutions:**

**Verify Structure:**
```bash
# Check tests directory exists
ls -la tests/

# Check conftest.py exists
cat tests/conftest.py

# Should see Python code starting with imports
```

**Run from Project Root:**
```bash
# Must be in .../Agentic-AI-Governance
cd /path/to/Agentic-AI-Governance

# Then run tests
pytest tests/test_policies.py -v
```

**Reinstall:**
```bash
python3 -m pip install -e .[dev]
pytest tests/ --collect-only
```

---

### Issue 7: Docker Build Fails

**Error:**
```
ERROR: failed to solve with frontend dockerfile.v0: failed to read dockerfile
```

**Why it happens:**
- Dockerfile not found
- Wrong working directory
- File permissions

**Solutions:**

**Check Dockerfile Exists:**
```bash
# In project root
ls -la Dockerfile.test

# Should exist
```

**Check Location:**
```bash
# Must be in project root
pwd
# Should be: .../Agentic-AI-Governance

cd Agentic-AI-Governance
```

**Try Docker Compose:**
```bash
# If Dockerfile doesn't work, use compose
docker-compose up

# This builds and runs everything
```

---

### Issue 8: Tests Fail with "No Module"

**Error:**
```
FAILED tests/test_policies.py::TestFileOperationsPolicies - 
ImportError: cannot import name 'PolicyEnforcementProxy'
```

**Solutions:**

**Option 1: Verify Installation**
```bash
# Full clean reinstall
python3 -m pip uninstall agentic-ai-governance -y
python3 -m pip cache purge
python3 -m pip install -e .[dev]
```

**Option 2: Check Python Path**
```bash
# Debug script to verify imports
cat > test_import.py << 'EOF'
import sys
print("Python Path:")
for p in sys.path:
    print(f"  {p}")

try:
    from proxy import PolicyEnforcementProxy
    print("✓ Import successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
EOF

python3 test_import.py
```

**Option 3: Check conftest.py**
```bash
# Verify conftest.py sets up path
head -20 tests/conftest.py

# Should show sys.path manipulation
```

---

### Issue 9: Permission Denied (Linux)

**Error:**
```
Got permission denied while trying to connect to Docker daemon
```

**Why it happens:**
- User not in docker group
- Permissions not set correctly

**Solutions:**

**Add User to Docker Group:**
```bash
# Add user to group
sudo usermod -aG docker $USER

# Activate new group (choose one)
# Option A: Log out and back in
# Option B: Run this command
newgrp docker

# Verify
groups
# Should show: user_name docker

# Test
docker ps  # Should work now
```

**Or Use sudo:**
```bash
# Temporary workaround
docker ps  # Won't work
sudo docker ps  # Will work

# But not recommended for production
```

---

### Issue 10: Out of Memory

**Error:**
```
Cannot allocate memory
```

**Why it happens:**
- Docker container using too much memory
- System running low on RAM
- Resource limits too high

**Solutions:**

**Check System Memory:**
```bash
# macOS
vm_stat

# Linux
free -h

# Windows PowerShell
Get-Process | Measure-Object -Property WorkingSet -Sum
```

**Lower Resource Limits:**
```bash
# Edit src/policies/resource_policies.rego
vim src/policies/resource_policies.rego

# Change:
max_memory_mb = 2048  # ← Lower this

# To:
max_memory_mb = 1024  # ← Lower limit
```

**Restart Docker:**
```bash
# Kill all containers
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Prune unused resources
docker system prune -a

# Restart service
docker restart
```

---

## ❓ Advanced FAQ

### Q1: Can I Use This with Kubernetes?

**A:** Yes! Here's how:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-governance
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-governance
  template:
    metadata:
      labels:
        app: ai-governance
    spec:
      containers:
      - name: proxy
        image: ai-governance:latest
        ports:
        - containerPort: 8181
      - name: opa
        image: openpolicyagent/opa:latest
        args: ["run", "--server"]
        ports:
        - containerPort: 8181
```

Deploy with:
```bash
kubectl apply -f deployment.yaml
kubectl get pods
```

---

### Q2: How to Add Custom Policies?

**A:** Create Rego rules in policy files:

```rego
# Add to src/policies/custom_policies.rego
package policy.custom

# Example: Block execution on specific times
deny_peak_hours {
    input.action == "execute"
    hour := time.now_ns() / 3600000000000 % 24
    hour >= 12  # Block noon to 1 PM
    hour < 13
}

# Example: Rate limiting
deny_too_many_requests {
    input.action == "execute"
    get_request_count >= 100  # Max 100 per hour
}
```

Test it:
```bash
pytest tests/test_policies.py -v -k "custom"
```

---

### Q3: How to Monitor in Production?

**A:** Set up logging and monitoring:

```bash
# Save audit logs to file
opa run --server src/policies/policy.rego >> audit_$(date +%Y%m%d).log 2>&1 &

# Monitor in real-time
tail -f audit_$(date +%Y%m%d).log

# Or pipe to monitoring service
opa run --server src/policies/policy.rego \
    | tee audit.log        # Save to file
    | grep "DENY"          # Show denials only
```

Integrate with ELK Stack:
```yaml
# logstash.conf
input {
  file {
    path => "/var/log/opa/audit.log"
    start_position => "beginning"
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "ai-governance-%{+YYYY.MM.dd}"
  }
}
```

---

### Q4: Can I Use This with OpenAI Function Calling?

**A:** Yes! Example:

```python
from openai import OpenAI
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy

client = OpenAI()
proxy = PolicyEnforcementProxy()

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a system command safely",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "args": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }
]

def execute_function_call(tool_name, args):
    if tool_name == "run_command":
        result = proxy.execute_tool(
            args["command"],
            args["args"],
            {"source": "openai-gpt"}
        )
        return result

# Use in conversation...
messages = [{"role": "user", "content": "List files in workspace"}]
response = client.chat.completions.create(model="gpt-4", messages=messages, tools=tools)

# Process response and call functions as needed
```

---

### Q5: How Do I Set Up High Availability?

**A:** Use multiple instances:

```
Load Balancer
├─ Instance 1: Proxy + OPA
├─ Instance 2: Proxy + OPA
└─ Instance 3: Proxy + OPA
    ↓
Shared Policies (Git Repository)
    ↓
Shared Audit Logs (Database)
```

Implementation:
```bash
# Use docker-compose with scaling
docker-compose up --scale proxy=3

# Or Kubernetes:
kubectl scale deployment ai-governance --replicas=3
```

---

### Q6: How to Backup Policies?

**A:** Use Git version control:

```bash
# Initialize git (if not already done)
cd src/policies
git init
git add .
git commit -m "Policy snapshot"
git push origin main

# Or backup to file
tar -czf policies_backup_$(date +%Y%m%d).tar.gz src/policies/
```

---

### Q7: Can Multiple Apps Use Same OPA Server?

**A:** Yes! Share single OPA instance:

```python
# App 1
proxy1 = PolicyEnforcementProxy(
    opa_client=OpaClient(opa_url="http://opaserver:8181/v1/data/policy/allow")
)

# App 2
proxy2 = PolicyEnforcementProxy(
    opa_client=OpaClient(opa_url="http://opaserver:8181/v1/data/policy/allow")
)

# App 3
proxy3 = PolicyEnforcementProxy(
    opa_client=OpaClient(opa_url="http://opaserver:8181/v1/data/policy/allow")
)

# All share same policies and decisions
```

Benefits:
- Single policy source of truth
- Consistent decisions across apps
- Centralized audit logs

---

### Q8: How to Debug Policy Decisions?

**A:** Use OPA debug mode:

```bash
# Enable full debug output
opa version  # Check version first

# Run with metrics
opa run --server \
    --set=decision_logs.console=true \
    --set=profiler.enabled=true \
    src/policies/policy.rego

# In another terminal, test:
curl -X POST http://localhost:8181/v1/data/policy/allow \
    -H "Content-Type: application/json" \
    -d '{
        "input": {
            "command_name": "cat",
            "action": "execute",
            "args": ["/workspace/file.txt"]
        }
    }'

# Shows: decision, timing, resource usage
```

---

### Q9: Can I Use Different Policy Languages?

**A:** Currently Rego (OPA), but alternatives:

```python
# Could implement custom policy engine:
class CustomPolicyEngine:
    def evaluate(self, request):
        # Your custom logic
        if request.command == "cat":
            return True  # Allow
        return False     # Deny

# Then use it:
proxy = PolicyEnforcementProxy(
    policy_engine=CustomPolicyEngine()
)
```

But Rego (OPA) recommended because:
- Battle-tested
- Widely adopted
- Auditable
- Performance optimized

---

### Q10: What About Cost/Resources?

**A:** Resource usage breakdown:

```
OPA Server:           ~50MB RAM, <1% CPU idle
Docker Daemon:        ~100MB RAM base
Per Container:        Configurable (default 2GB)
Audit Logs:           ~1KB per operation

Total Overhead:       ~200MB + configured container limits

To Optimize:
- Use smaller base images
- Reduce container limits if possible
- Clean up old logs
- Use shared OPA instance
```

---

### Q11: Can I Use This Offline?

**A:** Yes! No internet required after setup:

```bash
# Only needed during setup:
pip install (downloads packages)
opa download (downloads binary)
docker pull (downloads image)

# After that, everything is local
opa run --server src/policies/policy.rego  # Local
docker run ...                               # Local
python proxy.execute_tool(...)               # Local

# No internet needed for runtime
```

---

### Q12: How to Migrate From Old Version?

**A:** Upgrade path:

```bash
# 1. Backup current config
cp -r src src.backup

# 2. Pull latest code
git pull origin main

# 3. Install new version
python3 -m pip install -e .[dev]

# 4. Run tests
pytest tests/ -v

# 5. Compare policies
diff src.backup/policies/ src/policies/

# 6. Merge custom policies if needed
# Edit src/policies/*.rego

# 7. Restart service
```

---

### Q13: What About GDPR/Data Protection?

**A:** Built-in privacy features:

```
✓ Data minimization:
  - Only collect necessary info
  - Audit logs contain metadata only
  - Sensitive data redacted

✓ Data retention:
  - Set log rotation policies
  - Delete old logs automatically
  - Archive if needed

✓ Data access:
  - Expose audit API if needed
  - Support export format (JSON)
  - Comply with data subject rights

✓ Data security:
  - Encryption at rest (if stored)
  - Encryption in transit (HTTPS)
  - Access control (who sees logs)
```

---

### Q14: Can I Use This for Compliance?

**A:** Yes! Supports:

```
✓ SOC 2: Audit logs, access controls
✓ ISO 27001: Security policies, logging
✓ HIPAA: Isolation, access logs
✓ PCI-DSS: Secured execution, logging
✓ NIST: Compliance controls
✓ GDPR: Data protection, audit trails

Export logs for audit:
opa run --server ... > compliance_audit.log

Analyze logs:
grep "DENY" compliance_audit.log > denials.txt
```

---

### Q15: Emergency Procedures?

**A:** If something goes wrong:

```bash
# Emergency stop everything
docker stop $(docker ps -aq)
pkill -f opa
pkill -f python

# Check what happened
docker logs <container-id>
opa run --help

# Reset to known-good state
git checkout HEAD -- src/policies/

# Restart carefully
pytest tests/ -v  # Verify first
opa run --server src/policies/policy.rego &
python3 src/main.py
```

---

## 📞 Getting Help

### When Stuck:

1. **Check Logs** - Look at OPA console output
2. **Run Tests** - `pytest tests/test_policies.py -v`
3. **Read Docs** - [GUIDE.md](GUIDE.md)
4. **Check Examples** - Look at test files
5. **Search Issues** - GitHub Issues
6. **Simplify** - Reduce to minimal reproduction

### Minimal Reproduction Example:

```python
# test_issue.py
from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient

# Just the failing case
proxy = PolicyEnforcementProxy(opa_client=OpaClient())
result = proxy.execute_tool("your_command", [], {})
print(result)
```

### Report Issues With:
- Error message (full text)
- Reproduction steps
- Expected behavior
- Actual behavior
- Your environment (OS, Python version, Docker version)

---

## 🎓 Learning Resources

- **OPA Documentation:** https://www.openpolicyagent.org/docs/
- **Rego Language:** https://www.openpolicyagent.org/docs/latest/policy-language/
- **Docker Docs:** https://docs.docker.com/
- **This Guide:** GUIDE.md

---

**Still stuck?** Review:
1. [GUIDE.md](GUIDE.md) - Complete usage guide
2. [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) - How it works
3. [GETTING_STARTED_CHECKLIST.md](GETTING_STARTED_CHECKLIST.md) - Setup verification
4. Test files - Working examples
5. This document - Specific issues

**Remember:** Most issues have simple solutions! Start with the basics and work through systematically.
