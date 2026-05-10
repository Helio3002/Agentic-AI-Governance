# OpenClaw Setup Instructions

## Two Setup Options

### Option 1: Automated Setup (Recommended)
Runs everything automatically, including OPA server startup and cleanup.

```bash
bash examples/setup_openclaw_auto.sh
```

**What it does:**
- ✅ Checks Docker and OPA installation
- ✅ Creates workspace and logs directories
- ✅ Installs Python dependencies
- ✅ Starts OPA server automatically
- ✅ Runs the integration demo
- ✅ Shows audit results
- ✅ Stops OPA when done

**Time:** ~2-3 minutes

---

### Option 2: Manual Setup (Full Control)
Start OPA in a separate terminal, giving you more control.

```bash
# Terminal 1: Start OPA (keep running)
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# Terminal 2: Run setup
bash examples/setup_openclaw.sh
```

**What it does:**
- ✅ Checks Docker and OPA installation  
- ✅ Creates workspace directory
- ✅ Installs Python dependencies
- ✅ Waits for you to manually start OPA
- ✅ Runs the integration demo
- ✅ Shows results

**Benefits:** OPA server stays running for further testing

---

## Troubleshooting

### Setup hangs at "Installing Python dependencies"

**Problem:** Pip install taking too long or stuck

**Solution:**
```bash
# Stop with Ctrl+C and run manually:
pip install -e .[dev]

# Then try setup again
bash examples/setup_openclaw_auto.sh
```

### "OPA not found" error

**Problem:** OPA is not installed

**Solution:**
```bash
# Install OPA
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_x86_64
chmod +x opa
sudo mv opa /usr/local/bin/

# Verify
opa version
```

### "Docker not found" error

**Problem:** Docker is not installed or not running

**Solution:**
```bash
# Install Docker: https://docs.docker.com/get-docker/

# Start Docker service:
sudo systemctl start docker  # On Linux
# Or start Docker Desktop on macOS/Windows

# Verify
docker ps
```

### "OPA server not responding"

**Problem:** OPA failed to start

**Solution:**
```bash
# Check OPA directly
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# If error: check the policy file syntax
opa test src/policies/
```

### Setup shows audit_log.jsonl but it's empty

This is normal - commands may fail if GUIDE.md doesn't exist. The audit log still records the events.

---

## After Setup

### View Audit Logs
```bash
# See all events
tail logs/audit_log.jsonl

# Pretty print (last 5 events)
tail logs/audit_log.jsonl | python3 -m json.tool | head -50
```

### View Audit Summary
```bash
cat openclaw_audit_summary.json | python3 -m json.tool
```

### Integrate with Your Agent
```python
from examples.openclaw_integration import OpenClawIntegration

agent = OpenClawIntegration()
result = agent.list_directory("/workspace")
print(result)
```

---

## Running OPA Server Separately

If you want to keep OPA running for multiple integration tests:

```bash
# Terminal 1 (keep open)
opa run --server --set=decision_logs.console=true src/policies/policy.rego

# Terminal 2+ (run as many times as needed)
python examples/openclaw_integration.py
python examples/openclaw_integration.py  # Run again with fresh agent
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Auto setup | `bash examples/setup_openclaw_auto.sh` |
| Manual setup | `bash examples/setup_openclaw.sh` |
| Run demo only | `python examples/openclaw_integration.py` |
| Start OPA | `opa run --server src/policies/policy.rego` |
| View logs | `tail logs/audit_log.jsonl` |
| View summary | `cat openclaw_audit_summary.json \| python3 -m json.tool` |

---

## Next Steps

1. **Run the setup** using Option 1 or Option 2 above
2. **Review the audit logs** to see what was executed
3. **Read** [OPENCLAW_INTEGRATION.md](../OPENCLAW_INTEGRATION.md) for detailed integration guide
4. **Integrate** with your own OpenClaw agent

---

Need help? Check `OPENCLAW_INTEGRATION.md` for detailed usage examples.
