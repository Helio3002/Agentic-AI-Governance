#!/usr/bin/env bash
# OpenClaw Integration Quick Start Script

set -e

echo "🚀 OpenClaw Integration Setup"
echo "=============================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check OPA
if ! command -v opa &> /dev/null; then
    echo "❌ OPA not found. Please install OPA first."
    echo "   Visit: https://www.openpolicyagent.org/docs/latest/#running-opa"
    exit 1
fi

# Create workspace
echo "📁 Creating workspace directory..."
mkdir -p workspace

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -e .[dev] > /dev/null 2>&1

# Start OPA in background
echo "🔒 Starting OPA policy engine..."
opa run --server --set=decision_logs.console=true src/policies/policy.rego > /tmp/opa.log 2>&1 &
OPA_PID=$!
echo "   OPA started (PID: $OPA_PID)"

# Wait for OPA to be ready
sleep 2

# Run integration example
echo ""
echo "✅ Setup complete! Running OpenClaw integration demo..."
echo "=============================="
echo ""

python3 examples/openclaw_integration.py

echo ""
echo "📊 Checking audit logs..."
if [ -f "logs/audit_log.jsonl" ]; then
    echo "✅ Audit log found:"
    wc -l logs/audit_log.jsonl
fi

if [ -f "openclaw_audit_summary.json" ]; then
    echo ""
    echo "✅ Audit summary generated:"
    cat openclaw_audit_summary.json | python3 -m json.tool | head -20
fi

# Cleanup
echo ""
echo "🧹 Cleanup: Stopping OPA..."
kill $OPA_PID 2>/dev/null || true

echo "✨ Done! Your OpenClaw agent is now integrated with Agentic AI Governance"
