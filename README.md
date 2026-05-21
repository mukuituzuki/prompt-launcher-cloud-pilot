# Prompt Launcher Fast MVP

Prompt Launcher Fast MVP is a small local Python and Tkinter desktop app.
It lets a human operator select a project, workflow, and situation, preview a recommended prompt, copy it to the clipboard, and manually paste it into Codex, GPT, or notes.

```text
Human decides. Prompt Launcher suggests. Clipboard copies. Human pastes.
```

## What The App Is

- A local prompt selection helper.
- A copy-only launcher for practical Codex/GPT workflow prompts.
- A simple JSON-backed Skill library stored in `prompts.json`.
- A human trial tool for finding useful, missing, or confusing Skills.

## What The App Does Not Do

- It does not paste into Codex, GPT, Chrome, or any browser.
- It does not send messages, post content, browse websites, call APIs, or run remote actions.
- It does not commit, backup, delete files, edit credentials, or manage environment variables.
- It does not replace human review.

## Launch With BAT

From this folder:

```bat
start_prompt_launcher.bat
```

## Launch With PowerShell

From this folder:

```powershell
.\start_prompt_launcher.ps1
```

## Launch Directly With Python

From this folder:

```powershell
python prompt_launcher.py
```

## Basic Usage Flow

1. Select a `Project`.
2. Select a `Workflow`.
3. Select a `Situation`.
4. Read the Skill name, target, description, safety notes, and checklist.
5. Confirm the Prompt preview is the exact text you want to copy and paste.
6. Click `Copy prompt`.
7. Paste manually into the correct Codex/GPT thread or into human notes.
8. If unsure, paste into Notepad first.

## Prompt Preview And Copy Behavior

Prompt preview is the exact text copied by `Copy prompt`.

The preview contains a compact Prompt Launcher Guard followed by the actual prompt body. It does not include the selected Situation, Description, Safety notes, or Post-copy checklist.

Safety notes and Post-copy checklist remain visible in the UI for human review only. They are not copied into the prompt.

The guard reduces wrong-thread mistakes by naming the intended Project, Target, and Skill, but it does not replace human confirmation. The human operator must still confirm the target thread before pasting.

## Add A Skill

Open `prompts.json` and add one object to the top-level list:

```json
{
  "id": "unique_skill_id",
  "name": "Readable Skill name",
  "project": "Project name",
  "workflow": "Workflow name",
  "target": "Codex",
  "situation": "When to use this prompt",
  "description": "Short explanation for the operator.",
  "prompt": "The prompt text to copy.",
  "human_approval_required": true,
  "safety_notes": [
    "Keep this copy-only."
  ],
  "post_copy_checklist": [
    "Confirm the target before pasting."
  ]
}
```

Use `Codex`, `GPT`, or `Human` for `target`.

## Add A New Project

Add a Skill whose `project` value is the new project name. The app builds the Project selector from the values in `prompts.json`, so no code change is needed.

For a useful first project entry, add at least:

- one Codex-facing Step continuation Skill
- one GPT-facing review Skill
- one Human checklist or notes Skill

## Test JSON And Python

Run these from the app folder:

```powershell
python -m json.tool .\prompts.json
python -m py_compile .\prompt_launcher.py
```

If `python` is unavailable, try:

```powershell
py -m json.tool .\prompts.json
py -m py_compile .\prompt_launcher.py
```

## Human Trial Checklist

Use [docs/human_trial_checklist.md](docs/human_trial_checklist.md) for a short trial pass.

Minimum trial:

- Launch the app.
- Select one Skill from each project.
- Copy one prompt.
- Paste it into Notepad first.
- Confirm the Prompt Launcher Guard and target are correct.
- Record confusing labels or missing Skills in [docs/trial_notes_template.md](docs/trial_notes_template.md).

## Safety Boundaries

Clipboard copy is the maximum automation in this MVP.

Do not add:

- automatic paste
- automatic send/post
- Browser automation or Chrome control
- external API calls
- deletion or cleanup automation
- credential or environment variable handling
- automatic commit
- automatic backup

## Known Limitations

- No search box.
- No JSON schema validator beyond normal JSON parsing.
- No in-app Skill editor.
- No per-Skill tags or favorites.
- No automated GUI test suite.
- Prompt quality depends on manual review of `prompts.json`.

## Commit / Backup Reminder

Codex must not commit or backup automatically.

Before commit, the human operator should review the changed files, run validation, launch the app, copy one prompt into Notepad, and confirm the prompt remains copy-only. Backup only after a human-approved commit if the tool is useful.

## Web Preview (Vercel)

A minimal read-only Web preview is available under `web/`.

- It loads `prompts.json` as-is (no schema changes).
- It shows Project / Workflow / Situation selection, Skill details, and Prompt preview.
- It supports copy-only behavior for the displayed prompt.
- It does not edit data or call external APIs.

For local static preview, serve the repository root so `/prompts.json` is available, then open `/`.
