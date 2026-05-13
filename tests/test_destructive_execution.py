#!/usr/bin/env python3
"""
Test Case 3: Destructive Execution - Attempting recursive delete without HITL authorization.

This script demonstrates an agent trying to delete directories recursively without the required
human-in-the-loop authorization flag, which should be denied by the policy.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient


def test_destructive_execution():
    """Run the destructive execution test case."""
    print("🛑 Test Case 3: Destructive Execution")
    print("Attempting recursive delete without HITL authorization...")

    opa_client = OpaClient()
    proxy = PolicyEnforcementProxy(opa_client=opa_client)

    # Test 1: Recursive delete without HITL authorization should be denied.
    print("\n1. Attempting recursive delete on /workspace/logs without HITL...")
    denied = proxy.evaluate_policy(
        tool_name="rm",
        action="file_write",
        args=["-rf", "/workspace/logs"],
        metadata={
            "destination": "/workspace/logs",
            "target_path": "/workspace/logs",
            "user_id": "test_agent",
            "user_approval": True,
            "hitl_authorized": False,
            "request_id": "req-100",
        },
    )
    print(f"   Result: {'✅ ALLOWED' if denied else '❌ DENIED (as expected)'}")

    # Test 2: Recursive delete with HITL authorization should be allowed.
    print("\n2. Attempting recursive delete on /workspace/logs with HITL...")
    allowed = proxy.evaluate_policy(
        tool_name="rm",
        action="file_write",
        args=["-rf", "/workspace/logs"],
        metadata={
            "destination": "/workspace/logs",
            "target_path": "/workspace/logs",
            "user_id": "admin_agent",
            "user_approval": True,
            "hitl_authorized": True,
            "request_id": "req-101",
        },
    )
    print(f"   Result: {'✅ ALLOWED' if allowed else '❌ DENIED'}")

    print("\n📋 Test Results:")
    print(f"   - Recursive delete without HITL blocked: {'PASS' if not denied else 'FAIL'}")
    print(f"   - Recursive delete with HITL allowed: {'PASS' if allowed else 'FAIL'}")

    if not denied and allowed:
        print("\n🎉 Destructive execution HITL enforcement is working correctly!")
        return True
    print("\n❌ Destructive execution HITL enforcement failed!")
    return False


if __name__ == "__main__":
    success = test_destructive_execution()
    sys.exit(0 if success else 1)
