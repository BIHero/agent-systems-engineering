# Prompt Experiments

## Prompt Version

Version 0.1

## Observed Behavior

- The prompt is concise and easy to inspect.
- The schema is explicit, which helps constrain the output shape.
- The prompt should work well for short operational or business documents.

## Failure Cases

- Weak source documents may lead to vague action items.
- Models may still add extra keys unless the output layer is validated.
- Incomplete inputs can produce speculative open questions if the prompt is too loose.

## Next Prompt Adjustment

- Tighten wording around evidence-based action items.
- Add a reminder to avoid speculation when the source text is sparse.
- Evaluate whether the summary should be limited to one or two sentences.

