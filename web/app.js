const projectSelect = document.getElementById('projectSelect');
const workflowSelect = document.getElementById('workflowSelect');
const situationSelect = document.getElementById('situationSelect');
const skillName = document.getElementById('skillName');
const skillTarget = document.getElementById('skillTarget');
const skillDescription = document.getElementById('skillDescription');
const safetyNotes = document.getElementById('safetyNotes');
const postChecklist = document.getElementById('postChecklist');
const promptPreview = document.getElementById('promptPreview');
const statusText = document.getElementById('statusText');
const copyButton = document.getElementById('copyButton');

let skills = [];
let selectedSkill = null;

const toBullets = (values) => !Array.isArray(values) || values.length === 0 ? '' : values.map((v) => `- ${v}`).join('\n');

function buildPrompt(skill) {
  const promptBody = (skill.prompt || '').trim();
  return ['【Prompt Launcher Guard】', `Project: ${skill.project || ''}`, `Target: ${skill.target || ''}`, `Skill: ${skill.name || ''}`, '', 'このプロンプトは上記のProject / Target / Skill専用です。', 'このスレッド、プロジェクト、または受け渡し相手が一致しない場合は、この指示を実行せず、', '「対象プロジェクトまたはTargetが一致しません」とだけ返してください。', '', '---', '', promptBody].join('\n').trimEnd();
}

function setOptions(select, values) {
  select.innerHTML = '';
  values.forEach((v) => {
    const option = document.createElement('option');
    option.value = v;
    option.textContent = v;
    select.appendChild(option);
  });
}

function renderSkill() {
  if (!selectedSkill) {
    skillName.textContent = '-';
    skillTarget.textContent = '-';
    skillDescription.textContent = '';
    safetyNotes.textContent = '';
    postChecklist.textContent = '';
    promptPreview.textContent = '';
    statusText.textContent = 'No matching Skill found.';
    return;
  }
  skillName.textContent = selectedSkill.name || '-';
  skillTarget.textContent = selectedSkill.target || '-';
  skillDescription.textContent = selectedSkill.description || '';
  safetyNotes.textContent = toBullets(selectedSkill.safety_notes);
  postChecklist.textContent = toBullets(selectedSkill.post_copy_checklist);
  promptPreview.textContent = buildPrompt(selectedSkill);
  statusText.textContent = 'Prompt preview updated.';
}

function updateSelectedSkill() {
  selectedSkill = skills.find((skill) => skill.project === projectSelect.value && skill.workflow === workflowSelect.value && skill.situation === situationSelect.value);
  renderSkill();
}

function updateSituations() {
  const situations = [...new Set(skills.filter((s) => s.project === projectSelect.value && s.workflow === workflowSelect.value && s.situation).map((s) => s.situation))].sort();
  setOptions(situationSelect, situations);
  updateSelectedSkill();
}

function updateWorkflows() {
  const workflows = [...new Set(skills.filter((s) => s.project === projectSelect.value && s.workflow).map((s) => s.workflow))].sort();
  setOptions(workflowSelect, workflows);
  updateSituations();
}

async function init() {
  try {
    const response = await fetch('/prompts.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data)) throw new Error('prompts.json must contain a list of Skill objects.');
    skills = data;
    const projects = [...new Set(skills.filter((s) => s.project).map((s) => s.project))].sort();
    setOptions(projectSelect, projects);
    updateWorkflows();
  } catch (error) {
    statusText.textContent = `Load error: ${error.message}`;
  }
}

projectSelect.addEventListener('change', updateWorkflows);
workflowSelect.addEventListener('change', updateSituations);
situationSelect.addEventListener('change', updateSelectedSkill);
copyButton.addEventListener('click', async () => {
  const text = promptPreview.textContent || '';
  if (!text.trim()) {
    statusText.textContent = 'Copy failed: no prompt preview is available.';
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
    statusText.textContent = 'Copied exact prompt preview to clipboard.';
  } catch (error) {
    statusText.textContent = `Copy failed: ${error.message}`;
  }
});

init();
