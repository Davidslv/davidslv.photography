"""Home: From last light to last train (proposal F, locked 10 Oct 2026)."""
from pathlib import Path

P = Path("/Volumes/David Photography/Photography Projects")
FULL = P / "Shutter Hub - City Series London (Nov 2026)/_tools/full"

PATH = "/"
NAV_NAME = "Work"
TITLE = "David Silva · Street photographer in London"
OG_TITLE = "From last light to last train · David Silva"
DESC = ("Candid street photographs of people in London's light, mostly late in the day and after dark. "
        "One Saturday, from last light to last train, and other nights.")
HERO_LABEL = "Human street moments · London"
HERO_TITLE = "From last light to last train"
GALLERY_NAME = "One Saturday and other nights in London"
OG_IMAGE = "og.jpg"


def ph(src, alt, cap=None, taken=None, **kw):
    """taken: ISO 8601 with offset. Times show only for the 19 Oct 2024 Saturday."""
    return dict(src=src if isinstance(src, Path) else P / src, alt=alt, cap=cap, taken=taken,
                show_time=bool(taken and taken.startswith("2024-10-19")), **kw)


PHOTOS = {
    "n147": ph("After Hours/Enhanced/DSC_7356-Enhanced-NR.jpg", "Two women smile into a phone held up for a photo in a crowded street.", None, "2024-10-19T16:45:53+01:00"),
    "n108": ph("After Hours/Enhanced/DSC_6835-Enhanced-NR.jpg", "A young woman covers her mouth and laughs at a table with a bunch of roses.", None, "2024-10-19T14:59:53+01:00"),
    "n109": ph("After Hours/Enhanced/DSC_6845-Enhanced-NR.jpg", "A young man in sunglasses and a black jacket walks through a crowd.", None, "2024-10-19T15:00:55+01:00"),
    "n141": ph("After Hours/Enhanced/DSC_7269-Enhanced-NR.jpg", "An older man in glasses reads at a pavement café table, a coffee cup beside him.", None, "2024-10-19T16:35:54+01:00"),
    "n145": ph("After Hours/Enhanced/DSC_7297-Enhanced-NR.jpg", "A man walks away down a narrow cobbled lane lined with black bollards, in low sun.", None, "2024-10-19T16:41:09+01:00"),
    "n146": ph("After Hours/Enhanced/DSC_7335-Enhanced-NR.jpg", "Two young women laugh as they walk, one with pink hair holding an orange drink.", None, "2024-10-19T16:44:21+01:00"),
    "n153": ph("After Hours/Enhanced/DSC_7405-Enhanced-NR.jpg", "A woman in a patterned scarf smiles in a busy street.", None, "2024-10-19T16:49:48+01:00"),
    "n172": ph("After Hours/Enhanced/DSC_7593-Enhanced-NR.jpg", "Two chefs in aprons work at the pass of a busy restaurant kitchen.", None, "2024-10-19T17:18:04+01:00"),
    "n175": ph("After Hours/Enhanced/DSC_7713-Enhanced-NR.jpg", "A dancer in a sequinned dress performs on a square at dusk as a man films her.", None, "2024-10-19T18:26:19+01:00"),
    "n208": ph("After Hours/Revisited/DSC_7756-Enhanced-NR.jpg", "An older woman with white hair looks out from a red bus window at night.", None, "2024-10-19T18:45:11+01:00"),
    "n181": ph("After Hours/Enhanced/DSC_7772-Enhanced-NR.jpg", "An older woman smiles behind the lit window of a bus, shopping on her lap.", None, "2024-10-19T18:49:27+01:00"),
    "n188": ph("After Hours/Enhanced/DSC_7839-Enhanced-NR.jpg", "Three people cross a street at night in front of All Souls church, its spire lit gold.", "All Souls, Langham Place", "2024-10-19T19:15:53+01:00"),
    "n203": ph("After Hours/Revisited/Book Reserved/DSC_8137-Enhanced-NR.jpg", "A full Tube carriage, passengers sitting in two rows holding blue poles.", "The Tube", "2024-10-19T21:15:48+01:00"),
    "n201": ph("After Hours/Enhanced/DSC_8158-Enhanced-NR.jpg", "An empty Tube carriage, blue seats on both sides.", "The Tube", "2024-10-19T21:40:52+01:00"),
    "n055": ph("After Hours/DSC_0908.jpg", "An older woman in a bright scarf and green jacket stands on a street at dusk beside a man."),
    "n056": ph("After Hours/DSC_3187.jpg", "A woman with red hair in a leopard coat and red satin skirt walks along a street at night."),
    "n057": ph("After Hours/DSC_3200.jpg", "People stand in a queue on a pavement at night."),
    "n215": ph(FULL / "DSC_5906/03 03 Last Orders.jpg", "Two people look into a lit cake shop window under flowers and a neon sign.", "9 October 2026", "2026-10-09T22:02:00+01:00"),
    "n211": ph("After Hours/Revisited/DSC_9353.jpg", "The lit front of Beigel Bake on Brick Lane at night, a worker inside.", "Beigel Bake, Brick Lane", "2024-10-23T00:38:28+01:00"),
    "n040": ph("After Hours/2024-10-28-book-photos/DSC_8954.jpg", "A young man with a green guitar on his back walks across a bridge at night.", "Tower Bridge", "2024-10-22T23:13:55+01:00"),
    "n212": ph(FULL / "DSC_6125/02 02 Late Show.jpg", "A woman walks down the curved, lamp-lit stairs into Piccadilly Circus station.", "Piccadilly Circus station, 9 October 2026", "2026-10-09T22:16:00+01:00", lift=0.35),
    "n053": ph("After Hours/8 December 2024/DSC_9891-2.jpg", "Two figures in the lit doorway of Bow Road station at night.", "Bow Road"),
    "n038": ph("After Hours/2024-10-28-book-photos/DSC_8681.jpg", "A man walks alone down a dark lane beside a brick wall.", None, "2024-10-22T22:26:07+01:00"),
}

SEQUENCE = [
    ("hero", "n147"),
    ("part", "Part one", "One Saturday", "19 October 2024, from 14:59 to 21:40. One camera, one 35mm lens."),
    ("print", "n108", "left"), ("print", "n109", "right-small"), ("print", "n141", "centre"), ("print", "n145", "right-small"),
    ("pair", "n146", "n153"), ("wide", "n172"), ("print", "n175", "centre-large"), ("pair", "n208", "n181"),
    ("line", "For one frame everyone was moving in a different direction under the church."),
    ("print", "n188", "centre-large"), ("pair", "n203", "n201"),
    ("part", "Part two", "Other nights", "Soho, Brick Lane, the river and the stations. 2024 to 2026."),
    ("wide", "n055"), ("pair", "n056", "n057"), ("wide", "n215"), ("print", "n211", "left"), ("pair", "n040", "n212"),
    ("print", "n053", "right"), ("print", "n038", "centre-small"),
]

EMAIL, IG = "davidslv.london@gmail.com", "https://www.instagram.com/davidslv.photography/"


def after(meta):
    return f"""<section class="about" id="about">
<img src="/images/{meta['_portrait']}" width="800" height="800" loading="lazy" decoding="async" alt="Portrait of David Silva.">
<div><p class="lbl">About</p><h2>I photograph people in London’s light.</h2>
<p>Someone crossing a wet street, waiting in a doorway, laughing on a corner. Mostly late in the day and after dark, with one camera and a 35mm lens.</p>
<p>On Sunday mornings I photograph the car meets, for the same reason.</p></div></section>
<a class="next" href="/sunday/"><span class="lbl">Next</span><span class="next-title">It Started on a Sunday</span><span class="next-sub">The car meets, and the book out 15 November</span></a>
<section class="more" id="contact">
<div><p class="lbl">The book</p><h3><a href="/sunday/"><em>It Started on a Sunday</em></a></h3><p>The car meets in and around London. Out 15 November 2026. <a href="/sunday/">See the photographs</a></p></div>
<div><p class="lbl">Presets</p><h3>LAST ROLL and KERBSIDE</h3><p>The Lightroom looks I grade with. <a href="https://davidslv.gumroad.com/l/last-roll">LAST ROLL</a> · <a href="https://davidslv.gumroad.com/l/kerbside-preset">KERBSIDE</a></p></div>
<div><p class="lbl">Contact</p><h3>Commissions, prints and licensing</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}" rel="me">@davidslv.photography</a></p></div>
</section>"""
