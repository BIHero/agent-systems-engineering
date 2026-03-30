"""Runnable example for the Document Analysis Agent."""

from app.agent import analyze_document
from app.formatter import format_analysis
from app.llm import call_openai_provider


SAMPLE_DOCUMENT = """
The operations team reviewed the rollout of the internal reporting tool.
The pilot reduced manual reporting time by roughly 30 percent, but several
team leads said the onboarding instructions were incomplete. Two teams still
submit reports through email because they are unsure how exceptions should be
handled. The product manager asked for a short training guide and a clearer
escalation path before the wider launch next month.
""".strip()


def main() -> None:
    """Run the sample analysis flow and print a formatted result."""

    result = analyze_document(SAMPLE_DOCUMENT, llm_call=call_openai_provider)
    print(format_analysis(result))


if __name__ == "__main__":
    main()

