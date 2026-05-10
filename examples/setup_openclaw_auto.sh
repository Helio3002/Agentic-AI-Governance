#!/usr/bin/env bash
# OpenClaw Integration - Auto Setup (without manual steps)

echo "🚀 OpenClaw Integration Auto Setup"
echo "===================================="
echo ""

# Set error handling
trap 'echo "Error occurred. Cleaning up..."; kill $OPA_PID 2>/dev/null; exit 1' ERR

# Check prerequisites
echo "✓ Checking prerequisites..."
for cmd in docker opa python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd not found. Please install it first."
        exit 1
    fi
done
echo "  ✅ All prerequisites found"

# Setup
echo "✓ Creating workspace..."
mkdir -p workspace logs

echo "✓ Installing dependencies..."
timeout 180 pip install -e .[dev] 2>&1 | tail -5

echo "✓ Starting OPA server..."
opa run --server --set=decision_logs.console=true src/policies/policy.rego > /tmp/opa.log 2>&1 &
OPA_PID=$!

# Wait for OPA startup
sleep 3

if ! curl -s http://localhost:8181/v1/data/policy/allow > /dev/null 2>&1; then
    echo "❌ OPA server failed to start"
    cat /tmp/opa.log
    exit 1
fi
echo "  ✅ OPA server running (PID: $OPA_PID)"

# Run demo
echo ""
echo "🎉 Running OpenClaw Integration Demo"
echo "===================================="
echo ""

python3 examples/openclaw_integration.py

# Show results
echo ""
echo "📊 Demo Results"
echo "===================================="

if [ -f "logs/audit_log.jsonl" ]; then
    echo "✅ Audit log: $(wc -l < logs/audit_log.jsonl) events"
fi

if [ -f "openclaw_audit_summary.json" ]; then
    echo "✅ Summary saved to: openclaw_audit_summary.json"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up (stopping OPA)..."
kill $OPA_PID 2>/dev/null
sleep 1

echo "✨ Setup complete!"
echo ""
echo "📚 Next: Read OPENCLAW_INTEGRATION.md for integration guide"
