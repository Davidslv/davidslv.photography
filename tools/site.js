// Photo pairs drift a little against each other as you scroll. Nothing else moves.
(() => {
  const pairs = [...document.querySelectorAll(".pair")];
  if (!pairs.length || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  let tick = false;
  const drift = () => {
    tick = false;
    for (const p of pairs) {
      const r = p.getBoundingClientRect();
      const t = (innerHeight - r.top) / (innerHeight + r.height);
      p.style.setProperty("--d", ((Math.min(1, Math.max(0, t)) - .5) * 80).toFixed(1));
    }
  };
  addEventListener("scroll", () => { if (!tick) { tick = true; requestAnimationFrame(drift); } }, { passive: true });
  drift();
})();
