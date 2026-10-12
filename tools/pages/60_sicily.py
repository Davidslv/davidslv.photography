"""/sicily/: the 2025 harvest at Tenuta Tremollito, Sicily (built 12 Oct 2026, not deployed).

Sources are David's Nikon Z 6II NEFs on the NAS, graded with Altore (tools/grades/altore.py) from the camera's own
render inside each raw file. Film or Gentle per frame, as David chose in the picker
(https://claude.ai/artifact/9ZFe9RyH1jEZftB92JPBwy). Times are camera times. Selection: notes/sicily.md.
Words come only from David's interview, notes/sicily-interview.md. No claim about the age of the vines (David is not sure).
Left out: the town days (15 Aug, 7 Sept) and the 21 Aug evening, which have children and family in them.
"""
from pathlib import Path

N = Path("/Volumes/David Photography/2025")

PATH = "/sicily/"
NAV_NAME = "Sicily"
TITLE = "The harvest · Tenuta Tremollito, Sicily, 2025, photographed by David Silva"
OG_TITLE = "The harvest · David Silva"
DESC = ("The 2025 harvest at Tenuta Tremollito, a family vineyard in Sicily: early mornings in the rows, the pick and "
        "the work around it, in the order it happened. Photographs by David Silva.")
HERO_LABEL = "Tenuta Tremollito, Sicily · August and September 2025"
HERO_TITLE = "The harvest"
GALLERY_NAME = "The harvest at Tenuta Tremollito, Sicily, 2025"
OG_IMAGE = "og-sicily.jpg"
OG_TOP = 0.35


def ph(day, n, time, look, alt, **kw):
    return dict(src=N / day / f"DSC_{n}.NEF", alt=alt, cap=None, taken=f"{day}T{time}", show_time=True,
                grade="altore", look=look, **kw)


A19, A21, A23, S10 = "2025-08-19", "2025-08-21", "2025-08-23", "2025-09-10"
G, F = "gentle", "film"
PHOTOS = {
    "s8072": ph(A19, "8072", "06:23:01", G, "A trainer on the stony ground of the vineyard."),
    "s8099": ph(A19, "8099", "06:34:09", G, "Rows of vines on a hillside, bare branches in the foreground."),
    "s8126": ph(A19, "8126", "06:39:19", G, "Bunches of dark grapes hanging from a curving trunk, in morning light."),
    "s8153": ph(A19, "8153", "06:44:06", G, "A vine trunk with a bunch of white grapes above it, first sun on the bark."),
    "s8167": ph(A19, "8167", "06:45:52", F, "A hand holds a stone picked up from the vineyard."),
    "s8235": ph(A19, "8235", "18:31:34", G, "The bark of a vine trunk, close, in evening light."),
    "s8245": ph(A19, "8245", "18:32:45", F, "Red vine leaves fallen on pale soil."),
    "s8258": ph(A19, "8258", "18:42:12", F, "Monte Altore at dusk, vines and scrub below it."),
    "s8378": ph(A21, "8378", "10:54:15", G, "Long rows of vines running up to the hill, a picker far down one of them."),
    "s8268": ph(A21, "8268", "10:39:28", G, "A hand lifts a bunch of dark grapes from the vine."),
    "s8358": ph(A21, "8358", "10:52:20", G, "Two hands cut a bunch of dark grapes from the vine."),
    "s8443": ph(A21, "8443", "11:00:45", G, "A man in a blue shirt bends into the row to cut white grapes."),
    "s8681": ph(A23, "8681", "06:49:06", G, "A man drives a blue tractor and sprayer along the edge of the vineyard."),
    "s8783": ph(A23, "8783", "07:01:44", G, "Monte Altore above the vines in the morning."),
    "s8796g": ph(A23, "8796", "07:08:04", G, "A man in a cap and glasses, seen from below against the sky."),
    "s8801": ph(A23, "8801", "08:16:53", G, "Rows of vines climbing towards the top of the hill."),
    "s8830": ph(A23, "8830", "08:28:08", G, "Two men in the shed, reading the labels on bottles and cans."),
    "s8890": ph(A23, "8890", "08:32:13", G, "A man lies on his back under the tractor, working on the hitch."),
    "s8840g": ph(A23, "8840", "08:28:26", G, "A red Massey Ferguson crawler tractor in the shed."),
    "s8868g": ph(A23, "8868", "08:30:44", G, "Stacked blue harvest crates printed with Tenuta Tremollito."),
    "s0362": ph(S10, "0362", "07:24:12", G, "Empty crates at the end of a row of vines in autumn colour."),
    "s0379": ph(S10, "0379", "07:25:21", G, "Two men talk beside the crates and a blue tractor."),
    "s0392g": ph(S10, "0392", "07:26:38", G, "Three men talk beside the crates and a blue tractor at the end of a row."),
    "s0377": ph(S10, "0377", "07:25:17", G, "A row of vines in autumn colour, a track running up the middle."),
}

SEQUENCE = [
    ("hero", "s8801"),
    ("part", "19 August 2025 · 06:23", "Why I was there",
     "I was there doing the harvest, and taking photographs for the winery's Instagram account. "
     "I have done WSET Level 2. Here you get to know the soil and the geography."),
    ("wide", "s8099"),
    ("print", "s8072", "centre"),
    ("print", "s8167", "right-small"),
    ("part", "06:39", "The vines", "I was just looking for the details on the trunks."),
    ("wide", "s8126"),
    ("pair", "s8153", "s8235"),
    ("print", "s8245", "left"),
    ("wide", "s8258"),
    ("part", "21 August 2025 · 10:39", "The pick",
     "The vineyard is on a slope, so it is harder to walk on the ground. While you work, you need a lot of water."),
    ("wide", "s8378"),
    ("pair", "s8268", "s8358"),
    ("wide", "s8443"),
    ("part", "23 August 2025 · 06:49", "Before the heat",
     "At five in the morning you already have sunlight. It gets hotter and hotter through the day. "
     "At midday it is almost impossible to be in the vineyard."),
    ("wide", "s8681"),
    ("wide", "s8783"),
    ("print", "s8796g", "right-small"),
    ("pair", "s8830", "s8890"),
    ("wide", "s8840g"),
    ("print", "s8868g", "centre"),
    ("part", "10 September 2025 · 07:24", "Harvest", "We are at 620 metres."),
    ("wide", "s0362"),
    ("pair", "s0379", "s0392g"),
    ("wide", "s0377"),
    ("line", "I was there to help with the harvest and to take photographs. I took a lot of joy in doing it."),
]

WINERY = "https://www.tenuta-tremollito.com/"


def after(meta):
    return f"""<section class="pitch" id="winery">
<p class="lbl">The vineyard</p>
<h2>Tenuta Tremollito is a family vineyard near Licodia Eubea, in Sicily.</h2>
<p><a class="btn" href="{WINERY}">Tenuta Tremollito</a></p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
