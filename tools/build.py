"""Build davidslv.photography into site/ from David's full-resolution files on the NAS.

  ~/projects/LUT/.venv/bin/python tools/build.py          # images + HTML (needs the NAS mounted)
  ~/projects/LUT/.venv/bin/python tools/build.py --html   # HTML only, reuse site/img

Design: proposal F, locked by David on 10 Oct 2026 (source in ~/projects/photography/web/concepts).
The page is rendered here as static HTML, so search engines and link previews see everything
without running JavaScript. The only script is the drift on photo pairs.

Images: AVIF with a JPEG fallback, 1200 and 2400 px wide, never upscaled. Each JPEG carries
IPTC/XMP creator, credit and copyright, and the page has schema.org ImageObject data, so Google
Images can show the credit and copyright.
"""
import html
import json
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
IMG = SITE / "img"
URL = "https://davidslv.photography"
P = Path("/Volumes/David Photography/Photography Projects")
FULL = P / "Shutter Hub - City Series London (Nov 2026)/_tools/full"
PORTRAIT = Path.home() / "projects/davidslv.github.com/img/david-silva.jpg"
NAME, EMAIL, IG = "David Silva", "davidslv.london@gmail.com", "https://www.instagram.com/davidslv.photography/"
TITLE = "David Silva · Street photographer in London"
DESC = ("Candid street photographs of people in London's light, mostly late in the day and after dark. "
        "One Saturday, from last light to last train, and other nights.")

# id: (source, alt, caption, taken "YYYY-MM-DD HH:MM:SS" or None)
SRC = {
    147: ("After Hours/Enhanced/DSC_7356-Enhanced-NR.jpg", "Two women smile into a phone held up for a photo in a crowded street.", None, "2024-10-19 16:45:53"),
    108: ("After Hours/Enhanced/DSC_6835-Enhanced-NR.jpg", "A young woman covers her mouth and laughs at a table with a bunch of roses.", None, "2024-10-19 14:59:53"),
    109: ("After Hours/Enhanced/DSC_6845-Enhanced-NR.jpg", "A young man in sunglasses and a black jacket walks through a crowd.", None, "2024-10-19 15:00:55"),
    141: ("After Hours/Enhanced/DSC_7269-Enhanced-NR.jpg", "An older man in glasses reads at a pavement café table, a coffee cup beside him.", None, "2024-10-19 16:35:54"),
    145: ("After Hours/Enhanced/DSC_7297-Enhanced-NR.jpg", "A man walks away down a narrow cobbled lane lined with black bollards, in low sun.", None, "2024-10-19 16:41:09"),
    146: ("After Hours/Enhanced/DSC_7335-Enhanced-NR.jpg", "Two young women laugh as they walk, one with pink hair holding an orange drink.", None, "2024-10-19 16:44:21"),
    153: ("After Hours/Enhanced/DSC_7405-Enhanced-NR.jpg", "A woman in a patterned scarf smiles in a busy street.", None, "2024-10-19 16:49:48"),
    172: ("After Hours/Enhanced/DSC_7593-Enhanced-NR.jpg", "Two chefs in aprons work at the pass of a busy restaurant kitchen.", None, "2024-10-19 17:18:04"),
    175: ("After Hours/Enhanced/DSC_7713-Enhanced-NR.jpg", "A dancer in a sequinned dress performs on a square at dusk as a man films her.", None, "2024-10-19 18:26:19"),
    208: ("After Hours/Revisited/DSC_7756-Enhanced-NR.jpg", "An older woman with white hair looks out from a red bus window at night.", None, "2024-10-19 18:45:11"),
    181: ("After Hours/Enhanced/DSC_7772-Enhanced-NR.jpg", "An older woman smiles behind the lit window of a bus, shopping on her lap.", None, "2024-10-19 18:49:27"),
    188: ("After Hours/Enhanced/DSC_7839-Enhanced-NR.jpg", "Three people cross a street at night in front of All Souls church, its spire lit gold.", "All Souls, Langham Place", "2024-10-19 19:15:53"),
    203: ("After Hours/Revisited/Book Reserved/DSC_8137-Enhanced-NR.jpg", "A full Tube carriage, passengers sitting in two rows holding blue poles.", "The Tube", "2024-10-19 21:15:48"),
    201: ("After Hours/Enhanced/DSC_8158-Enhanced-NR.jpg", "An empty Tube carriage, blue seats on both sides.", "The Tube", "2024-10-19 21:40:52"),
    55: ("After Hours/DSC_0908.jpg", "An older woman in a bright scarf and green jacket stands on a street at dusk beside a man.", None, None),
    56: ("After Hours/DSC_3187.jpg", "A woman with red hair in a leopard coat and red satin skirt walks along a street at night.", None, None),
    57: ("After Hours/DSC_3200.jpg", "People stand in a queue on a pavement at night.", None, None),
    215: (FULL / "DSC_5906/03 03 Last Orders.jpg", "Two people look into a lit cake shop window under flowers and a neon sign.", "9 October 2026", "2026-10-09 22:02:00"),
    211: ("After Hours/Revisited/DSC_9353.jpg", "The lit front of Beigel Bake on Brick Lane at night, a worker inside.", "Beigel Bake, Brick Lane", "2024-10-23 00:38:28"),
    40: ("After Hours/2024-10-28-book-photos/DSC_8954.jpg", "A young man with a green guitar on his back walks across a bridge at night.", "Tower Bridge", "2024-10-22 23:13:55"),
    212: (FULL / "DSC_6125/02 02 Late Show.jpg", "A woman walks down the curved, lamp-lit stairs into Piccadilly Circus station.", "Piccadilly Circus station, 9 October 2026", "2026-10-09 22:16:00"),
    53: ("After Hours/8 December 2024/DSC_9891-2.jpg", "Two figures in the lit doorway of Bow Road station at night.", "Bow Road", None),
    38: ("After Hours/2024-10-28-book-photos/DSC_8681.jpg", "A man walks alone down a dark lane beside a brick wall.", None, "2024-10-22 22:26:07"),
}
LIFT = {212: 0.35}
SHOW_TIME = {k for k, v in SRC.items() if v[3] and v[3].startswith("2024-10-19")}

SEQUENCE = [
    ("hero", 147),
    ("part", "Part one", "One Saturday", "19 October 2024, from 14:59 to 21:40. One camera, one 35mm lens."),
    ("print", 108, "left"), ("print", 109, "right-small"), ("print", 141, "centre"), ("print", 145, "right-small"),
    ("pair", 146, 153), ("wide", 172), ("print", 175, "centre-large"), ("pair", 208, 181),
    ("line", "For one frame everyone was moving in a different direction under the church."),
    ("print", 188, "centre-large"), ("pair", 203, 201),
    ("part", "Part two", "Other nights", "Soho, Brick Lane, the river and the stations. 2024 to 2026."),
    ("wide", 55), ("pair", 56, 57), ("wide", 215), ("print", 211, "left"), ("pair", 40, 212),
    ("print", 53, "right"), ("print", 38, "centre-small"),
]
WIDTHS = (640, 1200, 2400)


def load(i):
    src = SRC[i][0]
    im = ImageOps.exif_transpose(Image.open(src if isinstance(src, Path) else P / src)).convert("RGB")
    if i in LIFT:
        a = np.asarray(im, np.float32) / 255
        lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4) * 2 ** LIFT[i]
        s = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, 1) ** (1 / 2.4) - 0.055)
        im = Image.fromarray((np.clip(s, 0, 1) * 255 + .5).astype(np.uint8))
    return im


def slug(i):
    alt = SRC[i][1].lower()
    words = "".join(c if c.isalnum() else " " for c in alt).split()[:6]
    return f"{i:03d}-" + "-".join(words)


def export_one(i):
    im = load(i)
    out = []
    for target in WIDTHS:
        w = min(target, im.width)
        if out and w == out[-1]:
            break
        v = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        base = IMG / f"{slug(i)}-{w}"
        v.save(f"{base}.jpg", quality=82, optimize=True, progressive=True)
        v.save(f"{base}.avif", quality=60, speed=6)
        out.append(w)
    return i, im.width, im.height, out


def tag_jpegs():
    """Embed creator, credit and copyright in every JPEG (IPTC + XMP), the fields Google Images reads."""
    year = date.today().year
    subprocess.run(["exiftool", "-q", "-overwrite_original", "-P",
                    f"-XMP-dc:Creator={NAME}", f"-IPTC:By-line={NAME}",
                    f"-XMP-photoshop:Credit={NAME}", f"-IPTC:Credit={NAME}",
                    f"-XMP-dc:Rights=© {year} {NAME}. All rights reserved.", f"-IPTC:CopyrightNotice=© {year} {NAME}",
                    f"-EXIF:Copyright=© {year} {NAME}", f"-XMP-xmpRights:WebStatement={URL}/#contact",
                    f"-XMP-plus:LicensorURL={URL}/#contact", str(IMG)], check=True)


def og_image():
    im = load(147)
    w, h = im.size
    th = round(w * 630 / 1200)
    top = int((h - th) * 0.22)
    im.crop((0, top, w, top + th)).resize((1200, 630), Image.LANCZOS).save(SITE / "og.jpg", quality=84, optimize=True)


# ---------- HTML ----------
E = html.escape


def picture(i, meta, sizes, eager=False, cls=""):
    w, h, ws = meta[i]
    s = slug(i)
    avif = ", ".join(f"img/{s}-{x}.avif {x}w" for x in ws)
    jpg = ", ".join(f"img/{s}-{x}.jpg {x}w" for x in ws)
    load_attr = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="img/{s}-{ws[0]}.jpg" srcset="{jpg}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{E(SRC[i][1])}" {load_attr}></picture>')


def fig(i, meta, sizes):
    _, alt, cap, taken = SRC[i]
    bits = []
    if i in SHOW_TIME:
        bits.append(f'<time class="t" datetime="{taken.replace(" ", "T")}+01:00">{taken[11:16]}</time>')
    if cap:
        bits.append(f"<span>{E(cap)}</span>")
    fc = f'<figcaption class="lbl">{"".join(bits)}</figcaption>' if bits else ""
    return f"<figure>{picture(i, meta, sizes)}{fc}</figure>"


PRINT_SIZES = {
    "left": "(max-width:720px) 100vw, min(66vw, 900px)", "right": "(max-width:720px) 100vw, min(52vw, 720px)",
    "right-small": "(max-width:720px) 78vw, min(37vw, 480px)", "centre": "(max-width:720px) 100vw, min(48vw, 640px)",
    "centre-large": "(max-width:720px) 100vw, min(61vw, 820px)", "centre-small": "(max-width:720px) 78vw, min(31vw, 420px)",
}
PAIR_SIZES = "(max-width:720px) 46vw, min(44vw, 560px)"


def body(meta):
    out = []
    for s in SEQUENCE:
        k = s[0]
        if k == "hero":
            out.append(f'<section class="hero">{picture(s[1], meta, "100vw", eager=True)}'
                       '<div class="words"><p class="lbl">Human street moments · London</p>'
                       '<h1>From last light to last train</h1></div></section><main id="work">')
        elif k == "part":
            out.append(f'<section class="block part"><p class="lbl">{s[1]}</p><h2>{s[2]}</h2><p class="sub">{s[3]}</p></section>')
        elif k == "line":
            out.append(f'<section class="block line"><p>{E(s[1])}</p></section>')
        elif k == "wide":
            out.append(f'<section class="block wide">{fig(s[1], meta, "100vw")}</section>')
        elif k == "print":
            out.append(f'<section class="block"><div class="print {s[2]}">{fig(s[1], meta, PRINT_SIZES[s[2]])}</div></section>')
        elif k == "pair":
            land = meta[s[1]][0] > meta[s[1]][1]
            out.append(f'<section class="block pair{" landscape" if land else ""}">'
                       f'{fig(s[1], meta, PAIR_SIZES)}{fig(s[2], meta, PAIR_SIZES)}</section>')
    out.append("</main>")
    return "\n".join(out)


def jsonld(meta):
    person = {"@type": "Person", "@id": f"{URL}/#david", "name": NAME, "url": f"{URL}/",
              "jobTitle": "Street photographer", "image": f"{URL}/img/david-silva.jpg", "email": f"mailto:{EMAIL}",
              "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
              "sameAs": [IG, "https://davidslv.uk/"]}
    images = []
    for s in SEQUENCE:
        for i in [x for x in s[1:] if isinstance(x, int)]:
            w, h, ws = meta[i]
            _, alt, cap, taken = SRC[i]
            o = {"@type": "ImageObject", "@id": f"{URL}/#photo-{i}", "contentUrl": f"{URL}/img/{slug(i)}-{ws[-1]}.jpg",
                 "width": w if ws[-1] == w else ws[-1], "height": round(h * ws[-1] / w),
                 "caption": alt if not cap else f"{cap}. {alt}", "creator": {"@id": f"{URL}/#david"},
                 "creditText": NAME, "copyrightNotice": f"© {NAME}", "copyrightHolder": {"@id": f"{URL}/#david"},
                 "license": f"{URL}/#contact", "acquireLicensePage": f"{URL}/#contact"}
            if taken:
                o["dateCreated"] = taken.replace(" ", "T") + ("+01:00" if taken.startswith("2024-10") else "+01:00")
            images.append(o)
    page = {"@type": "CollectionPage", "@id": f"{URL}/#page", "url": f"{URL}/", "name": "From last light to last train",
            "headline": "From last light to last train", "description": DESC, "inLanguage": "en-GB",
            "isPartOf": {"@type": "WebSite", "@id": f"{URL}/#site", "url": f"{URL}/", "name": f"{NAME} Photography",
                         "publisher": {"@id": f"{URL}/#david"}, "inLanguage": "en-GB"},
            "author": {"@id": f"{URL}/#david"}, "primaryImageOfPage": {"@id": f"{URL}/#photo-147"},
            "mainEntity": {"@type": "ImageGallery", "name": "One Saturday and other nights in London", "associatedMedia": images}}
    return json.dumps({"@context": "https://schema.org", "@graph": [person, page]}, ensure_ascii=False, indent=1)


def page(meta):
    hero = meta[147]
    hs = slug(147)
    css = (ROOT / "tools/fonts-local.css").read_text() + (ROOT / "tools/site.css").read_text()
    js = (ROOT / "tools/site.js").read_text()
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(TITLE)}</title>
<meta name="description" content="{E(DESC)}">
<link rel="canonical" href="{URL}/">
<meta name="author" content="{NAME}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#efece6">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME} Photography">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{URL}/">
<meta property="og:title" content="From last light to last train · {NAME}">
<meta property="og:description" content="{E(DESC)}">
<meta property="og:image" content="{URL}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(SRC[147][1])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="/fonts/Newsreader-normal-300.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/PublicSans-normal-400.woff2" crossorigin>
<link rel="preload" as="image" type="image/avif" imagesrcset="{", ".join(f"img/{hs}-{x}.avif {x}w" for x in hero[2])}" imagesizes="100vw" fetchpriority="high">
<style>{css}</style>
<script type="application/ld+json">{jsonld(meta)}</script>
</head>
<body>
<a class="skip" href="#work">Skip to the photographs</a>
<header class="site"><a class="name" href="/">{NAME}</a>
<nav aria-label="Main"><a href="#work">Work</a><a href="#about">About</a><a href="#contact">Contact</a></nav></header>
{body(meta)}
<section class="about" id="about">
<img src="img/david-silva.jpg" width="800" height="800" loading="lazy" decoding="async" alt="Portrait of {NAME}.">
<div><p class="lbl">About</p><h2>I photograph people in London’s light.</h2>
<p>Someone crossing a wet street, waiting in a doorway, laughing on a corner. Mostly late in the day and after dark, with one camera and a 35mm lens.</p>
<p>On Sunday mornings I photograph the car meets, for the same reason.</p></div></section>
<section class="more" id="contact">
<div><p class="lbl">The book</p><h3><em>It Started on a Sunday</em></h3><p>The car meets of Surrey and south-west London. Out 15 November 2026.</p></div>
<div><p class="lbl">Presets</p><h3>LAST ROLL and KERBSIDE</h3><p>The Lightroom looks I grade with. <a href="https://davidslv.gumroad.com/l/last-roll">LAST ROLL</a> · <a href="https://davidslv.gumroad.com/l/kerbside-preset">KERBSIDE</a></p></div>
<div><p class="lbl">Contact</p><h3>Commissions, prints and licensing</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}" rel="me">@davidslv.photography</a></p></div>
</section>
<footer><span>{NAME} · London</span><span>All photographs © {NAME}. Please ask before using them.</span><a href="https://davidslv.uk/" rel="me">Writing and engineering: davidslv.uk</a></footer>
<script>{js}</script>
</body>
</html>
"""


def extras():
    (SITE / "CNAME").write_text("davidslv.photography\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    imgs = "".join(f"<image:image><image:loc>{URL}/img/{slug(i)}-{WIDTHS[-1] if (IMG / f'{slug(i)}-{WIDTHS[-1]}.jpg').exists() else WIDTHS[0]}.jpg</image:loc></image:image>"
                   for s in SEQUENCE for i in s[1:] if isinstance(i, int))
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        f"<url><loc>{URL}/</loc><lastmod>{date.today().isoformat()}</lastmod>{imgs}</url>\n</urlset>\n")
    (SITE / "site.webmanifest").write_text(json.dumps({
        "name": f"{NAME} Photography", "short_name": "David Silva", "start_url": "/", "display": "browser",
        "background_color": "#efece6", "theme_color": "#efece6",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    (SITE / ".nojekyll").write_text("")
    (SITE / "404.html").write_text(f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Not found · {NAME}</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#efece6;color:#1b1916;font:300 22px/1.4 Georgia,serif;text-align:center;padding:16px}}a{{color:inherit}}</style></head>
<body><p>This page isn’t here.<br><a href="/">Back to the photographs</a></p></body></html>
""")


def icons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#1b1916"/>'
           '<text x="32" y="43" text-anchor="middle" font-family="Georgia, serif" font-size="30" fill="#efece6">DS</text></svg>')
    (SITE / "favicon.svg").write_text(svg)
    from PIL import ImageDraw, ImageFont
    font = "/System/Library/Fonts/Supplemental/Georgia.ttf"
    for name, n in (("favicon-32.png", 32), ("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
        im = Image.new("RGB", (n, n), (27, 25, 22))
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(font, int(n * .47))
        d.text((n / 2, n * .53), "DS", font=f, fill=(239, 236, 230), anchor="mm")
        im.save(SITE / name)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    ids = [x for s in SEQUENCE for x in s[1:] if isinstance(x, int)]
    meta_file = ROOT / "tools/images.json"
    if "--html" not in sys.argv:
        with ProcessPoolExecutor(6) as ex:
            meta = {i: (w, h, ws) for i, w, h, ws in ex.map(export_one, ids)}
        Image.open(PORTRAIT).save(IMG / "david-silva.jpg", quality=86, optimize=True)
        tag_jpegs()
        og_image()
        icons()
        meta_file.write_text(json.dumps({str(k): v for k, v in meta.items()}))
    meta = {int(k): tuple(v) for k, v in json.loads(meta_file.read_text()).items()}
    (SITE / "index.html").write_text(page(meta))
    extras()
    print("built", SITE / "index.html", len(ids), "photos")
