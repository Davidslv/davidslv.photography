"""/sunday/: the car meets and the book It Started on a Sunday (David's picks, 10 Oct 2026).

Photos are the book's own KERBSIDE-graded masters. Titles and times are the book's (the Nikon's clock stayed on
summer time, so winter times are an hour earlier than its EXIF; the book prints the corrected time).
"""
import calendar
import subprocess
from datetime import datetime
from pathlib import Path

from PIL import Image

BOOK = Path("/Volumes/David Photography/Photography Projects/It Started on a Sunday (book)")
MASTERS = BOOK / "01_book_source/car-meet-book/masters_picks"
PDF = BOOK / "03_outputs/It_Started_on_a_Sunday_v4_picks_KERBSIDE1.0_proof.pdf"

PATH = "/sunday/"
NAV_NAME = "Sunday"
TITLE = "It Started on a Sunday · Car meet photographs by David Silva"
OG_TITLE = "It Started on a Sunday · David Silva"
DESC = ("Candid photographs of car meets in and around London, and the people who love the cars. "
        "From the book It Started on a Sunday, out 15 November 2026.")
HERO_LABEL = "Cars and the people who love them"
HERO_TITLE = "It Started on a Sunday"
GALLERY_NAME = "Sunday car meets, November 2024 to October 2026"
OG_IMAGE = "og-sunday.jpg"
OG_TOP = 0.45
LEAD = "2025-03-02"


def nice_date(iso):
    d = datetime.fromisoformat(iso)
    return f"{d.day} {calendar.month_name[d.month]} {d.year}"


def ph(id_, alt, title, taken):
    date, f = id_.split("/")
    lead = date == LEAD
    return dict(src=MASTERS / date / f"{f}_full.jpg", alt=alt, taken=taken, show_time=lead,
                cap=title if lead else f"{title} · {nice_date(taken)}")


PHOTOS = {
    's3706': ph('2025-03-02/DSC_3706', 'Owners stand around a vintage open racing car on frosted grass in the morning fog.', 'Frost, Fog and an Open Racer', '2025-03-02T08:10:00+00:00'),
    's3575': ph('2025-03-02/DSC_3575', 'A red hatchback faces the camera on double yellow lines in a misty, tree-lined road.', 'Head-On, Double Yellows', '2025-03-02T08:03:00+00:00'),
    's3756': ph('2025-03-02/DSC_3756', 'The cockpit of a vintage racing car: a wooden steering wheel, brass dials and worn leather.', "The Racer's Office", '2025-03-02T08:14:00+00:00'),
    's3782': ph('2025-03-02/DSC_3782', 'Two men in winter coats lean over a vintage car; one opens his hands to explain the engine.', 'Show and Tell', '2025-03-02T08:15:00+00:00'),
    's4027': ph('2025-03-02/DSC_4027', 'People and cars line a road that runs into hazy low sun.', 'Into the Haze', '2025-03-02T08:55:00+00:00'),
    's4098': ph('2025-03-02/DSC_4098', 'Owners gather around classic cars parked along the edge of a green.', 'Bonnet Up', '2025-03-02T08:59:00+00:00'),
    's4138': ph('2025-03-02/DSC_4138', 'Four polished air trumpets on the engine of a blue car, its bonnet open.', 'Four Trumpets', '2025-03-02T09:01:00+00:00'),
    's4476': ph('2025-03-02/DSC_4476', 'A silver grand tourer and a red coupé side by side in low winter sun.', 'Low Sun, Long Shadows', '2025-03-02T09:23:00+00:00'),
    's5054': ph('2024-11-03/DSC_5054', 'A pale blue Alfa Romeo convertible parked on a quiet road in autumn.', 'Where It Started', '2024-11-03T10:56:00+00:00'),
    's8831': ph('2024-12-01/DSC_8831', 'A man bends to look closely at the side of a red supercar on a wet road.', 'A Closer Look', '2024-12-01T10:22:00+00:00'),
    's2157': ph('2025-01-05/DSC_2157', 'People under red and white umbrellas around a dark blue saloon parked on wet grass.', 'Umbrellas Up', '2025-01-05T09:42:00+00:00'),
    's5190': ph('2025-04-06/DSC_5190', 'Owners talk around a vintage open tourer parked in morning sun.', 'Old Hands', '2025-04-06T08:43:00+01:00'),
    's5734': ph('2025-05-04/DSC_5734', 'Two men talk beside a classic Porsche, a red classic car in front, under a pale sky.', 'Whale Tail', '2025-05-04T08:18:00+01:00'),
    's5951': ph('2025-05-04/DSC_5951', 'A man pushes a baby in a pram past a red sports car.', 'Twelve Days', '2025-05-04T08:41:00+01:00'),
    's6239': ph('2025-05-04/DSC_6239', 'A man in a flat cap sits in a black open sports car.', 'Flat Cap', '2025-05-04T09:50:00+01:00'),
    'si2262': ph('2026-02-28/IMG_2262', 'The bonnet and headlight of a black classic Porsche, bare trees reflected in the paint.', 'Black Paint, Bare Trees', '2026-02-28T08:19:00+00:00'),
    's1254': ph('2026-02-28/DSC_1254', 'A crowd gathers around sports cars on a London square lined with white stucco houses.', 'Where Everyone Gathered', '2026-02-28T09:06:00+00:00'),
    's2003': ph('2026-03-01/DSC_2003', 'People and their dogs stand around a white Porsche on a grey morning.', 'Dogs and a GT3 RS', '2026-03-01T08:27:00+00:00'),
    'si3781': ph('2026-04-05/IMG_3781', "Over a photographer's shoulder, a red vintage racing car drives down a road lined with people.", 'Over His Shoulder', '2026-04-05T08:07:00+01:00'),
    's4196': ph('2026-04-15/DSC_4196', 'Two men talk among Porsches parked on the grass at an evening meet.', 'The Conversation', '2026-04-15T19:23:00+01:00'),
    's5291': ph('2026-10-04/DSC_5291', 'A small group still talking in a gravel car park as the meet winds down.', 'Still Talking', '2026-10-04T10:43:00+01:00'),
}

SEQUENCE = [
    ("hero", "s3706"),
    ("part", "Part one", "One Sunday", "2 March 2025, Southside Common, Wimbledon Village. From 08:03 to 09:23."),
    ("line", "The common was white with frost and the street was lost in fog."),
    ("wide", "s3575"),
    ("pair", "s3756", "s3782"),
    ("print", "s4027", "left"),
    ("print", "s4098", "right"),
    ("print", "s4138", "centre-small"),
    ("line", "By twenty past nine the fog had burned off and the sun was low and hard across the road."),
    ("wide", "s4476"),
    ("part", "Part two", "Other Sundays", "Twelve more mornings and one evening, November 2024 to October 2026."),
    ("print", "s5054", "left"),
    ("print", "s8831", "right-small"),
    ("wide", "s2157"),
    ("print", "s5190", "centre"),
    ("pair", "s5734", "s5951"),
    ("print", "s6239", "right-small"),
    ("print", "si2262", "centre"),
    ("wide", "s1254"),
    ("print", "s2003", "left"),
    ("print", "si3781", "centre-large"),
    ("wide", "s4196"),
    ("print", "s5291", "centre"),
]

IG = "https://www.instagram.com/davidslv.photography/"
GUMROAD = "https://davidslv.gumroad.com/l/it-started-on-a-sunday"
# Stripe Payment Link for the printed hardcover (live, 14 Oct 2026).
HARDCOVER = "https://buy.stripe.com/cNiaEQdKGgzY93LcjJb3q00"   # LIVE (test link: https://buy.stripe.com/test_7sY6oA1zLaWCc4Q0G0f7i00)
WIDTHS = {"book-cover": (800, 1600), "book-spread-umbrellas": (800, 1600, 2000), "book-spread-show-and-tell": (800, 1600, 2000)}


def assets(img_dir):
    """Cover and two spreads, rendered from the book PDF (pages 1, 24-25 and 32-33)."""
    tmp = img_dir.parent.parent / "tools/.pdf"
    tmp.mkdir(exist_ok=True)
    for n in (1, 24, 25, 32, 33):
        subprocess.run(["pdftoppm", "-r", "220", "-png", "-f", str(n), "-l", str(n), "-singlefile", str(PDF),
                        str(tmp / f"p{n:03d}")], check=True)
    pages = {n: Image.open(tmp / f"p{n:03d}.png").convert("RGB") for n in (1, 24, 25, 32, 33)}
    gap = 0
    for name, (a, b) in (("book-spread-umbrellas", (24, 25)), ("book-spread-show-and-tell", (32, 33))):
        l, r = pages[a], pages[b]
        im = Image.new("RGB", (l.width + r.width + gap, max(l.height, r.height)), (255, 255, 255))
        im.paste(l, (0, 0)); im.paste(r, (l.width + gap, 0))
        pages[name] = im
    pages["book-cover"] = pages[1]
    out = {}
    for name in ("book-cover", "book-spread-umbrellas", "book-spread-show-and-tell"):
        im = pages[name]
        out[name] = {}
        for w in WIDTHS[name]:
            w2 = min(w, im.width)
            v = im.resize((w2, round(im.height * w2 / im.width)), Image.LANCZOS)
            v.save(img_dir / f"{name}-{w2}.jpg", quality=84, optimize=True, progressive=True)
            v.save(img_dir / f"{name}-{w2}.avif", quality=62, speed=6)
            out[name][w2] = {"jpg": str(img_dir / f"{name}-{w2}.jpg"), "avif": str(img_dir / f"{name}-{w2}.avif")}
    return out


def book_img(meta, name, alt, sizes, ratio):
    files = meta["_assets"][name]
    ws = sorted(files, key=int)
    avif = ", ".join(f"/images/{files[w]['avif']} {w}w" for w in ws)
    jpg = ", ".join(f"/images/{files[w]['jpg']} {w}w" for w in ws)
    w = int(ws[-1])
    h = round(w * ratio)
    return (f'<picture><source type="image/avif" srcset="{avif}" sizes="{sizes}"><img src="/images/{files[ws[0]]["jpg"]}" '
            f'srcset="{jpg}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async"></picture>')


def after(meta):
    cover = book_img(meta, "book-cover", "The cover of It Started on a Sunday: owners around a vintage racing car on frosted grass in fog.",
                     "(max-width:720px) 100vw, 46vw", 595.276 / 841.89)
    s1 = book_img(meta, "book-spread-umbrellas", "A spread from the book: people under umbrellas around a blue saloon on the left, the story and how it was shot on the right.",
                  "(max-width:720px) 100vw, 1100px", 595.276 / (2 * 841.89))
    s2 = book_img(meta, "book-spread-show-and-tell", "A spread from the book: two men at a vintage car on the left, the story of the photograph on the right.",
                  "(max-width:720px) 100vw, 1100px", 595.276 / (2 * 841.89))
    return f"""<section class="book" id="book">
<div class="book-head">
  <div class="book-cover">{cover}</div>
  <div class="book-text"><p class="lbl">The book · hardcover available now</p>
  <h2><em>It Started on a Sunday</em></h2>
  <p class="sub">Cars and the people who love them.</p>
  <p>72 photographs from fourteen car meets, November 2024 to October 2026. Each one comes with its story, how it was shot, and the KERBSIDE look it was graded with. Five pages go behind the shot and show the frames either side of the one I kept.</p>
  <div class="buy">
    <div><p class="lbl">Hardcover</p><p>A4 landscape, 164 pages, printed to order. £44.99 plus £6.99 UK delivery.</p>
    <p><a class="btn" href="{HARDCOVER}">Buy the hardcover · £44.99</a></p>
    <p class="note">UK delivery only for now. Each copy is printed when you order and posted within 7 to 12 working days. <a style="color:inherit" href="/terms/">Terms of sale</a></p></div>
    <div><p class="lbl">PDF</p><p>The same book as an A4 landscape PDF. £17.99.</p>
    <p><a class="btn" href="{GUMROAD}">Get the PDF · £17.99</a></p>
    <p class="note">Download it straight away and read it on an iPad, laptop or phone.</p></div>
  </div>
  <p style="font-size:.9em"><a style="color:inherit" href="{IG}" rel="me">Follow @davidslv.photography for the launch</a></p></div>
</div>
<figure class="spread">{s1}<figcaption class="lbl">From Winter: Umbrellas Up</figcaption></figure>
<figure class="spread">{s2}<figcaption class="lbl">From Early spring: Show and Tell</figcaption></figure>
<div class="terms" id="hardcover-terms">
<div><p class="lbl">Delivery</p><p>The hardcover is printed to order by my print partner, Prodigi, and posted from the UK. Delivery is £6.99 and takes 7 to 12 working days. UK addresses only for now.</p></div>
<div><p class="lbl">Returns</p><p>If your copy arrives damaged or misprinted, email me a photo within 30 days and I'll send a new one. You can also cancel within 14 days of receiving it and send it back unused for a refund of the book price.</p></div>
<div><p class="lbl">Your details</p><p>Payments are handled by Stripe. Your name, address, email and phone go to Prodigi only to print and post your book. I'll only send you news if you ticked yes at checkout.</p></div>
<div><p class="lbl">Questions</p><p><a href="mailto:hello@davidslv.photography">hello@davidslv.photography</a><br><a href="/terms/">Full terms of sale</a></p></div>
</div>
</section>
<a class="next" href="/mclaren/"><span class="lbl">Next</span><span class="next-title">Made to be used</span><span class="next-sub">A day at the McLaren Technology Centre</span></a>
<section class="more" id="contact">
<div><p class="lbl">More photographs</p><h3><a href="/">From last light to last train</a></h3><p>One Saturday in London, and other nights.</p></div>
<div><p class="lbl">Presets</p><h3>KERBSIDE</h3><p>The looks this book was graded with. 26 Lightroom presets for car-meet light. <a href="https://davidslv.gumroad.com/l/kerbside-preset">KERBSIDE on Gumroad · £8.99</a></p></div>
<div><p class="lbl">Contact</p><h3>Photographs of your meet</h3><p>I photograph club meets and events. Email for rates.<br><a href="mailto:hello@davidslv.photography">hello@davidslv.photography</a><br><a href="{IG}" rel="me">@davidslv.photography</a></p></div>
</section>"""


def extra_jsonld(meta):
    return [{"@type": "Book", "@id": "https://davidslv.photography/sunday/#book", "name": "It Started on a Sunday",
             "alternativeHeadline": "Cars and the People Who Love Them", "author": {"@id": "https://davidslv.photography/#david"},
             "datePublished": "2026-11-15", "bookFormat": "https://schema.org/EBook", "inLanguage": "en-GB",
             "image": "https://davidslv.photography/images/" + meta["_assets"]["book-cover"][max(meta["_assets"]["book-cover"], key=int)]["jpg"], "genre": "Photography",
             "about": "Classic and sports car meets in and around London, and the people at them",
             "url": "https://davidslv.photography/sunday/#book"}]
