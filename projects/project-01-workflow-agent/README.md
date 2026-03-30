# Document Analysis Agent

## Purpose

The Document Analysis Agent is the first Layer 1 project in this repository. It introduces agent systems engineering through a controlled single-agent workflow that accepts plain text, analyzes it, and returns a validated structured result.

## Why This Is A Good First Single-Agent System

This use case is simple enough to reason about and disciplined enough to teach core system design habits. The input is clear, the task is narrow, the output schema is explicit, and the failure modes are easy to inspect.

## Architecture Overview

The system uses a single agent with a controlled, deterministic workflow.
The agent is responsible for orchestrating prompt construction, model invocation,
and schema validation:

1. Accept raw text input.
2. Validate that the input is not empty.
3. Build a concise analysis prompt.
4. Send the prompt through an LLM interface.
5. Validate the returned payload against a strict schema.
6. Format the result for human review.

The LLM is accessed through an injected callable interface, allowing the system
to remain independent of any specific provider.

This design emphasizes input validation, structured outputs, and explicit failure handling,
which are essential for production-grade AI systems.

## File Structure

```text
project-01-workflow-agent/
├── .gitignore
├── README.md
├── app/
│   ├── agent.py
│   ├── formatter.py
│   ├── main.py
│   ├── prompts.py
│   └── schemas.py
├── notebooks/
│   └── prompt_experiments.md
├── pyproject.toml
└── tests/
    └── test_agent.py
```

Each component has a clear responsibility:
- `agent.py` handles workflow and control
- `schemas.py` defines the output contract
- `prompts.py` defines model behavior
- `formatter.py` handles presentation
- `tests/` ensures system reliability

## Development

Use `uv` for dependency management and local execution:

- `uv sync`
- `uv run python -m app.main`
- `uv run python -m unittest discover -s tests -v`

Tests focus on system behavior rather than model intelligence, ensuring that
validation, error handling, and formatting remain reliable regardless of the
underlying model provider.

## Current Limitations

- The LLM call is still a placeholder interface.
- The runnable example uses a local demo response instead of a real model provider.
- The system handles one document at a time and does not persist results.
- There is no retrieval, memory, or external context enrichment by design.

## Next Steps

- Replace the placeholder LLM interface with a real provider adapter.
- Add schema-aware retry behavior for malformed model outputs.
- Add a CLI or API wrapper around the agent entry point.
- Build a small evaluation set for summaries, action items, and graceful failure handling.
