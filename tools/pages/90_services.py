"""/services/: ways to work with David (4 Nov 2026, branch services-home, preview). No prices anywhere.

Copy is David's, from the brief of 4 Nov 2026. No form for now (David, 4 Nov): the start section gives the email
address and a message template, each with a copy button, plus a mailto link as a shortcut.
"""
PATH = "/services/"
NAV_NAME = "Services"
TITLE = "Ways to work with me · David Silva, London"
OG_TITLE = "Ways to work with me · David Silva"
DESC = ("Photos, short videos and websites for small businesses, from David Silva in London. Four ways to work "
        "together, each shaped around your business. Every project is quoted after we talk.")
HERO_TITLE = "Ways to work with me"
GALLERY_NAME = ""
OG_IMAGE = "og-home.jpg"
OG_ALT = "Two chefs in aprons work at the pass of a busy restaurant kitchen."
SKIP = ("#main", "Skip to the content")
BODY_CLASS = "plain"
PHOTOS = {}
SEQUENCE = []

URL = "https://davidslv.photography"

SERVICES = [
    ("contact-sheet", "Contact Sheet", "Know what makes you different, and where to show it.",
     ["I spend half a day with you and your business.",
      "I look at your customers, your competition and what you publish today.",
      "You get a written plan: the one thing to fix first, then where to show up and what to make."],
     "If the plan isn't useful, you get your money back."),
    ("the-reveal", "The Reveal", "Your business at its best, ready to post this week.",
     ["I plan the shoot and script short videos with you.",
      "Photos of your people, place and product, curated for you and your business.",
      "Simple vertical videos for Reels, and captions written for you.",
      "You choose your favourites in your own online gallery, and I finish them within 24 hours."],
     "I reshoot or refund. Terms apply."),
    ("the-showroom", "The Showroom", "Look as good online as you are in person, and be found by the people looking for you.",
     ["An interview about the image you want, and ideas to make your business stand out.",
      "Your story, a shoot, and a website built around your photos, on accounts you own.",
      "Set up so you're found on Google, with social profiles to match.",
      "A handover, so you can run it day to day."],
     None),
    ("growth-partner", "Growth Partner", "Show up every week without thinking about it, and see what it brings in.",
     ["A shoot every month.",
      "Your social media planned, made and posted for you.",
      "Your Google profile and website kept up to date.",
      "A monthly report: what was posted, who saw it, who got in touch, and the one thing to focus on next."],
     None),
]

EMAIL = "hello@davidslv.photography"
SUBJECT = "About my business"
TEMPLATE = """Hi David,

My name is ... and my business is ...
Website or Instagram: ...

What we do, in a sentence: ...
What I'd like more of (enquiries, bookings, sales, people finding us online): ...
In six months, I'd like: ...
I'd like to start: as soon as possible / in the next three months / just looking

Thanks,
..."""
from urllib.parse import quote as _q
SUBJECT_Q, BODY_Q = _q(SUBJECT), _q(TEMPLATE)

STEPS = ["Tell me about your business (the message below).", "A short call, prepared from your answers.",
         "A plan and a fixed quote by email.", "The work.", "You choose.", "Launch, then a monthly check if we keep going."]

FAQ = [
    ("Who owns what?", "Your website, domain, accounts and data are yours. The photos come with a licence to use them on "
                       "your website, social media, Google and email. I keep the copyright."),
    ("How much does it cost?", "Every project is quoted after we talk, so you only pay for what you need."),
    ("How long does it take?", "Photos and videos arrive within days of the shoot. A website takes about four to six weeks."),
    ("What if I don't like the photos?", "I reshoot or refund. Terms apply."),
]


def extra_jsonld(meta):
    return [
        {"@type": "ProfessionalService", "@id": f"{URL}/services/#business", "name": "David Silva Photography",
         "url": f"{URL}/services/", "email": "mailto:hello@davidslv.photography", "founder": {"@id": f"{URL}/#david"},
         "description": DESC, "areaServed": {"@type": "City", "name": "London"},
         "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Ways to work with me", "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "@id": f"{URL}/services/#{i}", "name": n,
                                                "description": line, "url": f"{URL}/services/#{i}",
                                                "provider": {"@id": f"{URL}/#david"}}}
             for i, n, line, _, _ in SERVICES]}},
        {"@type": "FAQPage", "@id": f"{URL}/services/#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]


def body(meta, b):
    E = b.E
    sections = []
    for i, n, line, bullets, guarantee in SERVICES:
        lis = "".join(f"<li>{E(x)}</li>" for x in bullets)
        g = f'<h3>If it isn\'t right</h3><p>{E(guarantee)}</p>' if guarantee else ""
        sections.append(f"""<section class="svc" id="{i}" aria-labelledby="{i}-h"><h2 id="{i}-h">{E(n)}</h2>
<p class="svc-line">{E(line)}</p>
<h3>What happens</h3><ul>{lis}</ul>{g}
<p><a class="svc-start" href="#start">Start with {E(n)}</a></p></section>""")
    steps = "".join(f"<li>{E(s)}</li>" for s in STEPS)
    faq = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in FAQ)
    form = f"""<section class="svc start" id="start" aria-labelledby="start-h"><h2 id="start-h">Tell me about your business</h2>
<p>Send me an email. Copy the message below, fill in the gaps and send it to me. Then the first call is about you and your business.</p>
<p class="copy-row"><span class="copy-label">Email</span> <a class="copy-email" href="mailto:{EMAIL}?subject={SUBJECT_Q}">{EMAIL}</a>
<button class="btn copy-btn" type="button" data-copy="email">Copy address</button></p>
<pre class="template" id="template" tabindex="0">{E(TEMPLATE)}</pre>
<p class="copy-row"><button class="btn solid copy-btn" type="button" data-copy="template">Copy message</button>
<a class="btn" href="mailto:{EMAIL}?subject={SUBJECT_Q}&amp;body={BODY_Q}">Open in my email app</a></p>
<p class="copy-note" role="status" aria-live="polite"></p></section>
<script>
document.querySelectorAll(".copy-btn").forEach(b => b.addEventListener("click", async () => {{
  const text = b.dataset.copy === "email" ? "{EMAIL}" : document.getElementById("template").textContent;
  const note = document.querySelector(".copy-note");
  try {{ await navigator.clipboard.writeText(text); note.textContent = b.dataset.copy === "email" ? "Email address copied." : "Message copied. Paste it into a new email to {EMAIL}."; }}
  catch (e) {{ const r = document.createRange(); r.selectNodeContents(b.dataset.copy === "email" ? document.querySelector(".copy-email") : document.getElementById("template"));
    const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); note.textContent = "Selected. Press Ctrl+C or Cmd+C to copy."; }}
}}));
</script>"""
    return f"""<main id="main" class="terms-page services">
<p class="lbl">Services</p>
<h1>Ways to work with me</h1>
<p class="lead">Every business is different, so every project is shaped around yours. The method stays the same: find the one thing holding you back, fix that first, then keep going.</p>
<nav class="svc-toc" aria-label="Services on this page">{"".join(f'<a href="#{i}">{E(n)}</a>' for i, n, *_ in SERVICES)}</nav>
{"".join(sections)}
<section class="svc" id="how" aria-labelledby="how-h"><h2 id="how-h">How a project runs</h2><ol class="runs">{steps}</ol></section>
<section class="svc" id="faq" aria-labelledby="faq-h"><h2 id="faq-h">Questions</h2>{faq}</section>
{form}
</main>"""
