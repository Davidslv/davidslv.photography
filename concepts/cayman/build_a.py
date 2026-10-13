"""Concept A, "Four lights": the page takes on the light of each session; a camera clock and a 24-hour day line
track the photo in view. Static HTML from photos.json (real camera times and exif); one small script for the clock
and the colour change. Prototype only (13 Oct 2026): concepts/cayman/a/index.html.

    python3 concepts/cayman/build_a.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = {p["key"]: p for p in json.loads((HERE / "photos.json").read_text())}
E = html.escape

# one red, Guards Red at hue ~3 deg: #b3221d on light pages, #e5443d on dark (AA large text both, 13 Oct 2026)
# light per session: background, ink, muted, accent (each pair AA for body text)
LIGHTS = {
    "rain": ("#29313b", "#edf0f2", "#a9b3bd", "#e5443d"),
    "moor": ("#ead7b2", "#241c12", "#6a5638", "#b3221d"),
    "april": ("#f4f2ec", "#1b1b1a", "#66645e", "#b3221d"),
    "cabin": ("#17120e", "#f2e2c9", "#b39b7c", "#e5443d"),
}
CHAPTERS = [
    ("rain", "15 March 2026", "17:56", "Rain", [
        ("full", "c2530"), ("offset-r", "c2697"), ("pair", "c2680", "c2718"), ("full", "c2709")]),
    ("moor", "21 March 2026", "06:14", "The moor", [
        ("trio", "i3038", "i3040", "i3042"), ("tall", "i3051"), ("full", "c2738"), ("full", "c2783"),
        ("full", "c2817"), ("tall", "i3055"), ("offset-r", "c2848")]),
    ("april", "19 April 2026", "06:50", "Low sun", [
        ("offset-l", "c4838"), ("tall", "c4846")]),
    ("cabin", "13 October 2026", "17:21", "Behind the wheel", [
        ("offset-l", "c8404"), ("full", "c8464"), ("trio", "c8549", "c8564", "c8554"), ("full", "c8706"),
        ("offset-r", "c8715"), ("end", "c8784")]),
]


def picture(k, sizes, eager=False):
    p = P[k]
    ws = sorted(int(w) for w in p["src"])
    ss = lambda ext: ", ".join(f'{p["src"][str(w)][ext]} {w}w' for w in ws)  # noqa: E731
    h = round(p["h"] * ws[-1] / p["w"])
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{ss("avif")}" sizes="{sizes}">'
            f'<img src="{p["src"][str(ws[1] if len(ws) > 1 else ws[0])]["jpg"]}" srcset="{ss("jpg")}" sizes="{sizes}" '
            f'width="{ws[-1]}" height="{h}" alt="{E(p["alt"])}" {load}></picture>')


def cap(k):
    p, x = P[k], P[k]["exif"]
    t = p["taken"][11:16]
    bits = [t, f'{round(x["focal"])}mm' if x.get("focal") else None, f'f/{x["f"]:g}' if x.get("f") else None,
            x.get("shutter"), f'ISO {x["iso"]}' if x.get("iso") else None]
    return f'<figcaption>{" · ".join(b for b in bits if b)}</figcaption>'


def fig(k, sizes, cls="", eager=False):
    return f'<figure class="ph {cls}" data-t="{P[k]["taken"]}">{picture(k, sizes, eager)}{cap(k)}</figure>'


def block(b):
    kind, *ks = b
    if kind == "full":
        return fig(ks[0], "100vw", "full")
    if kind == "end":
        return fig(ks[0], "100vw", "full end")
    if kind in ("offset-l", "offset-r"):
        return fig(ks[0], "(min-width:56rem) 62vw, 100vw", kind)
    if kind == "tall":
        return fig(ks[0], "(min-width:56rem) 40vw, 90vw", "tall")
    if kind == "pair":
        return '<div class="pair">' + "".join(fig(k, "(min-width:48rem) 48vw, 100vw") for k in ks) + "</div>"
    if kind == "trio":
        return '<div class="trio">' + "".join(fig(k, "(min-width:48rem) 32vw, 100vw") for k in ks) + "</div>"


def dayline():
    marks = "".join(f'<li style="--x:{(int(t[:2]) * 60 + int(t[3:])) / 1440:.4f}" data-light="{c}"><span>{t}</span></li>'
                    for c, _, t, _, _ in CHAPTERS)
    hours = "".join(f'<li style="--x:{h / 24:.4f}">{h:02d}</li>' for h in (0, 6, 12, 18, 24))
    return f'<ol class="hours" aria-hidden="true">{hours}</ol><ol class="marks">{marks}</ol>'


CSS = """
@font-face{font-family:News;src:url(/site/fonts/Newsreader-normal-300.woff2) format("woff2");font-weight:300;font-display:swap}
@font-face{font-family:News;src:url(/site/fonts/Newsreader-italic-300.woff2) format("woff2");font-weight:300;font-style:italic;font-display:swap}
@font-face{font-family:Sans;src:url(/site/fonts/PublicSans-normal-400.woff2) format("woff2");font-weight:400;font-display:swap}
:root{--bg:#f4f2ec;--ink:#1b1b1a;--muted:#66645e;--accent:#b3221d;--x:0;--fade:1.4s}
@media (prefers-reduced-motion:reduce){:root{--fade:0s}}
*{box-sizing:border-box;margin:0;padding:0}
html{background:var(--bg);color:var(--ink);transition:background-color var(--fade) ease,color var(--fade) ease}
body{font:400 1rem/1.6 Sans,system-ui,sans-serif;font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:var(--bg);padding:.5rem .8rem;z-index:30}.skip:focus{left:8px}
.lbl{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--muted);transition:color var(--fade)}
header.top{position:fixed;inset:0 0 auto;display:flex;justify-content:space-between;align-items:center;padding:14px 16px;z-index:20;mix-blend-mode:normal}
header.top a{text-decoration:none;font:300 1.05rem News,serif}
nav.ch{display:flex;gap:1.1rem;font-size:.78rem}
nav.ch a{text-decoration:none;color:var(--muted)}
nav.ch a[aria-current=true]{color:var(--ink);text-decoration:underline;text-underline-offset:.3em}
@media (max-width:44rem){nav.ch{display:none}}
.hero{min-height:100svh;display:grid;align-content:end;padding:0 16px 9vh}
.hero h1{font:300 clamp(4.2rem,17vw,15rem)/.86 News,serif;letter-spacing:-.04em;margin-left:-.04em}
.hero p{max-width:34rem;margin-top:1.4rem;font:300 italic clamp(1.15rem,2.2vw,1.5rem)/1.4 News,serif;color:var(--muted)}
.day{margin:3rem 0 0;max-width:46rem;position:relative}
.day ol{list-style:none;position:relative;height:1.6rem}
.day .hours{border-top:1px solid currentColor;opacity:.55}
.day .hours li{position:absolute;left:calc(var(--x)*100%);transform:translateX(-50%);font-size:.66rem;top:.35rem;color:var(--muted)}
.day .marks{position:absolute;inset:-.95rem 0 auto;height:0}
.day .marks li{position:absolute;left:calc(var(--x)*100%);transform:translateX(-50%)}
.day .marks li:before{content:"";display:block;width:.55rem;height:.55rem;border-radius:50%;background:var(--accent);margin:0 auto .2rem}
.day .marks span{font-size:.66rem;position:absolute;bottom:1.1rem;left:50%;transform:translateX(-50%);white-space:nowrap}
.day .marks li:nth-child(even) span{bottom:auto;top:1.9rem}
.day .marks li[data-light=april] span{transform:translateX(-100%)}.day .marks li[data-light=moor] span{transform:translateX(0)}
.chapter{padding:22vh 0 10vh}
.opener{padding:0 16px;display:grid;gap:.4rem;margin-bottom:12vh}
.opener .t{font:300 clamp(5rem,22vw,19rem)/.8 News,serif;letter-spacing:-.05em;margin-left:-.05em;color:var(--accent);transition:color var(--fade)}
.opener h2{font:300 italic clamp(2rem,5vw,3.6rem)/1 News,serif}
.ph{margin:0 0 14vh}
.ph img{display:block;width:100%;height:auto}
figcaption{font-size:.7rem;letter-spacing:.12em;color:var(--muted);margin-top:.6rem;padding:0 16px;transition:color var(--fade)}
.full figcaption{padding:0 16px}
.offset-l,.offset-r{width:min(62vw,62rem)}
.offset-l{margin-left:16px}.offset-r{margin-left:auto;margin-right:16px}
.offset-l figcaption,.offset-r figcaption{padding:0}
.tall{width:min(40vw,34rem);margin-left:auto;margin-right:auto}
.tall figcaption{padding:0}
.pair,.trio{display:grid;gap:16px;padding:0 16px;margin-bottom:14vh;align-items:end}
.pair{grid-template-columns:1fr 1fr}
.pair .ph:nth-child(2){margin-bottom:-6vh}
.trio{grid-template-columns:repeat(3,1fr)}
.pair .ph,.trio .ph{margin:0}.pair figcaption,.trio figcaption{padding:0}
@media (max-width:48rem){.offset-l,.offset-r,.tall{width:auto;margin-left:16px;margin-right:16px}.pair,.trio{grid-template-columns:1fr}.pair .ph:nth-child(2){margin-bottom:0}}
.end{margin-bottom:0}
.sign{padding:16vh 16px 10vh;display:grid;gap:1rem}
.sign p:first-child{font:300 clamp(3.4rem,12vw,10rem)/.9 News,serif;letter-spacing:-.04em}
.clock[hidden]{display:none}.clock{position:fixed;left:16px;bottom:14px;z-index:20;display:grid;gap:.15rem;pointer-events:none}
.clock b{font:300 clamp(1.6rem,3.2vw,2.6rem)/1 News,serif;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.clock span{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.clock i{display:block;width:clamp(6rem,14vw,11rem);height:1px;background:currentColor;opacity:.35;position:relative;margin-top:.35rem}
.clock i:after{content:"";position:absolute;top:-3px;left:calc(var(--x)*100%);width:7px;height:7px;border-radius:50%;background:var(--accent);transform:translateX(-50%);transition:left .6s ease}
@media (prefers-reduced-motion:reduce){.clock i:after{transition:none}}
footer{padding:4rem 16px 6rem;border-top:1px solid color-mix(in srgb,var(--ink) 18%,transparent);display:flex;justify-content:space-between;flex-wrap:wrap;gap:1rem;font-size:.8rem}
"""

JS = """
(()=>{const root=document.documentElement,L=__LIGHTS__;const chs=[...document.querySelectorAll('.chapter')];
const set=c=>{const v=L[c];if(!v)return;root.style.setProperty('--bg',v[0]);root.style.setProperty('--ink',v[1]);root.style.setProperty('--muted',v[2]);root.style.setProperty('--accent',v[3]);
document.querySelectorAll('nav.ch a').forEach(a=>a.setAttribute('aria-current',a.hash==='#'+c));};
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)set(e.target.id)})},{rootMargin:'-45% 0px -45% 0px'});chs.forEach(c=>io.observe(c));
const hero=document.querySelector('.hero');new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)set('april')})},{rootMargin:'-45% 0px -45% 0px'}).observe(hero);
const clock=document.querySelector('.clock'),b=clock.querySelector('b'),s=clock.querySelector('span');
const ph=[...document.querySelectorAll('.ph,.opener [data-t]')];const D=['January','February','March','April','May','June','July','August','September','October','November','December'];
let cur=null;const show=f=>{if(f===cur)return;cur=f;const t=f.dataset.t;b.textContent=t.slice(11,19);const d=new Date(t);s.textContent=d.getDate()+' '+D[d.getMonth()]+' '+d.getFullYear();
const m=+t.slice(11,13)*60+ +t.slice(14,16);root.style.setProperty('--x',(m/1440).toFixed(4));clock.hidden=false;};
new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){clock.hidden=true;cur=null}})},{rootMargin:'-50% 0px -50% 0px'}).observe(hero);
const io2=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)show(e.target)})},{rootMargin:'-50% 0px -50% 0px'});ph.forEach(f=>io2.observe(f));
})();
"""


def build():
    chapters = []
    for c, date, t, title, blocks in CHAPTERS:
        body = "".join(block(b) for b in blocks)
        chapters.append(f'<section class="chapter" id="{c}" aria-labelledby="{c}-h"><div class="opener">'
                        f'<p class="lbl" data-t="{P[blocks[0][1]]["taken"][:11]}{t}:00">{date}</p><p class="t" aria-hidden="true">{t}</p><h2 id="{c}-h">{title}<span class="sr"> · {t}</span></h2></div>{body}</section>')
    nav = "".join(f'<a href="#{c}">{title}</a>' for c, _, _, title, _ in CHAPTERS)
    lights = json.dumps(LIGHTS)
    doc = f"""<!doctype html>
<html lang="en-GB">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>My Cayman · Four lights · David Silva</title>
<meta name="description" content="David Silva's red Porsche Cayman in four kinds of light: rain at dusk, sunrise on the moor, low April sun, and behind the wheel.">
<meta name="robots" content="noindex">
<link rel="preload" href="/site/fonts/Newsreader-normal-300.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}</style></head>
<body>
<a class="skip" href="#rain">Skip to the photographs</a>
<header class="top"><a href="/">David Silva</a><nav class="ch" aria-label="Chapters">{nav}</nav></header>
<main>
<section class="hero" aria-labelledby="t"><p class="lbl">Porsche Cayman · 2026</p><h1 id="t">My Cayman</h1>
<p>Four kinds of light. Rain at dusk, sunrise on the moor, low April sun, and the last of the day behind the wheel.</p>
<div class="day" aria-label="When each set was taken, on a 24-hour line">{dayline()}</div></section>
{"".join(chapters)}
<section class="sign" aria-label="End"><p>My Cayman</p><p class="lbl">Photographs by David Silva · Nikon Z 6II</p></section>
</main>
<div class="clock" aria-hidden="true" hidden><b>00:00:00</b><span></span><i></i></div>
<footer><a href="/">David Silva · London</a><span class="lbl">Prototype · concept A, four lights</span></footer>
<script>{JS.replace("__LIGHTS__", lights)}</script>
</body></html>
"""
    (HERE / "a").mkdir(exist_ok=True)
    (HERE / "a/index.html").write_text(doc)
    print(HERE / "a/index.html")


if __name__ == "__main__":
    build()
