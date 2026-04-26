from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OpaClient:
    """OPA policy client with HTTP and local evaluation support.

    SECURITY NOTE: OPA is the deterministic policy decision point for all agent tool calls.
    """

    def __init__(self, opa_url: str = "http://localhost:8181/v1/data/policy/allow", opa_binary: str = "opa") -> None:
        self.opa_url = opa_url
        self.opa_binary = opa_binary

    def evaluate(self, input_data: Dict[str, Any], policy_path: Optional[str] = None) -> Dict[str, Any]:
        if self.opa_url:
            return self._evaluate_http(input_data)
        if policy_path is not None:
            return self._evaluate_local(input_data, policy_path)
        raise RuntimeError("No OPA evaluation backend configured.")

    def _evaluate_http(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        payload = json.dumps({"input": input_data}).encode("utf-8")
        request = Request(self.opa_url, data=payload, headers={"Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=10) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise RuntimeError(f"OPA HTTP policy evaluation failed: {exc.code} {exc.reason}")
        except URLError as exc:
            raise RuntimeError(f"OPA HTTP policy evaluation failed: {exc.reason}")

    def _evaluate_local(self, input_data: Dict[str, Any], policy_path: str) -> Dict[str, Any]:
        if shutil.which(self.opa_binary) is None:
            raise RuntimeError("OPA binary is not available on PATH.")
        command = [self.opa_binary, "eval", "--format", "json", "-d", policy_path, "data.policy.allow"]
        process = subprocess.run(
            command,
            input=json.dumps({"input": input_data}).encode("utf-8"),
            capture_output=True,
            check=False,
        )
        if process.returncode != 0:
            raise RuntimeError(
                f"OPA local policy evaluation failed: {process.stderr.decode('utf-8', errors='ignore')}"
            )
        return json.loads(process.stdout)
