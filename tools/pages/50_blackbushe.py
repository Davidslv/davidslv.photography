"""/blackbushe/: Porsche Club GB Region 29 meet at Blackbushe, Sunday 11 October 2026 (built 11 Oct 2026).

Sources are David's selects, already graded in the look he chose per photo (Cinematic 2.39:1, KERBSIDE D01, D03,
O01), so no grade key. Times are camera times (BST). Words come only from the confirmed, why and quote lines in
~/projects/photography/instagram/blackbushe/interview.md. Owners stay unnamed.
Not used: DSC_7467 (out of all Blackbushe work) and the five photos in the book's October coda
(6779, 7037, 7060, 7198, 7718), held until the book launches on 15 Nov 2026.
"""
from pathlib import Path

N = Path("/Volumes/David Photography/Photography/2026/2026-10-11 Selects")

PATH = "/blackbushe/"
NAV_NAME = "Blackbushe"
TITLE = "Something special · Porsche Club GB at Blackbushe, photographed by David Silva"
OG_TITLE = "Something special · David Silva"
DESC = ("A Porsche Club GB Region 29 morning at Blackbushe, 11 October 2026: the cars, the people round them and the "
        "details, in the order it happened. Photographs by David Silva.")
HERO_LABEL = "Porsche Club GB Region 29 · Blackbushe · 11 October 2026"
HERO_TITLE = "Something special"
GALLERY_NAME = "Porsche Club GB Region 29 at Blackbushe, 11 October 2026"
OG_IMAGE = "og-blackbushe.jpg"
OG_TOP = 0.2


def ph(file, time, alt, cap=None):
    return dict(src=N / file, alt=alt, cap=cap, taken=f"2026-10-11T{time}", show_time=True)


PHOTOS = {
    "b6723": ph("DSC_6723 KERBSIDE D01.jpg", "09:02:17", "Two race cars on trailers at a petrol station on the morning of the meet."),
    "b6833": ph("DSC_6833 KERBSIDE D01.jpg", "10:23:08", "A man walks past a yellow Porsche GT4 on the dirt car park."),
    "b7186": ph("DSC_7186 KERBSIDE D01.jpg", "11:00:59", "The headlamp and bonnet of a pale blue Porsche 911, close."),
    "b7215": ph("DSC_7215 KERBSIDE D01.jpg", "11:01:48", "The Porsche crest on pale blue paint."),
    "b7404": ph("DSC_7404 KERBSIDE D01.jpg", "11:10:26", "The headlamp and vent of a yellow Porsche GT4, from above."),
    "b7590": ph("DSC_7590 KERBSIDE D01.jpg", "11:16:49", "A red door mirror, the meet and the clubhouse beyond."),
    "b7779": ph("DSC_7779 KERBSIDE D01.jpg", "11:27:18", "Three owners talking and laughing between the parked cars."),
    "b6740": ph("DSC_6740 KERBSIDE D03.jpg", "10:16:24", "A silver Porsche 911 parked on the dirt car park, head-on."),
    "b6800": ph("DSC_6800 KERBSIDE D03.jpg", "10:20:28", "A red Porsche 911 convertible with yellow brake calipers, people behind."),
    "b6827": ph("DSC_6827 KERBSIDE O01.jpg", "10:22:41", "A yellow Porsche with a black side stripe among parked cars, two men beside it."),
    "b6843": ph("DSC_6843 KERBSIDE O01.jpg", "10:23:47", "A dark blue Porsche convertible with silver stripes, owners chatting nearby."),
    "b6943": ph("DSC_6943 Cinematic.jpg", "10:35:28", "A red classic Porsche 911 beside a yellow Porsche convertible."),
    "b6986": ph("DSC_6986 KERBSIDE D01.jpg", "10:41:43", "A white Porsche 911 convertible, low and close."),
    "b7010": ph("DSC_7010 KERBSIDE D01.jpg", "10:45:09", "A red Porsche with a large rear wing, from behind."),
    "b7087": ph("DSC_7087 Cinematic.jpg", "10:55:14", "The steering wheel and yellow dials of a Porsche cockpit."),
    "b7156": ph("DSC_7156 KERBSIDE D01.jpg", "10:57:13", "A white classic Porsche 911 with green Carrera script and green wheels, side on."),
    "b7162": ph("DSC_7162 Cinematic.jpg", "10:59:27", "The bonnet and headlights of a black Porsche 911, close up."),
    "b7252": ph("DSC_7252 Cinematic.jpg", "11:03:16", "A pale blue classic Porsche 911 side on, people behind."),
    "b7262": ph("DSC_7262 Cinematic.jpg", "11:03:25", "A red Porsche Cayman, close to the camera.", cap="My Cayman, washed on the way"),
    "b7279": ph("DSC_7279 Cinematic.jpg", "11:04:25", "A red Porsche 911 head-on, another red Porsche behind."),
    "b7310": ph("DSC_7310 Cinematic.jpg", "11:06:01", "A red Porsche 911 side on, a man standing beside it."),
    "b7422": ph("DSC_7422 Cinematic.jpg", "11:11:11", "A red Porsche 911 convertible with yellow brake calipers, side on."),
    "b7464": ph("DSC_7464 KERBSIDE O01.jpg", "11:12:55", "The rear of a red Porsche 911 Turbo S, its PORSCHE lettering above a wooden rail.",
                cap="The rail covers the plate and keeps the spoiler, the badge and the exhausts"),
    "b7557": ph("DSC_7557 KERBSIDE D01.jpg", "11:15:44", "A Porsche Turbo centre-lock wheel with a yellow brake caliper."),
    "b7603": ph("DSC_7603 KERBSIDE O01.jpg", "11:17:07", "A black Porsche 911 side on, people by the clubhouse behind."),
    "b7674": ph("DSC_7674 Cinematic.jpg", "11:19:24", "The rear wing of a yellow Porsche GT4, close up."),
    "b7708": ph("DSC_7708 Cinematic.jpg", "11:20:57", "The white classic 911 parked beside the pale blue 911."),
    "b7862": ph("DSC_7862 KERBSIDE O01.jpg", "11:30:57", "A white Porsche Cayman side on, shot low across the gravel."),
    "b7873": ph("DSC_7873 KERBSIDE D01.jpg", "11:31:27", "A blue Porsche 911 seen low across the ground."),
    "b7922": ph("DSC_7922 KERBSIDE D01.jpg", "11:34:02", "The white classic 911 head-on, owners talking around it."),
    "b7940": ph("DSC_7940 KERBSIDE O01.jpg", "11:34:34", "The white classic 911 seen low across the ground, the meet behind it."),
    "b7979": ph("DSC_7979 KERBSIDE D01.jpg", "11:35:11", "The white classic 911 framed past the curve of a red Porsche."),
    "b8304": ph("DSC_8304 KERBSIDE D01.jpg", "11:42:03", "A red classic Porsche 911, front three-quarter."),
}

SEQUENCE = [
    ("hero", "b7708"),
    ("part", "09:02", "Arrival", "I stopped a few miles away to wash the car, so it would look fresh for the meet."),
    ("wide", "b6723"),
    ("wide", "b6740"),
    ("pair", "b6800", "b6827"),
    ("pair", "b6833", "b6843"),
    ("wide", "b6943"),
    ("pair", "b6986", "b7010"),
    ("wide", "b7087"),
    ("part", "10:57", "The white RS", "I kept coming back to it. The group was gathering around the car, and that put people in the photographs."),
    ("wide", "b7156"),
    ("wide", "b7162"),
    ("pair", "b7186", "b7215"),
    ("wide", "b7252"),
    ("wide", "b7262"),
    ("pair", "b7279", "b7310"),
    ("print", "b7404", "right-small"),
    ("wide", "b7422"),
    ("part", "11:12", "Close to the ground", "For the low ones, the camera was touching the gravel."),
    ("print", "b7464", "left"),
    ("pair", "b7557", "b7590"),
    ("wide", "b7603"),
    ("wide", "b7674"),
    ("wide", "b7779"),
    ("pair", "b7862", "b7873"),
    ("pair", "b7922", "b7940"),
    ("wide", "b7979"),
    ("wide", "b8304"),
    ("line", "Afterwards I sat down on the wooden rail and thought about the conversations and the photographs from that morning. It was really something special."),
]


def after(meta):
    return """<section class="pitch" id="book">
<p class="lbl">In the book</p>
<h2>Five more from this morning are in the book.</h2>
<p class="pitch-lede">The people from Blackbushe close <i>It Started on a Sunday</i>, out on 15 November.</p>
<p><a class="btn" href="/sunday/">The book</a></p>
</section>
<a class="next" href="/sunday/"><span class="lbl">Next</span><span class="next-title">It Started on a Sunday</span><span class="next-sub">Car meet photographs and the book</span></a>"""
