"""LLM adapter layer for provider-specific integrations."""

import os
from openai import OpenAI
from typing import Any


class LLMProviderError(Exception):
    """Raised when a provider call fails or returns unusable output."""


def call_openai_provider(prompt: str) -> str:
    """Call the OpenAI API with a given prompt and return the response as a string."""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMProviderError("OpenAI API key not found in environment variable OPENAI_API_KEY")
    
    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model="gpt-5.4",
            input= prompt,
        )

        if not response.output:
            raise LLMProviderError("OpenAI response is missing 'output' field.")
        
        first_output = response.output[0]
        if not first_output.content:
            raise LLMProviderError("OpenAI response output is missing 'content' field.")
        
        first_content = first_output.content[0]
        text = getattr(first_content, "text", None)
        if not text:
            raise LLMProviderError("OpenAI response content is missing 'text' field.")

        return text
    except Exception as exc:
        raise LLMProviderError(f"OpenAI provider call failed: {exc}") from exc
    

def call_demo_provider(_: str) -> dict[str, object]:
    """Return a deterministic demo response for local development."""

    return {
        "summary": (
            "The reporting tool pilot improved efficiency, but rollout readiness is "
            "limited by incomplete onboarding guidance and unclear exception handling."
        ),
        "key_points": [
            "The pilot reduced manual reporting time by about 30 percent.",
            "Some team leads found the onboarding instructions incomplete.",
            "Two teams still rely on email because exception handling is unclear.",
        ],
        "action_items": [
            "Create a short training guide for new users.",
            "Define and communicate an escalation path for exceptions before launch.",
        ],
        "open_questions": [
            "What exception types should remain outside the standard workflow?",
            "Who owns support during the wider launch next month?",
        ],
        "completeness_note": (
            "The document is sufficient for a first-pass analysis, but it does not "
            "define owners, timelines, or exception categories."
        ),
    }
