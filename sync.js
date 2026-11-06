// Device sync: keeps flashcard marks and lesson progress the same across a user's devices.
// The apps keep saving to localStorage as before. This file compares that saved data with its own list of
// items, gives each change a time, and swaps the list with the server (scripts/sync-worker.js). The latest
// change to an item wins. scripts/build-lessons.js copies this file into each lesson, so lessons stay one file.
(function () {
  // Set SYNC_URL to the deployed Worker's address. While it is empty, sync stays hidden and does nothing.
  const SYNC_URL = "https://natrium-sync.natriumfundamentals.workers.dev";
  const BASE = /^(localhost|127\.0\.0\.1)$/.test(location.hostname) ? "http://localhost:8787" : SYNC_URL;
  const KEY = "natrium-sync", MARKS = "natrium-flashcards-marks", LESSONS = "natrium-lessons-progress";
  const LETTERS = "0123456789ABCDEFGHJKMNPQRSTVWXYZ", WAIT = 60000, KEEPALIVE_LIMIT = 60000;
  let timer = null, busy = false, again = false, note = "";

  const json = key => { try { return JSON.parse(localStorage.getItem(key)) || {}; } catch (e) { return {}; } };
  const load = () => { const s = json(KEY); return s.code ? s : null; };
  const store = s => { try { localStorage.setItem(KEY, JSON.stringify(s)); return true; } catch (e) { return false; } };
  const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  // Same rule as newer() in scripts/sync-worker.js
  const newer = (a, b) => !b || a[1] > b[1] || (a[1] === b[1] && JSON.stringify(a[0]) > JSON.stringify(b[0]));

  // What the apps have saved, as flat items: c/<card ID> 1 known, 2 missed; d/<slug> date; p/<slug> last page
  function saved() {
    const out = {}, marks = json(MARKS);
    const add = (ids, bit) => (Array.isArray(ids) ? ids : []).forEach(id => { out["c/" + id] = (out["c/" + id] || 0) | bit; });
    add(marks.known, 1);
    add(marks.missed, 2);
    for (const [slug, p] of Object.entries(json(LESSONS))) {
      if (p && p.done) out["d/" + slug] = p.done;
      if (p && p.page) out["p/" + slug] = [p.page, p.n, p.total];
    }
    return out;
  }

  // Record anything that changed since the last look. An item that has gone becomes 0, so its removal syncs too.
  function stamp(s, time) {
    const now = saved();
    for (const [key, value] of Object.entries(now)) {
      if (!s.items[key] || !same(s.items[key][0], value)) s.items[key] = [value, time];
    }
    for (const key of Object.keys(s.items)) {
      if (!(key in now) && s.items[key][0] !== 0) s.items[key] = [0, time];
    }
  }

  // Write the merged items back where the apps read them
  function apply(items) {
    const marks = { known: [], missed: [] }, lessons = {};
    for (const [key, [value]] of Object.entries(items)) {
      if (!value) continue;
      const id = key.slice(2), lesson = () => (lessons[id] = lessons[id] || {});
      if (key[0] === "c") {
        if (value & 1) marks.known.push(id);
        if (value & 2) marks.missed.push(id);
      } else if (key[0] === "d") lesson().done = value;
      else Object.assign(lesson(), { page: value[0], n: value[1], total: value[2] });
    }
    try {
      localStorage.setItem(MARKS, JSON.stringify(marks));
      localStorage.setItem(LESSONS, JSON.stringify(lessons));
    } catch (e) {}
  }

  function show(text) {
    note = text;
    document.querySelectorAll(".sync-status").forEach(el => { el.textContent = statusText(); });
  }
  function statusText() {
    const s = load();
    if (note) return note;
    return s && s.at ? "Last synced " + new Date(s.at).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) : "Not synced yet";
  }

  async function sync(leaving) {
    const s = load();
    if (!s || !BASE) return;
    if (busy) { again = true; return; }
    busy = true;
    clearTimeout(timer);
    timer = null;
    stamp(s, Date.now());
    store(s);
    try {
      const body = JSON.stringify({ items: s.items });
      const res = await fetch(BASE + "/sync/" + s.code, { method: "POST", body, keepalive: !!leaving && body.length < KEEPALIVE_LIMIT });
      if (!res.ok) throw new Error("sync " + res.status);
      const { items } = await res.json();
      const fresh = load();
      if (fresh && fresh.code === s.code) {
        stamp(fresh, Date.now());
        let got = false;
        for (const [key, item] of Object.entries(items)) {
          if (newer(item, fresh.items[key])) { fresh.items[key] = item; got = true; }
        }
        fresh.at = Date.now();
        store(fresh);
        if (got) {
          apply(fresh.items);
          dispatchEvent(new Event("natrium-sync"));
        }
      }
      show("");
    } catch (e) {
      show("Waiting for a connection. Progress is saved on this device.");
    }
    busy = false;
    if (again) { again = false; sync(); }
  }

  // The apps call this after saving. The change gets its time now, and waiting keeps a run of cards to one upload.
  function changed() {
    const s = BASE && load();
    if (!s) return;
    stamp(s, Date.now());
    store(s);
    if (!timer) timer = setTimeout(sync, WAIT);
  }

  function newCode() {
    return [...crypto.getRandomValues(new Uint8Array(16))].map(b => LETTERS[b % 32]).join("");
  }
  // Typed codes may have spaces, dashes, lower case, or letters that look like digits
  const clean = text => text.toUpperCase().replace(/[^0-9A-Z]/g, "").replace(/O/g, "0").replace(/[IL]/g, "1");
  const pretty = code => code.match(/.{4}/g).join("-");

  // Items already on a device get the earliest time, so a device joining late never overrides newer progress.
  function begin(code) {
    const s = { code, items: {} };
    stamp(s, 1);
    if (!store(s)) return false;
    note = "";
    sync();
    return true;
  }

  async function join(code, say) {
    if (!/^[0-9A-HJKMNP-TV-Z]{16}$/.test(code)) return say("A sync code has 16 letters and digits. Check it and try again.");
    say("Checking the code...");
    try {
      const res = await fetch(BASE + "/sync/" + code);
      if (res.status === 404) return say("That code was not found. Check it, or try again in a minute.");
      if (!res.ok) throw new Error("check " + res.status);
    } catch (e) { return say("Could not reach the sync service. Try again when you are online."); }
    if (!begin(code)) return say("This browser is not allowing saved data, so sync cannot start.");
    return true;
  }

  const CSS = `
.sync { border: 1px solid var(--line); border-radius: 10px; background: var(--card); padding: 12px 14px; text-align: left; font-size: 0.9rem; }
.sync summary { cursor: pointer; font-weight: 600; color: var(--fg); }
.sync p { margin: 10px 0 0; color: var(--muted); }
.sync .sync-code { display: block; margin-top: 10px; color: var(--fg); font: 600 1.05rem/1.4 ui-monospace, Menlo, Consolas, monospace; user-select: all; overflow-wrap: anywhere; }
.sync .sync-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.sync input { flex: 1 1 180px; min-width: 0; font: inherit; font-size: 16px; padding: 8px 10px; border-radius: 8px; border: 1px solid var(--line); background: var(--bg); color: var(--fg); }
.sync button { font: inherit; font-weight: 600; padding: 8px 12px; border-radius: 8px; border: 1px solid var(--accent); background: transparent; color: var(--accent); cursor: pointer; }
.sync button.main { background: var(--accent); color: var(--bg); }
.sync :is(button, input, summary):focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
`;

  // The settings box. Each installed app has its own copy, because a phone may keep its data apart.
  function panel(root) {
    if (!root || !BASE) return;
    if (!document.getElementById("sync-css")) {
      const style = document.createElement("style");
      style.id = "sync-css";
      style.textContent = CSS;
      document.head.append(style);
    }
    const draw = open => {
      const s = load();
      root.innerHTML = `<details class="sync"${open ? " open" : ""}><summary>Sync across devices: ${s ? "on" : "off"}</summary>` + (s ? `
<p>Enter this code on your other devices. On a phone, each app added to the home screen may need it too.</p>
<span class="sync-code">${pretty(s.code)}</span>
<div class="sync-row"><button class="main" data-do="now">Sync now</button><button data-do="copy">Copy code</button></div>
<p class="sync-status" role="status"></p>
<p>Anyone with this code can see and change this progress. A lost code cannot be recovered, so keep it somewhere safe. Clearing marks here also clears them on your other devices.</p>
<div class="sync-row"><button data-do="off">Turn off on this device</button></div>` : `
<p>Keep flashcard marks and lesson progress the same on all your devices. Progress is stored online under a private code, with no name or email.</p>
<div class="sync-row"><button class="main" data-do="start">Get a sync code</button></div>
<p>Already have a code from another device?</p>
<div class="sync-row"><input aria-label="Sync code" placeholder="XXXX-XXXX-XXXX-XXXX" autocapitalize="characters" autocomplete="off" spellcheck="false"><button data-do="join">Use code</button></div>
<p class="sync-say" role="status"></p>`) + "</details>";
      const status = root.querySelector(".sync-status");
      if (status) status.textContent = statusText();
    };
    root.addEventListener("click", async e => {
      const action = e.target.dataset && e.target.dataset.do;
      if (!action) return;
      const say = text => { const el = root.querySelector(".sync-say"); if (el) el.textContent = text; };
      if (action === "start") {
        if (begin(newCode())) draw(true);
        else say("This browser is not allowing saved data, so sync cannot start.");
      } else if (action === "join") {
        if (await join(clean(root.querySelector("input").value), say) === true) draw(true);
      } else if (action === "now") {
        show("Syncing...");
        sync();
      } else if (action === "copy") {
        try { await navigator.clipboard.writeText(pretty(load().code)); e.target.textContent = "Copied"; }
        catch (err) { e.target.textContent = "Select the code above to copy it"; }
      } else if (action === "off") {
        try { localStorage.removeItem(KEY); } catch (err) {}
        note = "";
        draw(true);
      }
    });
    draw(false);
  }

  window.Sync = { changed, panel, now: sync };
  if (!BASE) return;
  sync();
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") { if (timer) sync(true); }
    else sync();
  });
  addEventListener("pagehide", () => { if (timer) sync(true); });
  addEventListener("online", () => sync());
})();
