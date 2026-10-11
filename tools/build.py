"""Build davidslv.photography into site/ from David's full-resolution files on the NAS.

  tools/run.sh          # images + HTML for every page (needs the NAS mounted)
  tools/run.sh --html   # HTML only, reuse site/images

Design: proposal F, locked by David on 10 Oct 2026 (source in ~/projects/photography/web/concepts).
Pages are rendered here as static HTML, so search engines and link previews see everything without
running JavaScript. The only script is the drift on photo pairs.

Images: AVIF with a JPEG fallback, 640/1200/2400 px wide, never upscaled. Every JPEG carries IPTC/XMP
creator, credit and copyright; each page has schema.org data so Google Images can show the credit.

Pages live in tools/pages/*.py. Each defines PHOTOS, SEQUENCE and the page's own text.
"""
import hashlib
import html
import importlib.util
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
IMG = SITE / "images"
URL = "https://davidslv.photography"
NAME, EMAIL, IG = "David Silva", "davidslv.london@gmail.com", "https://www.instagram.com/davidslv.photography/"
PORTRAIT = Path.home() / "projects/davidslv.github.com/img/david-silva.jpg"
WIDTHS = (640, 1200)  # plus the cap below
CAP_COLUMN, CAP_WIDE = 1600, 2000  # David, 10 Oct 2026: keep web copies too small for a quality large print
E = html.escape
NAV = [("Work", "/#work"), ("Sunday", "/sunday/"), ("McLaren", "/mclaren/"), ("Ericeira", "/ericeira/"), ("Blackbushe", "/blackbushe/"), ("About", "/#about"), ("Contact", "/#contact")]


def load_pages():
    pages = []
    for f in sorted((ROOT / "tools/pages").glob("*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        pages.append(mod)
    return pages


PAGES = load_pages()
PHOTOS = {k: v for p in PAGES for k, v in p.PHOTOS.items()}


# ---------- images ----------
def load(key):
    ph = PHOTOS[key]
    im = ImageOps.exif_transpose(Image.open(ph["src"])).convert("RGB")
    if ph.get("rotate"):  # degrees, counter-clockwise; small angles level a horizon, cropping to the same aspect
        import math
        w, h = im.size
        t = math.radians(abs(ph["rotate"]) % 180)
        c, sn = abs(math.cos(t)), abs(math.sin(t))
        a = ph.get("aspect", w / h)  # a wider aspect keeps more width after levelling
        hh = min(w / (a * c + sn), h / (a * sn + c))
        im = im.rotate(ph["rotate"], resample=Image.BICUBIC)
        cw, ch = round(hh * a), round(hh)
        im = im.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch))
    if ph.get("crop"):  # fractions of width/height: (left, top, right, bottom)
        l, t, r, b = ph["crop"]
        im = im.crop((round(l * im.width), round(t * im.height), round(r * im.width), round(b * im.height)))
    if ph.get("grade") == "papaya":
        sys.path.insert(0, str(ROOT / "tools/grades"))
        from papaya import grade
        im = grade(im, keep=ph.get("keep", 0.45))
    elif ph.get("grade") == "atlantic":
        sys.path.insert(0, str(ROOT / "tools/grades"))
        from atlantic import grade as atlantic
        im = atlantic(im, ev=ph.get("ev", 0.0), shadows=ph.get("shadows", 0.0))
    elif ph.get("grade") == "cine":
        sys.path.insert(0, str(ROOT / "tools/grades"))
        from atlantic import cine
        im = cine(im, ev=ph.get("ev", 0.0), shadows=ph.get("shadows", 0.0))
    if ph.get("lift"):
        a = np.asarray(im, np.float32) / 255
        lin = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4) * 2 ** ph["lift"]
        s = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * np.clip(lin, 0, 1) ** (1 / 2.4) - 0.055)
        im = Image.fromarray((np.clip(s, 0, 1) * 255 + .5).astype(np.uint8))
    return im


def slug(key):
    words = "".join(c if c.isalnum() else " " for c in PHOTOS[key]["alt"].lower()).split()[:6]
    return f"{key}-" + "-".join(words)


def cap(key):
    wide = any(s[0] in ("hero", "wide") and key in s[1:] for page in PAGES for s in page.SEQUENCE)
    return CAP_WIDE if wide else CAP_COLUMN


def hashed(path):
    """Rename a written file to include a short content hash, so it can be cached for a year (immutable)."""
    path = Path(path)
    h = hashlib.sha1(path.read_bytes()).hexdigest()[:10]
    new = path.with_name(f"{path.stem}.{h}{path.suffix}")
    path.replace(new)
    return new.name


def export_one(key):
    im = load(key)
    out, names = [], {}
    for target in WIDTHS + (cap(key),):
        w = min(target, im.width)
        if out and w == out[-1]:
            break
        v = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        base = IMG / f"{slug(key)}-{w}"
        v.save(f"{base}.jpg", quality=82, optimize=True, progressive=True)
        v.save(f"{base}.avif", quality=60, speed=6)
        out.append(w)
        names[w] = {"jpg": str(base) + ".jpg", "avif": str(base) + ".avif"}
    return key, im.width, im.height, out, names


def tag_jpegs(files):
    """Embed creator, credit and copyright in these JPEGs (IPTC + XMP), the fields Google Images reads."""
    year = date.today().year
    subprocess.run(["exiftool", "-q", "-overwrite_original", "-P",
                    f"-XMP-dc:Creator={NAME}", f"-IPTC:By-line={NAME}",
                    f"-XMP-photoshop:Credit={NAME}", f"-IPTC:Credit={NAME}",
                    f"-XMP-dc:Rights=© {year} {NAME}. All rights reserved.", f"-IPTC:CopyrightNotice=© {year} {NAME}",
                    f"-EXIF:Copyright=© {year} {NAME}", f"-XMP-xmpRights:WebStatement={URL}/#contact",
                    f"-XMP-plus:LicensorURL={URL}/#contact", *map(str, files)], check=True)


def og_image(key, out, top_frac=0.22):
    im = load(key)
    w, h = im.size
    th = round(w * 630 / 1200)
    top = int((h - th) * top_frac)
    im.crop((0, top, w, top + th)).resize((1200, 630), Image.LANCZOS).save(SITE / out, quality=84, optimize=True)


# ---------- HTML pieces ----------
def src(key, meta, w, fmt):
    return "/images/" + meta[key][3][str(w)][fmt]


def picture(key, meta, sizes, eager=False):
    w, h, ws, _ = meta[key]
    avif = ", ".join(f"{src(key, meta, x, 'avif')} {x}w" for x in ws)
    jpg = ", ".join(f"{src(key, meta, x, 'jpg')} {x}w" for x in ws)
    load_attr = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<img src="{src(key, meta, ws[0], "jpg")}" srcset="{jpg}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{E(PHOTOS[key]["alt"])}" {load_attr}></picture>')


def fig(key, meta, sizes):
    ph = PHOTOS[key]
    bits = []
    if ph.get("show_time"):
        bits.append(f'<time class="t" datetime="{ph["taken"]}">{ph["taken"][11:16]}</time>')
    if ph.get("cap"):
        bits.append(f"<span>{E(ph['cap'])}</span>")
    fc = f'<figcaption class="lbl">{"".join(bits)}</figcaption>' if bits else ""
    return f"<figure>{picture(key, meta, sizes)}{fc}</figure>"


PRINT_SIZES = {
    "left": "(max-width:720px) 100vw, min(66vw, 900px)", "right": "(max-width:720px) 100vw, min(52vw, 720px)",
    "right-small": "(max-width:720px) 78vw, min(37vw, 480px)", "centre": "(max-width:720px) 100vw, min(48vw, 640px)",
    "centre-large": "(max-width:720px) 100vw, min(61vw, 820px)", "centre-small": "(max-width:720px) 78vw, min(31vw, 420px)",
}
PAIR_SIZES = "(max-width:720px) 46vw, min(44vw, 560px)"


def sequence_html(page, meta):
    out = []
    for s in page.SEQUENCE:
        k = s[0]
        if k == "hero":
            out.append(f'<section class="hero">{picture(s[1], meta, "100vw", eager=True)}'
                       f'<div class="words"><p class="lbl">{E(page.HERO_LABEL)}</p><h1>{E(page.HERO_TITLE)}</h1></div></section>'
                       '<main id="work">')
        elif k == "part":
            out.append(f'<section class="block part"><p class="lbl">{s[1]}</p><h2>{E(s[2])}</h2><p class="sub">{E(s[3])}</p></section>')
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


def person(meta):
    return {"@type": "Person", "@id": f"{URL}/#david", "name": NAME, "url": f"{URL}/",
            "jobTitle": "Street photographer", "image": f"{URL}/images/{meta['_portrait']}", "email": f"mailto:{EMAIL}",
            "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
            "sameAs": [IG, "https://davidslv.uk/"]}


def image_objects(page, meta):
    out = []
    for s in page.SEQUENCE:
        for key in [x for x in s[1:] if isinstance(x, str) and x in PHOTOS]:
            w, h, ws, _ = meta[key]
            ph = PHOTOS[key]
            o = {"@type": "ImageObject", "@id": f"{URL}{page.PATH}#photo-{key}",
                 "contentUrl": URL + src(key, meta, ws[-1], "jpg"), "width": ws[-1], "height": round(h * ws[-1] / w),
                 "caption": f"{ph['cap']}. {ph['alt']}" if ph.get("cap") else ph["alt"],
                 "creator": {"@id": f"{URL}/#david"}, "creditText": NAME, "copyrightNotice": f"© {NAME}",
                 "copyrightHolder": {"@id": f"{URL}/#david"}, "license": f"{URL}/#contact",
                 "acquireLicensePage": f"{URL}/#contact"}
            if ph.get("taken"):
                o["dateCreated"] = ph["taken"]
            out.append(o)
    return out


def jsonld(page, meta):
    site = {"@type": "WebSite", "@id": f"{URL}/#site", "url": f"{URL}/", "name": f"{NAME} Photography",
            "publisher": {"@id": f"{URL}/#david"}, "inLanguage": "en-GB"}
    hero = page.SEQUENCE[0][1]
    gallery = {"@type": "ImageGallery", "name": page.GALLERY_NAME, "associatedMedia": image_objects(page, meta)}
    node = {"@type": "CollectionPage", "@id": f"{URL}{page.PATH}#page", "url": f"{URL}{page.PATH}", "name": page.HERO_TITLE,
            "headline": page.HERO_TITLE, "description": page.DESC, "inLanguage": "en-GB", "isPartOf": {"@id": f"{URL}/#site"},
            "author": {"@id": f"{URL}/#david"}, "primaryImageOfPage": {"@id": f"{URL}{page.PATH}#photo-{hero}"},
            "dateModified": date.today().isoformat()}
    if page.PATH == "/":
        # The home page is David's own profile: Google's ProfilePage, with the gallery as part of it.
        node.update({"@type": ["ProfilePage", "CollectionPage"], "mainEntity": {"@id": f"{URL}/#david"}, "hasPart": gallery})
    else:
        node["mainEntity"] = gallery
    graph = [person(meta), site, node]
    graph += getattr(page, "extra_jsonld", lambda meta: [])(meta)
    if page.PATH != "/":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Photography", "item": f"{URL}/"},
            {"@type": "ListItem", "position": 2, "name": page.NAV_NAME, "item": f"{URL}{page.PATH}"}]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def head(page, meta):
    hero = page.SEQUENCE[0][1]
    hw = meta[hero][2]
    css = "".join((ROOT / f"tools/{f}").read_text() for f in ("fonts-local.css", "fonts-fallback.css", "site.css"))
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(page.TITLE)}</title>
<meta name="description" content="{E(page.DESC)}">
<link rel="canonical" href="{URL}{page.PATH}">
<meta name="author" content="{NAME}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#efece6">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME} Photography">
<meta property="og:locale" content="en_GB">
<meta property="og:url" content="{URL}{page.PATH}">
<meta property="og:title" content="{E(page.OG_TITLE)}">
<meta property="og:description" content="{E(page.DESC)}">
<meta property="og:image" content="{URL}/{page.OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(PHOTOS[hero]['alt'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="/fonts/Newsreader-normal-300.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/fonts/PublicSans-normal-400.woff2" crossorigin>
<link rel="preload" as="image" type="image/avif" imagesrcset="{", ".join(f"{src(hero, meta, x, 'avif')} {x}w" for x in hw)}" imagesizes="100vw" fetchpriority="high">
<style>{css}</style>
<script type="application/ld+json">{jsonld(page, meta)}</script>
<script type="speculationrules">{{"prerender": [{{"where": {{"and": [{{"href_matches": "/*"}}, {{"not": {{"href_matches": "/images/*"}}}}]}}, "eagerness": "moderate"}}]}}</script>
</head>"""


def header(page):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == page.PATH else ""}>{n}</a>' for n, h in NAV)
    return (f'<body>\n<a class="skip" href="#work">Skip to the photographs</a>\n'
            f'<header class="site"><a class="name" href="/">{NAME}</a><nav aria-label="Main">{links}</nav></header>')


def footer():
    js = (ROOT / "tools/site.js").read_text()
    links = "".join(f'<a href="{h}">{n}</a>' for n, h in NAV)
    return (f'<footer><nav aria-label="Footer">{links}</nav><span>{NAME} · London</span><span>All photographs © {NAME}. Please ask before using them.</span>'
            f'<a href="https://davidslv.uk/" rel="me">Writing and engineering: davidslv.uk</a></footer>\n'
            f"<script>{js}</script>\n</body>\n</html>\n")


def render(page, meta):
    return "\n".join([head(page, meta), header(page), sequence_html(page, meta), page.after(meta), footer()])


# ---------- site files ----------
def extras(meta):
    (SITE / "CNAME").write_text("davidslv.photography\n")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n")
    urls = []
    for page in PAGES:
        imgs = "".join(f"<image:image><image:loc>{URL}{src(k, meta, meta[k][2][-1], 'jpg')}</image:loc></image:image>"
                       for s in page.SEQUENCE for k in s[1:] if isinstance(k, str) and k in PHOTOS)
        urls.append(f"<url><loc>{URL}{page.PATH}</loc><lastmod>{date.today().isoformat()}</lastmod>{imgs}</url>")
    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")
    (SITE / "site.webmanifest").write_text(json.dumps({
        "name": f"{NAME} Photography", "short_name": "David Silva", "start_url": "/", "display": "browser",
        "background_color": "#efece6", "theme_color": "#efece6",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=1))
    (SITE / ".nojekyll").write_text("")
    key = (ROOT / "tools/indexnow-key").read_text().strip()  # IndexNow: Bing, Yandex, Seznam, Naver (tools/indexnow.sh)
    (SITE / f"{key}.txt").write_text(key + "\n")
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
        ImageDraw.Draw(im).text((n / 2, n * .53), "DS", font=ImageFont.truetype(font, int(n * .47)), fill=(239, 236, 230), anchor="mm")
        im.save(SITE / name)


if __name__ == "__main__":
    IMG.mkdir(parents=True, exist_ok=True)
    meta_file = ROOT / "tools/images.json"
    meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
    meta = {k: (tuple(v) if k in PHOTOS else v) for k, v in meta.items()}
    if "--html" not in sys.argv:
        todo = [k for k in PHOTOS if k not in meta or "--all" in sys.argv]
        with ProcessPoolExecutor(6) as ex:
            exported = list(ex.map(export_one, todo))
        portrait = IMG / "david-silva.jpg"
        Image.open(PORTRAIT).save(portrait, quality=86, optimize=True)
        assets = {}
        for page in PAGES:
            if hasattr(page, "assets"):
                assets.update(page.assets(IMG))
        new_jpgs = [n["jpg"] for *_, names in exported for n in names.values()] + [str(portrait)] + \
                   [n["jpg"] for sizes in assets.values() for n in sizes.values()]
        tag_jpegs(new_jpgs)  # before hashing, so the hash covers the final bytes
        for k, w, h, ws, names in exported:
            meta[k] = (w, h, ws, {str(x): {f: hashed(n) for f, n in v.items()} for x, v in names.items()})
        meta["_portrait"] = hashed(portrait)
        meta["_assets"] = {name: {str(w): {f: hashed(n) for f, n in v.items()} for w, v in sizes.items()}
                           for name, sizes in assets.items()}
        for page in PAGES:
            og_image(page.SEQUENCE[0][1], page.OG_IMAGE, getattr(page, "OG_TOP", 0.22))
        icons()
        meta_file.write_text(json.dumps(meta, indent=0))
    for page in PAGES:
        out = SITE / page.PATH.strip("/") / "index.html" if page.PATH != "/" else SITE / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(page, meta))
        print("built", out.relative_to(ROOT))
    extras(meta)
