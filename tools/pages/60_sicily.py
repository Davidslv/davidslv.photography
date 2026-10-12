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
PHOTOS = {
    "s8099": ph(A19, "8099", "06:34:09", "gentle", "Rows of vines on a hillside, bare branches in the foreground."),
    "s8126": ph(A19, "8126", "06:39:19", "gentle", "Bunches of dark grapes hanging from a curving trunk, in morning light."),
    "s8128": ph(A19, "8128", "06:39:51", "film", "A row of vines, a dirt track between them, low sun from one side."),
    "s8143": ph(A19, "8143", "06:42:59", "gentle", "A row of vines seen through a loop in a vine's trunk."),
    "s8153": ph(A19, "8153", "06:44:06", "gentle", "A vine trunk with a bunch of white grapes above it, first sun on the bark."),
    "s8167": ph(A19, "8167", "06:45:52", "film", "A hand holds a stone picked up from the vineyard."),
    "s8173": ph(A19, "8173", "06:46:23", "film", "Dry, cracked soil between the vines."),
    "s8176": ph(A19, "8176", "06:46:54", "gentle", "White grapes half hidden behind a vine's trunk."),
    "s8207": ph(A19, "8207", "18:26:11", "film", "A stone pressed into the dry soil."),
    "s8235": ph(A19, "8235", "18:31:34", "gentle", "The bark of a vine trunk, close, in evening light."),
    "s8245": ph(A19, "8245", "18:32:45", "film", "Red vine leaves fallen on pale soil."),
    "s8258": ph(A19, "8258", "18:42:12", "film", "Monte Altore at dusk, vines and scrub below it."),
    "s8268": ph(A21, "8268", "10:39:28", "gentle", "A hand lifts a bunch of dark grapes from the vine."),
    "s8289": ph(A21, "8289", "10:42:30", "gentle", "Two heavy bunches of dark grapes under the leaves."),
    "s8358": ph(A21, "8358", "10:52:20", "gentle", "Two hands cut a bunch of dark grapes from the vine."),
    "s8399": ph(A21, "8399", "10:56:56", "gentle", "A bunch of white grapes against dark leaves."),
    "s8722": ph(A23, "8722", "06:55:40", "gentle", "Dark grapes hanging along a vine's trunk."),
    "s8748": ph(A23, "8748", "06:58:13", "gentle", "Bunches of dark grapes along a row, seen low."),
    "s8775": ph(A23, "8775", "07:00:42", "gentle", "A vine's cordon with grapes against the sky."),
    "s8796": ph(A23, "8796", "07:08:04", "film", "A man in a cap and glasses, seen from below against the sky."),
    "s8840": ph(A23, "8840", "08:28:26", "film", "A red Massey Ferguson crawler tractor in the shed."),
    "s8868": ph(A23, "8868", "08:30:44", "film", "Stacked blue harvest crates printed with Tenuta Tremollito."),
    "s0392": ph(S10, "0392", "07:26:38", "film", "Three men talk beside the crates and a blue tractor at the end of a row."),
    "s0377": ph(S10, "0377", "07:25:17", "gentle", "A row of vines in autumn colour, a track running up the middle."),
}

SEQUENCE = [
    ("hero", "s8128"),
    ("part", "19 August 2025 · 06:34", "First light",
     "I was there doing the harvest, and taking photographs for the winery's Instagram account. "
     "At five in the morning you already have sunlight. By half past six the sun is coming up behind the trees."),
    ("wide", "s8099"),
    ("pair", "s8126", "s8143"),
    ("pair", "s8153", "s8167"),
    ("pair", "s8173", "s8176"),
    ("part", "18:26", "Evening", "I was looking for the details on the trunks."),
    ("pair", "s8207", "s8235"),
    ("print", "s8245", "right-small"),
    ("wide", "s8258"),
    ("part", "21 August 2025 · 10:39", "The pick",
     "The vineyard is on a slope, so it is harder to walk on the ground. While you work, you need a lot of water."),
    ("pair", "s8268", "s8289"),
    ("pair", "s8358", "s8399"),
    ("part", "23 August 2025 · 06:55", "Before the heat",
     "We are at 620 metres. It gets hotter and hotter through the day. At midday it is almost impossible to be in the vineyard."),
    ("print", "s8722", "left"),
    ("wide", "s8748"),
    ("print", "s8775", "right-small"),
    ("wide", "s8796"),
    ("wide", "s8840"),
    ("print", "s8868", "centre"),
    ("part", "10 September 2025 · 07:25", "Harvest",
     "I have done WSET Level 2. Here you get to know the soil, the geography and the whole process of making the wine."),
    ("wide", "s0392"),
    ("wide", "s0377"),
    ("line", "I was there to help with the harvest and to take photographs. I took a lot of joy in doing it."),
]

WINERY = "https://www.tenuta-tremollito.com/"


def after(meta):
    return f"""<section class="pitch" id="winery">
<p class="lbl">The vineyard</p>
<h2>Tenuta Tremollito is my family's vineyard near Licodia Eubea, in Sicily.</h2>
<p><a class="btn" href="{WINERY}">Tenuta Tremollito</a></p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
