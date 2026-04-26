import unittest

from proxy.validator import ToolRequestValidator


class ToolRequestValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = ToolRequestValidator()

    def test_validate_tool_name_allows_known_tool(self) -> None:
        self.assertEqual(self.validator.validate_tool_name("echo"), "echo")

    def test_validate_tool_name_rejects_unknown_tool(self) -> None:
        with self.assertRaises(ValueError):
            self.validator.validate_tool_name("rm -rf")

    def test_validate_args_rejects_forbidden_path_segment(self) -> None:
        with self.assertRaises(ValueError):
            self.validator.validate_args(["../secret.txt"])

    def test_validate_args_accepts_safe_arguments(self) -> None:
        safe_args = ["/workspace/data.txt", "--output"]
        self.assertEqual(self.validator.validate_args(safe_args), safe_args)


if __name__ == "__main__":
    unittest.main()
