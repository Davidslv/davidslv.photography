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
SICILY = ["s0392c", "s8268"]   # wide + single, the same row height as the story grid

STEPS = [
    ("Understand", "What makes your business different, and who buys from you."),
    ("Story", "The story worth telling, and where to tell it."),
    ("Content", "Photos and short videos of your people, place and product."),
    ("Presence", "A website and search set up on accounts you own."),
    ("Grow", "Keep showing up, measure what it brings in, fix the next thing."),
]
VALUES = [
    ("People first", "Your business is its people. My photos show them, not just the product."),
    ("Your success is my success", "The work is only good if it works for you: more people finding you, getting in touch and buying."),
    ("You own it", "Your domain, website, accounts and data are yours, and your photos come with a licence to use them. No lock-in to me or to a platform."),
    ("Honest work", "I tell you what it does and what it costs. I promise less and deliver more, and I never invent a number."),
    ("Done, then better", "Something working this month beats something perfect next year. We launch, measure, and improve."),
    ("You'll understand it", "I explain how it all works in plain words, so you can run it day to day without me."),
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

    sic = "".join(f"<figure>{b.picture(k, meta, '(max-width:720px) 100vw, 66vw')}</figure>" for k in SICILY)
    client = f"""<!-- PREVIEW: needs David's and the family's OK before going live -->
<section class="home-sec client" aria-labelledby="client-h"><p class="lbl">Client story</p><h2 id="client-h">Sicily: a family vineyard</h2>
<div class="client-photos">{sic}</div>
<p class="home-line">Photographs of a family vineyard in Sicily, for the website I'm building for them.</p>
<p><a class="btn" href="/sicily/">See the harvest</a></p></section>"""

    vals = "".join(f"<li><h3>{E(n)}</h3><p>{E(t)}</p></li>" for n, t in VALUES)
    about = f"""<section class="about about-home" id="about" aria-labelledby="about-h">
<img src="/images/{meta['_portrait']}" width="800" height="800" loading="lazy" decoding="async" alt="David Silva in his car, holding his camera.">
<div><p class="lbl">About</p><h2 id="about-h">I'm David Silva.</h2>
<p>I grew up in Lisbon and wrote my first code at 12. I've built software for a living since 2009, and I moved to London in 2013.</p>
<p>Years later I picked up a camera. I photographed London at night, then spent two years of Sundays at car meets. I went for the cars and stayed for the people. Both became books.</p>
<p>Now I bring the two together for small businesses. You talk to me, and I make it all: the photos, the videos and the website.</p>
<p class="about-why">Small businesses are people doing what they love. I want them to be seen properly, and to own everything they build.</p>
</div></section>
<section class="values-sec" aria-labelledby="values-h"><p class="lbl">What I believe</p><h2 id="values-h">How I work with you</h2>
<ul class="values">{vals}</ul>
<p class="values-cta"><a class="btn solid" href="/services/">Ways to work with me</a> <a class="btn" href="/services/#start">Tell me about your business</a></p></section>"""

    photographers = """<section class="more" aria-labelledby="ph-h"><h2 id="ph-h" class="lbl more-head">For photographers</h2>
<div><p class="lbl">The book</p><h3><a href="/sunday/"><em>It Started on a Sunday</em></a></h3><p>Candid photographs of car meets in and around London, and the people who love the cars.</p></div>
<div><p class="lbl">Guides</p><h3><a href="/guides/">What I learned, written down</a></h3><p>Free how-to guides for photographers: editing car meet photos, the systems behind a photography business, and making and selling my own book.</p></div>
<div><p class="lbl">Studio Kit</p><h3><a href="/studio-kit/">Studio Kit</a></h3><p>Your domain, email, website, Google, mailing list, social posting and shop, set up with Claude in plain English. You approve every step.</p></div>
</section>"""

    contact = f"""<section class="home-sec contact" id="contact" aria-labelledby="contact-h"><p class="lbl">Contact</p><h2 id="contact-h">Tell me about your business</h2>
<p>The quickest way to start is a short email. The services page has a message you can copy, fill in and send.</p>
<p><a class="btn solid" href="/services/#start">Tell me about your business</a></p>
<p>Or email <a href="mailto:{EMAIL}">{EMAIL}</a>, or message me on Instagram: <a href="{IG}" rel="me">@davidslv.photography</a></p></section>"""

    return "\n".join([hero, '<main id="main">', work, how, ways, client, about, photographers, contact, "</main>"])
