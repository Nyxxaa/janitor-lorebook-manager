const STORE_KEYS = {
  profiles: "profiles",
  activeProfileId: "activeProfileId",
  bundles: "bundles",
  backups: "backups"
};

const DEFAULT_PROFILE = {
  id: "kyber-rpg",
  name: "Kyber RPG",
  sourceMode: "github",
  manifestUrl: "",
  lastAppliedVersion: "",
  capBytes: 450 * 1024,
  warningBytes: 400 * 1024
};

chrome.runtime.onInstalled.addListener(async () => {
  const current = await chrome.storage.local.get([STORE_KEYS.profiles, STORE_KEYS.activeProfileId]);
  if (!current[STORE_KEYS.profiles]) {
    await chrome.storage.local.set({
      [STORE_KEYS.profiles]: [DEFAULT_PROFILE],
      [STORE_KEYS.activeProfileId]: DEFAULT_PROFILE.id,
      [STORE_KEYS.bundles]: {},
      [STORE_KEYS.backups]: {}
    });
  }
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  handleMessage(message, sender)
    .then(sendResponse)
    .catch((error) => sendResponse({ ok: false, error: error.message || String(error) }));
  return true;
});

async function handleMessage(message, sender) {
  switch (message?.type) {
    case "profiles:get":
      return getProfiles();
    case "profiles:save":
      return saveProfile(message.profile);
    case "github:fetchManifest":
      return fetchManifest(message.profileId);
    case "bundle:store":
      return storeBundle(message.profileId, message.bundle);
    case "bundle:getActive":
      return getActiveBundle(message.profileId);
    case "backup:store":
      return storeBackup(message.profileId, message.backup);
    case "backup:list":
      return listBackups(message.profileId);
    default:
      throw new Error(`Unknown message type: ${message?.type}`);
  }
}

async function getProfiles() {
  const data = await chrome.storage.local.get([STORE_KEYS.profiles, STORE_KEYS.activeProfileId]);
  const profiles = data[STORE_KEYS.profiles] || [DEFAULT_PROFILE];
  return { ok: true, profiles, activeProfileId: data[STORE_KEYS.activeProfileId] || profiles[0]?.id };
}

async function saveProfile(profile) {
  if (!profile?.id || !profile?.name) throw new Error("Profile requires id and name.");
  const data = await chrome.storage.local.get([STORE_KEYS.profiles]);
  const profiles = data[STORE_KEYS.profiles] || [];
  const next = profiles.filter((item) => item.id !== profile.id);
  next.push({ ...DEFAULT_PROFILE, ...profile });
  next.sort((a, b) => a.name.localeCompare(b.name));
  await chrome.storage.local.set({ [STORE_KEYS.profiles]: next, [STORE_KEYS.activeProfileId]: profile.id });
  return { ok: true, profiles: next, activeProfileId: profile.id };
}

async function getProfile(profileId) {
  const { profiles, activeProfileId } = await getProfiles();
  return profiles.find((profile) => profile.id === (profileId || activeProfileId)) || profiles[0] || DEFAULT_PROFILE;
}

async function fetchManifest(profileId) {
  const profile = await getProfile(profileId);
  if (!profile.manifestUrl) throw new Error("Set a public GitHub raw manifest URL first.");
  const manifest = await fetchJson(profile.manifestUrl);
  validateManifest(manifest);
  const base = new URL(profile.manifestUrl);
  const files = [];
  for (const item of manifest.files || []) {
    const fileUrl = item.url?.startsWith("http") ? item.url : new URL(item.url || item.path, base).toString();
    const text = await fetchText(fileUrl);
    const hash = await sha256(text);
    if (item.sha256 && hash !== item.sha256) {
      throw new Error(`Hash mismatch for ${item.filename || item.name}.`);
    }
    const entries = parseLorebook(text, item.filename || item.name);
    files.push({
      ...item,
      url: fileUrl,
      text,
      sha256: hash,
      entries: entries.length,
      validation: validateLorebook(entries, text, profile)
    });
  }
  const bundle = {
    source: "github",
    profileId: profile.id,
    project: manifest.project || profile.name,
    version: manifest.version || new Date().toISOString(),
    generated: manifest.generated || "",
    fetchedAt: new Date().toISOString(),
    warningBytes: manifest.warningBytes || profile.warningBytes,
    capBytes: manifest.capBytes || profile.capBytes,
    files
  };
  await storeBundle(profile.id, bundle);
  return { ok: true, bundle: summarizeBundle(bundle) };
}

async function storeBundle(profileId, bundle) {
  if (!bundle?.files?.length) throw new Error("Bundle has no lorebook files.");
  const profile = await getProfile(profileId);
  for (const file of bundle.files) {
    const entries = parseLorebook(file.text, file.filename || file.name);
    file.validation = validateLorebook(entries, file.text, profile);
    file.entries = entries.length;
    file.bytes = byteLength(file.text);
    file.sha256 = file.sha256 || await sha256(file.text);
  }
  const data = await chrome.storage.local.get([STORE_KEYS.bundles]);
  const bundles = data[STORE_KEYS.bundles] || {};
  bundles[profile.id] = bundle;
  await chrome.storage.local.set({ [STORE_KEYS.bundles]: bundles });
  return { ok: true, bundle: summarizeBundle(bundle) };
}

async function getActiveBundle(profileId) {
  const profile = await getProfile(profileId);
  const data = await chrome.storage.local.get([STORE_KEYS.bundles]);
  const bundle = (data[STORE_KEYS.bundles] || {})[profile.id];
  return { ok: true, bundle };
}

async function storeBackup(profileId, backup) {
  const profile = await getProfile(profileId);
  const data = await chrome.storage.local.get([STORE_KEYS.backups]);
  const backups = data[STORE_KEYS.backups] || {};
  const list = backups[profile.id] || [];
  list.unshift({ ...backup, createdAt: new Date().toISOString() });
  backups[profile.id] = list.slice(0, 10);
  await chrome.storage.local.set({ [STORE_KEYS.backups]: backups });
  return { ok: true, count: backups[profile.id].length };
}

async function listBackups(profileId) {
  const profile = await getProfile(profileId);
  const data = await chrome.storage.local.get([STORE_KEYS.backups]);
  return { ok: true, backups: (data[STORE_KEYS.backups] || {})[profile.id] || [] };
}

async function fetchJson(url) {
  const text = await fetchText(url);
  return JSON.parse(text);
}

async function fetchText(url) {
  const response = await fetch(url, { cache: "no-store" });
  if (!response.ok) throw new Error(`Fetch failed ${response.status}: ${url}`);
  return response.text();
}

function validateManifest(manifest) {
  if (!manifest || typeof manifest !== "object") throw new Error("Manifest is not an object.");
  if (!Array.isArray(manifest.files) || manifest.files.length === 0) throw new Error("Manifest has no files.");
}

function parseLorebook(text, label) {
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error(`${label} is not valid JSON.`);
  }
  if (!Array.isArray(parsed)) throw new Error(`${label} root must be an array.`);
  return parsed;
}

function validateLorebook(entries, text, profile) {
  const issues = [];
  const names = new Set();
  const ids = new Set();
  entries.forEach((entry, index) => {
    if (!entry || typeof entry !== "object") {
      issues.push(`entry ${index} is not an object`);
      return;
    }
    ["name", "content", "key", "keysRaw", "keywordsRaw"].forEach((field) => {
      if (!(field in entry)) issues.push(`entry ${index} missing ${field}`);
    });
    if (entry.id) {
      if (ids.has(entry.id)) issues.push(`duplicate id ${entry.id}`);
      ids.add(entry.id);
    }
    const lowerName = String(entry.name || "").toLowerCase();
    if (lowerName) {
      if (names.has(lowerName)) issues.push(`duplicate name ${entry.name}`);
      names.add(lowerName);
    }
    if (Array.isArray(entry.key)) {
      const joined = entry.key.join(", ");
      if (entry.keysRaw !== joined) issues.push(`entry ${index} keysRaw mismatch`);
      if (entry.keywordsRaw !== joined) issues.push(`entry ${index} keywordsRaw mismatch`);
    } else {
      issues.push(`entry ${index} key is not an array`);
    }
  });
  const bytes = byteLength(text);
  if (bytes >= (profile.capBytes || 450 * 1024)) issues.push(`over cap: ${bytes} bytes`);
  return {
    ok: issues.length === 0,
    issues,
    bytes,
    warning: bytes >= (profile.warningBytes || 400 * 1024),
    overCap: bytes >= (profile.capBytes || 450 * 1024)
  };
}

function summarizeBundle(bundle) {
  return {
    source: bundle.source,
    project: bundle.project,
    version: bundle.version,
    fetchedAt: bundle.fetchedAt,
    files: bundle.files.map((file) => ({
      name: file.name,
      filename: file.filename,
      bytes: file.bytes,
      entries: file.entries,
      sha256: file.sha256,
      validation: file.validation
    }))
  };
}

async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function byteLength(text) {
  return new TextEncoder().encode(text).length;
}
