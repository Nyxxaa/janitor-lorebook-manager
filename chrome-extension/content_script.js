const PANEL_ID = "jlm-panel";
let activeBundle = null;
let activeCharacter = null;
let detectedTargets = [];

syncPanelForRoute();
window.addEventListener("popstate", syncPanelForRoute);
setInterval(syncPanelForRoute, 1000);

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message).then(sendResponse).catch((error) => sendResponse({ ok: false, error: error.message }));
  return true;
});

async function handleMessage(message) {
  if (message?.type === "jm:autoCreateCharacter") {
    return autoCreateCharacter(message.profileId, message.characterId);
  }
  if (message?.type === "jm:autoUpdateCharacter") {
    return autoUpdateCharacter(message.profileId, message.characterId);
  }
  if (message?.type === "jm:autoUpdateLorebook") {
    return autoUpdateLorebook(message.profileId, message.fileKey);
  }
  if (message?.type === "jm:loadCharacter") {
    const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId: message.profileId });
    activeCharacter = response.bundle?.characters?.find((character) => character.id === message.characterId) || null;
    if (!activeCharacter) throw new Error("Character package was not found in the active repository bundle.");
    setStatus(`Loaded character: ${activeCharacter.name}. Preview before applying.`);
    previewCharacter();
    return { ok: true };
  }
  if (message?.type === "jm:exportLorebook") {
    return { ok: true, backup: await buildLorebookBackup() };
  }
  if (message?.type !== "jlm:loadBundle") throw new Error("Unknown page message.");
  const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId: message.profileId });
  if (!response.ok || !response.bundle) throw new Error("No active lorebook bundle loaded.");
  activeBundle = response.bundle;
  setStatus(`Loaded ${activeBundle.files.length} lorebooks from ${activeBundle.source}.`);
  renderSummary();
  return { ok: true };
}

async function autoCreateCharacter(profileId, characterId) {
  if (!/^\/create_character\/?$/i.test(location.pathname)) throw new Error("Automatic creation only runs on Janitor's character creation page.");
  const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId });
  const character = response.bundle?.characters?.find((item) => item.id === characterId);
  if (!character) throw new Error("Character package was not found in the active bundle.");
  if (character.validation?.ok === false) throw new Error(`Refusing invalid character package: ${(character.validation.errors || []).join("; ")}`);
  if (!character.avatarUrl) throw new Error("Character has no compiled avatar.");
  activeCharacter = character;
  await waitForCharacterForm();
  const plan = applyCharacter(false);
  if (plan.unmatched.length) throw new Error(`Refusing to create with ${plan.unmatched.length} unmatched repository fields.`);
  await setCharacterAvatar(character.avatarUrl, character.name);
  const createButton = findCharacterCreateButton();
  if (!createButton) throw new Error("A visible Create Character button was not found.");
  const startingUrl = location.href;
  createButton.scrollIntoView({ block: "center" });
  createButton.click();
  await waitForCreationConfirmation(startingUrl, createButton);
  return { ok: true, savedAt: new Date().toISOString(), createdUrl: location.href, matched: plan.matched.length };
}

async function setCharacterAvatar(url, name) {
  const input = Array.from(document.querySelectorAll("input[type='file']")).find((element) => isVisible(element) && /image|png|jpe?g|webp/i.test(element.accept || "image"));
  if (!input) throw new Error("A visible avatar file input was not found.");
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Avatar fetch failed: ${response.status}`);
  const blob = await response.blob();
  const extension = blob.type.includes("png") ? "png" : blob.type.includes("webp") ? "webp" : "jpg";
  const file = new File([blob], `${safeFilename(name)}-avatar.${extension}`, { type: blob.type || "image/png" });
  const transfer = new DataTransfer();
  transfer.items.add(file);
  input.files = transfer.files;
  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
}

function findCharacterCreateButton() {
  return Array.from(document.querySelectorAll("button, [role='button'], input[type='submit']")).find((element) => {
    if (!isVisible(element) || element.disabled || element.closest(`#${PANEL_ID}`)) return false;
    const text = [element.textContent, element.value, element.getAttribute("aria-label")].filter(Boolean).join(" ").trim();
    return /^(create|publish)(?:\s+character)?$/i.test(text);
  }) || null;
}

async function waitForCreationConfirmation(startingUrl, button) {
  for (let attempt = 0; attempt < 150; attempt += 1) {
    if (location.href !== startingUrl && /\/(?:edit_character|characters?)\//i.test(location.pathname)) return;
    const status = Array.from(document.querySelectorAll("[role='alert'], [role='status'], [data-sonner-toast], [class*='toast']")).map((e) => e.textContent || "").join(" ");
    if (/created|published|success/i.test(status)) return;
    if (/error|failed|required/i.test(status)) throw new Error(`Janitor rejected creation: ${status.trim()}`);
    if (!document.contains(button) && attempt > 5) return;
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error("Create was clicked, but Janitor did not confirm creation.");
}

async function autoUpdateLorebook(profileId, fileKey) {
  if (!/^\/scripts\/[0-9a-f-]+\/edit\/?$/i.test(location.pathname)) throw new Error("Automatic lorebook publishing only runs on an existing script edit page.");
  const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId });
  const file = response.bundle?.files?.find((item) => (item.sha256 || item.filename || item.name) === fileKey);
  if (!file?.text) throw new Error("Lorebook payload was not found in the active repository bundle.");
  if (file.validation?.ok === false) throw new Error(`Refusing invalid lorebook: ${file.validation.issues.join("; ")}`);
  await waitForLorebookEditorPage();
  let targets = detectTargets();
  if (!targets.length) {
    await openLorebookJsonInterface();
    targets = detectTargets();
  }
  if (targets.length !== 1) throw new Error(`Expected exactly one lorebook JSON editor, found ${targets.length}.`);
  const backup = await buildLorebookBackup();
  await chrome.runtime.sendMessage({ type: "backup:store", profileId, backup });
  setTargetValue(targets[0], file.text);
  const saveButton = findExistingRecordSaveButton();
  if (!saveButton) throw new Error("A visible Save/Update/Publish button was not found.");
  saveButton.scrollIntoView({ block: "center" });
  saveButton.click();
  await waitForCharacterSaveConfirmation(saveButton);
  return { ok: true, savedAt: new Date().toISOString() };
}

async function autoUpdateCharacter(profileId, characterId) {
  if (!/^\/edit_character\/[0-9a-f-]+\/?$/i.test(location.pathname)) throw new Error("Automatic publishing only runs on an existing character edit page.");
  const response = await chrome.runtime.sendMessage({ type: "bundle:getActive", profileId });
  const character = response.bundle?.characters?.find((item) => item.id === characterId);
  if (!character) throw new Error("Character package was not found in the active repository bundle.");
  if (character.validation?.ok === false) throw new Error(`Refusing invalid character package: ${(character.validation.errors || []).join("; ")}`);
  activeCharacter = character;
  await waitForCharacterForm();
  const before = detectCharacterFields();
  await chrome.runtime.sendMessage({
    type: "backup:store",
    profileId,
    backup: {
      schema: "janitor-character-backup/v1",
      characterName: inferCharacterName(before) || character.name,
      sourceUrl: location.href,
      pageTitle: document.title,
      exportedAt: new Date().toISOString(),
      fields: before
    }
  });
  const plan = applyCharacter(false);
  if (plan.unmatched.length) throw new Error(`Refusing to save with ${plan.unmatched.length} unmatched repository fields.`);
  if (!plan.matched.length) return { ok: true, savedAt: "", matched: 0, unchanged: plan.unchanged.length, skippedSave: true };
  const saveButton = findCharacterSaveButton();
  if (!saveButton) throw new Error("A visible Save/Update Character button was not found.");
  saveButton.scrollIntoView({ block: "center" });
  saveButton.click();
  await waitForCharacterSaveConfirmation(saveButton);
  return { ok: true, savedAt: new Date().toISOString(), matched: plan.matched.length, unchanged: plan.unchanged.length };
}

async function waitForCharacterForm() {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    if (detectCharacterTargets().length) return;
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error("Timed out waiting for Janitor's character form.");
}

function findCharacterSaveButton() {
  return Array.from(document.querySelectorAll("button, [role='button'], input[type='submit']")).find((element) => {
    if (!isVisible(element) || element.disabled || element.closest(`#${PANEL_ID}`)) return false;
    const text = [element.textContent, element.value, element.getAttribute("aria-label"), element.getAttribute("title")].filter(Boolean).join(" ").trim();
    return /^(save|update)(?:\s+(?:changes|character))?$/i.test(text);
  }) || null;
}

function findExistingRecordSaveButton() {
  return Array.from(document.querySelectorAll("button, [role='button'], input[type='submit']")).find((element) => {
    if (!isVisible(element) || element.disabled || element.closest(`#${PANEL_ID}`)) return false;
    const text = [element.textContent, element.value, element.getAttribute("aria-label"), element.getAttribute("title")].filter(Boolean).join(" ").trim();
    return /^(save|update|publish)(?:\s+(?:changes|script|lorebook))?$/i.test(text) && !/delete|create|new/i.test(text);
  }) || null;
}

async function waitForCharacterSaveConfirmation(saveButton) {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const statusText = Array.from(document.querySelectorAll("[role='alert'], [role='status'], [data-sonner-toast], [class*='toast'], [class*='notification']"))
      .map((element) => element.textContent || "").join(" ");
    if (/saved|updated|success/i.test(statusText)) return;
    if (saveButton.disabled && attempt > 2) return;
    if (!document.contains(saveButton) && attempt > 2) return;
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
  throw new Error("Save was clicked, but Janitor did not provide a success confirmation.");
}

function injectPanel() {
  if (document.getElementById(PANEL_ID)) return;
  const panel = document.createElement("div");
  panel.id = PANEL_ID;
  panel.innerHTML = `
    <header>
      <h2>Janitor Manager</h2>
      <button type="button" data-jlm="collapse" aria-label="Collapse Janitor Manager">−</button>
    </header>
    <div class="jlm-body">
      <div class="jlm-status" data-jlm="status">Ready. Load a repository project from the extension popup when needed.</div>
      <div class="jlm-section-label">Lorebooks</div>
      <div class="jlm-row">
        <button type="button" data-jlm="detect">Scan Editors</button>
        <button type="button" data-jlm="backup">Backup Current</button>
      </div>
      <div class="jlm-row">
        <button type="button" data-jlm="backup-all">Backup Entire Library</button>
      </div>
      <div class="jlm-row">
        <button type="button" data-jlm="dryrun">Preview Repository Fill</button>
        <button type="button" data-jlm="apply">Fill Lorebook Editors</button>
      </div>
      <div class="jlm-section-label">Character</div>
      <div class="jlm-row">
        <button type="button" data-jlm="character-backup">Backup Current Character</button>
      </div>
      <div class="jlm-row">
        <button type="button" data-jlm="character-preview">Preview Character Fill</button>
        <button type="button" data-jlm="character-apply">Fill Character Form</button>
      </div>
      <div class="jlm-section-label">Loaded Project</div>
      <div class="jlm-row">
        <button type="button" data-jlm="copy">Copy First Lorebook</button>
        <button type="button" data-jlm="download">Download Project Bundle</button>
      </div>
      <pre data-jlm="output">No scan yet.</pre>
    </div>
  `;
  document.documentElement.appendChild(panel);
  panel.addEventListener("click", onPanelClick);
}

function syncPanelForRoute() {
  const allowed = /^\/scripts(?:\/|$)|^\/(?:create_character|edit_character)(?:\/|$)/i.test(location.pathname);
  const panel = document.getElementById(PANEL_ID);
  if (allowed && !panel) injectPanel();
  if (!allowed && panel) panel.remove();
}

async function onPanelClick(event) {
  const action = event.target?.dataset?.jlm;
  if (!action) return;
  try {
    if (action === "collapse") return toggleCollapse();
    if (action === "detect") return detectAndRender();
    if (action === "backup") return backupPage();
    if (action === "backup-all") return backupAllLorebooks();
    if (action === "character-backup") return backupCharacterHtml();
    if (action === "character-preview") return previewCharacter();
    if (action === "character-apply") return applyCharacter();
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
  const backup = await buildLorebookBackup();
  await chrome.runtime.sendMessage({ type: "backup:store", backup });
  downloadJson(`${safeFilename(backup.lorebookName)}-lorebook-backup-${timestampForFilename()}.json`, backup);
  setStatus(`Backed up ${backup.fields.length} lorebook fields.`);
}

async function buildLorebookBackup() {
  await waitForLorebookEditorPage();
  detectedTargets = detectTargets();
  if (!detectedTargets.length) {
    await openLorebookJsonInterface();
    detectedTargets = detectTargets();
  }
  if (!detectedTargets.length) throw new Error(`No editable lorebook fields detected. Visible controls: ${describeVisibleEditorControls() || "none"}`);
  const fullEditors = await readFullCodeMirrorDocuments();
  return {
    schema: "janitor-lorebook-backup/v2",
    url: location.href,
    title: document.title,
    lorebookName: document.title.replace(/^janitor\s*-\s*Scripts\s*-\s*/i, "").trim() || "Janitor Lorebook",
    exportedAt: new Date().toISOString(),
    fields: detectedTargets.map((target) => ({
      label: target.label,
      value: target.kind === "codemirror" ? (fullEditors[target.codeMirrorIndex] ?? getTargetValue(target)) : getTargetValue(target)
    }))
  };
}

async function waitForLorebookEditorPage() {
  if (!/^\/scripts\/[^/]+\/edit(?:\/|$)/i.test(location.pathname)) return;
  for (let attempt = 0; attempt < 100; attempt += 1) {
    const pageText = Array.from(document.querySelectorAll("button, [role='button'], [role='tab'], a, h1, h2, h3"))
      .filter((element) => !element.closest(`#${PANEL_ID}`))
      .map((element) => element.textContent || "")
      .join(" ");
    if (/history|script page|configure|publish|add entry|import json|export json|lorebook entries/i.test(pageText)) return;
    await new Promise((resolve) => setTimeout(resolve, 200));
  }
}

async function openLorebookJsonInterface() {
  const controls = Array.from(document.querySelectorAll("button, [role='button'], [role='tab'], a"));
  const priorities = [/export\s*json/i, /view\s*json/i, /edit\s*json/i, /json/i, /raw/i, /source/i, /code\s*editor/i, /advanced\s*editor/i, /import\s*json/i];
  let control = null;
  for (const pattern of priorities) {
    control = controls.find((element) => {
      const description = [
        element.textContent,
        element.getAttribute("aria-label"),
        element.getAttribute("title"),
        element.getAttribute("data-tooltip"),
        element.getAttribute("data-state")
      ].filter(Boolean).join(" ");
      return pattern.test(description) && isVisible(element);
    });
    if (control) break;
  }
  if (!control) return;
  control.click();
  for (let attempt = 0; attempt < 25; attempt += 1) {
    await new Promise((resolve) => setTimeout(resolve, 200));
    if (detectTargets().length) return;
  }
}

function describeVisibleEditorControls() {
  return Array.from(document.querySelectorAll("button, [role='button'], [role='tab'], a"))
    .filter((element) => isVisible(element) && !element.closest(`#${PANEL_ID}`))
    .map((element) => [
      element.textContent,
      element.getAttribute("aria-label"),
      element.getAttribute("title"),
      element.getAttribute("data-tooltip")
    ].filter(Boolean).join(" ").replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .filter((value, index, values) => values.indexOf(value) === index)
    .slice(0, 40)
    .join(" | ");
}

async function backupAllLorebooks() {
  setStatus("Batch backup running. Keep this Janitor tab open; background tabs will close automatically.");
  const response = await chrome.runtime.sendMessage({ type: "batch:backupLorebooks" });
  if (!response?.ok) throw new Error(response?.error || "Batch backup failed.");
  const bundle = response.bundle;
  downloadJson(`janitor-all-lorebooks-${timestampForFilename()}.json`, bundle);
  setOutput([
    `Backed up: ${bundle.lorebooks.length}`,
    `Failed: ${bundle.failures.length}`,
    "",
    ...bundle.lorebooks.map((item) => `- ${item.lorebookName}`),
    ...(bundle.failures.length ? ["", "Failures:", ...bundle.failures.map((item) => `- ${item.url}: ${item.error}`)] : [])
  ].join("\n"));
  setStatus(`Batch complete: ${bundle.lorebooks.length} backed up, ${bundle.failures.length} failed.`);
}

function backupCharacterHtml() {
  const fields = detectCharacterFields();
  if (!fields.length) throw new Error("No visible Janitor character fields detected. Open the character editor first.");
  const name = inferCharacterName(fields) || document.title || "Janitor Character";
  const backup = {
    schema: "janitor-character-backup/v1",
    characterName: name,
    sourceUrl: location.href,
    pageTitle: document.title,
    exportedAt: new Date().toISOString(),
    fields
  };
  downloadHtml(`${safeFilename(name)}-character-backup-${timestampForFilename()}.html`, renderCharacterBackup(backup));
  setStatus(`Downloaded HTML backup with ${fields.length} character fields.`);
}

function inferCharacterName(fields) {
  const explicit = fields.find((field) => field.canonical === "Character Name")?.value.trim();
  if (explicit) return explicit;
  const text = fields.map((field) => field.value).join("\n");
  const patterns = [
    /##(?:stage_name|full_name|name):##\s*([^\n#]+)/i,
    /\{\{char\}\}\s*=\s*([^\n|#]+)/i,
    /\{\{char\}\}\s+is\s+(?:an?\s+)?([^\n,.;#]{2,80})/i
  ];
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]?.trim()) return match[1].replace(/\s+/g, " ").trim();
  }
  return "";
}

function detectCharacterFields() {
  return detectCharacterTargets().map(({ element, ...field }) => field);
}

function detectCharacterTargets() {
  const codeMirror = Array.from(document.querySelectorAll(".cm-editor .cm-content[contenteditable='true']"));
  const standard = Array.from(document.querySelectorAll("input, textarea, select, [contenteditable='true']"))
    .filter((field) => !field.closest(".cm-editor"));
  const seen = new Set();
  return [...codeMirror, ...standard]
    .filter((field) => !field.closest(`#${PANEL_ID}`) && isExportableCharacterField(field))
    .map((field, index) => {
      const label = inferLabel(field, index).replace(/\s+/g, " ").trim();
      return { element: field, label, canonical: canonicalCharacterField(label), value: getElementValue(field) };
    })
    .filter((field) => {
      const key = `${normalize(field.label)}\u0000${field.value}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
}

function previewCharacter() {
  if (!activeCharacter) throw new Error("Choose a repository character in the extension popup first.");
  const plan = buildCharacterPlan(activeCharacter, detectCharacterTargets());
  setOutput(formatCharacterPlan(plan));
  setStatus(`Character preview: ${plan.matched.length} matched, ${plan.unmatched.length} unmatched fields.`);
  return plan;
}

function applyCharacter(showFeedback = true) {
  if (!activeCharacter) throw new Error("Choose a repository character in the extension popup first.");
  const plan = buildCharacterPlan(activeCharacter, detectCharacterTargets());
  if (!plan.matched.length) throw new Error("No matching Janitor character fields found on this page.");
  for (const item of plan.matched) setTargetValue(item.target, item.value);
  if (showFeedback) {
    setOutput(`${formatCharacterPlan(plan)}\n\nApplied to the page. Review every field, then manually save or publish.`);
    setStatus(`Applied ${plan.matched.length} changed fields; ${plan.unchanged.length} already matched. Manual Janitor save is still required.`);
  }
  return plan;
}

function buildCharacterPlan(character, targets) {
  const aliases = {
    charactername: "Character Name",
    name: "Character Name",
    charactercard: "Character Card",
    description: "Character Card",
    personalitydefinition: "Personality / Definition",
    personality: "Personality / Definition",
    definition: "Personality / Definition",
    scenario: "Scenario",
    initialmessage: "Initial Message",
    greeting: "Initial Message",
    exampledialogs: "Example Dialogs",
    creatornotes: "Creator Notes",
    systemprompt: "System Prompt",
    posthistoryinstructions: "Post-History Instructions",
    tags: "Tags"
  };
  const matched = [];
  const unchanged = [];
  const unmatched = [];
  for (const [sourceName, value] of Object.entries(character.fields || {})) {
    const compact = String(sourceName).toLowerCase().replace(/[^a-z0-9]/g, "");
    const canonical = aliases[compact] || canonicalCharacterField(sourceName);
    const target = targets.find((candidate) => candidate.canonical === canonical);
    if (target && canonical) {
      const item = { sourceName, canonical, value, target };
      if (normalizeFieldValue(getTargetValue(target)) === normalizeFieldValue(value)) unchanged.push(item);
      else matched.push(item);
    }
    else unmatched.push({ sourceName, canonical });
  }
  return { character, matched, unchanged, unmatched };
}

function normalizeFieldValue(value) {
  return String(value ?? "").replace(/\r\n?/g, "\n").replace(/[ \t]+$/gm, "").trim();
}

function formatCharacterPlan(plan) {
  const lines = [`Character: ${plan.character.name}`, `Changed: ${plan.matched.length}`, `Already current: ${plan.unchanged.length}`, `Unmatched: ${plan.unmatched.length}`, ""];
  for (const item of plan.matched) lines.push(`- ${item.sourceName} -> ${item.target.label} (${item.value.length} chars)`);
  if (plan.unmatched.length) {
    lines.push("", "Unmatched repository fields:");
    for (const item of plan.unmatched) lines.push(`- ${item.sourceName}`);
  }
  return lines.join("\n");
}

function isExportableCharacterField(field) {
  if (!isVisible(field) || field.disabled) return false;
  if (field.matches("input[type='hidden'], input[type='password'], input[type='file'], input[type='submit'], input[type='button'], input[type='checkbox'], input[type='radio']")) return false;
  const label = inferLabel(field, 0);
  const canonical = canonicalCharacterField(label);
  const hint = normalize(`${label} ${field.id || ""} ${field.getAttribute("name") || ""}`);
  if (/token|secret|password|email|search|url slug/.test(hint)) return false;
  return Boolean(canonical) || field.matches("textarea, select, [contenteditable='true']");
}

function canonicalCharacterField(label) {
  const text = normalize(label);
  const aliases = [
    ["Character Name", /^(character )?name$|display name/],
    ["Character Card", /character card|description|appearance|character bio/],
    ["Personality / Definition", /personality|definition|persona|character prompt/],
    ["Scenario", /scenario|setting|context/],
    ["Initial Message", /initial message|first message|greeting/],
    ["Example Dialogs", /example dialog|example conversation|dialogue example/],
    ["Creator Notes", /creator note|author note|public note/],
    ["System Prompt", /system prompt/],
    ["Post-History Instructions", /post history|jailbreak/],
    ["Tags", /^tags?$|category/],
    ["Avatar / Image", /avatar|image|portrait/]
  ];
  return aliases.find(([, pattern]) => pattern.test(text))?.[0] || "";
}

function renderCharacterBackup(backup) {
  const data = JSON.stringify(backup).replace(/</g, "\\u003c");
  const sections = backup.fields.map((field) => `
    <section>
      <h2>${escapeHtml(field.canonical || field.label)}</h2>
      ${field.canonical && field.canonical !== field.label ? `<p class="source">Page label: ${escapeHtml(field.label)}</p>` : ""}
      <pre>${escapeHtml(field.value)}</pre>
    </section>`).join("");
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(backup.characterName)} — Janitor character backup</title>
<style>body{max-width:980px;margin:2rem auto;padding:0 1rem;font:16px/1.5 system-ui,sans-serif;color:#202124}header,section{border:1px solid #d9dce1;border-radius:10px;padding:1rem 1.25rem;margin:1rem 0}h1,h2{margin:.1rem 0 .6rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f7f9;padding:1rem;border-radius:6px}.meta,.source{color:#666;font-size:.9rem}</style>
</head><body><header><h1>${escapeHtml(backup.characterName)}</h1><p class="meta">Exported ${escapeHtml(backup.exportedAt)} from <a href="${escapeHtml(backup.sourceUrl)}">${escapeHtml(backup.pageTitle)}</a></p></header>${sections}
<script type="application/json" id="janitor-character-backup">${data}</script></body></html>`;
}

function escapeHtml(value) {
  return String(value || "").replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
}

function safeFilename(value) {
  return String(value || "janitor-character").replace(/[<>:\"/\\|?*\x00-\x1f]/g, "-").replace(/\s+/g, " ").trim().slice(0, 80) || "janitor-character";
}

function timestampForFilename() {
  return new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z").replace("T", "-");
}

async function applyToPage() {
  requireBundle();
  detectedTargets = detectTargets();
  const plan = buildApplyPlan(activeBundle, detectedTargets);
  const invalid = plan.matched.filter((item) => item.file.validation && !item.file.validation.ok);
  if (invalid.length) throw new Error(`Refusing to apply ${invalid.length} invalid lorebook files.`);
  if (!plan.matched.length) throw new Error("No matching Janitor lorebook fields found.");
  const fullEditors = await readFullCodeMirrorDocuments();
  const backup = {
    url: location.href,
    title: document.title,
    fields: detectedTargets.map((target) => ({
      label: target.label,
      value: target.kind === "codemirror" ? (fullEditors[target.codeMirrorIndex] ?? getTargetValue(target)) : getTargetValue(target)
    }))
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
      codeMirrorIndex: field.closest(".cm-editor") ? codeMirrorEditors.indexOf(field) : -1,
      length: getElementValue(field).length
    }));
}

async function readFullCodeMirrorDocuments() {
  const response = await chrome.runtime.sendMessage({ type: "page:readCodeMirror" });
  if (!response?.ok) throw new Error(response?.error || "Could not read the full Janitor editor document.");
  return response.documents || [];
}

function isLikelyLorebookField(field) {
  const value = getElementValue(field);
  const label = inferLabel(field, 0).toLowerCase();
  if (value.trim().startsWith("[") && value.includes('"keysRaw"')) return true;
  try {
    const parsed = JSON.parse(value);
    if (Array.isArray(parsed) && parsed.some((entry) => entry && typeof entry === "object" && ("content" in entry || "key" in entry))) return true;
  } catch {}
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
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function downloadHtml(filename, html) {
  const blob = new Blob([html], { type: "text/html;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
