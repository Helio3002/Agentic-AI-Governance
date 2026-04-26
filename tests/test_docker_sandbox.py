import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from sandbox_manager.docker_sandbox import DockerSandboxManager


class DockerSandboxManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace_dir = Path("/tmp")

    @patch("sandbox_manager.docker_sandbox.shutil.which", return_value="/usr/bin/docker")
    @patch("sandbox_manager.docker_sandbox.subprocess.run")
    def test_run_builds_restricted_command(self, mock_run, mock_which):
        manager = DockerSandboxManager(workspace_dir=self.workspace_dir)
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="ok", stderr=""
        )
        exit_code, stdout, stderr = manager.run("echo", ["hello"], {"action": "execute"})
        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout, "ok")
        self.assertEqual(stderr, "")
        self.assertIn("--read-only", mock_run.call_args.args[0])
        self.assertIn("--network", mock_run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
