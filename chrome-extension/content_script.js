const PANEL_ID = "jlm-panel";
let activeBundle = null;
let detectedTargets = [];

injectPanel();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message).then(sendResponse).catch((error) => sendResponse({ ok: false, error: error.message }));
  return true;
});

async function handleMessage(message) {
  if (message?.type !== "jlm:loadBundle") throw new Error("Unknown page message.");
  const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId: message.profileId });
  if (!response.ok || !response.bundle) throw new Error("No active lorebook bundle loaded.");
  activeBundle = response.bundle;
  setStatus(`Loaded ${activeBundle.files.length} lorebooks from ${activeBundle.source}.`);
  renderSummary();
  return { ok: true };
}

function injectPanel() {
  if (document.getElementById(PANEL_ID)) return;
  const panel = document.createElement("div");
  panel.id = PANEL_ID;
  panel.innerHTML = `
    <header>
      <h2>Janitor Lorebook Manager</h2>
      <button type="button" data-jlm="collapse">_</button>
    </header>
    <div class="jlm-body">
      <div class="jlm-status" data-jlm="status">Open the extension popup and load a bundle.</div>
      <div class="jlm-row">
        <button type="button" data-jlm="detect">Detect Fields</button>
        <button type="button" data-jlm="backup">Backup Page</button>
      </div>
      <div class="jlm-row">
        <button type="button" data-jlm="dryrun">Dry Run</button>
        <button type="button" data-jlm="apply">Apply To Page</button>
      </div>
      <div class="jlm-row">
        <button type="button" data-jlm="copy">Copy First Changed</button>
        <button type="button" data-jlm="download">Download Bundle</button>
      </div>
      <pre data-jlm="output">No scan yet.</pre>
    </div>
  `;
  document.documentElement.appendChild(panel);
  panel.addEventListener("click", onPanelClick);
}

async function onPanelClick(event) {
  const action = event.target?.dataset?.jlm;
  if (!action) return;
  try {
    if (action === "collapse") return toggleCollapse();
    if (action === "detect") return detectAndRender();
    if (action === "backup") return backupPage();
    if (action === "dryrun") return dryRun();
    if (action === "apply") return applyToPage();
    if (action === "copy") return copyFirstChanged();
    if (action === "download") return downloadBundle();
  } catch (error) {
    setStatus(error.message, true);
  }
}

function toggleCollapse() {
  const body = document.querySelector(`#${PANEL_ID} .jlm-body`);
  body.style.display = body.style.display === "none" ? "block" : "none";
}

function detectAndRender() {
  detectedTargets = detectTargets();
  setOutput(formatTargets(detectedTargets));
  setStatus(`Detected ${detectedTargets.length} possible lorebook fields.`);
}

function dryRun() {
  requireBundle();
  detectedTargets = detectTargets();
  const plan = buildApplyPlan(activeBundle, detectedTargets);
  setOutput(formatPlan(plan));
  setStatus(`Dry run: ${plan.matched.length} matched, ${plan.unmatched.length} unmatched.`);
}

async function backupPage() {
  detectedTargets = detectTargets();
  if (!detectedTargets.length) throw new Error("No editable lorebook fields detected.");
  const backup = {
    url: location.href,
    title: document.title,
    fields: detectedTargets.map((target) => ({
      label: target.label,
      value: getTargetValue(target)
    }))
  };
  await chrome.runtime.sendMessage({ type: "backup:store", backup });
  downloadJson(`janitor-lorebook-backup-${Date.now()}.json`, backup);
  setStatus(`Backed up ${backup.fields.length} fields.`);
}

async function applyToPage() {
  requireBundle();
  detectedTargets = detectTargets();
  const plan = buildApplyPlan(activeBundle, detectedTargets);
  const invalid = plan.matched.filter((item) => item.file.validation && !item.file.validation.ok);
  if (invalid.length) throw new Error(`Refusing to apply ${invalid.length} invalid lorebook files.`);
  if (!plan.matched.length) throw new Error("No matching Janitor lorebook fields found.");
  const backup = {
    url: location.href,
    title: document.title,
    fields: detectedTargets.map((target) => ({ label: target.label, value: getTargetValue(target) }))
  };
  await chrome.runtime.sendMessage({ type: "backup:store", backup });
  for (const item of plan.matched) setTargetValue(item.target, item.file.text);
  setOutput(formatPlan(plan) + "\n\nApplied to page fields. Review in Janitor and manually save/publish.");
  setStatus(`Applied ${plan.matched.length} lorebooks. Manual Janitor save still required.`);
}

async function copyFirstChanged() {
  requireBundle();
  const file = activeBundle.files.find((item) => item.text);
  if (!file) throw new Error("No lorebook file available to copy.");
  await navigator.clipboard.writeText(file.text);
  setStatus(`Copied ${file.filename || file.name} to clipboard.`);
}

function downloadBundle() {
  requireBundle();
  downloadJson(`janitor-lorebook-bundle-${Date.now()}.json`, activeBundle);
}

function detectTargets() {
  const codeMirrorEditors = Array.from(document.querySelectorAll(".cm-editor"))
    .map((editor) => editor.querySelector(".cm-content[contenteditable='true']"))
    .filter(Boolean);
  const normalFields = Array.from(document.querySelectorAll("textarea, [contenteditable='true']"))
    .filter((field) => !field.closest(".cm-editor"));
  const fields = [...codeMirrorEditors, ...normalFields];
  return fields
    .filter((field) => isVisible(field) && isLikelyLorebookField(field))
    .map((field, index) => ({
      index,
      element: field,
      label: inferLabel(field, index),
      normalized: normalize(inferLabel(field, index)),
      signature: getLorebookSignature(getElementValue(field)),
      kind: field.closest(".cm-editor") ? "codemirror" : ("value" in field ? "field" : "contenteditable"),
      length: getElementValue(field).length
    }));
}

function isLikelyLorebookField(field) {
  const value = getElementValue(field);
  const label = inferLabel(field, 0).toLowerCase();
  if (value.trim().startsWith("[") && value.includes('"keysRaw"')) return true;
  if (label.includes("lorebook") || label.includes("lore book")) return true;
  if (value.includes('"activationMode"') && value.includes('"keywordsRaw"')) return true;
  return value.length > 1000 && value.includes('"content"') && value.includes('"key"');
}

function buildApplyPlan(bundle, targets) {
  const files = bundle.files || [];
  const matched = [];
  const unmatched = [];
  const claimedTargets = new Set();
  for (const file of files) {
    const fileName = normalize(file.name || file.filename || "");
    const fileStem = normalize(String(file.filename || "").replace(/\.json$/i, ""));
    const fileWords = significantFileWords(file);
    let target = targets.find((candidate) => !claimedTargets.has(candidate) && (candidate.normalized === fileName || candidate.normalized === fileStem));
    if (!target) {
      target = targets.find((candidate) => !claimedTargets.has(candidate) && (
        candidate.normalized.includes(fileName) ||
        candidate.normalized.includes(fileStem) ||
        fileName.includes(candidate.normalized) ||
        fileWords.every((word) => candidate.signature.includes(word))
      ));
    }
    if (!target && targets.length === 1 && files.length === 1) {
      target = targets[0];
    }
    if (target) {
      claimedTargets.add(target);
      matched.push({ file, target });
    }
    else unmatched.push(file);
  }
  const unusedTargets = targets.filter((target) => !matched.some((item) => item.target === target));
  return { matched, unmatched, unusedTargets };
}

function formatPlan(plan) {
  const lines = [
    `Matched: ${plan.matched.length}`,
    `Unmatched files: ${plan.unmatched.length}`,
    `Unused page fields: ${plan.unusedTargets.length}`,
    "",
    "Matched:"
  ];
  for (const item of plan.matched) {
    const validation = item.file.validation?.ok === false ? " INVALID" : "";
    lines.push(`- ${item.file.filename || item.file.name} -> ${item.target.label}${validation}`);
  }
  if (plan.unmatched.length) {
    lines.push("", "Unmatched files:");
    for (const file of plan.unmatched) lines.push(`- ${file.filename || file.name}`);
  }
  return lines.join("\n");
}

function formatTargets(targets) {
  if (!targets.length) return "No likely lorebook fields found. Open the Janitor character/lorebook editor, then try again.";
  return targets.map((target) => `- ${target.label} [${target.kind}] (${target.length} chars)\n  signature: ${target.signature || "none"}`).join("\n");
}

function renderSummary() {
  if (!activeBundle) return;
  const lines = [
    `${activeBundle.project || "Project"} ${activeBundle.version || ""}`,
    `Source: ${activeBundle.source}`,
    `Files: ${activeBundle.files.length}`,
    "",
    ...activeBundle.files.map((file) => `- ${file.filename || file.name}: ${file.entries || 0} entries, ${Math.round((file.bytes || 0) / 1024)} KB`)
  ];
  setOutput(lines.join("\n"));
}

function inferLabel(field, index) {
  const aria = field.getAttribute("aria-label") || field.getAttribute("aria-placeholder") || field.getAttribute("placeholder") || field.getAttribute("name");
  if (aria) return aria.trim();
  const id = field.id;
  if (id) {
    const label = document.querySelector(`label[for="${CSS.escape(id)}"]`);
    if (label?.textContent?.trim()) return label.textContent.trim();
  }
  const container = field.closest("section, form, div");
  const heading = container?.querySelector("h1,h2,h3,h4,label,[role='heading']");
  if (heading?.textContent?.trim()) return heading.textContent.trim();
  return `Editable field ${index + 1}`;
}

function getTargetValue(target) {
  return getElementValue(target.element);
}

function getElementValue(element) {
  const view = getCodeMirrorView(element);
  if (view?.state?.doc) return view.state.doc.toString();
  if ("value" in element) return element.value || "";
  return element.textContent || "";
}

function setTargetValue(target, value) {
  const element = target.element;
  const view = getCodeMirrorView(element);
  if (view?.state?.doc && typeof view.dispatch === "function") {
    view.focus();
    view.dispatch({
      changes: { from: 0, to: view.state.doc.length, insert: value },
      selection: { anchor: value.length }
    });
    element.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: value.slice(0, 1000) }));
    return;
  }
  if ("value" in element) {
    element.focus();
    element.value = value;
    element.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: value }));
    element.dispatchEvent(new Event("change", { bubbles: true }));
  } else {
    element.focus();
    if (!replaceContentEditableText(element, value)) {
      element.textContent = value;
      element.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: value.slice(0, 1000) }));
    }
  }
}

function getCodeMirrorView(element) {
  const editor = element.closest?.(".cm-editor") || element;
  const content = editor.querySelector?.(".cm-content") || element;
  const candidates = [content?.cmView, editor?.cmView, element?.cmView].filter(Boolean);
  for (const candidate of candidates) {
    const view = findViewFromCmNode(candidate);
    if (view) return view;
  }
  return null;
}

function findViewFromCmNode(node) {
  let current = node;
  for (let depth = 0; current && depth < 20; depth += 1) {
    if (current.view?.state?.doc && typeof current.view.dispatch === "function") return current.view;
    current = current.parent;
  }
  return null;
}

function replaceContentEditableText(element, value) {
  const selection = window.getSelection();
  if (!selection) return false;
  element.focus();
  const range = document.createRange();
  range.selectNodeContents(element);
  selection.removeAllRanges();
  selection.addRange(range);
  return document.execCommand("insertText", false, value);
}

function getLorebookSignature(text) {
  try {
    const data = JSON.parse(text);
    if (!Array.isArray(data)) return "";
    const categories = new Set();
    const names = [];
    for (const entry of data.slice(0, 20)) {
      if (entry?.category) categories.add(String(entry.category));
      if (entry?.name) names.push(String(entry.name));
    }
    return normalize([...categories, ...names.slice(0, 5)].join(" "));
  } catch {
    const category = text.match(/"category"\s*:\s*"([^"]+)"/)?.[1] || "";
    const name = text.match(/"name"\s*:\s*"([^"]+)"/)?.[1] || "";
    return normalize(`${category} ${name}`);
  }
}

function significantFileWords(file) {
  return normalize(file.name || file.filename || "")
    .split(/\s+/)
    .filter((word) => word && !["kyber", "rpg", "json"].includes(word) && !/^\d+$/.test(word));
}

function normalize(text) {
  return String(text || "").toLowerCase().replace(/\.json$/i, "").replace(/[^a-z0-9]+/g, " ").trim();
}

function isVisible(element) {
  const rect = element.getBoundingClientRect();
  const style = getComputedStyle(element);
  return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
}

function requireBundle() {
  if (!activeBundle?.files?.length) throw new Error("Load a GitHub or local bundle from the extension popup first.");
}

function setStatus(text, isError = false) {
  const node = document.querySelector(`#${PANEL_ID} [data-jlm="status"]`);
  node.textContent = text;
  node.className = `jlm-status${isError ? " jlm-error" : ""}`;
}

function setOutput(text) {
  document.querySelector(`#${PANEL_ID} [data-jlm="output"]`).textContent = text;
}

function downloadJson(filename, value) {
  const blob = new Blob([JSON.stringify(value, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}
