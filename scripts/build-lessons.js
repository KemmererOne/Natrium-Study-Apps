#!/usr/bin/env node
// Builds the lesson topics from work/manifest.json and work/topics/*.json:
//   - adds new knowledge checks and key facts to quiz/questions.js and flashcards/cards.js
//   - writes topics/<slug>/index.html (one file, many pages, no outside files)
//   - writes lessons/index.html, the button on index.html, topics/sources.json and root sw.js
//   - runs reference/generate.js
// Run from anywhere:  node scripts/build-lessons.js
const fs = require("fs"), path = require("path"), vm = require("vm"), crypto = require("crypto"), cp = require("child_process");
const ROOT = path.join(__dirname, "..");
const at = f => path.join(ROOT, f);
const read = f => fs.readFileSync(at(f), "utf8");
const write = (f, s) => { fs.mkdirSync(path.dirname(at(f)), { recursive: true }); fs.writeFileSync(at(f), s); };
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const js = s => JSON.stringify(s);
const today = process.env.LESSON_DATE || new Date().toISOString().slice(0, 10);

const manifest = JSON.parse(read("work/manifest.json"));
const topics = fs.readdirSync(at("work/topics")).filter(f => f.endsWith(".json")).sort().map(f => JSON.parse(read("work/topics/" + f)));
const email = read("feedback.js").match(/FEEDBACK_EMAIL = "([^"]+)"/)[1];
const mailto = (subject, body) => "mailto:" + email + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);

function load() {
  const c = {};
  vm.createContext(c);
  vm.runInContext(read("quiz/questions.js").replace(/\bconst QS\b/, "var QS"), c);
  vm.runInContext(read("flashcards/cards.js").replace(/\bconst CARDS\b/, "var CARDS").replace(/\bconst TOPIC_GROUPS\b/, "var TOPIC_GROUPS"), c);
  return c;
}
const srcOf = (t, p) => {
  const w = p.cite.match(/^Word: (.+\.docx), (.+)$/);
  if (w) return `${manifest.word_files.find(f => f.file === w[1]).source_id} (${w[1]}), ${w[2]}`;
  const n = p.cite.match(/^NRC slides (\S+), slide (\d+)$/);
  if (n) return `${n[1]} (${n[1]}.pdf), slide ${n[2]}`;
  if (p.cite.startsWith("PSAR")) return p.cite;
  const [, mod, page] = p.cite.match(/ ([A-Z]{2}-\d\d) p\.(\S+)$/);
  return `${t.source_id} (${t.handbook}), ${p.sec}, ${mod} p. ${page}`;
};

// 1. Export. An item whose question text is already in the file is not added again.
function exportItems() {
  const c = load();
  const hasQ = new Set(c.QS.map(q => q.q)), hasC = new Set(c.CARDS.map(x => x[1]));
  let nextQ = Math.max(...c.QS.map(q => +q.id.slice(1))) + 1, nextC = Math.max(...c.CARDS.map(x => +x[6].slice(1))) + 1;
  const qLines = [], cLines = [], log = [];
  for (const t of topics) {
    const passage = id => t.passages.find(p => p.id === id);
    for (const con of t.concepts) for (const k of con.checks) {
      if (k.existing || hasQ.has(k.q)) continue;
      const p = passage(k.p), id = "Q" + nextQ++, src = srcOf(t, p);
      hasQ.add(k.q);
      const [qt, qtopic] = k.place || [t.quiz_t, t.quiz_topic];
      qLines.push(`  { id: ${js(id)}, t: ${js(qt)}, topic: ${js(qtopic)}, q: ${js(k.q)},\n    o: ${js(k.o)}, a: ${k.a},\n    x: ${js(k.x)},\n    src: ${js(src)} },`);
      log.push(`- **${id}** (${qtopic}): ${k.q}\n  - Source: ${src}\n  - Quote: "${p.quote}"`);
    }
    for (const f of t.facts) {
      if (hasC.has(f.q)) continue;
      const p = passage(f.p), id = "C" + nextC++, src = srcOf(t, p);
      hasC.add(f.q);
      const ctopic = f.place ? f.place[1] : t.quiz_topic;
      cLines.push(`  [${js(ctopic)}, ${js(f.q)}, ${js(f.a)}, ${js(src)}, null, null, ${js(id)}],`);
      log.push(`- **${id}** (${ctopic}): ${f.q}\n  - Source: ${src}\n  - Quote: "${p.quote}"`);
    }
  }
  const append = (f, lines) => {
    if (!lines.length) return;
    const s = read(f), end = s.lastIndexOf("];");
    write(f, s.slice(0, end) + lines.join("\n") + "\n" + s.slice(end));
  };
  append("quiz/questions.js", qLines);
  append("flashcards/cards.js", cLines);
  const bump = f => write(f, read(f).replace(/VERSION = "v(\d+)"/, (m, n) => `VERSION = "v${+n + 1}"`));
  if (qLines.length) bump("quiz/sw.js");
  if (cLines.length) bump("flashcards/sw.js");
  if (log.length) {
    const head = `\n## ${today}: Lesson topics (knowledge checks and key facts)\n\nAdded ${qLines.length} quiz questions and ${cLines.length} flashcards from the lesson topics. Every quote passed scripts/verify-quotes.py. Calculation questions use new numbers with the method the quote supports.\n\n`;
    write("CHANGELOG.md", read("CHANGELOG.md").trimEnd() + "\n" + head + log.join("\n") + "\n");
  }
  console.log(`Exported ${qLines.length} questions, ${cLines.length} cards`);
}
exportItems();
const items = load();
const qByText = new Map(items.QS.map(q => [q.q, q])), qById = new Map(items.QS.map(q => [q.id, q]));
const cByText = new Map(items.CARDS.map(x => [x[1], x]));

// 2. Pages
const CSS = `
:root { --bg: #f4f4f1; --card: #ffffff; --fg: #1c2230; --muted: #5a6376; --line: #d6d9e0; --accent: #8a5f00; --good: #1f6f43; --bad: #a33a2c; color-scheme: light; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4; --line: #2c3645; --accent: #f2c14e; --good: #6fcf97; --bad: #f08a7b; color-scheme: dark; }
}
:root[data-theme="dark"] { --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4; --line: #2c3645; --accent: #f2c14e; --good: #6fcf97; --bad: #f08a7b; color-scheme: dark; }
* { box-sizing: border-box; }
html, body { min-height: 100%; }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-size: 16px; line-height: 1.55;
  padding: 16px max(16px, env(safe-area-inset-right, 0px)) calc(48px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); }
.wrap { max-width: 640px; margin: 0 auto; min-width: 0; }
.js .page { display: none; } .js .page.on { display: block; }
.page { margin-bottom: 40px; min-width: 0; } .js .page { margin-bottom: 0; }
a { color: var(--accent); font-weight: 600; }
a:focus-visible, button:focus-visible, summary:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.top { display: flex; justify-content: space-between; align-items: center; gap: 12px; font-size: 0.9rem; }
.home { text-decoration: none; padding: 8px 0; display: inline-block; } .plans { margin-left: 12px; }
.count { color: var(--muted); font-size: 0.85rem; }
h1, h2 { font-family: Georgia, "Times New Roman", serif; font-weight: 600; line-height: 1.25; }
h1 { font-size: 1.6rem; margin: 8px 0 6px; } h2 { font-size: 1.3rem; margin: 8px 0 12px; }
h3 { font-size: 1rem; margin: 16px 0 6px; }
p { margin: 0 0 12px; } ul, ol { margin: 0 0 12px; padding-left: 22px; } li { margin-bottom: 4px; }
.tags { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 12px; padding: 0; list-style: none; }
.tag { border: 1px solid var(--accent); color: var(--accent); border-radius: 999px; padding: 1px 10px; font-size: 0.78rem; font-weight: 600; margin: 0; }
cite { display: inline; font-style: normal; font-size: 0.74rem; color: var(--muted); overflow-wrap: anywhere; white-space: normal; }
cite::before { content: "["; } cite::after { content: "]"; }
blockquote { margin: 0 0 12px; padding: 8px 12px; border-left: 3px solid var(--accent); background: var(--card); border-radius: 0 8px 8px 0; }
.eq { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 8px 12px; margin: 0 0 12px; overflow-wrap: anywhere; }
.eq b { font-family: ui-monospace, Menlo, monospace; font-weight: 600; font-size: 0.95rem; }
.fig { margin: 0 0 14px; background: #fff; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.fig img { display: block; width: 100%; height: auto; max-height: 70vh; object-fit: contain; }
.fig figcaption { background: var(--card); color: var(--fg); font-size: 0.85rem; padding: 6px 10px; border-top: 1px solid var(--line); }
.menu { margin: 8px 0 14px; font-size: 0.9rem; } .menu summary { cursor: pointer; color: var(--accent); font-weight: 600; padding: 6px 0; }
.menu ol { margin-top: 6px; }
.letters { list-style: none; padding-left: 1.25em; }
.obj { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; margin-bottom: 12px; }
.num { font-weight: 700; font-variant-numeric: tabular-nums; }
.check, .ex { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; margin-bottom: 14px; min-width: 0; }
.meta { display: flex; justify-content: space-between; gap: 10px; color: var(--muted); font-size: 0.8rem; margin-bottom: 6px; }
.opts { display: flex; flex-direction: column; gap: 8px; margin: 10px 0; }
.opt { text-align: left; font: inherit; color: var(--fg); background: var(--bg); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-height: 44px; cursor: pointer; overflow-wrap: anywhere; }
.opt[aria-disabled="true"] { cursor: default; } .opt.right { border-color: var(--good); color: var(--good); font-weight: 600; } .opt.wrong { border-color: var(--bad); color: var(--bad); }
.result { margin: 0; } .result[hidden] { display: none; }
.verdict { font-weight: 700; margin-bottom: 4px; } .verdict.right { color: var(--good); } .verdict.wrong { color: var(--bad); }
.report { font-size: 0.85rem; }
.answer { font-weight: 600; margin-bottom: 8px; }
.pager { display: flex; justify-content: space-between; gap: 12px; border-top: 1px solid var(--line); margin-top: 20px; padding-top: 12px; }
.pager a { text-decoration: none; padding: 8px 0; max-width: 48%; } .pager .next { text-align: right; margin-left: auto; }
.finish { margin: 20px 0 0; }
.mark { width: 100%; min-height: 44px; font: inherit; font-weight: 600; color: var(--bg); background: var(--accent); border: 1px solid var(--accent); border-radius: 8px; padding: 10px 12px; cursor: pointer; }
.mark.is-done { color: var(--good); background: transparent; border-color: var(--good); }
.mark-note { color: var(--bad); font-size: 0.85rem; margin: 6px 0 0; } .mark-note[hidden] { display: none; }
.menu a.is-done::after, .side a.is-done::after, .page.is-done > .top .count::after { content: " ✓"; content: " ✓" / "Completed"; color: var(--good); font-weight: 700; }
.moved { background: var(--card); border: 1px solid var(--accent); border-radius: 8px; padding: 8px 12px; margin: 8px 0 0; font-size: 0.9rem; } .moved[hidden] { display: none; }
.side { display: none; }
/* Wide screens get the page list beside the lesson. Phones keep the single column. */
@media (min-width: 900px) {
  .wrap { max-width: 1120px; display: grid; grid-template-columns: 280px minmax(0, 1fr); column-gap: 36px; align-items: start; }
  .pages { min-width: 0; max-width: 760px; }
  .menu { display: none; }
  .side { display: block; position: sticky; top: 16px; max-height: calc(100vh - 32px); overflow-y: auto; font-size: 0.88rem; padding-right: 4px; }
  .side h2 { font-size: 1rem; margin: 8px 0; }
  .side ol { list-style: none; padding: 0; margin: 0 0 12px; } .side li { margin: 0; }
  .side a { display: block; padding: 5px 8px; border-left: 3px solid transparent; color: var(--fg); font-weight: 400; text-decoration: none; }
  .side a:hover { color: var(--accent); }
  .side a.on { border-left-color: var(--accent); background: var(--card); color: var(--accent); font-weight: 600; }
  .side .finish { margin: 0; }
}
`;
const SYNC_LIB = read("sync.js");
const SCRIPT = `
document.documentElement.classList.add("js");
const pages = [...document.querySelectorAll(".page")];
// Progress is saved on this device, and sync.js copies it to the user's other devices if sync is on.
// It is stored by lesson slug, as one record for all lessons. A completed page is its own entry, "<slug>.<page id>",
// with the same done date as a lesson, so sync.js merges pages one at a time.
const KEY = "natrium-lessons-progress", slug = document.querySelector("main").dataset.slug;
const moved = document.createElement("p"), movedLink = document.createElement("a");
moved.className = "moved"; moved.hidden = true; moved.append(movedLink);
document.querySelector(".pages").prepend(moved);
function loadAll() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
function saveAll(all) { try { localStorage.setItem(KEY, JSON.stringify(all)); Sync.changed(); return true; } catch (e) { return false; } }
function today() {
  const d = new Date();
  return [d.getFullYear(), String(d.getMonth() + 1).padStart(2, "0"), String(d.getDate()).padStart(2, "0")].join("-");
}
// A lesson marked complete shows every page checked. Undoing it brings back the pages actually finished.
function showChecks() {
  const all = loadAll(), lessonDone = !!(all[slug] || {}).done;
  const finished = id => lessonDone || !!all[slug + "." + id];
  pages.forEach(p => p.classList.toggle("is-done", finished(p.id)));
  document.querySelectorAll(".menu a, .side a").forEach(a => a.classList.toggle("is-done", finished(a.getAttribute("href").slice(1))));
}
// A page is finished by moving on with Next. A page of checks needs every check answered first.
function finishPage(page) {
  const all = loadAll(), key = slug + "." + page.id;
  if (all[key] || page.querySelector(".check:not([data-done])")) return;
  all[key] = { done: today() };
  saveAll(all);
  showChecks();
}
// When another device has moved on while this lesson sat open, offer that page without jumping to it
function offerMove() {
  const p = loadAll()[slug] || {}, there = !p.done && pages.find(x => x.id === p.page);
  moved.hidden = !there || there.classList.contains("on");
  if (moved.hidden) return;
  movedLink.href = "#" + there.id;
  movedLink.textContent = "Continue on page " + (pages.indexOf(there) + 1) + " of " + pages.length + ", where you left off on another device";
}
function show() {
  const id = location.hash.slice(1), page = pages.find(p => p.id === id) || pages[0];
  pages.forEach(p => p.classList.toggle("on", p === page));
  document.querySelectorAll(".side a").forEach(a => {
    const on = a.getAttribute("href") === "#" + page.id;
    a.classList.toggle("on", on);
    if (on) { a.setAttribute("aria-current", "page"); a.scrollIntoView({ block: "nearest" }); } else a.removeAttribute("aria-current");
  });
  const all = loadAll();
  all[slug] = Object.assign({}, all[slug], { page: page.id, n: pages.indexOf(page) + 1, total: pages.length });
  saveAll(all);
  if (page === pages[pages.length - 1]) finishPage(page);
  showChecks();
  moved.hidden = true;
  window.scrollTo(0, 0);
}
// A link with no page named picks up at the last page, unless the lesson is complete
const last = loadAll()[slug] || {};
if (!location.hash && !last.done && pages.some(p => p.id === last.page)) history.replaceState(null, "", "#" + last.page);
addEventListener("hashchange", show); show();
document.querySelectorAll(".pager .next").forEach(a => a.addEventListener("click", () => finishPage(a.closest(".page"))));
function showMark(failed) {
  const done = !!(loadAll()[slug] || {}).done;
  document.querySelectorAll(".mark").forEach(b => {
    b.textContent = done ? "Completed. Select to undo" : "Mark lesson complete";
    b.classList.toggle("is-done", done);
    b.setAttribute("aria-pressed", done);
  });
  document.querySelectorAll(".mark-note").forEach(n => { n.hidden = !failed; });
}
document.querySelectorAll(".mark").forEach(b => b.addEventListener("click", () => {
  const all = loadAll(), p = Object.assign({}, all[slug]);
  if (p.done) delete p.done;
  else p.done = today();
  all[slug] = p;
  showMark(!saveAll(all));
  showChecks();
}));
showMark(false);
addEventListener("natrium-sync", () => { showMark(false); showChecks(); offerMove(); });
addEventListener("keydown", e => {
  if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
  if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
  const links = [...document.querySelectorAll(".page.on .pager a")];
  const a = links.find(l => l.classList.contains("next") === (e.key === "ArrowRight"));
  if (a) a.click();
});
document.querySelectorAll(".check").forEach(c => {
  const opts = [...c.querySelectorAll(".opt")], key = +c.dataset.a, result = c.querySelector(".result"), verdict = c.querySelector(".verdict");
  opts.forEach((b, i) => b.addEventListener("click", () => {
    if (c.dataset.done) return;
    c.dataset.done = "1";
    opts.forEach((o, j) => { o.setAttribute("aria-disabled", "true"); if (j === key) o.classList.add("right"); });
    if (i !== key) b.classList.add("wrong");
    verdict.textContent = i === key ? "Correct" : "Not correct";
    verdict.classList.add(i === key ? "right" : "wrong");
    result.hidden = false;
    finishPage(c.closest(".page"));
  }));
});
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) navigator.serviceWorker.register("../../sw.js").catch(() => {});
`;
const cite = c => `<cite>${esc(c)}</cite>`;
const LETTERS = "ABCD";

function checkHtml(t, k) {
  const q = k.existing ? qById.get(k.existing) : qByText.get(k.q);
  if (!q) throw new Error("No quiz item for check: " + (k.existing || k.q));
  const p = t.passages.find(x => x.id === k.p), c = p ? p.cite : q.src;
  return `<div class="check" data-a="${q.a}">
  <div class="meta"><span>${/^\d/.test(k.eo) ? "Objective " : ""}${esc(k.eo)}</span><span>${esc(q.id)}</span></div>
  <p>${esc(q.q)}</p>
  <div class="opts">${q.o.map((o, i) => `<button type="button" class="opt">${LETTERS[i]}. ${esc(o)}</button>`).join("")}</div>
  <div class="result" hidden>
    <p class="verdict"></p>
    <p>The answer is ${LETTERS[q.a]}. ${esc(q.x)} ${cite(c)}</p>
    <a class="report" href="${esc(mailto("Problem with " + q.id, `Item: ${q.id}\nTopic: ${q.topic}\nQuestion: ${q.q.slice(0, 160)}\nSource: ${q.src}\n\nWhat looks wrong:\n`))}">Report a problem</a>
  </div>
</div>`;
}
// Figures are embedded so each lesson stays one file and works offline
function figure(f) {
  const data = fs.readFileSync(at(`work/figs/${f.id}.png`)).toString("base64");
  return `<figure class="fig"><img src="data:image/png;base64,${data}" alt="${esc(f.alt)}"><figcaption>Figure ${esc(f.num)}. ${esc(f.cap)} ${cite(f.cite)}</figcaption></figure>`;
}
function block(t, b) {
  if (b.t === "quote") {
    const p = t.passages.find(x => x.id === b.p);
    return `<blockquote>"${esc(p.quote)}" ${cite(p.cite)}</blockquote>`;
  }
  if (b.t === "p") return `<p>${esc(b.text)} ${cite(b.cite)}</p>`;
  if (b.t === "eq") return `<p class="eq"><b>${esc(b.text)}</b> ${cite(b.cite)}</p>`;
  if (b.t === "fig") return figure(b);
  if (b.t === "list") return `<ul>${b.items.map(i => `<li>${esc(i)}</li>`).join("")}</ul><p>${cite(b.cite)}</p>`;
  throw new Error("Unknown block " + b.t);
}
const PSAR_FILE = "ML25276A288.pdf";
const objCite = t => o => o.cite || `${t.handbook} ${t.module_id} p.${o.page.printed}`;
function objectives(t, mod) {
  const c = objCite(t);
  const one = o => `${o.items.length ? `<p><span class="num">${esc(o.number)}</span> ${esc(o.text)} ${cite(c(o))}</p><ul class="letters">${o.items.map(i => `<li>${esc(i)}</li>`).join("")}</ul>` : `<p><span class="num">${esc(o.number)}</span> ${esc(o.text)} ${cite(c(o))}</p>`}`;
  return t.objectives.map(x => `<div class="obj"><h3>Terminal objective</h3>${one(x)}${x.enabling.length ? `<h3>Enabling objectives</h3>${x.enabling.map(one).join("")}` : ""}</div>`).join("");
}
function references(t) {
  const m = manifest.modules.find(x => x.module_id === t.module_id);
  const seen = new Set();
  const add = c => c && seen.add(c);
  t.passages.forEach(p => add(p.cite));
  t.concepts.forEach(c => c.body.forEach(b => add(b.cite)));
  t.examples.forEach(e => { add(e.cite); if (e.fig) add(e.fig.cite); });
  t.summary.forEach(s => add(s.cite));
  t.objectives.forEach(x => [x, ...x.enabling].forEach(o => add(objCite(t)(o))));
  const pages = [...seen].filter(c => !c.startsWith("Word:") && !c.startsWith("NRC slides") && !c.startsWith("PSAR")).map(c => c.match(/ p\.(\S+)$/)[1]);
  const words = new Map();
  for (const c of new Set([...seen, ...t.word_sequence.map(w => w.cite)])) {
    const n = c.match(/^NRC slides (\S+), slide (\d+)$/);
    if (n) {
      const f = n[1] + ".pdf";
      if (!words.has(f)) words.set(f, []);
      if (!words.get(f).some(x => x[0] === n[2])) words.get(f).push([n[2]]);
      continue;
    }
    const s = c.match(/^PSAR .*, p\. (\S+)$/);
    if (s) {
      if (!words.has(PSAR_FILE)) words.set(PSAR_FILE, []);
      if (!words.get(PSAR_FILE).some(x => x[0] === s[1])) words.get(PSAR_FILE).push([s[1]]);
      continue;
    }
    const w = c.match(/^Word: (.+\.docx), slide (\d+)\.(\d+)/);
    if (!w) continue;
    if (!words.has(w[1])) words.set(w[1], []);
    if (!words.get(w[1]).some(x => x[0] === w[2] && x[1] === w[3])) words.get(w[1]).push([w[2], w[3]]);
  }
  const wordRefs = [...words].map(([file, list]) => ({ file, slides: list.sort((a, b) => a[0].localeCompare(b[0], "en", { numeric: true }) || a[1] - b[1]).map(x => x.join(".")) }));
  const roman = p => /^[ivxl]+$/.test(p);
  const rv = { v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10, xi: 11, xii: 12, xiii: 13 };
  pages.sort((a, b) => roman(a) !== roman(b) ? (roman(a) ? -1 : 1) : roman(a) ? rv[a] - rv[b] : a - b);
  const quiz = [], cards = [];
  t.concepts.forEach(c => c.checks.forEach(k => quiz.push((k.existing ? qById.get(k.existing) : qByText.get(k.q)).id)));
  t.facts.forEach(f => cards.push(cByText.get(f.q)[6]));
  return { file: m.file, doc: t.handbook, module: t.module_id, pages, words: wordRefs, quiz, cards };
}
const built = [];
for (const t of topics) {
  const ref = references(t);
  built.push({ t, ref });
  const list = [{ id: "objectives", title: "Objectives" }];
  t.concepts.forEach((c, i) => {
    list.push({ id: "concept-" + (i + 1), title: c.title, c });
    if (c.checks.length) list.push({ id: "check-" + (i + 1), title: "Knowledge check: " + c.title, k: c });
  });
  if (t.examples.length) list.push({ id: "examples", title: "Worked examples" });
  list.push({ id: "summary", title: "Summary" }, { id: "references", title: "References" });
  const tagList = p => [t.status, ...t.scope_tags, ...((p.c || p.k || {}).tag ? [(p.c || p.k).tag] : [])].map(x => `<li class="tag">${esc(x)}</li>`).join("");
  const marked = list.filter(p => p.c && p.c.tag).map(p => p.title);
  const body = p => {
    if (p.id === "objectives") return `<p>${t.handbook ? `${esc(t.handbook)}, Module ${esc(String(+t.module_id.slice(3)))}.` : "Sodium system lesson, built from the lesson plan."}</p>${marked.length ? `<p>These pages are tagged Water-system only: ${esc(marked.join("; "))}. Other pages apply to the sodium and salt systems.</p>` : ""}${objectives(t)}`;
    if (p.c) return `<h2>${esc(p.title)}</h2><p class="count">${p.c.eo.length ? "Objectives " + esc(p.c.eo.join(", ")) : t.handbook ? "From the lesson plan" : "From the cited sources"}</p>${p.c.body.map(b => block(t, b)).join("\n")}`;
    if (p.k) return `<h2>${esc(p.title)}</h2>${p.k.checks.map(k => checkHtml(t, k)).join("\n")}`;
    if (p.id === "examples") return `<h2>Worked examples</h2>${t.examples.map(e => `<div class="ex"><div class="meta"><span>Objective ${esc(e.eo)}</span>${e.tag ? `<span class="tag">${esc(e.tag)}</span>` : ""}</div><h3>${esc(e.title)}</h3><p>${esc(e.problem)}</p>${e.fig ? figure(e.fig) : ""}<ol>${e.steps.map(s => `<li>${esc(s)}</li>`).join("")}</ol><p class="answer">Answer: ${esc(e.answer)}</p><p>${cite(e.cite)}</p></div>`).join("\n")}`;
    if (p.id === "summary") return `<h2>Summary</h2><ul>${t.summary.map(s => `<li>${esc(s.text)} ${cite(s.cite)}</li>`).join("")}</ul>`;
    return `<h2>References</h2><p>Everything in this lesson comes from the sources below. No outside material was used.</p>
${ref.file ? `<div class="obj"><h3>${esc(ref.doc)}</h3><p>File: ${esc(ref.file)}</p><p>Module ${esc(ref.module)}, pages ${esc(ref.pages.join(", "))}</p></div>` : ""}
${ref.words.map(w => `<div class="obj"><h3>${w.file === PSAR_FILE ? "Kemmerer Unit 1 PSAR" : w.file.endsWith(".pdf") ? "NRC fast reactor training slides" : "Lesson plan"}</h3><p>File: ${esc(w.file)}</p><p>${w.file === PSAR_FILE ? "Pages" : "Slides"} ${esc(w.slides.join(", "))}</p></div>`).join("")}
${t.word_sequence.length ? `<div class="obj"><h3>Lesson plan sequence</h3><ol>${t.word_sequence.map(w => `<li>${esc(w.step)} ${cite(w.cite)}</li>`).join("")}</ol></div>` : ""}
<p>Quiz questions from this lesson: ${esc(ref.quiz.join(", "))}.</p><p>Flashcards from this lesson: ${esc(ref.cards.join(", "))}.</p>
<p><a href="../../reference/">All sources and references</a></p>
<p><a class="report" href="${esc(mailto("Problem with lesson " + t.module_id, `Lesson: ${t.module_id} ${t.title}\nPage:\n\nWhat looks wrong:\n`))}">Report a problem with this lesson</a></p>`;
  };
  const menu = `<details class="menu"><summary>All pages</summary><ol>${list.map(p => `<li><a href="#${p.id}">${esc(p.title)}</a></li>`).join("")}</ol></details>`;
  const finish = `<div class="finish"><button type="button" class="mark">Mark lesson complete</button><p class="mark-note" hidden>Could not save on this device.</p></div>`;
  const side = `<nav class="side" aria-label="Lesson pages"><h2>Pages</h2><ol>${list.map(p => `<li><a href="#${p.id}">${esc(p.title)}</a></li>`).join("")}</ol>${finish}</nav>`;
  const sections = list.map((p, i) => `<section class="page" id="${p.id}">
<div class="top"><span><a class="home" href="../../"><span aria-hidden="true">←</span> Home</a> <a class="home plans" href="../../lessons/">Lesson plans</a></span><span class="count">Page ${i + 1} of ${list.length}</span></div>
<h1>${esc(t.title)}</h1>
<ul class="tags">${tagList(p)}</ul>
${menu}
${body(p)}
${p.id === "summary" || p.id === "references" ? finish : ""}
<div class="pager">${i ? `<a href="#${list[i - 1].id}"><span aria-hidden="true">←</span> ${esc(list[i - 1].title)}</a>` : ""}${i + 1 < list.length ? `<a class="next" href="#${list[i + 1].id}">${esc(list[i + 1].title)} <span aria-hidden="true">→</span></a>` : ""}</div>
</section>`).join("\n");
  write(`topics/${t.slug}/index.html`, `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f4f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131821" media="(prefers-color-scheme: dark)">
<title>${esc(t.title)}</title>
<style>${CSS}</style>
<main class="wrap" data-slug="${esc(t.slug)}">
${side}
<div class="pages">
${sections}
</div>
</main>
<script>${SYNC_LIB}</script>
<script>${SCRIPT}</script>
</html>
`);
}

// 3. Lesson plans page. The list comes from the manifest; only topics with a page can be chosen.
const done = new Map(topics.map(t => [t.module_id, t]));
const groups = new Map();
manifest.modules.forEach(m => { if (!groups.has(m.handbook_title)) groups.set(m.handbook_title, []); groups.get(m.handbook_title).push(m); });
const planLink = m => {
  const t = done.get(m.module_id);
  if (!t) return `<li><span class="off">${esc(m.title)}</span><small>In progress</small></li>`;
  return `<li><a href="../topics/${t.slug}/" data-slug="${t.slug}">${esc(m.title)}</a><small>${esc([t.status, ...t.scope_tags].join(", "))}</small></li>`;
};
const option = m => {
  const t = done.get(m.module_id);
  const where = m.handbook ? `${m.handbook}${m.volume && /\/\d/.test(m.handbook) ? ", Volume " + m.volume : ""}` : "Sodium system lesson";
  const status = t ? [t.status, ...t.scope_tags, ...(t.page_tags || []).map(x => x + " pages")].join(", ") : "In progress";
  return t
    ? `        <option value="../topics/${t.slug}/" data-title="${esc(m.title)}" data-where="${esc(where)}" data-status="${esc(status)}">${esc(m.title)} (${esc(status)})</option>`
    : `        <option disabled>${esc(m.title)} (In progress)</option>`;
};
const planPage = ({ file, title, total, groups, intro, extra = "" }) => write(file, `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f4f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131821" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" sizes="192x192" href="../flashcards/icons/icon-192.png">
<title>${esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Generated by scripts/build-lessons.js from the manifest. Edit that script, not this page. */
:root { --bg: #f4f4f1; --card: #ffffff; --fg: #1c2230; --muted: #5a6376; --line: #d6d9e0; --accent: #8a5f00; color-scheme: light; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4; --line: #2c3645; --accent: #f2c14e; color-scheme: dark; }
}
:root[data-theme="dark"] { --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4; --line: #2c3645; --accent: #f2c14e; color-scheme: dark; }
* { box-sizing: border-box; }
html, body { min-height: 100%; }
body { margin: 0; background: var(--bg); color: var(--fg); font-family: "IBM Plex Sans", system-ui, sans-serif; font-size: 15px; line-height: 1.5;
  padding: 16px max(16px, env(safe-area-inset-right, 0px)) calc(48px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px)); }
.wrap { max-width: 480px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }
a { color: var(--accent); font-weight: 600; }
a:focus-visible, select:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.home { text-decoration: none; font-size: 0.9rem; padding: 8px 0; display: inline-block; }
h1 { margin: 0; font-family: "Source Serif 4", Georgia, serif; font-weight: 600; font-size: 2rem; }
label { display: block; font-weight: 600; margin-bottom: 6px; }
select { width: 100%; min-height: 52px; font: inherit; font-size: 16px; color: var(--fg); background: var(--card); border: 1px solid var(--accent); border-radius: 10px; padding: 10px 12px; }
.chosen { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.chosen[hidden] { display: none; }
.chosen h2 { margin: 0; font-size: 1.1rem; }
.chosen p { margin: 0; color: var(--muted); font-size: 0.9rem; }
.big { display: block; text-align: center; text-decoration: none; font-weight: 600; font-size: 1.25rem; padding: 20px 16px; border-radius: 10px; border: 1px solid var(--accent); background: var(--accent); color: var(--bg); }
.note { margin: 0; text-align: center; color: var(--muted); font-size: 0.9rem; }
.pane { display: flex; flex-direction: column; gap: 16px; min-width: 0; }
.all { display: none; }
/* Wide screens also show every lesson at once. Phones keep the drop selector only. */
@media (min-width: 900px) {
  .wrap { max-width: 1120px; display: grid; grid-template-columns: 340px minmax(0, 1fr); gap: 36px; align-items: start; }
  .pane { position: sticky; top: 16px; }
  .all { display: block; min-width: 0; }
  .all h2 { margin: 8px 0 12px; font-family: "Source Serif 4", Georgia, serif; font-weight: 600; font-size: 1.3rem; }
  .groups { columns: 2; column-gap: 28px; }
  .group { break-inside: avoid; margin-bottom: 18px; }
  .group h3 { margin: 0 0 6px; font-size: 0.95rem; display: flex; justify-content: space-between; gap: 10px; }
  .group h3 span { color: var(--muted); font-weight: 400; white-space: nowrap; }
  .group ul { list-style: none; margin: 0; padding: 0; }
  .group li { padding: 5px 0; border-top: 1px solid var(--line); }
  .group a { text-decoration: none; } .group a:hover { text-decoration: underline; }
  .group a.is-done::before { content: "\\2713\\00a0"; color: var(--good); }
  .group small { display: block; color: var(--muted); }
  .group .off { color: var(--muted); }
}
</style>
<main class="wrap">
 <div class="pane">
  <a class="home" href="../"><span aria-hidden="true">←</span> Home</a>
  <h1>${esc(title)}</h1>
  ${intro}
  <div>
    <label for="plan">Choose a lesson plan</label>
    <select id="plan">
      <option value="">Select a lesson plan</option>
${groups.map(g => `      <optgroup label="${esc(g.title)}">
${g.options}
      </optgroup>`).join("\n")}
    </select>
  </div>
  <section class="chosen" id="chosen" hidden>
    <h2 id="chosen-title"></h2>
    <p id="chosen-where"></p>
    <p id="chosen-status"></p>
    <p id="chosen-progress"></p>
    <a class="big" id="start">Start lesson</a>
  </section>
  <p class="note" id="progress">0 of ${total} lessons completed</p>
  <p class="note">Lesson progress is saved on this device. Turn on sync on the main page to share it with your other devices.</p>
  ${extra}<p class="note"><a href="../reference/#lesson-references">References</a></p>
 </div>
 <section class="all" aria-label="All lesson plans">
  <h2>All lesson plans</h2>
  <div class="groups">
${groups.map(g => `   <div class="group"><h3>${esc(g.title)} <span></span></h3><ul>${g.links}</ul></div>`).join("\n")}
  </div>
 </section>
</main>
<script src="../sync.js"></script>
<script>
const plan = document.getElementById("plan"), chosen = document.getElementById("chosen");
const KEY = "natrium-lessons-progress";
const slugOf = v => v.split("/")[2];
const options = [...plan.options].filter(o => o.value);
options.forEach(o => { o.dataset.label = o.textContent; });
function loadAll() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
function dateText(d) { return new Date(d + "T12:00:00").toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }); }
function show() {
  const o = plan.options[plan.selectedIndex];
  chosen.hidden = !plan.value;
  if (!plan.value) return;
  const p = loadAll()[slugOf(plan.value)], start = document.getElementById("start"), resume = p && !p.done && p.n > 1;
  document.getElementById("chosen-title").textContent = o.dataset.title;
  document.getElementById("chosen-where").textContent = o.dataset.where;
  document.getElementById("chosen-status").textContent = "Status: " + o.dataset.status;
  document.getElementById("chosen-progress").textContent = "Your progress: " + (p && p.done ? "Completed " + dateText(p.done) : resume ? "Stopped at page " + p.n + " of " + p.total : p ? "Started" : "Not started");
  start.textContent = p && p.done ? "Review lesson" : resume ? "Resume lesson" : "Start lesson";
  start.href = plan.value + (resume ? "#" + p.page : "");
}
function refresh() {
  const all = loadAll();
  options.forEach(o => {
    const p = all[slugOf(o.value)];
    o.textContent = (p && p.done ? "\u2713 " : p ? "Started: " : "") + o.dataset.label;
  });
  document.querySelectorAll(".group").forEach(g => {
    const links = [...g.querySelectorAll("a")];
    links.forEach(a => a.classList.toggle("is-done", !!(all[a.dataset.slug] || {}).done));
    g.querySelector("h3 span").textContent = links.filter(a => a.classList.contains("is-done")).length + " of " + links.length;
  });
  const finished = options.filter(o => (all[slugOf(o.value)] || {}).done).length;
  document.getElementById("progress").textContent = finished + " of " + options.length + " lessons completed";
  show();
}
plan.addEventListener("change", show);
addEventListener("pageshow", refresh);
addEventListener("natrium-sync", refresh);
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) navigator.serviceWorker.register("../sw.js").catch(() => {});
</script>
</html>
`);
planPage({
  file: "lessons/index.html", title: "Fundamentals Lesson Plans", total: topics.length, intro: "",
  groups: [...groups].map(([title, mods]) => ({ title, options: mods.map(option).join("\n"), links: mods.map(planLink).join("") }))
});

// PSAR lessons: their own pages, and their own plans page with the same selector and tracking
// PSAR terms. A term with two meanings carries the other one and the words that call for it.
const acr = JSON.parse(read("work/psar/glossary/acronyms.json"));
const TERMS = {};
for (const a of acr.listed) if (!TERMS[a.term]) TERMS[a.term] = [a.d, a.page];
for (const a of acr.extra) TERMS[a.term] = [a.d, a.page];
TERMS["HT-9"] = TERMS.HT9;
for (const [t, c] of Object.entries(acr.context)) TERMS[t] = [c.d, c.page, c.alts.map(a => [a.d, a.page, a.when])];
const GLOSSARY_LIB = read("scripts/glossary-lib.js");
const glossary = `// Generated by scripts/build-lessons.js from work/psar/glossary/acronyms.json and scripts/glossary-lib.js.\nwindow.PSAR_TERMS = ${JSON.stringify(TERMS)};\n${GLOSSARY_LIB}`;
if (!fs.existsSync(at("glossary.js")) || read("glossary.js") !== glossary) {
  write("glossary.js", glossary);
  for (const f of ["quiz/sw.js", "flashcards/sw.js"]) write(f, read(f).replace(/VERSION = "v(\d+)"/, (m, n) => `VERSION = "v${+n + 1}"`));
}
const psar = require("./build-psar.js")({ at, read, write, esc, cite, CSS, SCRIPT, SYNC_LIB, mailto, TERMS, GLOSSARY_LIB, acr });

// PSAR lesson checks go to the quiz. As with the topics, a question already in the file is not added again.
function exportPsarChecks() {
  const plan = JSON.parse(read("work/psar/plan.json")), c = load();
  const has = new Set(c.QS.map(q => q.q));
  let next = Math.max(...c.QS.map(q => +q.id.slice(1))) + 1;
  // Lessons in groups the quiz already splits or names differently keep the quiz's existing topic
  const place = { "SY-13": "Radwaste Systems", "SY-14": "Ancillary Systems", "SY-15": "Ancillary Systems", "SY-23": "Electrical Systems", "SY-24": "Buildings and Structures" };
  const topicOf = id => place[id] || (g => g === "Instrumentation and Control" ? "Integrated Controls Systems" : g)(plan.groups.find(g => g.lessons.includes(id)).title);
  const sup = s => s.replace(/(\d)x10-(\d+)/g, (m, a, n) => a + "×10⁻" + [...n].map(d => "⁰¹²³⁴⁵⁶⁷⁸⁹"[d]).join(""));
  // Number choices stay in ascending order in the quiz (seq), like the other numeric questions
  const size = o => parseFloat(o.replace(/,/g, "")) * (/\byears?\b/.test(o) ? 31536000 : /\bdays?\b/.test(o) ? 86400 : /\bhours?\b/.test(o) ? 3600 : 1);
  const lines = [], log = [];
  for (const t of psar.lessons) for (const con of t.concepts) for (const k of con.checks) {
    const q = sup(k.q);
    if (has.has(q)) continue;
    has.add(q);
    let o = k.o.map(sup), a = k.a, seq = "";
    if (o.every(x => /^[\d.,]+\b/.test(x)) && !o.some(x => x.startsWith("10 CFR"))) {
      const right = o[a];
      o = o.slice().sort((x, y) => size(x) - size(y));
      a = o.indexOf(right);
      seq = ", seq: true";
    }
    const id = "Q" + next++, topic = "PSAR: " + topicOf(t.id);
    lines.push(`  { id: ${JSON.stringify(id)}, t: "PSAR design basis", topic: ${JSON.stringify(topic)}, q: ${JSON.stringify(q)},\n    o: ${JSON.stringify(o)}, a: ${a},\n    x: ${JSON.stringify(sup(k.x))},\n    src: ${JSON.stringify(k.cite)}${seq} },`);
    log.push(`- **${id}** (${topic}): ${q}\n  - Source: ${k.cite}\n  - Quote: "${k.anchor}"`);
  }
  if (!lines.length) return;
  const s = read("quiz/questions.js"), end = s.lastIndexOf("];");
  write("quiz/questions.js", s.slice(0, end) + lines.join("\n") + "\n" + s.slice(end));
  write("quiz/sw.js", read("quiz/sw.js").replace(/VERSION = "v(\d+)"/, (m, n) => `VERSION = "v${+n + 1}"`));
  write("CHANGELOG.md", read("CHANGELOG.md").trimEnd() + `\n\n## ${today}: PSAR lesson plans (knowledge checks)\n\nAdded ${lines.length} quiz questions from the PSAR lesson plans.\n\n` + log.join("\n") + "\n");
  console.log(`Exported ${lines.length} PSAR questions`);
}
exportPsarChecks();
planPage({
  file: "psar/index.html", title: "PSAR Lesson Plans", total: psar.lessons.length, groups: psar.groups,
  extra: `<p class="note"><a href="acronyms/">Acronyms and abbreviations</a></p>\n  `,
  intro: `<p class="note">Written from the Kemmerer Unit 1 PSAR, Revision 1. A construction-stage document, so an introduction to NRC exam preparation, not a replacement for plant procedures.</p>`
});

// The landing page has a button for each lesson set, like the two apps
const lessons = `<!-- lessons:start (generated by scripts/build-lessons.js) -->
  <div class="choice">
    <a class="big" href="lessons/">Fundamentals Lesson Plans</a>
    <p class="note lesson-note" data-prefix="topics" data-total="${topics.length}">${topics.length} lesson plans</p>
  </div>
  <div class="choice">
    <a class="big" href="psar/">PSAR Lesson Plans</a>
    <p class="note lesson-note" data-prefix="psar" data-total="${psar.lessons.length}">${psar.lessons.length} lesson plans</p>
  </div>
  <!-- lessons:end -->`;
write("index.html", read("index.html").replace(/<!-- lessons:start[\s\S]*?<!-- lessons:end -->/, () => lessons));

// 4. Sources used by the lessons, for the reference page
const bySource = new Map();
for (const { t, ref } of built) {
  if (ref.file) {
    if (!bySource.has(ref.file)) bySource.set(ref.file, { doc: ref.doc, file: ref.file, lessons: [] });
    bySource.get(ref.file).lessons.push({ module: ref.module, title: t.title, slug: t.slug, pages: ref.pages, label: "pages" });
  }
  for (const w of ref.words) {
    if (!bySource.has(w.file)) bySource.set(w.file, { doc: w.file === PSAR_FILE ? "Kemmerer Unit 1 PSAR" : (w.file.endsWith(".pdf") ? "NRC fast reactor training slides: " : "Lesson plan: ") + w.file.replace(/\.(docx|pdf)$/, ""), file: w.file, lessons: [] });
    bySource.get(w.file).lessons.push({ module: ref.module, title: t.title, slug: t.slug, pages: w.slides, label: w.file === PSAR_FILE ? "pages" : "slides" });
  }
}
if (!bySource.has(psar.file)) bySource.set(psar.file, { doc: "Kemmerer Unit 1 PSAR", file: psar.file, lessons: [] });
bySource.get(psar.file).lessons.push(...psar.sources);
write("topics/sources.json", JSON.stringify([...bySource.values()], null, 1) + "\n");
cp.execFileSync("node", [at("reference/generate.js")], { stdio: "inherit" });

// 5. Root service worker: new topic URLs are listed, and any content change bumps VERSION
const urls = [...topics.map(t => `./topics/${t.slug}/`), "./psar/", "./psar/acronyms/", ...psar.lessons.map(t => `./psar/${t.slug}/`)];
const hash = crypto.createHash("sha256");
["index.html", "lessons/index.html", "psar/index.html", "psar/acronyms/index.html", "feedback.js", "sync.js", "reference/index.html", ...topics.map(t => `topics/${t.slug}/index.html`), ...psar.lessons.map(t => `psar/${t.slug}/index.html`)].forEach(f => hash.update(read(f)));
const digest = hash.digest("hex").slice(0, 12);
let sw = read("sw.js");
if (!sw.includes(`CONTENT = "${digest}"`)) {
  sw = sw.replace(/VERSION = "v(\d+)"/, (m, n) => `VERSION = "v${+n + 1}"`).replace(/CONTENT = "[^"]*"/, `CONTENT = "${digest}"`);
}
sw = sw.replace(/const TOPICS = \[[\s\S]*?\];/, () => `const TOPICS = ${JSON.stringify(urls, null, 2)};`);
write("sw.js", sw);
console.log(`Built ${topics.length} topics of ${manifest.modules.length}`);
