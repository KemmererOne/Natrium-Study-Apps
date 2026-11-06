// Offline cache for the landing page, the lesson plans page, the reference page, and the lessons.
// scripts/build-lessons.js keeps TOPICS current and bumps VERSION when any of those pages change.
// flashcards/ and quiz/ have their own service workers, so this one leaves them alone.
const APP = "site";
const VERSION = "v24";
const CONTENT = "7eb58d91a268";
const CACHE = APP + "-" + VERSION;

const FONT_CSS = "https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap";
const TOPICS = [
  "./topics/ch-01-fundamentals-of-chemistry/",
  "./topics/ch-02-corrosion/",
  "./topics/ch-03-reactor-water-chemistry/",
  "./topics/ch-04-principles-of-water-treatment/",
  "./topics/ch-05-hazards-of-chemicals-and-gases/",
  "./topics/cp-01-unit-systems/",
  "./topics/cp-02-vectors/",
  "./topics/cp-03-force-and-motion/",
  "./topics/cp-04-application-of-newton-s-laws/",
  "./topics/cp-05-energy-work-and-power/",
  "./topics/es-01-basic-electrical-theory/",
  "./topics/es-02-basic-dc-theory/",
  "./topics/es-03-dc-circuits/",
  "./topics/es-04-batteries/",
  "./topics/es-05-dc-generators/",
  "./topics/es-06-dc-motors/",
  "./topics/es-07-basic-ac-theory/",
  "./topics/es-08-basic-ac-reactive-components/",
  "./topics/es-09-basic-ac-power/",
  "./topics/es-10-ac-generators/",
  "./topics/es-11-voltage-regulators/",
  "./topics/es-12-ac-motors/",
  "./topics/es-13-transformers/",
  "./topics/es-14-test-instruments-and-measuring-devices/",
  "./topics/es-15-electrical-distribution-systems/",
  "./topics/ht-01-thermodynamics/",
  "./topics/ht-02-heat-transfer/",
  "./topics/ht-03-fluid-flow/",
  "./topics/ic-01-temperature-detectors/",
  "./topics/ic-02-pressure-detectors/",
  "./topics/ic-03-level-detectors/",
  "./topics/ic-04-flow-detectors/",
  "./topics/ic-05-position-indicators/",
  "./topics/ic-06-radiation-detectors/",
  "./topics/ic-07-process-controls/",
  "./topics/me-01-diesel-engine-fundamentals/",
  "./topics/me-02-heat-exchangers/",
  "./topics/me-03-pumps/",
  "./topics/me-04-valves/",
  "./topics/me-05-miscellaneous-mechanical-components/",
  "./topics/ms-01-structure-of-metals/",
  "./topics/ms-02-properties-of-metals/",
  "./topics/ms-03-thermal-shock/",
  "./topics/ms-04-brittle-fracture/",
  "./topics/ms-05-plant-materials/",
  "./topics/na-01-cold-traps-and-sodium-coolant-purification/",
  "./topics/na-02-plugging-temperature-indicators/",
  "./topics/na-03-sodium-leak-detectors/",
  "./topics/np-01-atomic-and-nuclear-physics/",
  "./topics/np-02-reactor-theory-neutron-characteristics/",
  "./topics/np-03-reactor-theory-nuclear-parameters/",
  "./topics/np-04-reactor-theory-reactor-operations/",
  "./topics/pr-01-introduction-to-print-reading/",
  "./topics/pr-02-engineering-fluid-diagrams-and-prints/",
  "./topics/pr-03-electrical-diagrams-and-schematics/",
  "./topics/pr-04-electronic-diagrams-and-schematics/",
  "./topics/pr-05-logic-diagrams/",
  "./topics/pr-06-engineering-fabrication-construction-and-architectural-drawings/"
];
const LOCAL = ["./", "./lessons/", "./feedback.js", "./reference/", ...TOPICS];
const OWN_WORKER = ["flashcards/", "quiz/"].map(p => new URL(p, self.location).pathname);

// Fonts for the landing and reference pages. Best effort: fallback fonts work offline.
async function cacheFonts(cache) {
  const res = await fetch(FONT_CSS, { mode: "cors" });
  if (!res.ok) throw new Error("font css " + res.status);
  const css = await res.clone().text();
  await cache.put(FONT_CSS, res);
  const urls = [...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map(m => m[1]);
  await Promise.all(urls.map(async u => {
    const r = await fetch(u, { mode: "cors" });
    if (r.ok) await cache.put(u, r);
  }));
}

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(LOCAL.map(u => new Request(u, { cache: "reload" })));
    try { await cacheFonts(cache); } catch (e) { console.warn("Font caching failed", e); }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith(APP + "-") && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin === self.location.origin && OWN_WORKER.some(p => url.pathname.startsWith(p))) return;
  const fonts = url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com";
  if (url.origin !== self.location.origin && !fonts) return;

  // Serve the cached copy at once and refresh it in the background.
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(req, { ignoreSearch: !fonts });
    const fresh = fetch(req).then(res => {
      if (res.ok) cache.put(req, res.clone());
      return res;
    });
    if (cached) { event.waitUntil(fresh.catch(() => {})); return cached; }
    return fresh;
  })());
});
