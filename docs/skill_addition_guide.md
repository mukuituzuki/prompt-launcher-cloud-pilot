# Skill Addition Guide

Add Skills by editing the top-level list in `prompts.json`.

Minimal example:

```json
{
  "id": "example_codex_continue",
  "name": "Example Codex Continue",
  "project": "Example Project",
  "workflow": "Codex Step運用",
  "target": "Codex",
  "situation": "current Stepを継続したい",
  "description": "A short explanation shown in the app.",
  "prompt": "The exact prompt text to copy.",
  "human_approval_required": true,
  "safety_notes": [
    "Do not request automatic send or paste."
  ],
  "post_copy_checklist": [
    "Confirm the target thread before pasting."
  ]
}
```

Field notes:

- `id`: Stable unique identifier. Use lowercase words separated by underscores.
- `name`: Short label shown as the recommended Skill.
- `project`: Project selector value. A new value creates a new project option.
- `workflow`: Workflow selector value within the project.
- `target`: Use `Codex`, `GPT`, or `Human`.
- `situation`: Situation selector value. Make it concrete and action-oriented.
- `description`: Brief human-readable explanation.
- `prompt`: The copied prompt body.
- `human_approval_required`: Keep `true` for this MVP.
- `safety_notes`: Short warnings shown before copy.
- `post_copy_checklist`: What the human should check after copying.

After editing, run:

```powershell
python -m json.tool .\prompts.json
```
