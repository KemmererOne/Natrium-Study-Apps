// Tests sync.js against scripts/sync-worker.js, with two pretend devices and a memory store.
// Run with: node scripts/test-sync.js
const fs = require("fs"), path = require("path"), vm = require("vm"), assert = require("assert");

const MARKS = "natrium-flashcards-marks", LESSONS = "natrium-lessons-progress", KEY = "natrium-sync";
const ORIGIN = "http://localhost:8100", CODE = "ABCD2345EFGH6789";
const pause = () => new Promise(r => setTimeout(r, 5));

(async () => {
  const { default: worker } = await import("./sync-worker.js");
  const data = new Map();
  const env = { ORIGINS: ORIGIN, SYNC: { get: async k => (data.has(k) ? data.get(k) : null), put: async (k, v) => { data.set(k, v); } } };
  const call = (url, init = {}) => worker.fetch(new Request(url, { ...init, headers: { Origin: ORIGIN, ...init.headers } }), env);

  function device() {
    const store = new Map(), events = [];
    const localStorage = {
      getItem: k => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: k => store.delete(k)
    };
    const window = {};
    const box = {
      window, localStorage, location: { hostname: "localhost" }, fetch: call, setTimeout, clearTimeout, console, crypto,
      document: { addEventListener() {}, querySelectorAll: () => [], visibilityState: "visible" },
      addEventListener() {}, dispatchEvent: e => events.push(e.type), Event: class { constructor(type) { this.type = type; } }
    };
    vm.runInNewContext(fs.readFileSync(path.join(__dirname, "..", "sync.js"), "utf8"), box);
    return {
      events, sync: () => window.Sync.now(),
      edit: (key, value) => { localStorage.setItem(key, JSON.stringify(value)); window.Sync.changed(); },
      set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
      get: key => JSON.parse(localStorage.getItem(key) || "{}"),
      join: async items => { localStorage.setItem(KEY, JSON.stringify({ code: CODE, items })); await window.Sync.now(); }
    };
  }

  const a = device(), b = device();
  const sorted = list => [...list].sort();
  let passed = 0;
  const check = (name, fn) => { fn(); passed++; console.log("ok  " + name); };

  // A device's existing progress is stamped the earliest time by begin(); the join helper mirrors that
  a.set(MARKS, { known: ["C1", "C2"], missed: ["C3"] });
  a.set(LESSONS, { "psar-sy-01": { page: "p3", n: 3, total: 9, done: "2026-11-01" } });
  await a.join({ "c/C1": [1, 1], "c/C2": [1, 1], "c/C3": [2, 1], "d/psar-sy-01": ["2026-11-01", 1], "p/psar-sy-01": [["p3", 3, 9], 1] });
  b.set(MARKS, { known: ["C9"], missed: [] });
  await b.join({ "c/C9": [1, 1] });
  check("a second device gets the first device's progress and keeps its own", () => {
    assert.deepStrictEqual(sorted(b.get(MARKS).known), ["C1", "C2", "C9"]);
    assert.deepStrictEqual(b.get(MARKS).missed, ["C3"]);
    assert.strictEqual(b.get(LESSONS)["psar-sy-01"].done, "2026-11-01");
    assert.strictEqual(b.get(LESSONS)["psar-sy-01"].n, 3);
    assert.deepStrictEqual(b.events, ["natrium-sync"]);
  });

  await a.sync();
  check("the first device picks up the second device's card", () => assert.deepStrictEqual(sorted(a.get(MARKS).known), ["C1", "C2", "C9"]));

  await pause();
  b.set(MARKS, { known: ["C1", "C9"], missed: ["C3"] });
  await b.sync(); await a.sync();
  check("removing a mark reaches the other device", () => assert.deepStrictEqual(sorted(a.get(MARKS).known), ["C1", "C9"]));

  await pause();
  b.edit(MARKS, { known: ["C1", "C5", "C9"], missed: ["C3"] });
  await pause();
  a.edit(MARKS, { known: ["C1", "C9"], missed: ["C3", "C5"] });
  await pause();
  await a.sync(); await pause(); await b.sync(); await a.sync();
  check("when both devices change a card, the later edit wins on both, whichever syncs last", () => {
    for (const d of [a, b]) {
      assert.ok(d.get(MARKS).missed.includes("C5"));
      assert.ok(!d.get(MARKS).known.includes("C5"));
    }
  });

  await pause();
  const lessons = a.get(LESSONS);
  delete lessons["psar-sy-01"].done;
  a.set(LESSONS, lessons);
  await a.sync(); await b.sync();
  check("undoing a completed lesson reaches the other device and keeps its page", () => {
    assert.strictEqual(b.get(LESSONS)["psar-sy-01"].done, undefined);
    assert.strictEqual(b.get(LESSONS)["psar-sy-01"].page, "p3");
  });

  await pause();
  const first = a.get(LESSONS);
  first["psar-sy-01.concept-1"] = { done: "2026-11-06" };
  a.edit(LESSONS, first);
  const second = b.get(LESSONS);
  second["psar-sy-01.concept-2"] = { done: "2026-11-06" };
  b.edit(LESSONS, second);
  await a.sync(); await b.sync(); await a.sync();
  check("pages finished on two devices all reach both, and the last page stays", () => {
    for (const d of [a, b]) {
      assert.deepStrictEqual(d.get(LESSONS)["psar-sy-01.concept-1"], { done: "2026-11-06" });
      assert.deepStrictEqual(d.get(LESSONS)["psar-sy-01.concept-2"], { done: "2026-11-06" });
      assert.strictEqual(d.get(LESSONS)["psar-sy-01"].page, "p3");
    }
  });

  const before = data.get(CODE);
  await a.sync();
  check("a sync with no changes writes nothing", () => assert.strictEqual(data.get(CODE), before));

  const url = "http://x/sync/" + CODE, post = body => ({ method: "POST", body });
  const status = async (u, init) => (await call(u, init)).status;
  assert.strictEqual(await status(url), 204);
  assert.strictEqual(await status("http://x/sync/ZZZZ2345EFGH6789"), 404);
  assert.strictEqual(await status("http://x/sync/too-short"), 404);
  assert.strictEqual(await status(url, post("not json")), 400);
  assert.strictEqual(await status(url, post("x".repeat(400001))), 413);
  assert.strictEqual(await status(url, { method: "PUT", body: "{}" }), 405);
  assert.strictEqual(await status(url, { headers: { Origin: "https://example.com" } }), 403);
  await call(url, post(JSON.stringify({ items: { "x/C1": [1, 9], "c/C8": [9, 9], "d/s": ["<b>", 9], "c/C7": [1, -1] } })));
  check("the server answers bad requests correctly and drops bad items", () => {
    const stored = JSON.parse(data.get(CODE));
    for (const key of ["x/C1", "c/C8", "d/s", "c/C7"]) assert.ok(!(key in stored));
  });

  console.log(passed + " checks passed");
  process.exit(0);
})().catch(e => { console.error(e); process.exit(1); });
