"""Reading report from the site-stats D1 database.  python3 tools/stats-worker/report.py [days]  (default 28)
Per page: views, devices, sources, how far people scroll, real viewing time, where they stop, top photos, clicks."""
import json, subprocess, sys
from collections import Counter, defaultdict
from pathlib import Path

days = int(sys.argv[1]) if len(sys.argv) > 1 else 28
q = f"SELECT path,ref,device,scroll,ended,secs,last_photo,photos,clicks FROM views WHERE day >= date('now','-{days} days')"
out = subprocess.run(["npx", "--yes", "wrangler@4.151.0", "d1", "execute", "site-events", "--remote", "--json", "--command", q],
                     cwd=Path(__file__).parent, capture_output=True, text=True, check=True).stdout
rows = json.loads(out)[0]["results"]
by = defaultdict(list)
for r in rows:
    by[r["path"]].append(r)
pct = lambda a, b: f"{round(100 * a / b)}%" if b else "-"
med = lambda xs: sorted(xs)[len(xs) // 2] if xs else 0
print(f"Last {days} days: {len(rows)} page views\n")
for path, rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    n = len(rs)
    print(f"== {path}  ({n} views)")
    print("   devices:", dict(Counter(r["device"] for r in rs).most_common()))
    print("   from:   ", dict(Counter(r["ref"] or "direct/unknown" for r in rs).most_common(6)))
    print("   reached 25/50/75/end:", " / ".join(pct(sum(r["scroll"] >= t for r in rs), n) for t in (25, 50, 75)),
          "/", pct(sum(r["ended"] for r in rs), n))
    for dev in ("phone", "desktop", "tablet"):
        d = [r for r in rs if r["device"] == dev]
        if d: print(f"   {dev}: median {med([r['secs'] for r in d])}s on page, reached end {pct(sum(r['ended'] for r in d), len(d))}")
    print("   stopped at (last photo seen):", Counter(r["last_photo"] for r in rs if r["last_photo"] and not r["ended"]).most_common(5))
    photo = Counter()
    for r in rs:
        for k, v in json.loads(r["photos"] or "{}").items(): photo[k] += v
    print("   most looked-at photos (total seconds):", photo.most_common(8))
    clicks = Counter()
    for r in rs:
        clicks.update(json.loads(r["clicks"] or "{}"))
    print("   clicks:", dict(clicks.most_common(10)), "\n")
