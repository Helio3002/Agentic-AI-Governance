import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .opa_client import OpaClient
from .validator import ToolRequestValidator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

SENSITIVE_PATTERNS = [
    r"(?:AKIA|ASIA)[A-Z0-9]{16}",
    r"(?:\bpassword\b|\bpasswd\b|\bsecret\b)\s*[:=]\s*\S+",
    r"\b\d{3}-\d{2}-\d{4}\b",
]


class PolicyEnforcementProxy:
    """Proxy that mediates all autonomous agent tool calls through OPA and sandboxing.

    SECURITY NOTE: Deterministic policy decisions are made by OPA, not by the LLM.
    Security controls rely on an explicit default-deny policy and strong input validation.
    """

    def __init__(
        self,
        opa_client: Optional[OpaClient] = None,
        sandbox_manager: Optional[Any] = None,
        validator: Optional[ToolRequestValidator] = None,
        policy_path: Optional[Path] = None,
        audit_log_path: Optional[Path] = None,
    ) -> None:
        self.opa_client = opa_client or OpaClient()
        self.sandbox_manager = sandbox_manager
        self.validator = validator or ToolRequestValidator()
        self.policy_path = policy_path or Path(__file__).resolve().parents[1] / "policies" / "policy.rego"

        if audit_log_path is not None:
            self.audit_log_path = Path(audit_log_path)
        elif os.getenv("AGENTIC_AUDIT_LOG_PATH"):
            self.audit_log_path = Path(os.getenv("AGENTIC_AUDIT_LOG_PATH"))
        else:
            default_log_path = Path(__file__).resolve().parents[2] / "logs" / "audit_log.jsonl"
            legacy_log_path = Path(__file__).resolve().parents[1] / "logs" / "audit_log.jsonl"
            self.audit_log_path = (
                legacy_log_path
                if legacy_log_path.exists() and not default_log_path.exists()
                else default_log_path
            )

        self.audit_log_file = None
        if self.audit_log_path is not None:
            self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
            self.audit_log_file = self.audit_log_path.open("a", encoding="utf-8")

    def _mask_sensitive_output(self, raw_output: str) -> str:
        sanitized = raw_output
        for pattern in SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED]", sanitized)
        return sanitized

    def sanitize_argument(self, arg: str) -> str:
        return self.validator.validate_args([arg])[0]

    def filter_output(self, raw_output: str) -> str:
        return self._mask_sensitive_output(raw_output)

    def _log(self, event_type: str, payload: Dict[str, Any]) -> None:
        record = {"event": event_type, "payload": payload}
        message = json.dumps(record, ensure_ascii=False)
        logger.info(message)
        if self.audit_log_file is not None:
            self.audit_log_file.write(message + "\n")
            self.audit_log_file.flush()

    def _build_policy_input(self, tool_name: str, action: str, args: List[str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "tool": tool_name,
            "command_name": tool_name,
            "action": action,
            "args": args,
            "metadata": metadata,
        }

    def evaluate_policy(self, tool_name: str, action: str, args: List[str], metadata: Dict[str, Any]) -> bool:
        request_payload = self._build_policy_input(tool_name, action, args, metadata)
        self._log("policy_request", request_payload)

        response = self.opa_client.evaluate(request_payload, str(self.policy_path))
        if isinstance(response, dict):
            allow = bool(response.get("result", False))
        else:
            allow = bool(response)

        self._log("policy_decision", {"allow": allow, "opa_response": response})
        return allow

    def execute_tool(self, tool_name: str, args: List[str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        if self.sandbox_manager is None:
            raise RuntimeError("Sandbox manager is required to execute tool calls.")

        sanitized_tool = self.validator.validate_tool_name(tool_name)
        sanitized_args = self.validator.validate_args(args)
        policy_allowed = self.evaluate_policy(sanitized_tool, "execute", sanitized_args, metadata)
        if not policy_allowed:
            return {"allowed": False, "reason": "Policy denied execution."}

        exit_code, stdout, stderr = self.sandbox_manager.run(sanitized_tool, sanitized_args, metadata)
        filtered_stdout = self._mask_sensitive_output(stdout)
        filtered_stderr = self._mask_sensitive_output(stderr)

        result = {
            "allowed": True,
            "exit_code": exit_code,
            "stdout": filtered_stdout,
            "stderr": filtered_stderr,
        }
        self._log("tool_result", result)
        return result
