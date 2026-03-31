"""Core workflow for the Document Analysis Agent."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from pydantic import ValidationError

from .prompts import build_analysis_prompt
from .schemas import DocumentAnalysis

import re


import json
import re
from typing import Any
from collections.abc import Callable, Mapping

from pydantic import ValidationError

from .prompts import build_analysis_prompt
from .schemas import DocumentAnalysis


def _extract_json_from_text(text: str) -> dict:
    """Extract the first JSON object from a string."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    array_match = re.search(r"\[.*\]", text, re.DOTALL)
    if array_match:
        raise TypeError("Received JSON array but expected object.")

    raise json.JSONDecodeError("No JSON object found", text, 0)

LLMCallable = Callable[[str], Any]


class DocumentAnalysisError(Exception):
    """Base error for document analysis workflow failures."""


class EmptyInputError(DocumentAnalysisError):
    """Raised when the provided document text is empty."""


class OutputValidationError(DocumentAnalysisError):
    """Raised when the model output does not match the schema."""


def analyze_document(raw_text: str, llm_call: LLMCallable) -> DocumentAnalysis:
    """Analyze a document and return a validated structured result."""

    document_text = raw_text.strip()
    if not document_text:
        raise EmptyInputError("Document text must not be empty.")

    prompt = build_analysis_prompt(document_text)

    try:
        raw_response = llm_call(prompt)
    except Exception as exc:  # pragma: no cover - defensive boundary
        raise DocumentAnalysisError("LLM invocation failed.") from exc

    try:
        return _parse_document_analysis(raw_response)
    except (TypeError, json.JSONDecodeError, ValidationError) as exc:
        raise OutputValidationError(
            "LLM output could not be validated as DocumentAnalysis."
        ) from exc


def _parse_document_analysis(raw_response: Any) -> DocumentAnalysis:
    """Convert raw model output into a validated DocumentAnalysis object."""

    if isinstance(raw_response, DocumentAnalysis):
        return raw_response

    if isinstance(raw_response, str):
        try:
            payload = json.loads(raw_response)
        except json.JSONDecodeError:
            payload = _extract_json_from_text(raw_response)
    elif isinstance(raw_response, Mapping):
        payload = dict(raw_response)
    else:
        raise TypeError("Unsupported response type returned by LLM layer.")

    return DocumentAnalysis(**payload)

