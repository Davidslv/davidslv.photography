"""/mclaren/: a day at the McLaren Technology Centre open day, March 2024 (built 11 Oct 2026).

Graded with the papaya film-still look (tools/grades/papaya.py): everything quiet except papaya and red.
The camera clock was wrong (it read 2015), so no capture times are shown, only the order of the day.
Words in quotes are from David's own caption for the day (mclaren_cinematic/instagram/caption.txt).
"""
from pathlib import Path

N = Path("/Volumes/David Photography/Photography/McLaren Open Day 2024")

PATH = "/mclaren/"
NAV_NAME = "McLaren"
TITLE = "Made to be used · A day at McLaren, photographed by David Silva"
OG_TITLE = "Made to be used · David Silva"
DESC = ("A day at the McLaren Technology Centre open day: race cars from the 1970s to now, the people who came to see "
        "them, the details, and the factory floor. Photographs by David Silva.")
HERO_LABEL = "McLaren Technology Centre · open day, March 2024"
HERO_TITLE = "Made to be used"
GALLERY_NAME = "A day at the McLaren Technology Centre open day, 2024"
OG_IMAGE = "og-mclaren.jpg"
OG_TOP = 0.5


def ph(file, alt, **kw):
    root = N / file
    src = root if root.exists() else N / "ORIGINAL" / file
    return dict(src=src, alt=alt, cap=None, taken=None, show_time=False, grade="papaya", **kw)


PHOTOS = {
    "m0206": ph("DSC_0206.JPG", "A long white corridor of racing cars: one car on the floor in front, another behind it, a papaya car mounted high on the wall.", crop=(0, 0.275, 1, 0.9025)),
    "m0063": ph("DSC_0063.JPG", "A white and red McLaren Honda racing car with Shell and Goodyear markings, close to the camera in a dark hall."),
    "m0015": ph("DSC_0015.JPG", "A young girl in a pink jacket reaches into the cockpit of a papaya racing car."),
    "m0084": ph("DSC_0084.JPG", "A man in a papaya jacket walks past a glass cabinet full of silver trophies."),
    "m0116": ph("DSC_0116.JPG", "A bright glass atrium full of visitors walking between cars and displays."),
    "m0139": ph("DSC_0139.JPG", "A man in a blue shirt leans over the cockpit of a white and red racing car from the 1970s."),
    "m0210": ph("DSC_0210.JPG", "A hand holds up a phone, photographing the corridor of racing cars."),
    "m0174": ph("DSC_0174.JPG", "A bright papaya spring tucked inside the white bodywork of a car."),
    "m0146": ph("DSC_0146.JPG", "The worn leather steering wheel and the black harness straps in an old racing cockpit."),
    "m0009": ph("DSC_0009.JPG", "The papaya and black front wing of a current racing car, its stripes catching the light in a dark hall."),
    "m0020": ph("DSC_0020.JPG", "A Pirelli P Zero racing tyre with coloured rings on the wheel cover."),
    "m0233": ph("DSC_0233.JPG", "A Michelin racing tyre and silver wheel on a grey and black car."),
    "m0178": ph("DSC_0178.JPG", "A full-size clay model of a sports car, seen head-on."),
    "m0297": ph("DSC_0297.JPG", "A car body shell, without doors or engine, sits on a frame on the factory floor under a sign that reads Paint."),
    "m0305": ph("DSC_0305.JPG", "A rack of painted body panels in white, papaya, green, blue and black on the factory floor."),
    "m0308": ph("DSC_0308.JPG", "Hands in blue gloves work on a carbon fibre tub on the factory floor."),
    "m0299": ph("DSC_0299.JPG", "Robot arms and white machines on the assembly line."),
    "m0310": ph("DSC_0310.JPG", "Three finished sports cars, pale blue, papaya and green, waiting in a row on a white tiled floor."),
    "m0112": ph("DSC_0112.JPG", "A still lake under a grey sky, trees on the far bank reflected in the water, a small car parked at the water's edge."),
}

SEQUENCE = [
    ("hero", "m0206"),
    ("part", "Part one", "The boulevard", "Race cars from the 1970s to now, and the people who came to see them."),
    ("wide", "m0063"),
    ("pair", "m0015", "m0084"),
    ("wide", "m0116"),
    ("print", "m0139", "left"),
    ("print", "m0210", "right-small"),
    ("part", "Part two", "Up close", "Every part was made to be used."),
    ("pair", "m0174", "m0146"),
    ("wide", "m0009"),
    ("pair", "m0020", "m0233"),
    ("print", "m0178", "centre"),
    ("part", "Part three", "Where they are made", "The factory floor, open for the day."),
    ("wide", "m0297"),
    ("pair", "m0305", "m0308"),
    ("print", "m0299", "left"),
    ("wide", "m0310"),
    ("part", "Part four", "Outside", "Rare cars belong on the road, not in a museum."),
    ("wide", "m0112"),
    ("line", "At the end of the day, a car parked by the lake outside. That's where they belong."),
]

EMAIL, IG = "davidslv.london@gmail.com", "https://www.instagram.com/davidslv.photography/"


def after(meta):
    return f"""<section class="pitch" id="commission">
<p class="lbl">For brands</p>
<h2>A day like this, told as a story.</h2>
<p class="pitch-lede">I photograph open days, launches and factory floors, and the people at them. What you see on this page is what you get: one day, in the order it happened, in one look.</p>
<ul class="pitch-list">
<li><span class="lbl">The story</span>A page like this one, with your day in order, from arrival to the last frame.</li>
<li><span class="lbl">The photographs</span>A full graded set in one consistent look, made for your colours. Here, only papaya keeps its colour.</li>
<li><span class="lbl">The hero</span>A cinematic 2.39:1 frame for the top of a page or a screen, like the corridor above.</li>
<li><span class="lbl">The set</span>Crops for Instagram in 4:5 and 16:9, ready to post.</li>
</ul>
<p><a class="btn" href="mailto:{EMAIL}?subject=Commission%20a%20story">Commission a story</a></p>
<p class="pitch-note">{EMAIL} · <a href="{IG}" rel="me">@davidslv.photography</a></p>
<p class="pitch-small">Photographed as a visitor at the McLaren open day, March 2024, on a Nikon D5500 with a 35mm lens. Not affiliated with or endorsed by McLaren.</p>
</section>
<a class="next" href="/"><span class="lbl">Next</span><span class="next-title">From last light to last train</span><span class="next-sub">One Saturday in London, and other nights</span></a>"""
