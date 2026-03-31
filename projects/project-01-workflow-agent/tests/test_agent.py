"""Tests for the Document Analysis Agent."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.agent import EmptyInputError, OutputValidationError, analyze_document
from app.formatter import format_analysis
from app.schemas import DocumentAnalysis


def fake_llm_call(_: str) -> dict[str, object]:
    """Return a stable payload for tests."""
    return {
        "summary": "A short and accurate summary.",
        "key_points": ["Point one", "Point two"],
        "action_items": ["Do the next thing"],
        "open_questions": ["What is still missing?"],
        "completeness_note": "The input has enough detail for a basic analysis.",
    }


def invalid_missing_field_llm(_: str) -> dict[str, object]:
    """Return a payload missing required fields."""
    return {
        "summary": "Only summary",
    }

def wrapped_json_llm(_: str) -> str:
    """Return valid JSON wrapped in extra commentary."""
    return (
        'Here is the analysis:\n\n'
        '{"summary":"Summary",'
        '"key_points":["Point one"],'
        '"action_items":["Do the thing"],'
        '"open_questions":["What is missing?"],'
        '"completeness_note":"Good enough."}'
    )


def invalid_wrong_type_llm(_: str) -> dict[str, object]:
    """Return a payload with an invalid field type."""
    return {
        "summary": "Summary",
        "key_points": "not a list",
        "action_items": [],
        "open_questions": [],
        "completeness_note": "note",
    }


def invalid_extra_field_llm(_: str) -> dict[str, object]:
    """Return a payload with a forbidden extra field."""
    return {
        "summary": "Summary",
        "key_points": [],
        "action_items": [],
        "open_questions": [],
        "completeness_note": "note",
        "extra_field": "should fail",
    }


def json_string_llm(_: str) -> str:
    """Return a valid JSON string payload."""
    return '{"summary":"Summary","key_points":[],"action_items":[],"open_questions":[],"completeness_note":"note"}'


def malformed_json_llm(_: str) -> str:
    return '{"summary": "oops",'

class DocumentAnalysisAgentTests(unittest.TestCase):
    """Basic behavior checks for the project scaffold."""

    def test_empty_input_handling(self) -> None:
        with self.assertRaises(EmptyInputError):
            analyze_document("   ", llm_call=fake_llm_call)

    def test_valid_schema_structure(self) -> None:
        result = analyze_document("Useful document text.", llm_call=fake_llm_call)

        self.assertIsInstance(result, DocumentAnalysis)
        self.assertEqual(result.summary, "A short and accurate summary.")
        self.assertEqual(len(result.key_points), 2)
        self.assertEqual(result.action_items[0], "Do the next thing")

    def test_formatter_output_not_failing(self) -> None:
        result = analyze_document("Useful document text.", llm_call=fake_llm_call)
        formatted = format_analysis(result)

        self.assertIn("Document Analysis", formatted)
        self.assertIn("Summary", formatted)
        self.assertIn("A short and accurate summary.", formatted)

    def test_missing_required_field_raises_validation_error(self) -> None:
        with self.assertRaises(OutputValidationError):
            analyze_document("Useful document text.", llm_call=invalid_missing_field_llm)

    def test_wrong_field_type_raises_validation_error(self) -> None:
        with self.assertRaises(OutputValidationError):
            analyze_document("Useful document text.", llm_call=invalid_wrong_type_llm)

    def test_extra_field_raises_validation_error(self) -> None:
        with self.assertRaises(OutputValidationError):
            analyze_document("Useful document text.", llm_call=invalid_extra_field_llm)

    def test_json_string_response_is_accepted(self) -> None:
        result = analyze_document("Useful document text.", llm_call=json_string_llm)

        self.assertIsInstance(result, DocumentAnalysis)
        self.assertEqual(result.summary, "Summary")
        self.assertEqual(result.key_points, [])
        self.assertEqual(result.action_items, [])
        self.assertEqual(result.open_questions, [])
        self.assertEqual(result.completeness_note, "note")

    def test_malformed_json_raises_validation_error(self) -> None:
        with self.assertRaises(OutputValidationError):
            analyze_document("Useful document text.", llm_call=malformed_json_llm)

    def test_wrapped_json_response_is_accepted(self) -> None:
        result = analyze_document("Useful document text.", llm_call=wrapped_json_llm)

        self.assertIsInstance(result, DocumentAnalysis)
        self.assertEqual(result.summary, "Summary")
        self.assertEqual(result.key_points, ["Point one"])
        self.assertEqual(result.action_items, ["Do the thing"])
        self.assertEqual(result.open_questions, ["What is missing?"])
        self.assertEqual(result.completeness_note, "Good enough.")

if __name__ == "__main__":
    unittest.main()