import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class DockerSandboxManager:
    """Runs agent tool calls inside a hardened Docker sandbox.

    SECURITY NOTE: Uses container-level controls to limit host exposure and reduce blast radius.
    """

    def __init__(self, workspace_dir: Path, image: str = "python:3.11-slim") -> None:
        self.workspace_dir = workspace_dir.resolve()
        self.image = image
        self._ensure_workspace_exists()
        self._ensure_docker_available()

    def _ensure_workspace_exists(self) -> None:
        if not self.workspace_dir.exists():
            self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_docker_available(self) -> None:
        if shutil.which("docker") is None:
            raise RuntimeError("Docker is required for sandboxed execution but was not found on PATH.")

    def _requires_workspace_write(self, args: List[str]) -> bool:
        return any(arg in {"-o", "--output"} for arg in args)

    def _build_docker_command(self, tool_name: str, args: List[str], metadata: Optional[Dict[str, Any]] = None) -> List[str]:
        mount_mode = "rw" if self._requires_workspace_write(args) else "ro"
        network_flags = ["--network", "none"]
        if metadata and metadata.get("action") == "network":
            network_flags = ["--network", "bridge"]

        return [
            "docker",
            "run",
            "--rm",
            "--read-only",
            "--security-opt",
            "no-new-privileges",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=64m",
            *network_flags,
            "--cap-drop=ALL",
            "--pids-limit=64",
            "--memory=256m",
            "-v",
            f"{self.workspace_dir}:{self.workspace_dir}:{mount_mode}",
            self.image,
            tool_name,
            *args,
        ]

    def run(self, tool_name: str, args: List[str], metadata: Optional[Dict[str, Any]] = None) -> tuple[int, str, str]:
        docker_command = self._build_docker_command(tool_name, args, metadata)
        process = subprocess.run(
            docker_command,
            capture_output=True,
            text=True,
            cwd=str(self.workspace_dir),
            check=False,
        )
        return process.returncode, process.stdout, process.stderr
