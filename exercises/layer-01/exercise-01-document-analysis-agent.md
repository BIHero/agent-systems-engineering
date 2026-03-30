# Exercise 01: Build a Document Analysis Agent

## Objective

Build a single-agent system that accepts raw text and returns a structured analysis.

## Requirements

- Input must be plain text
- Output must follow a strict schema
- The schema must include:
  - summary
  - key_points
  - action_items
  - open_questions
  - completeness_note

## Constraints

- No retrieval
- No memory
- No multi-agent design
- No external web access
- Must validate output before returning it

## Evaluation Criteria

- Output is valid and structured
- Summary is concise and accurate
- Action items are concrete
- Open questions reflect actual uncertainty in the input
- System handles weak or incomplete input gracefully

