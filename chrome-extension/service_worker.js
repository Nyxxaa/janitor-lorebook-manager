const STORE_KEYS = {
  profiles: "profiles",
  activeProfileId: "activeProfileId",
  bundles: "bundles",
  backups: "backups",
  lastRun: "lastRun",
  runControl: "runControl"
};

const DEFAULT_PROFILE = {
  id: "production-queue",
  name: "Production Queue",
  sourceMode: "github",
  manifestUrl: "https://raw.githubusercontent.com/Nyxxaa/janitor-lorebook-manager/main/production/due-2026-08-21/janitor-manager-manifest.json",
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
  } else {
    const profiles = current[STORE_KEYS.profiles];
    const legacy = profiles.find((profile) => profile.id === "kyber-rpg" && !profile.manifestUrl);
    if (legacy) {
      Object.assign(legacy, DEFAULT_PROFILE);
    }
    const production = profiles.find((profile) => profile.id === DEFAULT_PROFILE.id);
    if (production) Object.assign(production, DEFAULT_PROFILE);
    else profiles.unshift({ ...DEFAULT_PROFILE });
    await chrome.storage.local.set({
      [STORE_KEYS.profiles]: profiles,
      [STORE_KEYS.activeProfileId]: DEFAULT_PROFILE.id,
      [STORE_KEYS.runControl]: {
        running: false,
        stopRequested: false,
        resetAt: new Date().toISOString(),
        resetReason: "extension-installed-or-updated"
      }
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
    case "page:readCodeMirror":
      return readCodeMirrorDocuments(sender);
    case "batch:backupLorebooks":
      return batchBackupLorebooks(sender);
    case "batch:publishProject":
      return batchPublishProject(message.profileId);
    case "batch:publishCharacters":
      return runCharacterBatch(message.profileId);
    case "batch:testCharacter":
      return testCharacter(message.profileId);
    case "batch:compareCharacters":
      return compareCharacters(message.profileId, message.sourceTabId);
    case "batch:stop":
      return requestStop();
    case "batch:getRunState":
      return getRunState();
    case "batch:getLastRun":
      return getLastRun();
    default:
      throw new Error(`Unknown message type: ${message?.type}`);
  }
}

async function batchPublishProject(profileId) {
  await beginRun("bulk");
  try {
    const lorebookResult = await batchPublishLorebooks(profileId);
    const characterResult = await batchPublishCharacters(profileId);
    const result = { ok: true, mode: "bulk", stopped: await isStopRequested(), skipped: lorebookResult.skipped + characterResult.skipped, results: [...lorebookResult.results, ...characterResult.results] };
    await chrome.storage.local.set({ [STORE_KEYS.lastRun]: result });
    await downloadRunLog(result);
    return result;
  } finally {
    await finishRun();
  }
}

async function runCharacterBatch(profileId) {
  await beginRun("characters");
  try {
    const result = { ...(await batchPublishCharacters(profileId)), mode: "characters", stopped: await isStopRequested() };
    await chrome.storage.local.set({ [STORE_KEYS.lastRun]: result });
    await downloadRunLog(result);
    return result;
  } finally {
    await finishRun();
  }
}

async function testCharacter(profileId) {
  await beginRun("smoke");
  try {
    const result = { ...(await batchPublishCharacters(profileId, 1)), mode: "smoke", stopped: await isStopRequested() };
    await chrome.storage.local.set({ [STORE_KEYS.lastRun]: result });
    await downloadRunLog(result);
    return result;
  } finally {
    await finishRun();
  }
}

async function beginRun(mode) {
  const state = await getRunState();
  if (state.running) throw new Error(`A ${state.mode || "batch"} run is already active.`);
  await chrome.storage.local.set({ [STORE_KEYS.runControl]: { running: true, stopRequested: false, mode, startedAt: new Date().toISOString() } });
}

async function finishRun() {
  await chrome.storage.local.set({ [STORE_KEYS.runControl]: { running: false, stopRequested: false, finishedAt: new Date().toISOString() } });
}

async function getRunState() {
  const data = await chrome.storage.local.get([STORE_KEYS.runControl]);
  return { ok: true, running: false, stopRequested: false, ...(data[STORE_KEYS.runControl] || {}) };
}

async function requestStop() {
  const state = await getRunState();
  if (!state.running) return { ok: false, error: "No batch run is active." };
  await chrome.storage.local.set({ [STORE_KEYS.runControl]: { ...state, stopRequested: true, stopRequestedAt: new Date().toISOString() } });
  return { ok: true };
}

async function isStopRequested() {
  return (await getRunState()).stopRequested;
}

async function getLastRun() {
  const data = await chrome.storage.local.get([STORE_KEYS.lastRun]);
  return { ok: true, run: data[STORE_KEYS.lastRun] || null };
}

async function downloadRunLog(result) {
  const payload = {
    schema: "janitor-manager-run-log/v1",
    generatedAt: new Date().toISOString(),
    ...result
  };
  const text = JSON.stringify(payload, null, 2);
  const url = `data:application/json;charset=utf-8,${encodeURIComponent(text)}`;
  await chrome.downloads.download({
    url,
    filename: "Janitor Manager Logs/janitor-manager-last-run.json",
    conflictAction: "overwrite",
    saveAs: false
  });
}

async function batchPublishLorebooks(profileId) {
  const response = await getActiveBundle(profileId);
  const files = response.bundle?.files || [];
  const eligible = files.filter((file) => file.editUrl);
  const results = [];
  for (const file of eligible) {
    if (await isStopRequested()) break;
    let tab;
    try {
      const url = new URL(file.editUrl);
      if (!/^https:\/\/(?:www\.)?janitorai\.com$/i.test(url.origin) || !/^\/scripts\/[0-9a-f-]+\/edit\/?$/i.test(url.pathname)) throw new Error("Refusing a non-Janitor or non-edit lorebook URL.");
      tab = await chrome.tabs.create({ url: url.toString(), active: false });
      await waitForTabComplete(tab.id, 30000);
      const result = await sendTabMessageWithRetry(tab.id, { type: "jm:autoUpdateLorebook", profileId, fileKey: file.sha256 || file.filename || file.name }, 30, 500);
      if (!result?.ok) throw new Error(result?.error || "Janitor did not confirm the lorebook update.");
      results.push({ name: `Lorebook: ${file.name || file.filename}`, editUrl: file.editUrl, ok: true, savedAt: result.savedAt });
    } catch (error) {
      results.push({ name: `Lorebook: ${file.name || file.filename}`, editUrl: file.editUrl, ok: false, error: error.message || String(error) });
    } finally {
      if (tab?.id) await chrome.tabs.remove(tab.id).catch(() => {});
    }
  }
  return { results, skipped: files.length - eligible.length };
}

async function batchPublishCharacters(profileId, limit = Infinity) {
  const response = await getActiveBundle(profileId);
  const bundle = response.bundle;
  if (!bundle?.characters?.length) return { ok: true, attempted: 0, skipped: 0, results: [] };
  await applyRememberedCharacterUrls(bundle, profileId);
  const allEligible = bundle.characters.filter((character) =>
    character.validation?.ok !== false && Boolean(character.editUrl)
  );
  const eligible = allEligible.slice(0, limit);
  if (!eligible.length) return { ok: true, attempted: 0, skipped: bundle.characters.length, results: [] };
  const results = [];
  for (const character of eligible) {
    if (await isStopRequested()) break;
    let tab;
    try {
      const creating = false;
      const url = new URL(character.editUrl);
      if (!/^https:\/\/(?:www\.)?janitorai\.com$/i.test(url.origin) || !/^\/edit_character\/[0-9a-f-]+\/?$/i.test(url.pathname)) throw new Error("Refusing an invalid Janitor character edit URL.");
      tab = await chrome.tabs.create({ url: url.toString(), active: false });
      await waitForTabComplete(tab.id, 30000);
      const result = await sendTabMessageWithRetry(tab.id, {
        type: "jm:autoUpdateCharacter",
        profileId,
        characterId: character.id
      }, 30, 500);
      if (!result?.ok) {
        const failure = new Error(result?.error || "Janitor did not confirm the update.");
        failure.diagnostics = result?.diagnostics;
        throw failure;
      }
      const savedUrl = toCharacterEditUrl(result.createdUrl || character.editUrl);
      let releaseResult = { releaseAction: "visibility-preserved" };
      results.push({
        id: character.id,
        name: character.name,
        action: "updated",
        editUrl: savedUrl || result.createdUrl || character.editUrl,
        ok: true,
        savedAt: result.savedAt,
        skippedSave: result.skippedSave || false,
        ...releaseResult
      });
    } catch (error) {
      results.push({ id: character.id, name: character.name, editUrl: character.editUrl, ok: false, error: error.message || String(error), diagnostics: error.diagnostics || null });
    } finally {
      if (tab?.id) await chrome.tabs.remove(tab.id).catch(() => {});
    }
  }
  return { ok: true, attempted: results.length, skipped: bundle.characters.length - results.length, results };
}

async function compareCharacters(profileId, sourceTabId) {
  await beginRun("compare");
  try {
    const sourceTab = await chrome.tabs.get(sourceTabId);
    if (!/^https:\/\/(?:www\.)?janitorai\.com\/my_characters/i.test(sourceTab.url || "")) throw new Error("Open Janitor's My Characters page before comparing.");
    const [{ result: inventory }] = await chrome.scripting.executeScript({
      target: { tabId: sourceTabId },
      world: "MAIN",
      func: async () => {
        const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
        const found = new Map();
        const startPage = document.querySelector('button[class*="pageButtonActive"]')?.textContent?.trim() || "1";
        for (let page = 0; page < 20; page += 1) {
          for (const card of document.querySelectorAll(".pp-cc-wrapper")) {
            const edit = card.querySelector('a[href^="/edit_character/"]');
            const publicLink = card.querySelector('a.profile-character-card-stack-link-component[href^="/characters/"]');
            const match = (edit?.getAttribute("href") || publicLink?.getAttribute("href") || "").match(/(?:edit_character\/|characters\/)([0-9a-f-]+)/i);
            if (!match) continue;
            found.set(match[1], {
              uuid: match[1],
              name: card.querySelector(".pp-cc-name")?.textContent?.trim() || "",
              editUrl: new URL(edit?.getAttribute("href") || `/edit_character/${match[1]}`, location.origin).href,
              publicUrl: publicLink ? new URL(publicLink.getAttribute("href"), location.origin).href : "",
              tags: Array.from(card.querySelectorAll(".pp-cc-tags-item")).map((node) => node.textContent.trim()).filter(Boolean)
            });
          }
          const next = document.querySelector('button[aria-label="Next Page"]');
          if (!next || next.disabled) break;
          const signature = document.querySelector('a[href^="/edit_character/"]')?.getAttribute("href") || "";
          next.click();
          for (let attempt = 0; attempt < 40; attempt += 1) {
            await sleep(250);
            const current = document.querySelector('a[href^="/edit_character/"]')?.getAttribute("href") || "";
            if (current && current !== signature) break;
          }
        }
        const returnButton = Array.from(document.querySelectorAll("button")).find((button) => button.textContent.trim() === startPage && !button.disabled);
        if (returnButton && !returnButton.matches('[class*="pageButtonActive"]')) returnButton.click();
        return Array.from(found.values());
      }
    });
    const bundle = (await getActiveBundle(profileId)).bundle;
    await applyRememberedCharacterUrls(bundle, profileId);
    const byUuid = new Map((inventory || []).map((item) => [item.uuid.toLowerCase(), item]));
    const normalizeInventoryName = (value) => String(value || "").toLowerCase()
      .normalize("NFKD").replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, " ").trim();
    const byName = new Map();
    for (const item of inventory || []) {
      const key = normalizeInventoryName(item.name);
      if (!key) continue;
      if (!byName.has(key)) byName.set(key, []);
      byName.get(key).push(item);
    }
    const results = [];
    for (const character of bundle.characters || []) {
      if (await isStopRequested()) break;
      const uuid = String(character.editUrl || "").match(/edit_character\/([0-9a-f-]+)/i)?.[1]?.toLowerCase();
      const uuidMatch = uuid ? byUuid.get(uuid) : null;
      const nameMatches = byName.get(normalizeInventoryName(character.name)) || [];
      const live = uuidMatch || (nameMatches.length === 1 ? nameMatches[0] : null);
      if (!live) {
        results.push({
          id: character.id,
          name: character.name,
          present: false,
          ok: true,
          matchMethod: "none",
          nameCandidates: nameMatches.map((item) => ({
            uuid: item.uuid,
            name: item.name,
            editUrl: item.editUrl,
            publicUrl: item.publicUrl
          }))
        });
        continue;
      }
      let tab;
      try {
        tab = await chrome.tabs.create({ url: live.editUrl, active: false });
        await waitForTabComplete(tab.id, 30000);
        const inspected = await sendTabMessageWithRetry(tab.id, { type: "jm:compareCharacter", profileId, characterId: character.id }, 30, 500);
        if (!inspected?.ok) throw new Error(inspected?.error || "Could not inspect the character editor.");
        results.push({
          id: character.id, name: character.name, liveName: live.name, editUrl: live.editUrl, present: true, ok: true,
          matchMethod: uuidMatch ? "uuid" : "unique-exact-name",
          different: inspected.comparison.different.length,
          current: inspected.comparison.current.length,
          unmatched: inspected.comparison.unmatched.length,
          fields: inspected.comparison,
          liveTags: live.tags
        });
      } catch (error) {
        results.push({ id: character.id, name: character.name, editUrl: live.editUrl, present: true, ok: false, error: error.message || String(error) });
      } finally {
        if (tab?.id) await chrome.tabs.remove(tab.id).catch(() => {});
      }
    }
    const result = {
      ok: true,
      mode: "compare",
      stopped: await isStopRequested(),
      inventoryCount: inventory?.length || 0,
      missing: results.filter((item) => !item.present).length,
      duplicateNameGroups: Array.from(byName.entries())
        .filter(([, items]) => items.length > 1)
        .map(([normalizedName, items]) => ({
          normalizedName,
          characters: items.map((item) => ({
            uuid: item.uuid,
            name: item.name,
            editUrl: item.editUrl,
            publicUrl: item.publicUrl
          }))
        })),
      unmatchedInventory: (inventory || []).filter((item) =>
        !results.some((result) => result.present && result.editUrl === item.editUrl)
      ),
      results
    };
    await chrome.storage.local.set({ [STORE_KEYS.lastRun]: result });
    await downloadRunLog(result);
    return result;
  } finally {
    await finishRun();
  }
}

async function applyRememberedCharacterUrls(bundle, profileId) {
  const data = await chrome.storage.local.get([STORE_KEYS.lastRun]);
  const remembered = new Map((data[STORE_KEYS.lastRun]?.results || [])
    .filter((item) => item.ok && item.id && item.editUrl)
    .map((item) => [item.id, toCharacterEditUrl(item.editUrl)]));
  let changed = false;
  for (const character of bundle.characters || []) {
    const editUrl = remembered.get(character.id);
    if (!character.editUrl && editUrl) {
      character.editUrl = editUrl;
      changed = true;
    }
  }
  if (changed) await persistBundle(profileId, bundle);
}

function toCharacterEditUrl(value) {
  if (!value) return "";
  try {
    const url = new URL(value);
    const publicMatch = url.pathname.match(/^\/characters\/([0-9a-f-]+)_character-/i);
    if (publicMatch) return `${url.origin}/edit_character/${publicMatch[1]}`;
    return url.toString();
  } catch {
    return "";
  }
}

function toCharacterPublicUrl(value, name) {
  if (!value) return "";
  try {
    const url = new URL(value);
    const publicMatch = url.pathname.match(/^\/characters\/([0-9a-f-]+)_character-/i);
    if (publicMatch) return url.toString();
    const editMatch = url.pathname.match(/^\/edit_character\/([0-9a-f-]+)/i);
    if (!editMatch) return "";
    const slug = String(name || "character").toLowerCase()
      .normalize("NFKD").replace(/[\u0300-\u036f]/g, "")
      .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    return `${url.origin}/characters/${editMatch[1]}_character-${slug || "character"}`;
  } catch {
    return "";
  }
}

function buildCharacterRelease(character) {
  const planned = new Date(character.plannedDate);
  if (Number.isNaN(planned.getTime())) throw new Error(`Refusing to release ${character.name || "character"} without a valid plannedDate.`);
  const localNow = new Date();
  const date = [
    planned.getFullYear(),
    String(planned.getMonth() + 1).padStart(2, "0"),
    String(planned.getDate()).padStart(2, "0")
  ].join("-");
  const today = [
    localNow.getFullYear(),
    String(localNow.getMonth() + 1).padStart(2, "0"),
    String(localNow.getDate()).padStart(2, "0")
  ].join("-");
  if (date <= today) return { mode: "now" };
  return { mode: "schedule", scheduleType: "countdown", date, time: "12:00" };
}

async function persistBundle(profileId, bundle) {
  const data = await chrome.storage.local.get([STORE_KEYS.bundles]);
  const bundles = data[STORE_KEYS.bundles] || {};
  bundles[profileId] = bundle;
  await chrome.storage.local.set({ [STORE_KEYS.bundles]: bundles });
}

async function batchBackupLorebooks(sender) {
  if (!sender.tab?.id) throw new Error("Start batch backup from the Janitor Manager page panel.");
  const sourceTabId = sender.tab.id;
  const discovery = await chrome.scripting.executeScript({
    target: { tabId: sourceTabId },
    world: "MAIN",
    func: async () => {
      const selector = 'div[role="button"][class*="_card_"][class*="_list_"][class*="_clickable_"]';
      const initialCards = Array.from(document.querySelectorAll(selector));
      if (!initialCards.length) throw new Error("Janitor script cards were not found with the verified selector.");
      const manifest = initialCards.map((card, index) => ({
        index,
        name: (card.textContent || "").replace(/\s+/g, " ").trim(),
        theme: card.getAttribute("data-color-theme") || ""
      }));
      const discovered = [];
      for (const item of manifest) {
        const freshCards = Array.from(document.querySelectorAll(selector));
        if (freshCards.length !== manifest.length || !freshCards[item.index]) {
          discovered.push({ ...item, error: `Card list changed: expected ${manifest.length}, found ${freshCards.length}` });
          continue;
        }
        const card = freshCards[item.index];
        card.scrollIntoView({ block: "center" });
        card.click();
        let selected = false;
        for (let attempt = 0; attempt < 50; attempt += 1) {
          await new Promise((resolve) => setTimeout(resolve, 100));
          const currentCards = Array.from(document.querySelectorAll(selector));
          const current = currentCards[item.index];
          if (current?.className && String(current.className).includes("_selected_")) {
            selected = true;
            break;
          }
        }
        const urlMatch = location.href.match(/^https:\/\/[^/]+\/scripts\/[0-9a-f-]+\/edit(?:[?#].*)?$/i);
        discovered.push({ ...item, url: urlMatch?.[0] || "", selected, actualCount: document.querySelectorAll(selector).length });
      }
      return discovered;
    }
  });
  const discoveryManifest = discovery[0]?.result || [];
  const urls = [...new Set(discoveryManifest.map((item) => item.url).filter(Boolean))];
  if (!urls.length) throw new Error("No lorebook edit links found. Open Janitor's Lorebook Library, then run Backup Entire Library.");
  const lorebooks = [];
  const failures = discoveryManifest
    .filter((item) => item.error || !item.url)
    .map((item) => ({ url: item.url || `sidebar-index:${item.index}`, error: item.error || `No script URL recorded for ${item.name}` }));
  if (urls.length !== discoveryManifest.length) {
    failures.push({ url: sender.tab.url || "sidebar", error: `Discovery mismatch: ${discoveryManifest.length} cards produced ${urls.length} unique script URLs.` });
  }
  for (const url of urls) {
    let tab;
    try {
      tab = await chrome.tabs.create({ url, active: false });
      await waitForTabComplete(tab.id, 30000);
      const response = await sendTabMessageWithRetry(tab.id, { type: "jm:exportLorebook" }, 20, 300);
      if (!response?.ok || !response.backup) throw new Error(response?.error || "No backup returned.");
      lorebooks.push(response.backup);
    } catch (error) {
      failures.push({ url, error: error.message || String(error) });
    } finally {
      if (tab?.id) await chrome.tabs.remove(tab.id).catch(() => {});
    }
  }
  return {
    ok: true,
    bundle: {
      schema: "janitor-lorebook-batch-backup/v1",
      exportedAt: new Date().toISOString(),
      sourcePage: sender.tab.url || "",
      discovery: {
        cardCount: discoveryManifest.length,
        uniqueUrlCount: urls.length,
        cards: discoveryManifest
      },
      lorebooks,
      failures
    }
  };
}

function waitForTabComplete(tabId, timeoutMs) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => finish(new Error("Timed out loading lorebook page.")), timeoutMs);
    const listener = (updatedId, changeInfo) => {
      if (updatedId === tabId && changeInfo.status === "complete") finish();
    };
    const finish = (error) => {
      clearTimeout(timeout);
      chrome.tabs.onUpdated.removeListener(listener);
      error ? reject(error) : resolve();
    };
    chrome.tabs.onUpdated.addListener(listener);
    chrome.tabs.get(tabId).then((tab) => {
      if (tab.status === "complete") finish();
    }).catch(finish);
  });
}

async function sendTabMessageWithRetry(tabId, message, attempts, delayMs) {
  let lastError;
  for (let attempt = 0; attempt < attempts; attempt += 1) {
    try {
      return await chrome.tabs.sendMessage(tabId, message);
    } catch (error) {
      lastError = error;
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
  throw lastError || new Error("Could not reach lorebook page.");
}

async function readCodeMirrorDocuments(sender) {
  if (!sender.tab?.id) throw new Error("CodeMirror read requires a Janitor page tab.");
  const results = await chrome.scripting.executeScript({
    target: { tabId: sender.tab.id },
    world: "MAIN",
    func: () => Array.from(document.querySelectorAll(".cm-editor")).map((editor) => {
      const content = editor.querySelector(".cm-content");
      const candidates = [content?.cmView, editor.cmView].filter(Boolean);
      for (const candidate of candidates) {
        let node = candidate;
        for (let depth = 0; node && depth < 30; depth += 1) {
          if (node.view?.state?.doc) return node.view.state.doc.toString();
          node = node.parent;
        }
      }
      return content?.innerText || content?.textContent || "";
    })
  });
  return { ok: true, documents: results[0]?.result || [] };
}

async function getProfiles() {
  const data = await chrome.storage.local.get([STORE_KEYS.profiles, STORE_KEYS.activeProfileId]);
  const storedProfiles = data[STORE_KEYS.profiles] || [DEFAULT_PROFILE];
  const profiles = storedProfiles.map((profile) => normalizeProfile(profile));
  if (JSON.stringify(profiles) !== JSON.stringify(storedProfiles)) {
    await chrome.storage.local.set({ [STORE_KEYS.profiles]: profiles });
  }
  return { ok: true, profiles, activeProfileId: data[STORE_KEYS.activeProfileId] || profiles[0]?.id };
}

async function saveProfile(profile) {
  if (!profile?.id || !profile?.name) throw new Error("Profile requires id and name.");
  const data = await chrome.storage.local.get([STORE_KEYS.profiles]);
  const profiles = data[STORE_KEYS.profiles] || [];
  const next = profiles.filter((item) => item.id !== profile.id);
  next.push(normalizeProfile({ ...DEFAULT_PROFILE, ...profile }));
  next.sort((a, b) => a.name.localeCompare(b.name));
  await chrome.storage.local.set({ [STORE_KEYS.profiles]: next, [STORE_KEYS.activeProfileId]: profile.id });
  return { ok: true, profiles: next, activeProfileId: profile.id };
}

async function getProfile(profileId) {
  const { profiles, activeProfileId } = await getProfiles();
  return profiles.find((profile) => profile.id === (profileId || activeProfileId)) || profiles[0] || DEFAULT_PROFILE;
}

function normalizeProfile(profile) {
  const normalized = { ...profile };
  const value = String(normalized.manifestUrl || "").trim();

  // Repair the production profile if text was pasted into the middle of its URL.
  if (
    normalized.id === DEFAULT_PROFILE.id &&
    (!isValidManifestUrl(value) || value.includes("janitohttps://") || value.includes("github.com/Nyxxaa/janitor-lorebook-managerr-"))
  ) {
    normalized.manifestUrl = DEFAULT_PROFILE.manifestUrl;
    return normalized;
  }

  normalized.manifestUrl = normalizeGitHubManifestUrl(value);
  if (normalized.manifestUrl && !isValidManifestUrl(normalized.manifestUrl)) {
    throw new Error("Manifest URL must be one complete HTTPS URL. Replace the field instead of pasting into the middle of it.");
  }
  return normalized;
}

function normalizeGitHubManifestUrl(value) {
  if (!value) return "";
  const match = value.match(/^https:\/\/github\.com\/([^/]+)\/([^/#?]+)\/blob\/([^/]+)\/(.+)$/i);
  if (!match) return value;
  return `https://raw.githubusercontent.com/${match[1]}/${match[2]}/${match[3]}/${match[4]}`;
}

function isValidManifestUrl(value) {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !url.pathname.includes("https://");
  } catch {
    return false;
  }
}

async function fetchManifest(profileId) {
  const profile = await getProfile(profileId);
  if (!profile.manifestUrl) throw new Error("Set a public GitHub raw manifest URL first.");
  const manifestUrl = withCacheBust(profile.manifestUrl, Date.now());
  const manifest = await fetchJson(manifestUrl);
  validateManifest(manifest);
  const base = new URL(profile.manifestUrl);
  const files = [];
  for (const item of manifest.lorebooks || manifest.files || []) {
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
  const characters = [];
  for (const item of manifest.characters || []) {
    const fields = {};
    for (const [fieldName, source] of Object.entries(item.fields || {})) {
      if (source && typeof source === "object" && "text" in source) {
        fields[fieldName] = String(source.text || "");
        continue;
      }
      if (typeof source === "string" && !isFieldPath(source)) {
        fields[fieldName] = source;
        continue;
      }
      const path = typeof source === "string" ? source : source?.path || source?.url;
      if (!path) continue;
      const rawFieldUrl = path.startsWith("http") ? path : new URL(path, base).toString();
      const fieldUrl = withCacheBust(rawFieldUrl, item.fieldHashes?.[fieldName] || manifest.generatedAt || Date.now());
      fields[fieldName] = await fetchText(fieldUrl);
    }
    characters.push({
      id: item.id || slugify(item.name || `character-${characters.length + 1}`),
      name: item.name || `Character ${characters.length + 1}`,
      group: item.group || "",
      productionNumber: item.productionNumber ?? null,
      plannedDate: item.plannedDate || "",
      editUrl: item.editUrl || item.sourceUrl || "",
      fields,
      changedFields: Array.isArray(item.changedFields) ? item.changedFields : [],
      fieldHashes: item.fieldHashes || {},
      validation: item.validation || { ok: true, errors: [], warnings: [] }
      ,avatarUrl: item.avatar ? (String(item.avatar).startsWith("http") ? item.avatar : new URL(item.avatar, base).toString()) : ""
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
    files,
    characters
  };
  await storeBundle(profile.id, bundle);
  return { ok: true, bundle: summarizeBundle(bundle) };
}

function withCacheBust(value, version) {
  const url = new URL(value);
  url.searchParams.set("_jm", String(version));
  return url.toString();
}

function isFieldPath(value) {
  const text = String(value || "").trim();
  return /^https:\/\//i.test(text) || /[\\/]/.test(text) || /\.(?:txt|md|html?|json)$/i.test(text);
}

async function storeBundle(profileId, bundle) {
  if (!bundle?.files?.length && !bundle?.characters?.length) throw new Error("Bundle has no lorebooks or characters.");
  const profile = await getProfile(profileId);
  bundle.files = bundle.files || [];
  bundle.characters = bundle.characters || [];
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
  const lorebooks = manifest.lorebooks || manifest.files || [];
  if (!Array.isArray(lorebooks) || !Array.isArray(manifest.characters || [])) throw new Error("Manifest collections must be arrays.");
  if (!lorebooks.length && !(manifest.characters || []).length) throw new Error("Manifest has no lorebooks or characters.");
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
    files: (bundle.files || []).map((file) => ({
      name: file.name,
      filename: file.filename,
      bytes: file.bytes,
      entries: file.entries,
      sha256: file.sha256,
      validation: file.validation
    })),
    characters: (bundle.characters || []).map((character) => ({
      id: character.id,
      name: character.name,
      group: character.group,
      editUrl: character.editUrl || "",
      fieldCount: Object.keys(character.fields || {}).length,
      changedFieldCount: (character.changedFields || []).length,
      validation: character.validation || { ok: true }
    }))
  };
}

function slugify(text) {
  return String(text || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "character";
}

async function sha256(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

function byteLength(text) {
  return new TextEncoder().encode(text).length;
}
