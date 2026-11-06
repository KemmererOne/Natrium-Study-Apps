// Runs scripts/sync-worker.js on this computer for testing, with a memory store in place of Cloudflare KV.
// sync.js uses this server on localhost. Start it with: node scripts/sync-dev-server.js
const http = require("http");

const data = new Map();
const env = {
  ORIGINS: "http://localhost:8100,http://127.0.0.1:8100",
  SYNC: { get: async key => (data.has(key) ? data.get(key) : null), put: async (key, value) => { data.set(key, value); } }
};

import("./sync-worker.js").then(({ default: worker }) => {
  http.createServer(async (req, res) => {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const body = req.method === "POST" ? Buffer.concat(chunks) : undefined;
    const out = await worker.fetch(new Request("http://localhost:8787" + req.url, { method: req.method, headers: req.headers, body }), env);
    res.writeHead(out.status, Object.fromEntries(out.headers));
    res.end(await out.text());
  }).listen(8787, "127.0.0.1", () => console.log("Sync test server on http://localhost:8787"));
});
