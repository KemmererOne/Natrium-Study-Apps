// Builds the PSAR lesson pages from work/psar/*.json. Called by scripts/build-lessons.js,
// which passes in the shared page styles and script so both lesson sets look and track alike.
const fs = require("fs");
const PSAR_FILE = "ML25276A288.pdf";
const EXTRA = `
.tbl { width: 100%; border-collapse: collapse; margin: 0 0 14px; font-size: 0.86rem; table-layout: fixed; }
.tbl th, .tbl td { border: 1px solid var(--line); padding: 6px 7px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }
.tbl th { background: var(--card); }
.gap { color: var(--muted); font-size: 0.85rem; margin: 2px 0 12px; }
.study { border-left: 3px solid var(--line); padding: 2px 0 2px 10px; color: var(--muted); }
.src { font-size: 0.9rem; }
`;
module.exports = ({ at, read, write, esc, cite, CSS, SCRIPT, mailto }) => {
  const plan = JSON.parse(read("work/psar/plan.json"));
  const lessons = fs.readdirSync(at("work/psar")).filter(f => f.endsWith(".json") && f !== "plan.json").map(f => JSON.parse(read("work/psar/" + f)));
  const byId = new Map(lessons.map(t => [t.id, t]));
  const LETTERS = "ABCD";
  const pageOf = c => c.match(/, p\. (\S+)$/)[1];
  const secOf = c => c.match(/Sec\. ([\d.]+),/)[1];
  const label = (a, b) => a.split("-")[0].localeCompare(b.split("-")[0], "en", { numeric: true }) || a.split("-")[1] - b.split("-")[1];
  function figure(f) {
    const data = fs.readFileSync(at(`work/figs/${f.id}.png`)).toString("base64");
    return `<figure class="fig"><img loading="lazy" src="data:image/png;base64,${data}" alt="${esc(f.alt)}"><figcaption>Figure ${esc(f.num)}. ${esc(f.cap)} ${cite(f.cite)}</figcaption></figure>`;
  }
  function block(t, b) {
    if (b.t === "quote") { const p = t.passages.find(x => x.id === b.p); return `<blockquote>"${esc(p.quote)}" ${cite(p.cite)}</blockquote>`; }
    if (b.t === "p") return `<p>${esc(b.text)} ${cite(b.cite)}</p>`;
    if (b.t === "note") return `<p class="study">${esc(b.text)}</p>`;
    if (b.t === "fig") return figure(b);
    if (b.t === "list") return `<ul>${b.items.map(i => `<li>${esc(i)}</li>`).join("")}</ul><p>${cite(b.cite)}</p>`;
    if (b.t === "table") return `<table class="tbl"><thead><tr>${b.head.map(h => `<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${b.rows.map(r => `<tr>${r.cells.map((c, i) => `<td>${esc(c)}${i === r.cells.length - 1 ? " " + cite(r.cite) : ""}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
    throw new Error("Unknown block " + b.t);
  }
  function refs(t) {
    const all = new Set();
    t.passages.forEach(p => all.add(p.cite));
    t.summary.forEach(s => all.add(s.cite));
    t.concepts.forEach(c => {
      c.body.forEach(b => { if (b.cite) all.add(b.cite); (b.rows || []).forEach(r => all.add(r.cite)); });
      c.checks.forEach(k => all.add(k.cite));
    });
    const pages = [...new Set([...all].map(pageOf))].sort(label);
    const secs = [...new Set([...all].map(secOf))].sort((a, b) => a.localeCompare(b, "en", { numeric: true }));
    return { pages, secs };
  }
  const built = [];
  for (const t of lessons) {
    const r = refs(t);
    built.push({ t, r });
    const head = `PSAR Rev 1 (NAT-9400), ${t.sec_note}`;
    const list = [{ id: "objectives", title: "Objectives" }];
    t.concepts.forEach((c, i) => {
      list.push({ id: "concept-" + (i + 1), title: c.title, c });
      if (c.checks.length) list.push({ id: "check-" + (i + 1), title: "Knowledge check: " + c.title, k: c });
    });
    list.push({ id: "summary", title: "Summary" }, { id: "references", title: "References" });
    let kn = 0;
    const check = k => {
      const id = `${t.id}-K${++kn}`;
      return `<div class="check" data-a="${k.a}">
  <div class="meta"><span>Objective ${esc(k.eo)}</span><span>${esc(id)}</span></div>
  <p>${esc(k.q)}</p>
  <div class="opts">${k.o.map((o, i) => `<button type="button" class="opt">${LETTERS[i]}. ${esc(o)}</button>`).join("")}</div>
  <div class="result" hidden>
    <p class="verdict"></p>
    <p>The answer is ${LETTERS[k.a]}. ${esc(k.x)} ${cite(k.cite)}</p>
    <a class="report" href="${esc(mailto("Problem with " + id, `Item: ${id}\nLesson: ${t.title}\nQuestion: ${k.q.slice(0, 160)}\nSource: ${k.cite}\n\nWhat looks wrong:\n`))}">Report a problem</a>
  </div>
</div>`;
    };
    const objective = o => {
      const pages = list.filter(p => p.c && p.c.eo.includes(o.number));
      return `<p><span class="num">${esc(o.number)}</span> ${esc(o.text)}</p>${pages.length
        ? `<p class="gap">Taught in: ${pages.map(p => `<a href="#${p.id}">${esc(p.title)}</a>`).join(", ")}</p>`
        : `<p class="gap">Not in PSAR Rev 1. This lesson does not teach it.</p>`}`;
    };
    const body = p => {
      if (p.id === "objectives") return `<p class="src">${esc(t.intro)} ${cite(head)}</p><div class="obj"><h3>Learning objectives</h3>${t.objectives.map(objective).join("")}</div>`;
      if (p.c) return `<h2>${esc(p.title)}</h2><p class="count">${p.c.eo.length ? "Objectives " + esc(p.c.eo.join(", ")) : "Background"}</p>${p.c.body.map(b => block(t, b)).join("\n")}`;
      if (p.k) return `<h2>${esc(p.title)}</h2>${p.k.checks.map(check).join("\n")}`;
      if (p.id === "summary") return `<h2>Summary</h2><ul>${t.summary.map(s => `<li>${esc(s.text)} ${cite(s.cite)}</li>`).join("")}</ul>`;
      return `<h2>References</h2><p>Everything in this lesson comes from PSAR Rev 1. No other source was used.</p>
<div class="obj"><h3>Kemmerer Unit 1 PSAR, NAT-9400, Revision 1</h3><p>File: ${PSAR_FILE}</p><p>Sections ${esc(r.secs.join(", "))}</p><p>Pages ${esc(r.pages.join(", "))}</p></div>
<p><a href="../../reference/#lesson-references">All sources and references</a></p>
<p><a class="report" href="${esc(mailto("Problem with lesson " + t.id, `Lesson: ${t.id} ${t.title}\nPage:\n\nWhat looks wrong:\n`))}">Report a problem with this lesson</a></p>`;
    };
    const links = `<ol>${list.map(p => `<li><a href="#${p.id}">${esc(p.title)}</a></li>`).join("")}</ol>`;
    const menu = `<details class="menu"><summary>All pages</summary>${links}</details>`;
    const finish = `<div class="finish"><button type="button" class="mark">Mark lesson complete</button><p class="mark-note" hidden>Could not save on this device.</p></div>`;
    const side = `<nav class="side" aria-label="Lesson pages"><h2>Pages</h2>${links}${finish}</nav>`;
    const sections = list.map((p, i) => `<section class="page" id="${p.id}">
<div class="top"><span><a class="home" href="../../"><span aria-hidden="true">←</span> Home</a> <a class="home plans" href="../">PSAR lessons</a></span><span class="count">Page ${i + 1} of ${list.length}</span></div>
<h1>${esc(t.title)}</h1>
<ul class="tags"><li class="tag">${esc(t.status)}</li><li class="tag">PSAR Rev 1</li></ul>
${menu}
${body(p)}
${p.id === "summary" || p.id === "references" ? finish : ""}
<div class="pager">${i ? `<a href="#${list[i - 1].id}"><span aria-hidden="true">←</span> ${esc(list[i - 1].title)}</a>` : ""}${i + 1 < list.length ? `<a class="next" href="#${list[i + 1].id}">${esc(list[i + 1].title)} <span aria-hidden="true">→</span></a>` : ""}</div>
</section>`).join("\n");
    write(`psar/${t.slug}/index.html`, `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f4f4f1" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131821" media="(prefers-color-scheme: dark)">
<title>${esc(t.title)}</title>
<style>${CSS}${EXTRA}</style>
<main class="wrap" data-slug="${esc(t.slug)}">
${side}
<div class="pages">
${sections.replace(/(\d)x10-(\d+)(?=[^<>]*<)/g, "$1×10<sup>-$2</sup>")}
</div>
</main>
<script>${SCRIPT}</script>
</html>
`);
  }
  // Selector entries come from the plan, so a planned lesson with no page shows as In progress
  const groups = plan.groups.map(g => {
    const rows = g.lessons.map(id => ({ id, t: byId.get(id), title: plan.titles[id] }));
    return {
      title: g.title,
      options: rows.map(x => x.t
        ? `        <option value="../psar/${x.t.slug}/" data-title="${esc(x.t.title)}" data-where="PSAR Rev 1, ${esc(x.t.sec_note)}" data-status="${esc(x.t.status)}">${esc(x.t.title)} (${esc(x.t.status)})</option>`
        : `        <option disabled>${esc(x.title)} (In progress)</option>`).join("\n"),
      links: rows.map(x => x.t
        ? `<li><a href="../psar/${x.t.slug}/" data-slug="${x.t.slug}">${esc(x.t.title)}</a><small>${esc(x.t.sec_note)}, ${esc(x.t.status)}</small></li>`
        : `<li><span class="off">${esc(x.title)}</span><small>In progress</small></li>`).join("")
    };
  });
  const sources = built.map(({ t, r }) => ({ module: t.id, title: t.title, slug: t.slug, dir: "psar", pages: r.pages, label: "pages" }));
  return { lessons, groups, sources, file: PSAR_FILE };
};
