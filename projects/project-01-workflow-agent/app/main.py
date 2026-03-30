"""Runnable example for the Document Analysis Agent."""

from app.agent import analyze_document
from app.formatter import format_analysis


SAMPLE_DOCUMENT = """
The operations team reviewed the rollout of the internal reporting tool.
The pilot reduced manual reporting time by roughly 30 percent, but several
team leads said the onboarding instructions were incomplete. Two teams still
submit reports through email because they are unsure how exceptions should be
handled. The product manager asked for a short training guide and a clearer
escalation path before the wider launch next month.
""".strip()


def demo_llm_call(_: str) -> dict[str, object]:
    """Temporary stand-in for a real LLM provider integration."""

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


def main() -> None:
    """Run the sample analysis flow and print a formatted result."""

    result = analyze_document(SAMPLE_DOCUMENT, llm_call=demo_llm_call)
    print(format_analysis(result))


if __name__ == "__main__":
    main()

