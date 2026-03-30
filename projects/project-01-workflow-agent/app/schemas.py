"""Schema definitions for the Document Analysis Agent."""

from pydantic import BaseModel, ConfigDict


class DocumentAnalysis(BaseModel):
    """Validated output for a single document analysis run."""

    model_config = ConfigDict(extra="forbid")

    summary: str
    key_points: list[str]
    action_items: list[str]
    open_questions: list[str]
    completeness_note: str

