"""/ericeira/: skimboarding at Ericeira, 26 February 2012, the first afternoon with a DSLR (built 11 Oct 2026).

Sources are the 40 JPEGs sold on Gumroad (https://davidslv.gumroad.com/l/hSKX), straight from a Sony DSLR-A350
with the 55-200 mm kit zoom. No grade: they are shown as they were sold. Times are the camera's own, 17:05 to 17:29.
Words are David's, from the Gumroad page.
"""
from pathlib import Path

N = Path("/Users/davidslv/Downloads/skimboard_photos_by_david_silva")

PATH = "/ericeira/"
NAV_NAME = "Ericeira"
TITLE = "The first afternoon · Skimboarding at Ericeira, 2012, photographed by David Silva"
OG_TITLE = "The first afternoon · David Silva"
DESC = ("Ericeira, 26 February 2012: the first afternoon David Silva held a DSLR. Skimboarders running into the "
        "white water below the cliffs, in the order it happened.")
HERO_LABEL = "Ericeira, Portugal · 26 February 2012"
HERO_TITLE = "The first afternoon"
GALLERY_NAME = "Skimboarding at Ericeira, 26 February 2012"
OG_IMAGE = "og-ericeira.jpg"
OG_TOP = 0.35


def ph(n, time, alt, **kw):
    return dict(src=N / f"DSC0{n}.JPG", alt=alt, cap=None, taken=f"2012-02-26T{time}", show_time=True, **kw)


PHOTOS = {
    "e8694": ph(8694, "17:18:28", "A skimboarder crouches low on a board as a green wave rises behind him.", crop=(0, 0.12, 1, 0.92)),
    "e8490": ph(8490, "17:05:52", "A skimboarder in a black wetsuit rides through white water, arms out for balance."),
    "e8494": ph(8494, "17:06:02", "A man in a wetsuit walks out of the surf with a pale board under his arm."),
    "e8495": ph(8495, "17:06:05", "A man carries his board back through the shallow foam."),
    "e8529": ph(8529, "17:09:06", "A skimboarder holds his board in front of the cliffs, looking out to sea."),
    "e8549": ph(8549, "17:09:40", "Two skimboarders on the sand at the foot of the rocks, waves breaking behind them."),
    "e8537": ph(8537, "17:09:16", "A skimboarder turns on the lip of a wave, one arm thrown up."),
    "e8618": ph(8618, "17:13:16", "A small figure rides a board across the face of a wave, far out."),
    "e8635": ph(8635, "17:14:48", "A man sprints along the wet sand into the light, board in hand."),
    "e8655": ph(8655, "17:16:29", "A skimboarder walks up the beach with his board under one arm."),
    "e8657": ph(8657, "17:16:33", "A man bends to set his green board down on the wet sand."),
    "e8659": ph(8659, "17:16:49", "The edge of a board stuck in the sand, footprints all around."),
    "e8661": ph(8661, "17:17:04", "Close up, the worn grip and stickers on a board lying in the sand."),
    "e8678": ph(8678, "17:17:44", "A skimboarder runs down the slope of the beach toward the water."),
    "e8687": ph(8687, "17:18:23", "Backlit, a man runs into the shallows holding his board ready to drop."),
    "e8725": ph(8725, "17:19:50", "A skimboarder carves into the foam of a breaking wave."),
    "e8739": ph(8739, "17:20:18", "Bare feet and the bottom of a wetsuit leg on the sand, a board edge in the corner."),
    "e8773": ph(8773, "17:22:28", "A skimboarder stands on the sand below the yellow cliffs, board at his side."),
    "e8784": ph(8784, "17:22:59", "A man runs along the shore, board held out in front of him."),
    "e8798": ph(8798, "17:23:20", "A skimboarder walks out of the sea with a green board."),
    "e8822": ph(8822, "17:25:17", "A skimboarder leans into a turn on a blue wave."),
    "e8843": ph(8843, "17:26:44", "Mid-stride, a man drops his board on the wet sand, splashing."),
    "e8848": ph(8848, "17:26:48", "A rider is thrown off the back of a wave in a burst of spray."),
    "e8849": ph(8849, "17:26:49", "A rider stands up on a wave with his arms out."),
    "e8853": ph(8853, "17:27:10", "A skimboarder in a wetsuit holds a green speckled board, another figure on the beach behind."),
    "e8863": ph(8863, "17:27:38", "A man wades out among the rocks and white water carrying a board."),
    "e8892": ph(8892, "17:28:22", "A man runs out of the rocks with a bright green board, another skimboarder in the water behind."),
    "e8904": ph(8904, "17:29:22", "Late light, a last run along the water's edge."),
}

SEQUENCE = [
    ("hero", "e8694"),
    ("part", "Ericeira, 26 February 2012", "Off the rocks",
     "I had a DSLR in my hands for the first time. I pointed it at people skimboarding off the rocks and I did not "
     "really know what I was doing."),
    ("wide", "e8490"),
    ("pair", "e8494", "e8495"),
    ("wide", "e8529"),
    ("print", "e8549", "left"),
    ("wide", "e8537"),
    ("part", "17:13", "The run", "Run, drop the board, jump on. Again and again."),
    ("print", "e8618", "right-small"),
    ("wide", "e8635"),
    ("pair", "e8655", "e8678"),
    ("pair", "e8659", "e8661"),
    ("wide", "e8687"),
    ("print", "e8725", "centre"),
    ("part", "17:22", "White water", "Some are sharp. Some are not. That was the afternoon."),
    ("pair", "e8773", "e8798"),
    ("wide", "e8784"),
    ("wide", "e8822"),
    ("pair", "e8848", "e8849"),
    ("wide", "e8843"),
    ("pair", "e8853", "e8739"),
    ("wide", "e8863"),
    ("wide", "e8892"),
    ("wide", "e8904"),
    ("line", "I came home with more than 3,000 photos. These are some of the ones I kept."),
]

GUMROAD = "https://davidslv.gumroad.com/l/hSKX"


def after(meta):
    return f"""<section class="pitch" id="first-sale">
<p class="lbl">The first sale</p>
<h2>It was also the first thing I ever sold online.</h2>
<p class="pitch-lede">Forty photographs from that afternoon. Rocks, white water, wetsuits and boards. Someone paid for them, the first time anyone paid for a photograph of mine. I am leaving it up.</p>
<p><a class="btn" href="{GUMROAD}">The 40 photos on Gumroad</a></p>
<p class="pitch-small">Pay what you want, from €2. Sony DSLR-A350, 55–200 mm kit zoom. Shown here as they came out of the camera.</p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
