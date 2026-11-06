#!/usr/bin/env node
// Checks the built lessons: every page cites a source and links home, every link works,
// nothing loads from outside, and the landing page and sw.js agree with what is built.
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, ".."), read = f => fs.readFileSync(path.join(ROOT, f), "utf8");
const errors = [], fail = m => errors.push(m);
const dirs = fs.readdirSync(path.join(ROOT, "topics"), { withFileTypes: true }).filter(d => d.isDirectory()).map(d => d.name);
let pages = 0;
for (const d of dirs) {
  const html = read(`topics/${d}/index.html`);
  if (/<link\b|<script[^>]+src=|\bsrc="(?!data:image\/png)|url\(http/.test(html)) fail(`${d}: loads an outside file`);
  for (const m of html.matchAll(/<img\b[^>]*>/g)) if (!/ alt="[^"]{10,}"/.test(m[0])) fail(`${d}: image with no alt text`);
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m => m[1]));
  for (const m of html.matchAll(/href="#([^"]+)"/g)) if (!ids.has(m[1])) fail(`${d}: broken page link #${m[1]}`);
  for (const m of html.matchAll(/href="(\.\.[^"#]*)/g)) {
    const t = path.resolve(ROOT, "topics", d, m[1]);
    if (!fs.existsSync(path.join(t, "index.html")) && !fs.existsSync(t)) fail(`${d}: broken link ${m[1]}`);
  }
  for (const s of html.split('<section class="page"').slice(1)) {
    pages++;
    const id = s.match(/id="([^"]+)"/)[1];
    if (!s.includes('class="home" href="../../"')) fail(`${d}#${id}: no link home`);
    if (!/<cite>/.test(s) && !/File: /.test(s)) fail(`${d}#${id}: no citation`);
    // Statements only: leave out the page menu, labels, and lists whose cite follows them
    const content = s.replace(/<details class="menu">.*?<\/details>/s, "").replace(/<p class="count">.*?<\/p>/s, "").replace(/<ul class="tags">.*?<\/ul>/s, "").replace(/<div class="pager">.*?<\/div>/s, "").replace(/<ul>(?:(?!<\/ul>).)*<\/ul><p><cite>/gs, "<p><cite>");
    for (const p of content.matchAll(/<(p|li)>(?!<cite>)(.*?)<\/\1>/gs)) {
      const text = p[2].replace(/<[^>]+>/g, "").trim();
      if (id.startsWith("concept") && text && !p[2].includes("<cite>")) fail(`${d}#${id}: statement with no cite: ${text.slice(0, 60)}`);
    }
  }
}
const landing = read("index.html");
if (!landing.includes('class="big" href="lessons/"')) fail("landing: no Lesson Plans button");
const plans = read("lessons/index.html");
for (const m of plans.matchAll(/value="\.\.\/(topics\/[^"]+)"/g)) if (!fs.existsSync(path.join(ROOT, m[1], "index.html"))) fail(`lessons: dead option ${m[1]}`);
const linked = new Set([...plans.matchAll(/value="\.\.\/topics\/([^/"]+)\/"/g)].map(m => m[1]));
const sw = read("sw.js");
for (const d of dirs) {
  if (!linked.has(d)) fail(`lessons: no option for built topic ${d}`);
  if (!sw.includes(`./topics/${d}/`)) fail(`sw.js: topic not cached: ${d}`);
}
if (!sw.includes('"./lessons/"')) fail("sw.js: lesson plans page not cached");
console.log(`${dirs.length} topics, ${pages} pages checked, ${errors.length} problems`);
errors.forEach(e => console.log("  " + e));
process.exit(errors.length ? 1 : 0);
