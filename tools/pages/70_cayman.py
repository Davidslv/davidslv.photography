"""/cayman/: David's red Porsche Cayman (987, 2007) on three days in spring 2026 (built 12 Oct 2026, not deployed).

Sources: Nikon Z 6II NEFs (15 and 21 March) and camera JPEGs (19 April) on the NAS, graded with Papaya
(tools/grades/papaya.py): everything quiet except the red. Times are camera times.
Words: none yet beyond "My Cayman" (David's caption on /blackbushe/). Part titles only say what is in the frames.
Left out: 15 March DSC_2561-2607 (family and a child at the door). The dealer listing photos in
2026/Porsche-987-Cayman-MX57DVO are not David's.
"""
from pathlib import Path

N = Path("/Volumes/David Photography/2026")

PATH = "/cayman/"
NAV_NAME = "Cayman"
TITLE = "My Cayman · A red Porsche Cayman in spring 2026, photographed by David Silva"
OG_TITLE = "My Cayman · David Silva"
DESC = ("David Silva's red Porsche Cayman on three days in spring 2026: in the rain at home, at sunrise on the moor, "
        "and in low April sun. Photographs by David Silva.")
HERO_LABEL = "Porsche Cayman · March and April 2026"
HERO_TITLE = "My Cayman"
GALLERY_NAME = "My Cayman, spring 2026"
OG_IMAGE = "og-cayman.jpg"
OG_TOP = 0.45


def ph(day, n, time, alt, ext="NEF", **kw):
    return dict(src=N / day / f"DSC_{n}.{ext}", alt=alt, cap=None, taken=f"{day}T{time}", show_time=True,
                grade="papaya", keep=0.6, **kw)


M15, M21, A19 = "2026-03-15", "2026-03-21", "2026-04-19"
PHOTOS = {
    "c2530": ph(M15, "2530", "18:56:47", "Rain on the red front wing and the wheel of a Porsche Cayman."),
    "c2537": ph(M15, "2537", "18:57:29", "The headlamp and fog lamp of a red Cayman, wet with rain."),
    "c2655": ph(M15, "2655", "19:01:23", "The Porsche crest on a red bonnet covered in raindrops."),
    "c2672": ph(M15, "2672", "19:01:42", "A Cayman headlamp, close, beaded with rain."),
    "c2680": ph(M15, "2680", "19:02:02", "A red door mirror covered in raindrops."),
    "c2685": ph(M15, "2685", "19:02:20", "The round fog lamp in the front grille, wet."),
    "c2690": ph(M15, "2690", "19:02:44", "The side air intake of a red Cayman."),
    "c2697": ph(M15, "2697", "19:03:26", "The rear lamp and wing of a red Cayman by a brick wall."),
    "c2709": ph(M15, "2709", "19:04:19", "The door and window of a red Cayman, seen past a gatepost."),
    "c2718": ph(M15, "2718", "19:05:27", "A Cayman headlamp in the rain, upright."),
    "c2738": ph(M21, "2738", "07:25:35", "A road curving across the moor, a sheep by the verge."),
    "c2771": ph(M21, "2771", "07:29:16", "A red Cayman from behind, on a gravel car park on the moor."),
    "c2775": ph(M21, "2775", "07:29:25", "The rear of a red Cayman, close, moorland behind."),
    "c2783": ph(M21, "2783", "07:34:33", "A red Cayman side on at the edge of a car park, sky behind."),
    "c2789": ph(M21, "2789", "07:35:09", "A red Cayman from behind, a tree and the hills beyond."),
    "c2817": ph(M21, "2817", "07:35:35", "A red Cayman side on, the sun coming up over the hill behind."),
    "c2828": ph(M21, "2828", "07:35:52", "The valley below the car park in the early light."),
    "c2836": ph(M21, "2836", "07:36:09", "A red Cayman side on, shot low across the tarmac."),
    "c2848": ph(M21, "2848", "07:36:37", "Empty picnic benches on the grass by the car park."),
    "c4823": ph(A19, "4823", "06:50:05", "A red Cayman side on in low sun, trees behind.", ext="JPG"),
    "c4838": ph(A19, "4838", "06:51:20", "The front wheel and wing of a red Cayman, low and close, in morning sun.", ext="JPG"),
    "c4843": ph(A19, "4843", "06:51:29", "A red Cayman three-quarter on in morning sun.", ext="JPG"),
    "c4846": ph(A19, "4846", "06:51:57", "A small red Cayman under a wide blue sky.", ext="JPG"),
}

SEQUENCE = [
    ("hero", "c2817"),
    ("part", "15 March 2026 · 18:56", "Rain", ""),
    ("wide", "c2530"),
    ("pair", "c2655", "c2672"),
    ("wide", "c2680"),
    ("pair", "c2685", "c2690"),
    ("print", "c2697", "left"),
    ("wide", "c2709"),
    ("print", "c2718", "right-small"),
    ("part", "21 March 2026 · 07:25", "Sunrise", ""),
    ("wide", "c2738"),
    ("wide", "c2771"),
    ("print", "c2775", "right"),
    ("wide", "c2783"),
    ("wide", "c2789"),
    ("pair", "c2828", "c2848"),
    ("wide", "c2836"),
    ("part", "19 April 2026 · 06:50", "Low sun", ""),
    ("wide", "c4823"),
    ("pair", "c4838", "c4843"),
    ("print", "c4846", "centre"),
]


def after(meta):
    return """<a class="next" href="/blackbushe/"><span class="lbl">Next</span><span class="next-title">Something special</span><span class="next-sub">Porsche Club GB at Blackbushe</span></a>"""
