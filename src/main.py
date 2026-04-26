from pathlib import Path

from proxy import PolicyEnforcementProxy
from proxy.opa_client import OpaClient
from sandbox_manager import DockerSandboxManager


def main() -> None:
    workspace_dir = Path.cwd() / "workspace"
    sandbox = DockerSandboxManager(workspace_dir=workspace_dir)
    opa_client = OpaClient()
    proxy = PolicyEnforcementProxy(opa_client=opa_client, sandbox_manager=sandbox)

    tool_name = "echo"
    args = ["Hello, secure proxy!"]
    metadata = {
        "source": "langgraph",
        "request_id": "req-123",
        "action": "execute",
        "user_approval": False,
    }

    result = proxy.execute_tool(tool_name, args, metadata)
    print("Proxy execution result:", result)


if __name__ == "__main__":
    main()
