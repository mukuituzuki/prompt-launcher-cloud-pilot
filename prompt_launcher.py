import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


APP_DIR = Path(__file__).resolve().parent
PROMPTS_PATH = APP_DIR / "prompts.json"


class PromptLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prompt Launcher Fast MVP")
        self.geometry("920x700")
        self.minsize(760, 560)

        self.skills = self.load_skills()
        self.selected_skill = None

        self.project_var = tk.StringVar()
        self.workflow_var = tk.StringVar()
        self.situation_var = tk.StringVar()
        self.skill_name_var = tk.StringVar(value="-")
        self.target_var = tk.StringVar(value="-")
        self.status_var = tk.StringVar(value="Select a project, workflow, and situation.")

        self.build_ui()
        self.populate_projects()

    def load_skills(self):
        try:
            with PROMPTS_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Load error", f"Missing prompts file:\n{PROMPTS_PATH}")
            return []
        except json.JSONDecodeError as exc:
            messagebox.showerror("Load error", f"Invalid JSON in prompts.json:\n{exc}")
            return []

        if not isinstance(data, list):
            messagebox.showerror("Load error", "prompts.json must contain a list of Skill objects.")
            return []
        return data

    def build_ui(self):
        root = ttk.Frame(self, padding=12)
        root.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        selectors = ttk.LabelFrame(root, text="Selection", padding=10)
        selectors.grid(row=0, column=0, columnspan=2, sticky="ew")
        selectors.columnconfigure(1, weight=1)
        selectors.columnconfigure(3, weight=1)
        selectors.columnconfigure(5, weight=2)

        ttk.Label(selectors, text="Project").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.project_combo = ttk.Combobox(selectors, textvariable=self.project_var, state="readonly")
        self.project_combo.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        self.project_combo.bind("<<ComboboxSelected>>", self.on_project_selected)

        ttk.Label(selectors, text="Workflow").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.workflow_combo = ttk.Combobox(selectors, textvariable=self.workflow_var, state="readonly")
        self.workflow_combo.grid(row=0, column=3, sticky="ew", padx=(0, 12))
        self.workflow_combo.bind("<<ComboboxSelected>>", self.on_workflow_selected)

        ttk.Label(selectors, text="Situation").grid(row=0, column=4, sticky="w", padx=(0, 6))
        self.situation_combo = ttk.Combobox(selectors, textvariable=self.situation_var, state="readonly")
        self.situation_combo.grid(row=0, column=5, sticky="ew")
        self.situation_combo.bind("<<ComboboxSelected>>", self.on_situation_selected)

        details = ttk.LabelFrame(root, text="Skill details", padding=10)
        details.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(0, 6))
        details.columnconfigure(1, weight=1)

        ttk.Label(details, text="Skill").grid(row=0, column=0, sticky="nw", padx=(0, 8), pady=(0, 6))
        ttk.Label(details, textvariable=self.skill_name_var, wraplength=390).grid(
            row=0, column=1, sticky="ew", pady=(0, 6)
        )

        ttk.Label(details, text="Target").grid(row=1, column=0, sticky="nw", padx=(0, 8), pady=(0, 6))
        ttk.Label(details, textvariable=self.target_var).grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ttk.Label(details, text="Description").grid(row=2, column=0, sticky="nw", padx=(0, 8))
        self.description_text = self.create_readonly_text(details, height=5)
        self.description_text.grid(row=2, column=1, sticky="nsew")

        lists = ttk.LabelFrame(root, text="Safety and checklist", padding=10)
        lists.grid(row=1, column=1, sticky="nsew", pady=(10, 10), padx=(6, 0))
        lists.columnconfigure(0, weight=1)
        lists.rowconfigure(1, weight=1)
        lists.rowconfigure(3, weight=1)

        ttk.Label(lists, text="Safety notes").grid(row=0, column=0, sticky="w")
        self.safety_text = self.create_readonly_text(lists, height=4)
        self.safety_text.grid(row=1, column=0, sticky="nsew", pady=(2, 8))

        ttk.Label(lists, text="Post-copy checklist").grid(row=2, column=0, sticky="w")
        self.checklist_text = self.create_readonly_text(lists, height=4)
        self.checklist_text.grid(row=3, column=0, sticky="nsew", pady=(2, 0))

        preview_frame = ttk.LabelFrame(root, text="Prompt preview", padding=10)
        preview_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        self.preview_text = tk.Text(preview_frame, wrap="word", undo=False)
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        preview_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        preview_scroll.grid(row=0, column=1, sticky="ns")
        self.preview_text.configure(yscrollcommand=preview_scroll.set)

        actions = ttk.Frame(root)
        actions.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        actions.columnconfigure(0, weight=1)

        ttk.Label(actions, textvariable=self.status_var).grid(row=0, column=0, sticky="w")
        ttk.Button(actions, text="Copy prompt", command=self.copy_prompt).grid(row=0, column=1, sticky="e")

    def create_readonly_text(self, parent, height):
        widget = tk.Text(parent, height=height, wrap="word", undo=False)
        widget.configure(state="disabled", relief="solid", borderwidth=1)
        return widget

    def populate_projects(self):
        projects = sorted({skill.get("project", "") for skill in self.skills if skill.get("project")})
        self.project_combo.configure(values=projects)
        if projects:
            self.project_var.set(projects[0])
            self.update_workflows()

    def on_project_selected(self, _event=None):
        self.update_workflows()

    def on_workflow_selected(self, _event=None):
        self.update_situations()

    def on_situation_selected(self, _event=None):
        self.update_selected_skill()

    def update_workflows(self):
        project = self.project_var.get()
        workflows = sorted(
            {
                skill.get("workflow", "")
                for skill in self.skills
                if skill.get("project") == project and skill.get("workflow")
            }
        )
        self.workflow_combo.configure(values=workflows)
        self.workflow_var.set(workflows[0] if workflows else "")
        self.update_situations()

    def update_situations(self):
        project = self.project_var.get()
        workflow = self.workflow_var.get()
        situations = sorted(
            {
                skill.get("situation", "")
                for skill in self.skills
                if skill.get("project") == project
                and skill.get("workflow") == workflow
                and skill.get("situation")
            }
        )
        self.situation_combo.configure(values=situations)
        self.situation_var.set(situations[0] if situations else "")
        self.update_selected_skill()

    def update_selected_skill(self):
        project = self.project_var.get()
        workflow = self.workflow_var.get()
        situation = self.situation_var.get()
        self.selected_skill = next(
            (
                skill
                for skill in self.skills
                if skill.get("project") == project
                and skill.get("workflow") == workflow
                and skill.get("situation") == situation
            ),
            None,
        )
        self.render_skill()

    def render_skill(self):
        if not self.selected_skill:
            self.skill_name_var.set("-")
            self.target_var.set("-")
            self.set_text(self.description_text, "")
            self.set_text(self.safety_text, "")
            self.set_text(self.checklist_text, "")
            self.set_text(self.preview_text, "")
            self.status_var.set("No matching Skill found.")
            return

        skill = self.selected_skill
        self.skill_name_var.set(skill.get("name", "-"))
        self.target_var.set(skill.get("target", "-"))
        self.set_text(self.description_text, skill.get("description", ""))
        self.set_text(self.safety_text, self.format_bullets(skill.get("safety_notes", [])))
        self.set_text(self.checklist_text, self.format_bullets(skill.get("post_copy_checklist", [])))
        self.set_text(self.preview_text, self.build_prompt(skill))
        self.status_var.set("Prompt preview updated.")

    def set_text(self, widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        if widget is not self.preview_text:
            widget.configure(state="disabled")

    def format_bullets(self, values):
        if not values:
            return ""
        return "\n".join(f"- {value}" for value in values)

    def build_prompt(self, skill):
        prompt_body = skill.get("prompt", "").strip()
        lines = [
            "【Prompt Launcher Guard】",
            f"Project: {skill.get('project', '')}",
            f"Target: {skill.get('target', '')}",
            f"Skill: {skill.get('name', '')}",
            "",
            "このプロンプトは上記のProject / Target / Skill専用です。",
            "このスレッド、プロジェクト、または受け渡し相手が一致しない場合は、この指示を実行せず、",
            "「対象プロジェクトまたはTargetが一致しません」とだけ返してください。",
            "",
            "---",
            "",
            prompt_body,
        ]
        return "\n".join(lines).rstrip()

    def copy_prompt(self):
        preview = self.preview_text.get("1.0", "end-1c")
        if not preview.strip():
            self.status_var.set("Copy failed: no prompt preview is available.")
            return

        try:
            self.clipboard_clear()
            self.clipboard_append(preview)
            self.update()
        except tk.TclError as exc:
            self.status_var.set(f"Copy failed: {exc}")
            return

        self.status_var.set("Copied exact prompt preview to clipboard.")


if __name__ == "__main__":
    app = PromptLauncher()
    app.mainloop()
