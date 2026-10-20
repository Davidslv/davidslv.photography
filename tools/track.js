/* Anonymous reading stats for this site (site-stats Worker). No cookies, nothing stored on the device,
   no IP kept. Skipped for browsers sending Global Privacy Control or Do Not Track, and for automation. */
(() => {
  try {
    if (navigator.webdriver || navigator.globalPrivacyControl || navigator.doNotTrack === "1") return;
    const END = "https://site-stats.davidslv-london.workers.dev/e";
    const pv = (crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36))
      .replace(/-/g, "").slice(0, 32);
    const w = innerWidth, coarse = matchMedia("(pointer: coarse)").matches;
    const device = w < 720 ? "phone" : coarse ? "tablet" : "desktop";
    const q = new URLSearchParams(location.search);
    let ref = q.get("utm_source") || "";
    if (!ref && document.referrer) {
      try { const h = new URL(document.referrer).hostname.replace(/^www\./, ""); if (h !== location.hostname) ref = h; } catch (e) {}
    }
    let seq = 0, maxScroll = 0, ended = 0, visMs = 0, last = null;
    let visSince = document.visibilityState === "visible" ? performance.now() : null;
    const photos = {}, clicks = {}, onScreen = new Map();
    const now = () => performance.now();

    const pid = img => {
      const f = (img.currentSrc || img.src || "").split("/").pop() || "";
      const m = f.match(/^([a-z]{1,3}\d{2,6}[a-z]?)[-.]/i);
      return m ? m[1] : (img.alt || "photo").slice(0, 40);
    };
    const stopPhoto = id => {
      const t = onScreen.get(id);
      if (t != null) { photos[id] = (photos[id] || 0) + (now() - t) / 1000; onScreen.delete(id); }
    };
    const io = new IntersectionObserver(entries => {
      for (const en of entries) {
        const id = pid(en.target);
        if (en.intersectionRatio >= 0.5 && document.visibilityState === "visible") {
          if (!onScreen.has(id)) onScreen.set(id, now());
          last = id;
        } else stopPhoto(id);
      }
    }, { threshold: [0, 0.5] });
    const watch = () => document.querySelectorAll("main img, section img, figure img").forEach(i => io.observe(i));

    let ticking = false;
    const onScroll = () => {
      if (ticking) return; ticking = true;
      requestAnimationFrame(() => {
        const d = document.documentElement;
        const p = Math.min(100, Math.round((scrollY + innerHeight) / Math.max(1, d.scrollHeight) * 100));
        if (p > maxScroll) maxScroll = p;
        if (p >= 97) ended = 1;
        ticking = false;
      });
    };

    const send = () => {
      const t = now();
      const running = [...onScreen.keys()];
      running.forEach(stopPhoto);                       // bank time so far, then restart the timers
      if (document.visibilityState === "visible") running.forEach(id => onScreen.set(id, t));
      const secs = Math.round((visMs + (visSince != null ? t - visSince : 0)) / 1000);
      const ph = {};
      for (const [k, v] of Object.entries(photos)) if (v >= 0.5) ph[k] = Math.round(v);
      const body = JSON.stringify({ pv, seq: ++seq, path: location.pathname, ref, device, vw: w,
        scroll: maxScroll, ended, secs, last_photo: last, photos: ph, clicks });
      try { navigator.sendBeacon(END, new Blob([body], { type: "text/plain" })); } catch (e) {}
    };

    document.addEventListener("click", ev => {
      const a = ev.target.closest && ev.target.closest("a, summary");
      if (!a) return;
      let k = null;
      if (a.tagName === "SUMMARY") k = "menu";
      else {
        const h = a.getAttribute("href") || "";
        if (/buy\.stripe\.com/.test(h)) k = "buy_hardcover";
        else if (/gumroad\.com/.test(h)) k = "get_pdf";
        else if (/instagram\.com/.test(h)) k = "instagram";
        else if (h.startsWith("mailto:")) k = "email";
        else if (h.startsWith("#")) k = "jump:" + h.slice(1);
        else { try { const u = new URL(h, location.href); k = u.hostname === location.hostname ? "page:" + u.pathname : "out:" + u.hostname; } catch (e) {} }
      }
      if (k && a.dataset && a.dataset.track) clicks[k + "@" + a.dataset.track] = (clicks[k + "@" + a.dataset.track] || 0) + 1;   // which button: data-track="hero" etc.
      if (k) { clicks[k] = (clicks[k] || 0) + 1; if (k === "buy_hardcover" || k === "get_pdf") send(); }
    }, true);

    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") {
        if (visSince != null) { visMs += now() - visSince; visSince = null; }
        send();
        [...onScreen.keys()].forEach(stopPhoto);
      } else visSince = now();
    });
    addEventListener("pagehide", send);
    addEventListener("scroll", onScroll, { passive: true });
    const start = () => { watch(); onScroll(); setTimeout(send, 15000); };   // one early summary for very short visits
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
  } catch (e) {}
})();
