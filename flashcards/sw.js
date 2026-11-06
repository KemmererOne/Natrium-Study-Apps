// Offline cache for the flashcards app.
// Bump VERSION after editing index.html or the content file so phones pick up the new copy.
const APP = "flashcards";
const VERSION = "v126";
const CACHE = APP + "-" + VERSION;

const FONT_CSS = "https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap";
// Figures named in the content file are cached with the app so they work offline.
importScripts("cards.js");
const IMAGES = [...new Set(CARDS.map(c => c[5]).filter(Boolean).map(f => "./" + f.f))];
const LOCAL = ["./", "./index.html", "../feedback.js", "../glossary.js", "../sync.js", "./cards.js", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", ...IMAGES];

// Fetch the font stylesheet and every font file it points to, so text
// renders in the right fonts even if the first visit was the only online one.
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
    // Bypass the browser's HTTP cache so a new version never stores a stale page
    await cache.addAll(LOCAL.map(u => new Request(u, { cache: "reload" })));
    // Fonts are best effort: the app still works offline with fallback fonts.
    try { await cacheFonts(cache); } catch (e) { console.warn("Font caching failed", e); }
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    // Only remove this app's old caches; the quiz may share the same origin.
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith(APP + "-") && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  // The page: serve the cached copy at once, refresh it in the background.
  if (req.mode === "navigate") {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      const cached = await cache.match("./index.html");
      const fresh = fetch(req).then(res => {
        if (res.ok) cache.put("./index.html", res.clone());
        return res;
      });
      if (cached) { event.waitUntil(fresh.catch(() => {})); return cached; }
      return fresh;
    })());
    return;
  }

  // Same-origin files and Google Fonts: cache first, then network (and keep it).
  if (url.origin === self.location.origin || url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com") {
    event.respondWith((async () => {
      const cache = await caches.open(CACHE);
      const cached = await cache.match(req, { ignoreSearch: url.origin === self.location.origin });
      if (cached) return cached;
      const res = await fetch(req);
      if (res.ok || res.type === "opaque") cache.put(req, res.clone());
      return res;
    })());
  }
});
