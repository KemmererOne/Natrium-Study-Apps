// Cloudflare Worker that stores each sync code's progress. See the Device sync section of CLAUDE.md.
// It needs one KV namespace bound as SYNC. Paste this file into the Worker's editor to deploy it.
//
// GET  /sync/<code>  says whether the code exists (204 or 404).
// POST /sync/<code>  merges the device's items into the stored ones and returns the result.
//
// An item is "key": [value, time]. The later time wins, and a value of 0 means the mark was removed.
// The stored data holds only card IDs, lesson slugs, page numbers and dates: no name or email.

const ORIGINS = "https://kemmererone.github.io";
const CODE = /^\/sync\/([0-9A-HJKMNP-TV-Z]{16})$/;
const MAX_BODY = 400000;
const KEEP_SECONDS = 400 * 86400; // A code unused for 400 days is deleted. Its devices restore it on their next sync.

const isItem = (key, item) => {
  if (!/^[cdp]\/[\w.-]{1,120}$/.test(key) || !Array.isArray(item) || item.length !== 2) return false;
  const [value, time] = item;
  if (!Number.isFinite(time) || time <= 0) return false;
  if (value === 0) return true;
  if (key[0] === "c") return Number.isInteger(value) && value >= 1 && value <= 3;
  if (key[0] === "d") return typeof value === "string" && /^\d{4}-\d{2}-\d{2}$/.test(value);
  return Array.isArray(value) && value.length === 3 && typeof value[0] === "string" && value[0].length <= 100 &&
    Number.isInteger(value[1]) && Number.isInteger(value[2]);
};

// Same rule as newer() in sync.js. Ties break on the value, so every copy reaches the same answer.
const newer = (a, b) => !b || a[1] > b[1] || (a[1] === b[1] && JSON.stringify(a[0]) > JSON.stringify(b[0]));

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin");
    if (!(env.ORIGINS || ORIGINS).split(",").includes(origin)) return new Response("Forbidden", { status: 403 });
    const headers = { "Access-Control-Allow-Origin": origin, Vary: "Origin" };
    const reply = (body, status) => new Response(body, { status, headers });

    const code = (new URL(request.url).pathname.match(CODE) || [])[1];
    if (!code) return reply("Not found", 404);

    if (request.method === "GET") return reply(null, (await env.SYNC.get(code)) === null ? 404 : 204);
    if (request.method !== "POST") return reply("Method not allowed", 405);

    const text = await request.text();
    if (text.length > MAX_BODY) return reply("Too large", 413);
    let sent;
    try { sent = JSON.parse(text).items; } catch (e) { return reply("Bad request", 400); }
    if (!sent || typeof sent !== "object" || Array.isArray(sent)) return reply("Bad request", 400);

    const raw = await env.SYNC.get(code), items = raw ? JSON.parse(raw) : {};
    let changed = raw === null;
    for (const [key, item] of Object.entries(sent)) {
      if (isItem(key, item) && newer(item, items[key])) { items[key] = item; changed = true; }
    }
    // A failed write is safe to ignore: the device still holds its items and sends them again next time.
    if (changed) { try { await env.SYNC.put(code, JSON.stringify(items), { expirationTtl: KEEP_SECONDS }); } catch (e) {} }
    headers["Content-Type"] = "application/json";
    return reply(JSON.stringify({ items }), 200);
  }
};
