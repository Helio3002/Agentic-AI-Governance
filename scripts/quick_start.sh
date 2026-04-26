#!/bin/bash
# Quick start script for Agentic AI Governance test environment

set -e

echo "=========================================="
echo "Agentic AI Governance - Quick Start Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo ""
echo "Installing project dependencies..."
python3 -m pip install --upgrade pip > /dev/null
python3 -m pip install -e .[dev] > /dev/null
echo "✓ Dependencies installed"

# Check OPA availability
echo ""
echo "Checking OPA availability..."
if command -v opa &> /dev/null; then
    opa_version=$(opa version 2>&1 | head -n 1)
    echo "✓ OPA is installed: $opa_version"
else
    echo "⚠ OPA not found. Install with:"
    echo "  macOS: brew install opa"
    echo "  Linux: curl https://openpolicyagent.org/downloads/latest/opa_linux_x86_64 -o opa && chmod +x opa && sudo mv opa /usr/local/bin/"
fi

# Create workspace directory
echo ""
echo "Creating workspace directory..."
mkdir -p workspace
echo "✓ Workspace directory created at: $(pwd)/workspace"

# Run basic tests
echo ""
echo "Running basic unit tests..."
pytest tests/test_policies.py::TestInputValidation -v --tb=short 2>&1 | tail -n 10
echo ""
echo "✓ Basic tests completed"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Run all unit tests (no OPA server required):"
echo "   pytest tests/test_policies.py -v"
echo ""
echo "2. Start OPA server (in a separate terminal):"
echo "   opa run --server --set=decision_logs.console=true src/policies/policy.rego"
echo ""
echo "3. Run integration tests (requires OPA server):"
echo "   pytest tests/test_integration.py -v"
echo ""
echo "4. Run all tests with coverage:"
echo "   pytest tests/ --cov=src --cov-report=html"
echo ""
echo "5. Use Docker Compose for isolated testing:"
echo "   docker-compose up"
echo ""
