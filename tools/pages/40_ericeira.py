"""/ericeira/: skimboarding at Ericeira, 26 February 2012, the first afternoon with a DSLR (built 11 Oct 2026).

Sources are the 40 JPEGs sold on Gumroad (https://davidslv.gumroad.com/l/hSKX), straight from a Sony DSLR-A350
with the 55-200 mm kit zoom. Graded for the site with tools/grades/atlantic.py (quiet colour, green boards kept). The Gumroad files are ungraded. Times are the camera's own, 17:05 to 17:29.
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
OG_TOP = 0.3


def ph(n, time, alt, **kw):
    return dict(src=N / f"DSC0{n}.JPG", alt=alt, cap=None, taken=f"2012-02-26T{time}", show_time=True,
                grade="atlantic", **kw)


PHOTOS = {
    "e8868": ph(8868, "17:28:00", "A small figure rides along the face of a long green wave, white water in front.", crop=(0, 0.16, 1, 0.79), ev=0.35),
    "e8490": ph(8490, "17:05:52", "A skimboarder in a black wetsuit rides through white water, arms out for balance."),
    "e8529": ph(8529, "17:09:06", "A skimboarder holds a green board in front of the cliffs, looking out to sea."),
    "e8549": ph(8549, "17:09:40", "Three skimboarders on the sand at the foot of the rocks, a wave breaking behind them."),
    "e8537": ph(8537, "17:09:16", "A skimboarder turns on the lip of a wave, one arm thrown up."),
    "e8635": ph(8635, "17:14:48", "Backlit, a man sprints along the wet sand toward the water."),
    "e8655": ph(8655, "17:16:29", "A skimboarder walks up the beach with his board under one arm."),
    "e8661": ph(8661, "17:17:04", "Close up, the worn grip and stickers on a board standing in the sand."),
    "e8739": ph(8739, "17:20:18", "A bare foot kicks up sand, the tail of a board in the corner."),
    "e8773": ph(8773, "17:22:28", "A skimboarder stands on the sand below the cliffs, board at his side."),
    "e8784": ph(8784, "17:22:59", "A man runs along the shore, board held out in front of him."),
    "e8822": ph(8822, "17:25:17", "A skimboarder leans into a turn on a blue wave.", ev=0.3),
    "e8843": ph(8843, "17:26:44", "Mid-stride, a man about to drop his board on the wet sand."),
    "e8849": ph(8849, "17:26:49", "A rider on a green board turns at the top of a breaking wave."),
    "e8853": ph(8853, "17:27:10", "A skimboarder holds a green speckled board, another figure on the beach behind."),
    "e8863": ph(8863, "17:27:38", "A man wades out among the rocks and white water carrying a board."),
}

SEQUENCE = [
    ("hero", "e8868"),
    ("part", "Ericeira, 26 February 2012", "Off the rocks",
     "I had a DSLR in my hands for the first time. I pointed it at people skimboarding off the rocks and I did not "
     "really know what I was doing."),
    ("wide", "e8490"),
    ("print", "e8529", "left"),
    ("wide", "e8537"),
    ("print", "e8549", "right-small"),
    ("part", "17:14", "The run", "Run, drop the board, jump on. Again and again."),
    ("wide", "e8635"),
    ("pair", "e8655", "e8661"),
    ("print", "e8739", "right-small"),
    ("part", "17:22", "White water", "The last minutes on the beach."),
    ("print", "e8773", "centre"),
    ("wide", "e8784"),
    ("wide", "e8822"),
    ("pair", "e8843", "e8849"),
    ("print", "e8853", "left"),
    ("wide", "e8863"),
    ("line", "Twenty-three minutes, more than 3,000 frames. These are the ones I kept."),
]

GUMROAD = "https://davidslv.gumroad.com/l/hSKX"
EMAIL, IG = "davidslv.london@gmail.com", "https://www.instagram.com/davidslv.photography/"


def after(meta):
    return f"""<section class="pitch" id="commission">
<p class="lbl">For brands</p>
<h2>Sport, told as a story.</h2>
<p class="pitch-lede">One afternoon on one beach, in the order it happened: the walk down, the run, the board in the sand, the wave. The same way I would photograph a team, an event or a product in use.</p>
<ul class="pitch-list">
<li><span class="lbl">The story</span>A page like this one, from arrival to the last run.</li>
<li><span class="lbl">The photographs</span>One graded set in one look. Here, only the green boards keep their full colour.</li>
<li><span class="lbl">The details</span>Boards, wetsuits and kit, close up and in use.</li>
</ul>
<p><a class="btn" href="mailto:{EMAIL}?subject=Commission%20a%20story">Commission a story</a></p>
<p class="pitch-note">{EMAIL} · <a href="{IG}" rel="me">@davidslv.photography</a></p>
</section>
<section class="pitch" id="first-sale">
<p class="lbl">The first sale</p>
<h2>It was also the first thing I ever sold online.</h2>
<p class="pitch-lede">Forty photographs from that afternoon, straight from the camera. Someone paid for them, the first time anyone paid for a photograph of mine. I am leaving it up.</p>
<p><a class="btn" href="{GUMROAD}">The 40 photos on Gumroad</a></p>
<p class="pitch-small">Pay what you want, from €2. Photographed as a spectator on 26 February 2012 with a Sony DSLR-A350 and the 55–200 mm kit zoom, my first DSLR. Not a commission.</p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
