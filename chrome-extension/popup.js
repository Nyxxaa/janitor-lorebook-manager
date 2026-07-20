let activeProfileId = "kyber-rpg";

const els = {
  status: document.getElementById("status"),
  profileName: document.getElementById("profileName"),
  manifestUrl: document.getElementById("manifestUrl"),
  saveProfile: document.getElementById("saveProfile"),
  fetchGithub: document.getElementById("fetchGithub"),
  localFiles: document.getElementById("localFiles"),
  loadLocal: document.getElementById("loadLocal"),
  openJanitor: document.getElementById("openJanitor"),
  sendToPage: document.getElementById("sendToPage"),
  bundleSummary: document.getElementById("bundleSummary")
};

init();

async function init() {
  await loadProfile();
  await refreshBundle();
  els.saveProfile.addEventListener("click", saveProfile);
  els.fetchGithub.addEventListener("click", fetchGithub);
  els.loadLocal.addEventListener("click", loadLocalFiles);
  els.openJanitor.addEventListener("click", () => chrome.tabs.create({ url: "https://janitorai.com/" }));
  els.sendToPage.addEventListener("click", sendBundleToPage);
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
  if (!response.ok) return setStatus(response.error);
  activeProfileId = response.activeProfileId;
  setStatus("Profile saved.");
}

async function fetchGithub() {
  await saveProfile();
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
    "",
    ...files.map((file) => `${file.filename || file.name}: ${file.entries || 0} entries, ${Math.round((file.bytes || 0) / 1024)} KB${file.validation?.ok === false ? " INVALID" : ""}`)
  ].join("\n");
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
