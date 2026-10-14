// site-stats: anonymous reading statistics for davidslv.photography.
// POST /e with a small JSON summary from the page (sent with sendBeacon as text/plain, so no CORS preflight).
// Nothing identifying is stored: no IP, no cookie, no user agent. The page id is random and dies with the page.

const MAX_BYTES = 8192;
const clip = (v, n) => (typeof v === "string" ? v.slice(0, n) : null);
const int = (v, lo, hi) => (Number.isFinite(+v) ? Math.max(lo, Math.min(hi, Math.round(+v))) : null);

function cleanMap(o, maxKeys, maxVal) {
  if (!o || typeof o !== "object") return "{}";
  const out = {};
  for (const [k, v] of Object.entries(o).slice(0, maxKeys)) {
    const key = String(k).slice(0, 80), n = int(v, 0, maxVal);
    if (key && n !== null) out[key] = n;
  }
  return JSON.stringify(out);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== "/e" || request.method !== "POST") return new Response("not found", { status: 404 });
    const origin = request.headers.get("Origin") || "";
    if (!env.ALLOWED_ORIGINS.split(",").includes(origin)) return new Response("forbidden", { status: 403 });
    const body = await request.text();
    if (body.length > MAX_BYTES) return new Response("too big", { status: 413 });
    let e;
    try { e = JSON.parse(body); } catch { return new Response("bad json", { status: 400 }); }
    const pv = clip(e.pv, 40);
    if (!pv || !/^[a-z0-9]{8,40}$/.test(pv)) return new Response("bad id", { status: 400 });
    const now = Math.floor(Date.now() / 1000);
    const row = [
      pv, int(e.seq, 0, 10000) ?? 0, new Date().toISOString().slice(0, 10), now,
      clip(e.path, 120) || "/", clip(e.ref, 60), ["phone", "tablet", "desktop"].includes(e.device) ? e.device : null,
      int(e.vw, 0, 10000), clip(request.cf?.country, 2), int(e.scroll, 0, 100), e.ended ? 1 : 0,
      int(e.secs, 0, 86400), clip(e.last_photo, 80), cleanMap(e.photos, 150, 86400), cleanMap(e.clicks, 40, 1000),
    ];
    await env.DB.prepare(`INSERT INTO views (pv,seq,day,ts,path,ref,device,vw,country,scroll,ended,secs,last_photo,photos,clicks)
      VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12,?13,?14,?15)
      ON CONFLICT(pv) DO UPDATE SET seq=excluded.seq, scroll=max(views.scroll, excluded.scroll), ended=max(views.ended, excluded.ended),
        secs=excluded.secs, last_photo=excluded.last_photo, photos=excluded.photos, clicks=excluded.clicks
      WHERE excluded.seq > views.seq`).bind(...row).run();
    return new Response(null, { status: 204, headers: { "Access-Control-Allow-Origin": origin } });
  },
};
