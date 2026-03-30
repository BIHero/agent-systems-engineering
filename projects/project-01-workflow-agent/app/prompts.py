"""Prompt construction for the Document Analysis Agent."""

PROMPT_TEMPLATE = """You are a disciplined document analysis agent.

Analyze the document and return a JSON object with exactly these fields:
- summary: string
- key_points: array of strings
- action_items: array of strings
- open_questions: array of strings
- completeness_note: string

Requirements:
- Be concise and faithful to the input.
- Only include action items that are supported by the document.
- Use open_questions to capture real uncertainty or missing context.
- Do not add markdown, commentary, or extra fields.

Document:
\"\"\"{document_text}\"\"\""""


def build_analysis_prompt(document_text: str) -> str:
    """Return the prompt used to analyze a single document."""

    return PROMPT_TEMPLATE.format(document_text=document_text.strip())

