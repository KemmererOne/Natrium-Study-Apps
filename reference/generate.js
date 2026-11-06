#!/usr/bin/env node
// Builds reference/index.html from SOURCES.md and the two content files.
// Run from anywhere:  node reference/generate.js
// Add --check to fail without writing if the page is out of date.
const fs = require("fs"), path = require("path"), vm = require("vm");
const ROOT = path.join(__dirname, "..");
const read = f => fs.readFileSync(path.join(ROOT, f), "utf8");
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

// SOURCES.md is stored as RTF: each line ends in a backslash and braces are escaped
const lines = read("SOURCES.md").split("\n").map(l => l.replace(/\\$/, "").replace(/\\([{}])/g, "$1").trimEnd());
function section(title) {
  const start = lines.findIndex(l => l.startsWith("## " + title));
  if (start < 0) throw new Error("SOURCES.md has no section: " + title);
  const end = lines.findIndex((l, i) => i > start && l.startsWith("## "));
  return lines.slice(start + 1, end < 0 ? undefined : end);
}
const cells = l => l.split("|").slice(1, -1).map(c => c.trim());
const rows = sec => sec.filter(l => l.startsWith("|") && !/^\|\s*-/.test(l)).slice(1).map(cells);
const included = rows(section("Included")).map(([id, file, doc, date, use]) => ({ id, file, doc, date, use, q: 0, c: 0 }));
const pending = rows(section("Pending"));
const superseded = rows(section("Superseded")).map(([id, file, doc, date, retired, reason]) => ({ id, file, doc, date, retired, reason }));
const excluded = section("Excluded").filter(l => l.startsWith("- ")).map(l => l.slice(2).replace(/}$/, ""));
const scope = section("Scope rule").filter(Boolean).join(" ");

// Document number, from the source's ID, title, or file name
function docNumber(s) {
  if (/^ML\d/.test(s.id)) return s.id;
  if (/^ML\d/.test(s.file)) return s.file.replace(/\.pdf$/, "");
  const inTitle = s.doc.match(/DOE-HDBK-\d+(?:\/\d)?-\d+|NUREG-\d+/);
  if (inTitle) return inTitle[0];
  const m = s.file.match(/^DOE-HDBK-(\d+)-(\d+)[_-]VOL(\d)/);
  if (m) return `DOE-HDBK-${m[1]}/${m[3]}-${m[2]}`;
  if (/^HEDL/.test(s.id)) return s.id;
  return "None";
}
included.forEach(s => { s.num = docNumber(s); });

// Which source an item's citation points to. Null means it names a handbook but not a volume.
const byNum = new Map(included.map(s => [s.num, s]));
const byId = new Map(included.map(s => [s.id, s]));
const byFile = new Map(included.map(s => [s.file, s]));
function sourceOf(src) {
  const id = src.match(/^([A-Za-z0-9-]+?)(?:,| \(|$)/);
  if (id && byId.has(id[1])) return byId.get(id[1]);
  const num = src.match(/DOE-HDBK-\d+\/\d-\d+/);
  if (num && byNum.has(num[0])) return byNum.get(num[0]);
  const file = src.match(/\(([^()]*(?:\([^()]*\))?[^()]*\.(?:docx|pdf))\)/);
  if (file && byFile.has(file[1])) return byFile.get(file[1]);
  const ml = src.match(/ML\d{8}|ML\d+[A-Z]\d+/);
  if (ml && byNum.has(ml[0])) return byNum.get(ml[0]);
  if (/^HEDL-SA-2325/.test(src)) return byId.get("HEDL-SA-2325");
  if (/^NRC bank 29|question bank \(BWR/.test(src)) return byId.get("NRC-BWR");
  return null;
}

const ctx = {};
vm.createContext(ctx);
vm.runInContext(read("quiz/questions.js").replace(/\bconst QS\b/, "var QS"), ctx);
vm.runInContext(read("flashcards/cards.js").replace(/\bconst CARDS\b/, "var CARDS").replace(/\bconst TOPIC_GROUPS\b/, "var TOPIC_GROUPS"), ctx);

// Every item needs a unique permanent ID, so an error report points at exactly one item
function checkIds(ids, prefix) {
  const bad = ids.filter((id, i) => !new RegExp("^" + prefix + "[1-9]\\d*$").test(id) || ids.indexOf(id) !== i);
  if (bad.length) throw new Error("Missing, malformed, or repeated IDs: " + bad.join(", "));
}
checkIds(ctx.QS.map(q => q.id), "Q");
checkIds(ctx.CARDS.map(c => c[6]), "C");
const email = read("feedback.js").match(/FEEDBACK_EMAIL = "([^"]+)"/)[1];

const whole = new Map(), unmatched = [];
function count(src, key) {
  const s = sourceOf(src);
  if (s) { s[key]++; return; }
  const h = src.match(/^DOE-HDBK-(\d+)/);
  if (!h) { unmatched.push(src); return; }
  const w = whole.get(h[1]) || { q: 0, c: 0 };
  w[key]++;
  whole.set(h[1], w);
}
ctx.QS.forEach(q => count(q.src, "q"));
ctx.CARDS.forEach(c => count(c[3], "c"));
if (unmatched.length) throw new Error("Citations with no source in SOURCES.md:\n" + [...new Set(unmatched)].join("\n"));

const useText = s => {
  const n = s.q + s.c;
  const role = s.use === "Yes" ? "Included source" : s.use;
  if (n) return `${role}. Items cite it directly.`;
  if (s.id === "NUREG-1021") return `${role}. Sets the writing rules for quiz questions, so no items cite it.`;
  return `${role}. No item cites it by volume or file yet.`;
};

const GROUPS = [
  ["DOE Fundamentals Handbooks", s => /^DOE-/.test(s.id)],
  ["NRC exam material", s => /^NRC-|^NUREG/.test(s.id)],
  ["PSAR", s => s.id === "PSAR"],
  ["NRC fast reactor training", s => /^ML19/.test(s.id)],
  ["Operating experience", s => /^HEDL/.test(s.id)],
  ["Lesson plans", s => /^LP-/.test(s.id)],
];
const slug = t => t.toLowerCase().replace(/[^a-z0-9]+/g, "-");
const left = included.filter(s => !GROUPS.some(([, f]) => f(s)));
if (left.length) throw new Error("Sources in no group: " + left.map(s => s.id).join(", "));

const card = s => `      <article class="src" id="${esc(s.id.toLowerCase())}">
        <h3>${esc(s.doc)}</h3>
        <dl>
          <div><dt>ID</dt><dd class="mono">${esc(s.id)}</dd></div>
          <div><dt>Document no.</dt><dd class="mono">${esc(s.num)}</dd></div>
          <div><dt>Date</dt><dd>${esc(s.date)}</dd></div>
          <div><dt>Use</dt><dd>${esc(useText(s))}</dd></div>
        </dl>
        <p class="counts"><span><b>${s.c}</b> flashcards</span><span><b>${s.q}</b> quiz questions</span></p>
      </article>`;

const wholeRows = [...whole].sort().map(([n, w]) =>
  `        <li><span class="mono">DOE-HDBK-${esc(n)}</span>: ${w.c} flashcards, ${w.q} quiz questions</li>`).join("\n");

const groups = GROUPS.map(([title, f]) => {
  const list = included.filter(f);
  const q = list.reduce((a, s) => a + s.q, 0), c = list.reduce((a, s) => a + s.c, 0);
  const note = title.startsWith("DOE") && wholeRows
    ? `\n      <div class="note"><p>These items cite a handbook without naming a volume, so they are not in the volume counts below:</p>\n      <ul>\n${wholeRows}\n      </ul></div>` : "";
  return `    <section id="${slug(title)}">
      <h2>${esc(title)}</h2>
      <p class="meta">${list.length} sources, ${c} flashcards, ${q} quiz questions cited by source</p>${note}
${list.map(card).join("\n")}
    </section>`;
}).join("\n");

// Sources the lessons use, written by scripts/build-lessons.js
const lessonFile = path.join(ROOT, "topics/sources.json");
const lessonSources = fs.existsSync(lessonFile) ? JSON.parse(fs.readFileSync(lessonFile, "utf8")) : [];
const lessonSection = `    <section id="lesson-references">
      <h2>Lesson references</h2>
      <p class="meta">Every source used across the lessons, with its file name and pages</p>
${lessonSources.map(s => `      <article class="src">
        <h3>${esc(s.doc)}</h3>
        <dl><div><dt>File</dt><dd class="mono">${esc(s.file)}</dd></div></dl>
        <ul class="plain">
${s.lessons.map(l => `          <li><a href="../topics/${esc(l.slug)}/">${esc(l.module)} ${esc(l.title)}</a>: ${esc(l.label)} ${esc(l.pages.join(", "))}</li>`).join("\n")}
        </ul>
      </article>`).join("\n")}
    </section>`;

const html = `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f4f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131821" media="(prefers-color-scheme: dark)">
<link rel="icon" type="image/png" sizes="192x192" href="../flashcards/icons/icon-192.png">
<title>Sources and Reference</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Generated by reference/generate.js from SOURCES.md. Edit that script, not this page. */
:root {
  --bg: #f4f4f1; --card: #ffffff; --fg: #1c2230; --muted: #5a6376; --line: #d6d9e0; --accent: #8a5f00;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4;
    --line: #2c3645; --accent: #f2c14e; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #131821; --card: #1b222e; --fg: #e7eaf0; --muted: #9aa3b4;
  --line: #2c3645; --accent: #f2c14e; color-scheme: dark;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: "IBM Plex Sans", system-ui, sans-serif; font-size: 15px; line-height: 1.5;
  padding: 24px max(16px, env(safe-area-inset-right, 0px)) calc(110px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px));
}
.wrap { max-width: 640px; margin: 0 auto; display: flex; flex-direction: column; gap: 24px; min-width: 0; }
a { color: var(--accent); font-weight: 600; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.home { font-size: 0.85rem; text-decoration: none; }
h1 { margin: 4px 0 0; font-family: "Source Serif 4", Georgia, serif; font-weight: 600; font-size: 1.75rem; }
h2 { margin: 0; font-family: "Source Serif 4", Georgia, serif; font-weight: 600; font-size: 1.3rem; }
h3 { margin: 0; font-size: 1rem; font-weight: 600; overflow-wrap: anywhere; }
section { display: flex; flex-direction: column; gap: 12px; scroll-margin-top: 12px; min-width: 0; }
p { margin: 0; }
.meta { color: var(--muted); font-size: 0.85rem; }
.mono { font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 0.8rem; overflow-wrap: anywhere; }
.totals { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }
.totals div { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 10px; }
.totals b { display: block; font-family: "Source Serif 4", Georgia, serif; font-size: 1.5rem; color: var(--accent); font-variant-numeric: tabular-nums; }
.totals span { font-size: 0.8rem; color: var(--muted); }
nav ul { margin: 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: 0.9rem; }
.src, .note { background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.note ul { margin: 0; padding-left: 18px; }
dl { margin: 0; display: flex; flex-direction: column; gap: 4px; }
dl div { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 8px; }
dt { color: var(--muted); font-size: 0.8rem; }
dd { margin: 0; font-size: 0.88rem; min-width: 0; overflow-wrap: anywhere; }
.counts { display: flex; flex-wrap: wrap; gap: 4px 16px; font-size: 0.85rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 8px; }
.counts b { color: var(--fg); font-variant-numeric: tabular-nums; }
.plain { margin: 0; padding-left: 18px; }
</style>

<main class="wrap">
  <header>
    <a class="home" href="../"><span aria-hidden="true">←</span> Home</a>
    <h1>Sources and Reference</h1>
  </header>

  <p>${esc(scope)}</p>
  <p>Feedback or an error? Email <a href="mailto:${esc(email)}">${esc(email)}</a> and include the item ID shown on the quiz question or flashcard, such as Q12 or C34.</p>

  <div class="totals">
    <div><b>${included.length}</b><span>included sources</span></div>
    <div><b>${ctx.CARDS.length}</b><span>flashcards</span></div>
    <div><b>${ctx.QS.length}</b><span>quiz questions</span></div>
  </div>

  <nav aria-label="Source groups">
    <ul>
${GROUPS.map(([t]) => `      <li><a href="#${slug(t)}">${esc(t)}</a></li>`).join("\n")}
      <li><a href="#lesson-references">Lesson references</a></li>
      <li><a href="#superseded">Superseded</a></li>
      <li><a href="#pending">Pending</a></li>
      <li><a href="#excluded">Excluded</a></li>
    </ul>
  </nav>

${groups}

${lessonSection}

    <section id="superseded">
      <h2>Superseded</h2>
      <p class="meta">Retired revisions, no longer used by the apps</p>
${superseded.map(s => `      <article class="src">
        <h3>${esc(s.doc)}</h3>
        <dl>
          <div><dt>Document no.</dt><dd class="mono">${esc(s.id)}</dd></div>
          <div><dt>Date</dt><dd>${esc(s.date)}</dd></div>
          <div><dt>Retired</dt><dd>${esc(s.retired)}</dd></div>
          <div><dt>Reason</dt><dd>${esc(s.reason)}</dd></div>
        </dl>
      </article>`).join("\n")}
    </section>

    <section id="pending">
      <h2>Pending identification</h2>
      <p class="meta">Not usable until confirmed</p>
${pending.map(([file, status]) => `      <article class="src"><h3 class="mono">${esc(file)}</h3><p>${esc(status)}</p></article>`).join("\n")}
    </section>

    <section id="excluded">
      <h2>Excluded</h2>
      <p class="meta">Removed from use</p>
      <ul class="plain">
${excluded.map(e => `        <li>${esc(e)}</li>`).join("\n")}
      </ul>
    </section>
</main>
</html>
`;

const out = path.join(__dirname, "index.html");
if (process.argv.includes("--check")) {
  const same = fs.existsSync(out) && fs.readFileSync(out, "utf8") === html;
  console.log(same ? "reference/index.html is up to date" : "reference/index.html is out of date: run node reference/generate.js");
  process.exit(same ? 0 : 1);
}
fs.writeFileSync(out, html);
console.log(`Wrote reference/index.html: ${included.length} sources, ${ctx.CARDS.length} cards, ${ctx.QS.length} questions`);
