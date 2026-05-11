#!/usr/bin/env python3
"""
Test Case 1: Spatial Overreach - Attempting to read sensitive host environment variables.

This script demonstrates an agent attempting to read sensitive environment variables
that are outside its assigned workspace volume mount, which should be denied by policy.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proxy.policy_enforcement_proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient


def test_spatial_overreach():
    """Test spatial overreach by attempting to read sensitive env vars."""

    print("🧪 Test Case 1: Spatial Overreach")
    print("Attempting to read sensitive host environment variables outside workspace...")

    # Initialize proxy
    opa_client = OpaClient()
    proxy = PolicyEnforcementProxy(opa_client=opa_client)

    # Test 1: Try to read allowed env var (should succeed)
    print("\n1. Attempting to read allowed environment variable 'PATH'...")
    allowed = proxy.evaluate_policy(
        tool_name="read_env",
        action="read_env",
        args=["PATH"],
        metadata={"user_id": "test_agent", "request_id": "test-001"}
    )
    print(f"   Result: {'✅ ALLOWED' if allowed else '❌ DENIED'}")

    # Test 2: Try to read sensitive env var (should be denied)
    print("\n2. Attempting to read sensitive environment variable 'HOST_IP'...")
    denied = proxy.evaluate_policy(
        tool_name="read_env",
        action="read_env",
        args=["HOST_IP"],
        metadata={"user_id": "test_agent", "request_id": "test-002"}
    )
    print(f"   Result: {'✅ ALLOWED' if denied else '❌ DENIED (as expected)'}")

    # Test 3: Try another sensitive var
    print("\n3. Attempting to read sensitive environment variable 'HOSTNAME'...")
    denied2 = proxy.evaluate_policy(
        tool_name="read_env",
        action="read_env",
        args=["HOSTNAME"],
        metadata={"user_id": "test_agent", "request_id": "test-003"}
    )
    print(f"   Result: {'✅ ALLOWED' if denied2 else '❌ DENIED (as expected)'}")

    print("\n📋 Test Results:")
    print(f"   - Allowed env var access: {'PASS' if allowed else 'FAIL'}")
    print(f"   - Sensitive env var blocked: {'PASS' if not denied else 'FAIL'}")
    print(f"   - Host env var blocked: {'PASS' if not denied2 else 'FAIL'}")

    if allowed and not denied and not denied2:
        print("\n🎉 Spatial overreach protection is working correctly!")
        return True
    else:
        print("\n❌ Spatial overreach protection failed!")
        return False


if __name__ == "__main__":
    success = test_spatial_overreach()
    sys.exit(0 if success else 1)