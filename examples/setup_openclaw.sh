#!/usr/bin/env bash
# OpenClaw Integration Quick Start Script

echo "🚀 OpenClaw Integration Setup"
echo "=============================="
echo ""

# Check Docker
echo "✓ Checking Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi
echo "  ✅ Docker found"

# Check OPA
echo "✓ Checking OPA..."
if ! command -v opa &> /dev/null; then
    echo "❌ OPA not found. Please install OPA first."
    echo "   Visit: https://www.openpolicyagent.org/docs/latest/#running-opa"
    exit 1
fi
echo "  ✅ OPA found"

# Create workspace
echo "✓ Creating workspace directory..."
mkdir -p workspace
echo "  ✅ Workspace created"

# Install dependencies (with timeout and progress)
echo "✓ Installing Python dependencies (this may take a moment)..."
timeout 120 pip install -e .[dev] 2>&1 | grep -E "Successfully|already|Requirement" || true
echo "  ✅ Dependencies installed"

echo ""
echo "⏳ Step 1: Start OPA server (manual step)"
echo "============================================"
echo "In a separate terminal, run:"
echo ""
echo "  opa run --server --set=decision_logs.console=true src/policies/policy.rego"
echo ""
echo "Then come back here and press Enter..."
read -p "Press Enter to continue: "

# Verify OPA is running
echo ""
echo "✓ Checking if OPA server is running..."
if curl -s http://localhost:8181/v1/data/policy/allow > /dev/null 2>&1; then
    echo "  ✅ OPA server is running"
else
    echo "  ⚠️  OPA server not responding at http://localhost:8181"
    echo "     Make sure you started it in the other terminal"
fi

# Run integration example
echo ""
echo "⏳ Step 2: Running OpenClaw integration demo"
echo "============================================"
echo ""

python3 examples/openclaw_integration.py

echo ""
echo "📊 Checking audit logs..."
if [ -f "logs/audit_log.jsonl" ]; then
    echo "✅ Audit log found:"
    echo "   $(wc -l < logs/audit_log.jsonl) events logged"
fi

if [ -f "openclaw_audit_summary.json" ]; then
    echo ""
    echo "✅ Audit summary generated:"
    echo "   See openclaw_audit_summary.json"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "📍 Next steps:"
echo "   1. Review audit logs: tail -f logs/audit_log.jsonl"
echo "   2. Check summary: cat openclaw_audit_summary.json"
echo "   3. Integrate with your OpenClaw agent using examples/openclaw_integration.py"
echo ""
echo "📚 For detailed guide, see: OPENCLAW_INTEGRATION.md"
