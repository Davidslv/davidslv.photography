"""Home (4 Nov 2026, branch services-home, preview): what David does for small businesses, the stories as proof.

The London story that was here is now /london/ (tools/pages/15_london.py). Laid out here in body(); the shared head,
menu and footer come from build.py. No new photos: every key is one the story pages already export.
Copy is David's, from the brief of 4 Nov 2026.
"""
PATH = "/"
NAV_NAME = "Home"
TITLE = "David Silva · Photos, video and websites for small businesses in London"
OG_TITLE = "Your business, seen properly · David Silva"
DESC = ("I help small businesses stand out and grow online: photos and short videos of your people, place and product, "
        "and a website on accounts you own. David Silva, photographer and software engineer in London.")
HERO_LABEL = "Photographer and software engineer · London"
HERO_TITLE = "Your business, seen properly."
GALLERY_NAME = "Stories by David Silva"
OG_IMAGE = "og-home.jpg"
SKIP = ("#main", "Skip to the content")
HERO = "n172"   # two chefs at the pass, London. Alternatives: s0392c (Sicily, three men by the crates), s3706 (Sunday, frost)

PHOTOS = {}   # all keys below belong to the story pages

# (name, path, cover key, one line from the story's own intro, object-position)
STORIES = [
    ("London", "/london/", "n147", "One Saturday in London, and other nights.", "50% 30%"),
    ("Sunday", "/sunday/", "s3706", "Car meets in and around London, and the people who love the cars.", "50% 60%"),
    ("McLaren", "/mclaren/", "m0206", "Race cars from the 1970s to now, and the people who came to see them.", "50% 50%"),
    ("Ericeira", "/ericeira/", "e8537", "The first time I had a DSLR in my hands.", "50% 50%"),
    ("Blackbushe", "/blackbushe/", "b7779", "A Porsche Club GB Region 29 morning at Blackbushe.", "50% 35%"),
    ("Cayman", "/cayman/", "c4823", "New tyres and brakes, a drive to Wales for the sunrise, and the view from behind the wheel.", "50% 62%"),
    ("Sicily", "/sicily/", "s8801", "Early mornings in the rows, the pick and the work around it.", "50% 45%"),
]
SICILY = ["s0392c", "s8268", "s8868l"]

STEPS = [
    ("Understand", "What makes your business different, and who buys from you."),
    ("Story", "The story worth telling, and where to tell it."),
    ("Content", "Photos and short videos of your people, place and product."),
    ("Presence", "A website and search set up on accounts you own."),
    ("Grow", "Keep showing up, measure what it brings in, fix the next thing."),
]
OFFERS = [
    ("contact-sheet", "Contact Sheet", "Know what makes you different, and where to show it."),
    ("the-reveal", "The Reveal", "Your business at its best, ready to post this week."),
    ("the-showroom", "The Showroom", "Look as good online as you are in person, and be found by the people looking for you."),
    ("growth-partner", "Growth Partner", "Show up every week without thinking about it, and see what it brings in."),
]

# hero first (link preview, primary image), then every photo the page shows: build.py reads these for JSON-LD and the sitemap
SEQUENCE = [("hero", HERO), ("grid", *[s[2] for s in STORIES]), ("grid", *SICILY)]

EMAIL, IG = "hello@davidslv.photography", "https://www.instagram.com/davidslv.photography/"


def body(meta, b):
    E = b.E
    hero = f"""<section class="hero home-hero">{b.picture(HERO, meta, "100vw", eager=True)}
<div class="words"><p class="lbl">{E(HERO_LABEL)}</p><h1>{E(HERO_TITLE)}</h1>
<p class="hero-sub">I help small businesses stand out and grow online. I find what makes you different, tell it with photos and video, and build the presence that brings you customers, on platforms you own.</p>
<div class="hero-buy"><a class="btn-solid" href="/services/#start">Tell me about your business</a><a class="btn-ghost" href="#work">See the work</a></div></div></section>"""

    cards = "\n".join(
        f'<a class="story" href="{path}">{b.picture(key, meta, "(max-width:720px) 100vw, (max-width:1000px) 50vw, 34vw").replace("<img ", f"<img style=\"object-position:{pos}\" ", 1)}'
        f'<span class="story-name">{E(name)}</span><span class="story-line">{E(line)}</span></a>'
        for name, path, key, line, pos in STORIES)
    work = f"""<section class="home-sec" id="work" aria-labelledby="work-h"><p class="lbl">Work</p><h2 id="work-h">Stories</h2>
<div class="stories">
{cards}
</div></section>"""

    steps = "".join(f"<li><h3>{E(n)}</h3><p>{E(t)}</p></li>" for n, t in STEPS)
    how = f"""<section class="home-sec" id="how" aria-labelledby="how-h"><p class="lbl">How I work</p><h2 id="how-h">Five steps</h2>
<ol class="steps">{steps}</ol>
<p class="home-line">Most businesses try to fix everything online at once. I find the one thing holding you back and fix that first.</p></section>"""

    offer_cards = "".join(f'<a class="offer" href="/services/#{i}"><span class="offer-name">{E(n)}</span><span class="offer-line">{E(t)}</span></a>'
                          for i, n, t in OFFERS)
    ways = f"""<section class="home-sec" id="ways" aria-labelledby="ways-h"><p class="lbl">Services</p><h2 id="ways-h">Ways to work with me</h2>
<div class="offers">{offer_cards}</div>
<p><a class="btn" href="/services/">All services</a></p></section>"""

    sic = "".join(f"<figure>{b.picture(k, meta, '(max-width:720px) 100vw, 33vw')}</figure>" for k in SICILY)
    client = f"""<!-- PREVIEW: needs David's and the family's OK before going live -->
<section class="home-sec client" aria-labelledby="client-h"><p class="lbl">Client story</p><h2 id="client-h">Sicily: a family vineyard</h2>
<div class="client-photos">{sic}</div>
<p class="home-line">Photographs of a family vineyard in Sicily, for the website I'm building for them.</p>
<p><a class="btn" href="/sicily/">See the harvest</a></p></section>"""

    about = f"""<section class="about" id="about">
<img src="/images/{meta['_portrait']}" width="800" height="800" loading="lazy" decoding="async" alt="Portrait of David Silva.">
<div><p class="lbl">About</p><h2>David Silva</h2>
<p>I'm David Silva, a photographer and software engineer in London. I've photographed London at night and two years of Sunday car meets, and made books of both. I've written software since I was 12. So the photos and the website come from the same person, and you deal with one person from start to finish.</p></div></section>"""

    photographers = """<section class="more" aria-labelledby="ph-h"><h2 id="ph-h" class="lbl more-head">For photographers</h2>
<div><p class="lbl">The book</p><h3><a href="/sunday/"><em>It Started on a Sunday</em></a></h3><p>Candid photographs of car meets in and around London, and the people who love the cars.</p></div>
<div><p class="lbl">Guides</p><h3><a href="/guides/">What I learned, written down</a></h3><p>Free how-to guides for photographers: editing car meet photos, the systems behind a photography business, and making and selling my own book.</p></div>
<div><p class="lbl">Studio Kit</p><h3><a href="/studio-kit/">Studio Kit</a></h3><p>Your domain, email, website, Google, mailing list, social posting and shop, set up with Claude in plain English. You approve every step.</p></div>
</section>"""

    contact = f"""<section class="home-sec contact" id="contact" aria-labelledby="contact-h"><p class="lbl">Contact</p><h2 id="contact-h">Tell me about your business</h2>
<p>The quickest way to start is the short form on the services page. It asks what you want more of and when you'd like to start.</p>
<p><a class="btn solid" href="/services/#start">Tell me about your business</a></p>
<p>Or email <a href="mailto:{EMAIL}">{EMAIL}</a>, or message me on Instagram: <a href="{IG}" rel="me">@davidslv.photography</a></p></section>"""

    return "\n".join([hero, '<main id="main">', work, how, ways, client, about, photographers, contact, "</main>"])
