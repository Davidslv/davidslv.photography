"""/cayman/: David's red Porsche Cayman (987, 2007) on three days in spring 2026 (built 12 Oct 2026, not deployed).

Sources: Nikon Z 6II NEFs (15 and 21 March) and camera JPEGs (19 April) on the NAS, graded with Papaya
(tools/grades/papaya.py): everything quiet except the red. Times are camera times.
Words: none yet beyond "My Cayman" (David's caption on /blackbushe/). Part titles only say what is in the frames.
13 October 2026: "Porsche & me", 19 camera JPEGs David took of himself at the wheel and of the cabin, on the NAS in
/Volumes/David Photography/Porsche & me/ (added 13 Oct 2026). Near-duplicates left out: 8407, 8539, 8556, 8712, 8732, 8799-8805.
Camera clock: the Nikon was an hour ahead in March (still on summer time; UK clocks changed 29 March 2026).
David's iPhone frames of 21 March read 06:14-06:35 and he confirms sunrise was about 06:15, so 15 and 21 March
times here are camera time minus one hour (13 Oct 2026). iPhone 14 Pro Max frames of the Wales drive are in
~/Pictures/Porsche & me - Wales iPhone 2026-03-21/ (David to move to the NAS). GPS is not copied into the web files.
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


ME = Path("/Volumes/David Photography/Porsche & me")


def me(n, time, alt, keep=0.6, **kw):
    """keep=0.85 on the portraits: Papaya at 0.6 turns skin grey (David, 13 Oct 2026)."""
    return dict(src=ME / f"DSC_{n}.JPG", alt=alt, cap=None, taken=f"2026-10-13T{time}", show_time=True,
                grade="papaya", keep=keep, **kw)


IPH = Path.home() / "Pictures/Porsche & me - Wales iPhone 2026-03-21"


def iph(n, time, alt, **kw):
    return dict(src=IPH / f"IMG_{n}.jpeg", alt=alt, cap=None, taken=f"2026-03-21T{time}", show_time=True,
                grade="papaya", keep=0.6, **kw)


def ph(day, n, time, alt, ext="NEF", **kw):
    return dict(src=N / day / f"DSC_{n}.{ext}", alt=alt, cap=None, taken=f"{day}T{time}", show_time=True,
                grade="papaya", keep=0.6, **kw)


M15, M21, A19 = "2026-03-15", "2026-03-21", "2026-04-19"
PHOTOS = {
    "c2530": ph(M15, "2530", "17:56:47", "Rain on the red front wing and the wheel of a Porsche Cayman."),
    "c2537": ph(M15, "2537", "17:57:29", "The headlamp and fog lamp of a red Cayman, wet with rain."),
    "c2655": ph(M15, "2655", "18:01:23", "The Porsche crest on a red bonnet covered in raindrops."),
    "c2672": ph(M15, "2672", "18:01:42", "A Cayman headlamp, close, beaded with rain."),
    "c2680": ph(M15, "2680", "18:02:02", "A red door mirror covered in raindrops."),
    "c2690": ph(M15, "2690", "18:02:44", "The side air intake of a red Cayman."),
    "c2697": ph(M15, "2697", "18:03:26", "The rear lamp and wing of a red Cayman by a brick wall."),
    "c2709": ph(M15, "2709", "18:04:19", "The door and window of a red Cayman, seen past a gatepost."),
    "c2718": ph(M15, "2718", "18:05:27", "A Cayman headlamp in the rain, upright."),
    "i3035": iph("3035", "06:14:41", "The road ahead over the bonnet, before sunrise."),
    "i3038": iph("3038", "06:14:49", "The red door mirror, an orange line of light on the horizon."),
    "i3039": iph("3039", "06:14:56", "A hand on the wheel, the dials reading 19 mph."),
    "i3042": iph("3042", "06:15:38", "The empty road curving away across the moor, seen over the dashboard."),
    "i3044": iph("3044", "06:15:41", "The door mirror against the sunrise."),
    "i3048": iph("3048", "06:23:10", "The red Cayman alone on a gravel car park below the hills."),
    "i3051": iph("3051", "06:23:20", "The red Cayman on the gravel, the quarried hillside behind."),
    "i3055": iph("3055", "06:35:11", "The sun clearing the hill, seen past the door mirror, picnic benches below."),
    "c2738": ph(M21, "2738", "06:25:35", "A road curving across the moor, a sheep by the verge."),
    "c2771": ph(M21, "2771", "06:29:16", "A red Cayman from behind, on a gravel car park on the moor."),
    "c2775": ph(M21, "2775", "06:29:25", "The rear of a red Cayman, close, moorland behind."),
    "c2783": ph(M21, "2783", "06:34:33", "A red Cayman side on at the edge of a car park, sky behind.", red=18),
    "c2789": ph(M21, "2789", "06:35:09", "A red Cayman from behind, a tree and the hills beyond."),
    "c2817": ph(M21, "2817", "06:35:35", "A red Cayman side on, the sun coming up over the hill behind."),
    "c2828": ph(M21, "2828", "06:35:52", "The valley below the car park in the early light."),
    "c2836": ph(M21, "2836", "06:36:09", "A red Cayman side on, shot low across the tarmac."),
    "c2848": ph(M21, "2848", "06:36:37", "Empty picnic benches on the grass by the car park."),
    "c4823": ph(A19, "4823", "06:50:05", "A red Cayman side on in low sun, trees behind.", ext="JPG"),
    "c4838": ph(A19, "4838", "06:51:20", "The front wheel and wing of a red Cayman, low and close, in morning sun.", ext="JPG"),
    "c4843": ph(A19, "4843", "06:51:29", "A red Cayman three-quarter on in morning sun.", ext="JPG"),
    "c4846": ph(A19, "4846", "06:51:57", "A small red Cayman under a wide blue sky.", ext="JPG"),
    "c8549": me("8549", "17:26:22", "The key in the ignition of a Cayman, the dashboard soft behind."),
    "c8464": me("8464", "17:23:00", "David at the wheel of his Cayman, a brick house through the window.", keep=0.85),
    "c8404": me("8404", "17:21:43", "David in the driver's seat, seen from low down by the door.", keep=0.85),
    "c8554": me("8554", "17:26:43", "The Porsche crest on the steering wheel."),
    "c8564": me("8564", "17:27:48", "The gear knob, close, the centre console behind."),
    "c8548": me("8548", "17:26:04", "The light switch on the dashboard, the red door beyond."),
    "c8715": me("8715", "17:31:58", "The speedometer and rev counter behind the wheel rim."),
    "c8706": me("8706", "17:31:29", "David in profile in the driver's seat, looking ahead.", keep=0.85),
    "c8728": me("8728", "17:33:17", "David seen through the steering wheel, looking past the camera."),
    "c8761": me("8761", "17:33:28", "David at the wheel in sunglasses."),
    "c8784": me("8784", "17:33:38", "David looks straight at the camera over the steering wheel.", keep=0.85),
}

SEQUENCE = [
    ("hero", "c2817"),
    ("part", "15 March 2026 · 17:56", "Rain", ""),
    ("wide", "c2530"),
    ("pair", "c2655", "c2672"),
    ("wide", "c2680"),
    ("print", "c2690", "right-small"),
    ("print", "c2697", "left"),
    ("wide", "c2709"),
    ("print", "c2718", "right-small"),
    ("part", "21 March 2026 · 06:14", "Wales", ""),
    ("print", "i3035", "left"),
    ("pair", "i3038", "i3039"),
    ("pair", "i3042", "i3044"),
    ("pair", "i3048", "i3051"),
    ("wide", "c2738"),
    ("wide", "c2783"),
    ("pair", "i3055", "c2775"),
    ("wide", "c2817"),
    ("wide", "c2848"),
    ("part", "19 April 2026 · 06:50", "Low sun", ""),
    ("wide", "c4823"),
    ("pair", "c4838", "c4843"),
    ("print", "c4846", "centre"),
    ("part", "13 October 2026 · 17:21", "Behind the wheel", ""),
    ("print", "c8404", "left"),
    ("wide", "c8464"),
    ("pair", "c8548", "c8549"),
    ("pair", "c8554", "c8564"),
    ("wide", "c8706"),
    ("print", "c8715", "right-small"),
    ("pair", "c8728", "c8761"),
    ("wide", "c8784"),
]


def after(meta):
    return """<a class="next" href="/blackbushe/"><span class="lbl">Next</span><span class="next-title">Something special</span><span class="next-sub">Porsche Club GB at Blackbushe</span></a>"""
