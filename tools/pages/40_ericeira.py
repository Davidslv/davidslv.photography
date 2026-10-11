"""/ericeira/: skimboarding at Ericeira, 26 February 2012, the first afternoon with a DSLR (built 11 Oct 2026).

Sources are the 40 JPEGs sold on Gumroad (https://davidslv.gumroad.com/l/hSKX), straight from a Sony DSLR-A350
with the 55-200 mm kit zoom. Graded for the site with cine() in tools/grades/atlantic.py (teal shadows and water, warm skin and sand, green boards kept). The Gumroad files are ungraded. Times are the camera's own, 17:05 to 17:29.
Words are David's: the Gumroad page and his own account of the day (11 Oct 2026). The camera was a friend's.
"""
from pathlib import Path

N = Path("/Users/davidslv/Downloads/skimboard_photos_by_david_silva")

PATH = "/ericeira/"
NAV_NAME = "Ericeira"
TITLE = "The first afternoon · Skimboarding at Ericeira, 2012, photographed by David Silva"
OG_TITLE = "The first afternoon · David Silva"
DESC = ("Ericeira, 26 February 2012: the first afternoon David Silva held a DSLR, a friend's camera. Skimboarders "
        "running into the white water below the cliffs, in the order it happened.")
HERO_LABEL = "Ericeira, Portugal · 26 February 2012"
HERO_TITLE = "The first afternoon"
GALLERY_NAME = "Skimboarding at Ericeira, 26 February 2012"
OG_IMAGE = "og-ericeira.jpg"
OG_TOP = 0.3


def ph(n, time, alt, **kw):
    return dict(src=N / f"DSC0{n}.JPG", alt=alt, cap=None, taken=f"2012-02-26T{time}", show_time=True,
                grade="cine", **kw)


PHOTOS = {
    "e8490": ph(8490, "17:05:52", "A skimboarder in a black wetsuit rides through white water, arms out for balance.", ev=0.35, shadows=1.0),
    "e8529": ph(8529, "17:09:06", "A skimboarder holds a green board in front of the cliffs, looking out to sea."),
    "e8549": ph(8549, "17:09:40", "Three skimboarders on the sand at the foot of the rocks, a wave breaking behind them."),
    "e8537": ph(8537, "17:09:16", "A skimboarder turns on the lip of a wave, one arm thrown up.", crop=(0.22, 0.1, 1, 0.833)),
    "e8635": ph(8635, "17:14:48", "Backlit, a man sprints along the wet sand toward the water.", ev=0.25, shadows=1.0),
    "e8655": ph(8655, "17:16:29", "A skimboarder walks up the beach with his board under one arm."),
    "e8661": ph(8661, "17:17:04", "Close up, the worn grip and stickers on a board standing in the sand."),
    "e8739": ph(8739, "17:20:18", "A bare foot kicks up sand, the tail of a board in the corner."),
    "e8773": ph(8773, "17:22:28", "A skimboarder stands on the sand below the cliffs, board at his side."),
    "e8784": ph(8784, "17:22:59", "A man runs along the shore, board held out in front of him."),
    "e8822": ph(8822, "17:25:17", "A skimboarder leans into a turn on a blue wave.", ev=0.6, shadows=1.0),
    "e8843": ph(8843, "17:26:44", "Mid-stride, a man about to drop his board on the wet sand."),
    "e8849": ph(8849, "17:26:49", "A rider on a green board turns at the top of a breaking wave."),
    "e8853": ph(8853, "17:27:10", "A skimboarder holds a green speckled board, another figure on the beach behind."),
    "e8863": ph(8863, "17:27:38", "A man wades out among the rocks and white water carrying a board."),
}

SEQUENCE = [
    ("hero", "e8537"),
    ("part", "Ericeira, 26 February 2012", "Off the rocks",
     "I went to the beach with a friend and he lent me his camera. It was the first time I had a DSLR in my hands. "
     "I had never shot before, and I had nothing planned for that afternoon."),
    ("wide", "e8490"),
    ("pair", "e8529", "e8549"),
    ("part", "17:14", "The run", "They skipped across the water, went up the wave and came down again. I thought it was fascinating."),
    ("wide", "e8635"),
    ("wide", "e8655"),
    ("print", "e8661", "left"),
    ("print", "e8739", "right-small"),
    ("part", "17:22", "White water", "They were doing their own thing. I was doing mine, trying a camera for the first time."),
    ("print", "e8773", "centre"),
    ("wide", "e8784"),
    ("wide", "e8822"),
    ("pair", "e8843", "e8849"),
    ("print", "e8853", "left"),
    ("wide", "e8863"),
    ("line", "I didn't get them all right. These are the best photos I took that day."),
]

GUMROAD = "https://davidslv.gumroad.com/l/hSKX"



def after(meta):
    return f"""<section class="pitch" id="first-sale">
<p class="lbl">The first sale</p>
<h2>It was also the first thing I ever sold online.</h2>
<p class="pitch-lede">Forty photographs from that afternoon, straight from the camera. Someone paid for them, the first time anyone paid for a photograph of mine. I am leaving it up.</p>
<p><a class="btn" href="{GUMROAD}">The 40 photos on Gumroad</a></p>
<p class="pitch-small">Pay what you want, from €2. Shot on 26 February 2012 with a Sony DSLR-A350 and a 55–200 mm zoom, lent to me by a friend.</p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
