let activeProfileId = "production-queue";

const els = {
  status: document.getElementById("status"),
  profileName: document.getElementById("profileName"),
  manifestUrl: document.getElementById("manifestUrl"),
  saveProfile: document.getElementById("saveProfile"),
  fetchGithub: document.getElementById("fetchGithub"),
  localProjectFiles: document.getElementById("localProjectFiles"),
  loadLocalProject: document.getElementById("loadLocalProject"),
  localFiles: document.getElementById("localFiles"),
  loadLocal: document.getElementById("loadLocal"),
  openJanitor: document.getElementById("openJanitor"),
  sendToPage: document.getElementById("sendToPage"),
  characterSelect: document.getElementById("characterSelect"),
  sendCharacter: document.getElementById("sendCharacter"),
  publishCharacters: document.getElementById("publishCharacters"),
  testCharacter: document.getElementById("testCharacter"),
  openCreate: document.getElementById("openCreate"),
  bundleSummary: document.getElementById("bundleSummary")
};

init();

async function init() {
  await loadProfile();
  await refreshBundle();
  els.saveProfile.addEventListener("click", saveProfile);
  els.fetchGithub.addEventListener("click", fetchGithub);
  els.loadLocalProject.addEventListener("click", loadLocalProject);
  els.loadLocal.addEventListener("click", loadLocalFiles);
  els.openJanitor.addEventListener("click", () => chrome.tabs.create({ url: "https://janitorai.com/scripts" }));
  els.sendToPage.addEventListener("click", sendBundleToPage);
  els.sendCharacter.addEventListener("click", sendCharacterToPage);
  els.publishCharacters.addEventListener("click", publishCharacters);
  els.testCharacter.addEventListener("click", testCharacter);
  els.openCreate.addEventListener("click", () => chrome.tabs.create({ url: "https://janitorai.com/create_character" }));
}

async function publishCharacters() {
  els.publishCharacters.disabled = true;
  setStatus("Updating existing Janitor characters...");
  try {
    const response = await send({ type: "batch:publishProject", profileId: activeProfileId });
    if (!response.ok) return setStatus(response.error);
    const succeeded = response.results.filter((item) => item.ok).length;
    const failed = response.results.length - succeeded;
    setStatus(`Project update finished: ${succeeded} saved, ${failed} failed, ${response.skipped || 0} skipped.`);
    els.bundleSummary.textContent = response.results.map((item) => `${item.ok ? "OK" : "FAILED"}: ${item.name}${item.error ? ` — ${item.error}` : ""}`).join("\n");
  } finally {
    els.publishCharacters.disabled = false;
  }
}

async function testCharacter() {
  els.testCharacter.disabled = true;
  setStatus("Testing the first character only...");
  try {
    const response = await send({ type: "batch:testCharacter", profileId: activeProfileId });
    if (!response.ok) return setStatus(response.error);
    const item = response.results[0];
    setStatus(item?.ok ? `Smoke test saved: ${item.name}.` : `Smoke test failed: ${item?.error || "Unknown error"}`);
    els.bundleSummary.textContent = item ? `${item.ok ? "OK" : "FAILED"}: ${item.name}${item.error ? ` — ${item.error}` : ""}` : "No eligible character found.";
  } finally {
    els.testCharacter.disabled = false;
  }
}

async function loadProfile() {
  const response = await send({ type: "profiles:get" });
  if (!response.ok) return setStatus(response.error);
  activeProfileId = response.activeProfileId;
  const profile = response.profiles.find((item) => item.id === activeProfileId) || response.profiles[0];
  if (profile) {
    els.profileName.value = profile.name || "";
    els.manifestUrl.value = profile.manifestUrl || "";
  }
  const previous = await send({ type: "batch:getLastRun" });
  if (previous.ok && previous.run?.results?.length) {
    const run = previous.run;
    els.bundleSummary.textContent = run.results.map((item) => `${item.ok ? "OK" : "FAILED"}: ${item.name}${item.error ? ` — ${item.error}` : ""}`).join("\n");
    const failed = run.results.filter((item) => !item.ok).length;
    setStatus(`Last ${run.mode || "production"} run: ${run.results.length - failed} saved, ${failed} failed.`);
    return;
  }
  setStatus("Ready.");
}

async function saveProfile() {
  const name = els.profileName.value.trim() || "Untitled Project";
  const profile = {
    id: slugify(name),
    name,
    sourceMode: "github",
    manifestUrl: els.manifestUrl.value.trim(),
    capBytes: 450 * 1024,
    warningBytes: 400 * 1024
  };
  const response = await send({ type: "profiles:save", profile });
  if (!response.ok) {
    setStatus(response.error);
    return false;
  }
  activeProfileId = response.activeProfileId;
  const saved = response.profiles.find((item) => item.id === activeProfileId);
  if (saved) els.manifestUrl.value = saved.manifestUrl || "";
  setStatus("Profile saved.");
  return true;
}

async function fetchGithub() {
  if (!(await saveProfile())) return;
  setStatus("Fetching GitHub manifest...");
  const response = await send({ type: "github:fetchManifest", profileId: activeProfileId });
  if (!response.ok) return setStatus(response.error);
  renderSummary(response.bundle);
  setStatus("GitHub bundle loaded.");
}

async function loadLocalFiles() {
  const files = Array.from(els.localFiles.files || []);
  if (!files.length) return setStatus("Choose one or more JSON files first.");
  const loaded = [];
  for (const file of files) {
    const text = await file.text();
    loaded.push({
      name: file.name.replace(/\.json$/i, ""),
      filename: file.name,
      path: file.name,
      url: file.name,
      text
    });
  }
  const bundle = {
    source: "local",
    profileId: activeProfileId,
    project: els.profileName.value.trim() || "Local Project",
    version: `local-${new Date().toISOString()}`,
    fetchedAt: new Date().toISOString(),
    files: loaded
  };
  const response = await send({ type: "bundle:store", profileId: activeProfileId, bundle });
  if (!response.ok) return setStatus(response.error);
  renderSummary(response.bundle);
  setStatus("Local files loaded.");
}

async function loadLocalProject() {
  const files = Array.from(els.localProjectFiles.files || []);
  const manifestFile = files.find((file) => /(?:^|\/)janitor-manager-manifest\.json$/i.test(file.webkitRelativePath || file.name));
  if (!manifestFile) return setStatus("Choose a compiled project folder containing janitor-manager-manifest.json.");
  setStatus("Loading local compiled project...");
  try {
    const manifest = JSON.parse(await manifestFile.text());
    const rootPrefix = (manifestFile.webkitRelativePath || manifestFile.name).replace(/janitor-manager-manifest\.json$/i, "");
    const byPath = new Map(files.map((file) => [(file.webkitRelativePath || file.name).replace(/\\/g, "/"), file]));
    const resolveFile = (path) => byPath.get(`${rootPrefix}${String(path).replace(/^\.\//, "")}`.replace(/\\/g, "/"));
    const loadedLorebooks = [];
    for (const item of manifest.lorebooks || []) {
      const file = resolveFile(item.path || item.url);
      if (!file) throw new Error(`Compiled lorebook file not selected: ${item.path || item.url}`);
      loadedLorebooks.push({ ...item, url: file.name, text: await file.text() });
    }
    const loadedCharacters = [];
    for (const item of manifest.characters || []) {
      const fields = {};
      for (const [fieldName, source] of Object.entries(item.fields || {})) {
        if (source && typeof source === "object" && "text" in source) {
          fields[fieldName] = String(source.text || "");
          continue;
        }
        const path = typeof source === "string" ? source : source?.path;
        const file = resolveFile(path);
        if (!file) throw new Error(`Compiled character field not selected: ${path}`);
        fields[fieldName] = await file.text();
      }
      let avatarUrl = "";
      if (item.avatar) {
        const avatarFile = resolveFile(item.avatar);
        if (!avatarFile) throw new Error(`Compiled avatar not selected: ${item.avatar}`);
        avatarUrl = await fileToDataUrl(avatarFile);
      }
      loadedCharacters.push({ ...item, fields, avatarUrl });
    }
    const bundle = {
      source: "local-project", profileId: activeProfileId, project: manifest.project,
      version: manifest.version, fetchedAt: new Date().toISOString(),
      files: loadedLorebooks, characters: loadedCharacters
    };
    const response = await send({ type: "bundle:store", profileId: activeProfileId, bundle });
    if (!response.ok) return setStatus(response.error);
    renderSummary(response.bundle);
    setStatus("Local compiled project loaded and validated.");
  } catch (error) {
    setStatus(error.message || String(error));
  }
}

function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ""));
    reader.onerror = () => reject(reader.error || new Error(`Could not read ${file.name}`));
    reader.readAsDataURL(file);
  });
}

async function refreshBundle() {
  const response = await send({ type: "bundle:getActive", profileId: activeProfileId });
  if (response.ok && response.bundle) renderSummary(response.bundle);
}

async function sendBundleToPage() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return setStatus("No active tab.");
  const response = await chrome.tabs.sendMessage(tab.id, { type: "jlm:loadBundle", profileId: activeProfileId }).catch((error) => ({
    ok: false,
    error: error.message
  }));
  if (!response?.ok) return setStatus(response?.error || "Could not reach Janitor page.");
  setStatus("Bundle sent to page.");
}

async function sendCharacterToPage() {
  const characterId = els.characterSelect.value;
  if (!characterId) return setStatus("Load a manifest and choose a character first.");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return setStatus("No active tab.");
  const response = await chrome.tabs.sendMessage(tab.id, { type: "jm:loadCharacter", profileId: activeProfileId, characterId }).catch((error) => ({ ok: false, error: error.message }));
  if (!response?.ok) return setStatus(response?.error || "Could not reach Janitor page.");
  setStatus("Character package sent. Preview and apply it from the page panel.");
}

function renderSummary(bundle) {
  const files = bundle.files || [];
  const invalid = files.filter((file) => file.validation && !file.validation.ok).length;
  const warnings = files.filter((file) => file.validation?.warning).length;
  els.bundleSummary.textContent = [
    `${bundle.project || "Project"} ${bundle.version || ""}`,
    `Source: ${bundle.source || "unknown"}`,
    `Files: ${files.length}`,
    `Invalid: ${invalid}`,
    `Warnings: ${warnings}`,
    `Characters: ${(bundle.characters || []).length}`,
    "",
    ...files.map((file) => `${file.filename || file.name}: ${file.entries || 0} entries, ${Math.round((file.bytes || 0) / 1024)} KB${file.validation?.ok === false ? " INVALID" : ""}`)
  ].join("\n");
  renderCharacters(bundle.characters || []);
}

function renderCharacters(characters) {
  els.characterSelect.replaceChildren();
  if (!characters.length) {
    els.characterSelect.add(new Option("No characters loaded", ""));
    return;
  }
  for (const character of characters) els.characterSelect.add(new Option(`${character.name} (${character.fieldCount} fields)`, character.id));
}

function setStatus(text) {
  els.status.textContent = text;
}

function send(message) {
  return chrome.runtime.sendMessage(message);
}

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "project";
}
