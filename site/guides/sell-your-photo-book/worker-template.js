// Book shop Worker: Stripe payment -> Prodigi print order.
// From "Sell your photo book from your own website" by David Silva (davidslv.photography).
// Free to use and change. No warranty: test it in test mode before you take real money.
//
// What it does
//   POST /stripe-webhook  Stripe says a checkout is paid. The Worker checks the message is really
//                         from Stripe, asks Stripe again for the order, and places the print order.
//                         If anything fails it answers 500, so Stripe tries again later (up to 3 days).
//   GET  /file/<name>     Lets Prodigi download your print files from your private R2 bucket,
//                         only with a signed link that expires.
//
// Settings (Cloudflare dashboard > your Worker > Settings > Variables and Secrets)
//   Secrets:   STRIPE_SECRET_KEY      restricted key: Checkout Sessions Read, PaymentIntents Write
//              STRIPE_WEBHOOK_SECRET  starts with whsec_
//              PRODIGI_API_KEY        from the Prodigi dashboard
//              FILE_SECRET            any long random text (40+ characters from a password manager)
//   Text:      PRODIGI_BASE           test: https://api.sandbox.prodigi.com/v4.0
//                                     live: https://api.prodigi.com/v4.0
//              PRODIGI_SKU            the book's product code, for example BOOK-FE-A4-L-HARD-G
//              PAGE_COUNT             pages in your book PDF, covers included, for example 164
//              BOOK_FILE              file name of the book PDF in R2, for example book.pdf
//              SPINE_FILE             optional: file name of a spine PDF in R2. Leave it out for a plain spine.
//              PAYMENT_LINK_ID        optional: starts with plink_. Only orders from this link get printed.
//              SHIPPING_METHOD        optional: Budget, Standard, Express or Overnight. Default Standard.
//   Binding:   R2 bucket, variable name BOOK

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

function safeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

// A download link for Prodigi that stops working after ttlSeconds.
async function signedFileUrl(env, origin, name, ttlSeconds) {
  const exp = Math.floor(Date.now() / 1000) + ttlSeconds;
  return `${origin}/file/${encodeURIComponent(name)}?exp=${exp}&sig=${await hmac(env.FILE_SECRET, `${name}:${exp}`)}`;
}

// Stripe signs every webhook: header "t=<time>,v1=<signature>" (docs.stripe.com/webhooks/signature).
async function verifyStripe(request, body, secret, toleranceSeconds = 300) {
  const header = request.headers.get("Stripe-Signature") || "";
  const t = Number((header.split(",").find(kv => kv.startsWith("t=")) || "").slice(2));
  const sigs = header.split(",").filter(kv => kv.startsWith("v1=")).map(kv => kv.slice(3));
  if (!t || !sigs.length || Math.abs(Date.now() / 1000 - t) > toleranceSeconds) return false;
  const expected = await hmac(secret, `${t}.${body}`);
  return sigs.some(s => safeEqual(s, expected));
}

async function stripe(env, path, form) {
  const r = await fetch(`https://api.stripe.com/v1/${path}`, {
    method: form ? "POST" : "GET",
    headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}`,
               ...(form ? { "Content-Type": "application/x-www-form-urlencoded" } : {}) },
    body: form ? new URLSearchParams(form) : undefined,
  });
  const data = await r.json();
  if (!r.ok) throw new Error(`Stripe ${path}: ${r.status} ${JSON.stringify(data.error || data)}`);
  return data;
}

async function placeProdigiOrder(env, origin, session) {
  const ship = session.collected_information?.shipping_details || session.shipping_details;
  if (!ship?.address?.line1) throw new Error(`session ${session.id} has no shipping address`);
  const a = ship.address;
  const copies = (session.line_items?.data || []).reduce((n, li) => n + (li.quantity || 0), 0) || 1;
  const ttl = 14 * 24 * 3600;   // Prodigi may download the files again within 14 days
  const assets = [{ printArea: "default", url: await signedFileUrl(env, origin, env.BOOK_FILE, ttl),
                    pageCount: Number(env.PAGE_COUNT) }];
  if (env.SPINE_FILE) assets.push({ printArea: "spine", url: await signedFileUrl(env, origin, env.SPINE_FILE, ttl) });
  const body = {
    merchantReference: session.id,
    idempotencyKey: session.id,   // the same Stripe order can never become two print orders
    shippingMethod: env.SHIPPING_METHOD || "Standard",
    recipient: {
      name: ship.name || session.customer_details?.name,
      email: session.customer_details?.email || undefined,
      phoneNumber: session.customer_details?.phone || undefined,
      address: { line1: a.line1, line2: a.line2 || undefined, postalOrZipCode: a.postal_code,
                 countryCode: a.country, townOrCity: a.city, stateOrCounty: a.state || undefined },
    },
    items: [{ sku: env.PRODIGI_SKU, copies, sizing: "fillPrintArea", assets }],
  };
  const r = await fetch(`${env.PRODIGI_BASE}/orders`, {
    method: "POST",
    headers: { "X-API-Key": env.PRODIGI_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok || !["Created", "CreatedWithIssues", "AlreadyExists"].includes(data.outcome))
    throw new Error(`Prodigi: ${r.status} ${JSON.stringify(data).slice(0, 500)}`);
  return data;
}

async function handleStripe(request, env, origin) {
  const body = await request.text();
  if (!await verifyStripe(request, body, env.STRIPE_WEBHOOK_SECRET)) return new Response("bad signature", { status: 400 });
  const event = JSON.parse(body);
  if (!["checkout.session.completed", "checkout.session.async_payment_succeeded"].includes(event.type))
    return new Response("ignored", { status: 200 });
  // Ask Stripe again rather than trusting the message alone.
  const session = await stripe(env, `checkout/sessions/${event.data.object.id}?expand[]=line_items`);
  if (env.PAYMENT_LINK_ID && session.payment_link !== env.PAYMENT_LINK_ID) return new Response("not the book", { status: 200 });
  if (session.payment_status !== "paid") return new Response("waiting for payment", { status: 200 });
  const result = await placeProdigiOrder(env, origin, session);
  const orderId = result.order?.id;
  console.log(JSON.stringify({ session: session.id, prodigi: orderId, outcome: result.outcome }));
  if (orderId && session.payment_intent) {   // shows the Prodigi order number on the payment in Stripe
    await stripe(env, `payment_intents/${session.payment_intent}`, { "metadata[prodigi_order]": orderId })
      .catch(e => console.log(String(e)));
  }
  return new Response(JSON.stringify({ prodigi: orderId, outcome: result.outcome }), { status: 200 });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/stripe-webhook" && request.method === "POST") {
      try {
        return await handleStripe(request, env, url.origin);
      } catch (e) {
        console.log("FAILED", String(e));
        return new Response("failed, please retry", { status: 500 });   // Stripe will try again
      }
    }
    const m = url.pathname.match(/^\/file\/(.+)$/);
    const name = m && decodeURIComponent(m[1]);
    const allowed = [env.BOOK_FILE, env.SPINE_FILE].filter(Boolean);
    if (name && allowed.includes(name) && (request.method === "GET" || request.method === "HEAD")) {
      const exp = url.searchParams.get("exp") || "";
      const sig = url.searchParams.get("sig") || "";
      if (!/^\d+$/.test(exp) || Number(exp) < Date.now() / 1000) return new Response("expired", { status: 403 });
      if (!safeEqual(sig, await hmac(env.FILE_SECRET, `${name}:${exp}`))) return new Response("forbidden", { status: 403 });
      const obj = await env.BOOK.get(name);
      if (!obj) return new Response("missing", { status: 404 });
      return new Response(request.method === "HEAD" ? null : obj.body, {
        headers: { "Content-Type": "application/pdf", "Content-Length": String(obj.size), "Cache-Control": "private, no-store" },
      });
    }
    return new Response("not found", { status: 404 });
  },
};
