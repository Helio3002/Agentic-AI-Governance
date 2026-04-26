# 🔧 Getting Started Checklist for Agentic AI Governance

Use this checklist to ensure you have successfully set up and configured the tool.

---

## ✓ Pre-Installation Checklist (10 min)

- [ ] **System Requirements Met**
  - [ ] macOS, Linux, or Windows
  - [ ] At least 4GB RAM
  - [ ] 2GB free disk space
  - [ ] Stable internet connection

- [ ] **Prerequisites Installed**
  - [ ] Python 3.11+ installed (verify: `python3 --version`)
  - [ ] Git installed (verify: `git --version`)
  - [ ] Comfortable using terminal/command line

---

## ✓ Installation Checklist (30 min)

### Part 1: Get the Code
- [ ] Clone or download repository
  ```bash
  git clone https://github.com/Helio3002/Agentic-AI-Governance.git
  cd Agentic-AI-Governance
  ```
- [ ] Verify files exist (especially `src/` folder)

### Part 2: Install Python Tools
- [ ] Upgraded pip: `python3 -m pip install --upgrade pip`
- [ ] Installed project dependencies: `python3 -m pip install -e .[dev]`
- [ ] Verify installation: `python3 -c "import proxy"`

### Part 3: Install Docker
- [ ] Docker installed
  - [ ] macOS: `brew install docker` or Docker Desktop
  - [ ] Linux: `sudo apt install docker.io`
  - [ ] Windows: Docker Desktop installed
- [ ] Verify: `docker --version` (shows version)
- [ ] Docker daemon running
  - [ ] macOS: Docker Desktop open
  - [ ] Linux: `sudo systemctl start docker`
  - [ ] Windows: Docker running in taskbar

### Part 4: Install OPA
- [ ] OPA installed
  - [ ] macOS: `brew install opa`
  - [ ] Linux: Downloaded and in PATH
  - [ ] Windows: `opa.exe` in Program Files
- [ ] Verify: `opa --version` (shows version)

### Part 5: Create Workspace
- [ ] Created `/workspace` directory: `mkdir -p workspace`
- [ ] Verified it exists: `ls -la workspace/`

---

## ✓ Verification Checklist (10 min)

### Run Quick Verification
- [ ] Python check:
  ```bash
  python3 -c "import sys; print(f'Python {sys.version}')"
  ```

- [ ] Docker check:
  ```bash
  docker ps  # Should not show error
  ```

- [ ] OPA check:
  ```bash
  opa version
  ```

- [ ] Project check:
  ```bash
  python3 -m pytest tests/test_policies.py::TestInputValidation -v
  ```

✅ **All checks pass?** Move to Configuration

---

## ✓ Configuration Checklist (15 min)

### 1. Review Default Configuration
- [ ] Read `src/policies/policy.rego`
- [ ] Read `src/proxy/validator.py`
- [ ] Understand default settings

### 2. Customize Allowed Commands (Optional)
- [ ] Edit `src/proxy/validator.py`
- [ ] Add/remove commands from `DEFAULT_ALLOWED_COMMANDS`
- [ ] Save file

### 3. Customize Allowed Paths (Optional)
- [ ] Edit `src/policies/file_operations.rego`
- [ ] Update `allowed_read_paths`
- [ ] Update `allowed_write_paths`
- [ ] Save file

### 4. Customize Network Access (Optional)
- [ ] Edit `src/policies/network_policies.rego`
- [ ] Update `allowed_domains`
- [ ] Update `allowed_ports`
- [ ] Save file

### 5. Customize Resource Limits (Optional)
- [ ] Edit `src/policies/resource_policies.rego`
- [ ] Review `max_memory_mb`
- [ ] Review `max_cpu_percent`
- [ ] Adjust if needed for your system

---

## ✓ Testing Checklist (15 min)

### Run Unit Tests
- [ ] No setup needed (no OPA server required)
  ```bash
  pytest tests/test_policies.py -v
  ```
- [ ] All 34 tests pass (green checkmarks)
- [ ] No errors or failures

### Run Specific Test Categories
- [ ] File operations tests: `pytest tests/test_policies.py::TestFileOperationsPolicies -v`
- [ ] Network tests: `pytest tests/test_policies.py::TestNetworkPolicies -v`
- [ ] Admin tests: `pytest tests/test_policies.py::TestAdminPolicies -v`
- [ ] All pass: ✓

### Generate Coverage Report
- [ ] Run: `pytest tests/ --cov=src --cov-report=html`
- [ ] Open `htmlcov/index.html`
- [ ] Choose minimum 80% coverage target

---

## ✓ Running Locally Checklist (10 min)

### Terminal 1: Start OPA Server
- [ ] Navigate to project directory
- [ ] Run OPA: `opa run --server --set=decision_logs.console=true src/policies/policy.rego`
- [ ] See: "Listening on http://127.0.0.1:8181"
- [ ] **Leave running**

### Terminal 2: Run Application
- [ ] Navigate to project directory
- [ ] Run: `python3 src/main.py`
- [ ] See output from proxy execution
- [ ] No errors displayed

### Verify Logs
- [ ] Check Terminal 1 for policy decisions
- [ ] See entries like "Policy Decision: ALLOW/DENY"
- [ ] Confirms system is working

---

## ✓ Using with Docker Checklist (10 min)

### Option 1: Docker Compose
- [ ] Docker daemon running
- [ ] Run: `docker-compose up`
- [ ] Wait for build and execution
- [ ] See test results
- [ ] Tests pass: ✓

### Option 2: Manual Docker
- [ ] Build image: `docker build -f Dockerfile.test -t ai-gov-test .`
- [ ] Run container: `docker run ai-gov-test`
- [ ] See tests execute

---

## ✓ Integration Checklist (20 min)

### Ready to Use with Your AI Agent?
- [ ] All tests pass: ✓
- [ ] OPA server runs successfully
- [ ] Configuration matches your needs
- [ ] Docker installed and working
- [ ] You understand policy decisions (read policy docs)

### First Integration
- [ ] Create simple test script:
  ```python
  from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
  from proxy.opa_client import OpaClient
  
  proxy = PolicyEnforcementProxy(opa_client=OpaClient())
  result = proxy.execute_tool("echo", ["hello"], {"action": "execute"})
  print(result)
  ```
- [ ] Run script: `python3 test_script.py`
- [ ] See result: Success ✓

### Integrate with Your Framework
- [ ] Choose framework: LangChain, OpenAI, etc.
- [ ] See examples in [GUIDE.md](GUIDE.md)
- [ ] Adapt code for your use case
- [ ] Test with test data first
- [ ] Move to production when ready

---

## ✓ Final Verification Checklist

### System is Ready When:
- [ ] ✅ All dependencies installed
- [ ] ✅ All tests passing
- [ ] ✅ OPA server can start and stop
- [ ] ✅ Docker works
- [ ] ✅ You understand policy files
- [ ] ✅ Configuration matches your needs
- [ ] ✅ Can run example code
- [ ] ✅ Audit logs appear in OPA console

### You Have Successfully Set Up:
- [ ] ✅ Python environment
- [ ] ✅ Docker sandbox
- [ ] ✅ OPA policy engine
- [ ] ✅ Security policies
- [ ] ✅ Testing framework
- [ ] ✅ Audit logging
- [ ] ✅ Documentation understanding

---

## 📊 Troubleshooting During Setup

### If Python Tests Fail
```bash
# 1. Clear cache
rm -rf .pytest_cache __pycache__

# 2. Reinstall
python3 -m pip install -e .[dev]

# 3. Try again
pytest tests/test_policies.py -v
```

### If Docker Won't Start
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker

# Windows
# Open Docker Desktop from Start Menu
```

### If OPA Won't Start
```bash
# Check if port is in use
lsof -i :8181

# Kill process if needed
kill -9 <PID>

# Try different port
opa run --server --addr localhost:8182 src/policies/policy.rego
```

### If Can't Import Modules
```bash
# Make sure you're in project directory
cd /path/to/Agentic-AI-Governance

# Reinstall in edit mode
python3 -m pip install -e .[dev]

# Test import
python3 -c "import proxy; print('OK')"
```

---

## 🎓 Next Steps

### Level 1: Beginner
- [ ] Completed all checklists above
- [ ] Read [GUIDE.md](GUIDE.md)
- [ ] Run examples from guide
- [ ] Understand basic operations

### Level 2: Intermediate  
- [ ] Customize all policy files
- [ ] Run integration tests with OPA server
- [ ] Create test scenarios for your use case
- [ ] Review audit logs

### Level 3: Advanced
- [ ] Write custom Rego rules
- [ ] Integrate with your AI framework
- [ ] Deploy using Docker Compose
- [ ] Set up CI/CD pipeline

---

## 📈 Success Metrics

Track your setup progress:

| Milestone | Status | Date |
|-----------|--------|------|
| Dependencies installed | ☐ | |
| All tests passing | ☐ | |
| OPA server running | ☐ | |
| Docker working | ☐ | |
| Policies customized | ☐ | |
| First integration test | ☐ | |
| Production ready | ☐ | |

---

## ✅ Setup Completion

When all boxes are checked, you're ready to use Agentic AI Governance!

**Estimated Total Time:** 60-90 minutes

**Need Help?**
1. Review [GUIDE.md](GUIDE.md)
2. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
3. Look at test examples in `tests/`
4. Check [src/policies/README.md](src/policies/README.md)

**Congratulations!** 🎉 You now have a production-ready secure AI governance system.
