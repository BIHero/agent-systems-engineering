"""Human-readable formatting helpers for document analysis results."""

from .schemas import DocumentAnalysis


def format_analysis(result: DocumentAnalysis) -> str:
    """Render a DocumentAnalysis object as readable plain text."""

    sections = [
        "Document Analysis",
        "=================",
        "",
        "Summary",
        "-------",
        result.summary,
        "",
        "Key Points",
        "----------",
        _format_list(result.key_points),
        "",
        "Action Items",
        "------------",
        _format_list(result.action_items),
        "",
        "Open Questions",
        "--------------",
        _format_list(result.open_questions),
        "",
        "Completeness Note",
        "-----------------",
        result.completeness_note,
    ]
    return "\n".join(sections)


def _format_list(items: list[str]) -> str:
    """Format a list of strings as bullet points."""

    if not items:
        return "- None."

    return "\n".join(f"- {item}" for item in items)

