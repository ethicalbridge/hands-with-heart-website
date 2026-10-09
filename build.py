#!/usr/bin/env python3
"""Static site generator for the Hands With Heart Foundation website.

Run:  python3 build.py        (writes the .html files next to this script)

Edit content in the PAGES / data sections below, then re-run. Placeholders that need real
content from the team are marked with the `todo` class and listed in README.md.
"""
import html
import os
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = "hello@handswithheartfoundation.org"
# Swap for the payment-page URL (Stripe, PayPal, bank-transfer page ...) when one exists.
DONATE_URL = f"mailto:{EMAIL}?subject=Donation%20to%20Hands%20With%20Heart"

e = html.escape

# ------------------------------------------------------------------ navigation
NAV = [
    ("About us", "index.html", [
        ("Our founder", "index.html#founder"),
        ("Our advisors", "index.html#advisors"),
        ("Our team", "index.html#team"),
        ("Our team leaders", "index.html#team-leaders"),
    ]),
    ("Our objectives", "objectives/index.html", [
        ("label", "External objectives"),
        ("1 · Free healthcare", "objectives/care.html"),
        ("2 · Training and mentorship", "objectives/knowledge.html"),
        ("3 · Community-based solutions", "objectives/permanence.html"),
        ("4 · Changing perceptions", "objectives/advocacy.html"),
        ("5 · Funding and partnerships", "objectives/sustainability.html"),
        ("label", "Internal objectives"),
        ("Systems for scale", "objectives/systems-for-scale.html"),
    ]),
    ("Our projects", "projects/index.html", [
        ("ParaSurf", "projects/parasurf.html"),
        ("Bahía de Niños", "projects/bahia-de-ninos.html"),
        ("Missions", "projects/missions.html"),
        ("indent", "Bali", "projects/missions.html#bali"),
        ("indent", "Costa Rica", "projects/missions.html#costa-rica"),
        ("indent", "Ukraine", "projects/missions.html#ukraine"),
        ("indent", "Romania", "projects/missions.html#romania"),
        ("indent", "Argentina / Chaco", "projects/missions.html#chaco"),
    ]),
    ("Stories", "stories.html", []),
    ("News", "news.html", []),
    ("Reports", "reports.html", []),
    ("Partners", "partners.html", []),
    ("Contact", "contact.html", []),
]


def nav_html(prefix, current):
    out = []
    for label, href, subs in NAV:
        cur = ' aria-current="page"' if href == current else ""
        if subs:
            items = []
            for s in subs:
                if s[0] == "label":
                    items.append(f'<li class="sub-label">{e(s[1])}</li>')
                elif s[0] == "indent":
                    items.append(f'<li class="indent"><a href="{prefix}{s[2]}">{e(s[1])}</a></li>')
                else:
                    items.append(f'<li><a href="{prefix}{s[1]}">{e(s[0])}</a></li>')
            out.append(
                f'<li class="has-sub"><a href="{prefix}{href}"{cur}>{e(label)}</a>'
                f'<button class="sub-toggle" aria-expanded="false" aria-label="Show {e(label)} menu"></button>'
                f'<ul class="sub">{"".join(items)}</ul></li>'
            )
        else:
            out.append(f'<li><a href="{prefix}{href}"{cur}>{e(label)}</a></li>')
    donate_cur = ' aria-current="page"' if current == "donate.html" else ""
    out.append(f'<li><a class="btn btn-primary" href="{prefix}donate.html"{donate_cur}>Donate</a></li>')
    return "".join(out)


def page(path, title, desc, body, current=None, hero_class=""):
    depth = path.count("/")
    prefix = "../" * depth
    current = current or path
    full_title = "Hands With Heart Foundation" if path == "index.html" else f"{title} · Hands With Heart Foundation"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" type="image/png" href="{prefix}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{prefix}index.html"><img src="{prefix}assets/img/logo.png" alt="Hands With Heart Foundation" width="120" height="48"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main"><ul>{nav_html(prefix, current)}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <span class="foot-logo"><img src="{prefix}assets/img/logo.png" alt="Hands With Heart Foundation"></span>
        <p style="color:#dcdcdc">Hands on. Heart in.<br>Free healthcare for people with disability.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>About</h4><ul>
        <li><a href="{prefix}index.html#founder">Our founder</a></li>
        <li><a href="{prefix}index.html#team">Our team</a></li>
        <li><a href="{prefix}partners.html">Partners</a></li>
        <li><a href="{prefix}reports.html">Reports</a></li></ul></div>
      <div><h4>Our work</h4><ul>
        <li><a href="{prefix}objectives/index.html">Our objectives</a></li>
        <li><a href="{prefix}projects/parasurf.html">ParaSurf</a></li>
        <li><a href="{prefix}projects/bahia-de-ninos.html">Bahía de Niños</a></li>
        <li><a href="{prefix}projects/missions.html">Missions</a></li></ul></div>
      <div><h4>Get involved</h4><ul>
        <li><a href="{prefix}donate.html">Donate</a></li>
        <li><a href="{prefix}contact.html">Volunteer or partner</a></li>
        <li><a href="{prefix}stories.html">Stories</a></li>
        <li><a href="{prefix}news.html">News</a></li></ul></div>
    </div>
    <p class="legal">© 2026 Hands With Heart Foundation. Care is free for the people we serve. We work through a Spanish association with public-utility status, a US 501(c)(3) and a Costa Rican foundation.</p>
  </div>
</footer>
<script src="{prefix}assets/js/site.js" defer></script>
</body>
</html>
"""
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print("wrote", path)


# ------------------------------------------------------------------ helpers
def head(title, lede, eyebrow, crumbs=None):
    cr = ""
    if crumbs:
        cr = '<p class="crumbs">' + " / ".join(
            f'<a href="{h}">{e(t)}</a>' if h else e(t) for t, h in crumbs) + "</p>"
    return f"""<div class="page-head"><div class="wrap">{cr}<span class="eyebrow">{e(eyebrow)}</span>
<h1>{title}</h1><p class="lede">{lede}</p></div></div>"""


def ul(items, cls="dash"):
    return f'<ul class="{cls}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def stat(num, label):
    return f'<div class="stat"><span class="num">{num}</span><span class="label">{label}</span></div>'


def table(headers, rows):
    th = "".join(f"<th scope='col'>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ------------------------------------------------------------------ ABOUT US (home)
def person_cards(people, example=False):
    """people: list of (name, role). example=True marks the cards as illustrative examples."""
    cards = []
    for name, role in people:
        tag = '<span class="rel">Example</span>' if example else ""
        cards.append(f"""<div class="person"><div class="portrait">Portrait<br>to be added</div>{tag}
<h3>{e(name)}</h3><p class="small">{e(role)}</p></div>""")
    return '<div class="grid g4">' + "".join(cards) + "</div>"


TEAM = [
    ("Dr Jorge Aranda", "Founder and CEO"),
    ("Rafael [surname]", "Operations and Strategic Manager"),
    ("[Name]", "Administration"),
    ("[Name]", "Role to be completed"),
    ("Lewi [surname]", "Fundraising"),
]
ADVISORS = [
    ("Example Advisor 1", "Paediatric rehabilitation · University"),
    ("Example Advisor 2", "Humanitarian health · NGO"),
    ("Example Advisor 3", "Disability rights · Lived experience"),
    ("Example Advisor 4", "Finance and governance"),
]
LEADER_AREAS = ["Osteopathy · Bali", "Physiotherapy · Bali", "Osteopathy · Costa Rica", "Physiotherapy · Costa Rica",
                "Osteopathy · Ukraine", "Rehabilitation · Ukraine", "Behavioural optometry", "Adaptive sport · Hawaii",
                "Adaptive sport · California", "Paediatric osteopathy", "Education and training", "Home visits"]
LEADERS = [(f"Example Team Leader {i + 1}", area) for i, area in enumerate(LEADER_AREAS)]


about_body = f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">About us · Since 2016</span>
    <h1>Care that returns.<br>Knowledge that stays.</h1>
    <p class="lede">Hands With Heart provides free, specialised care to children and adults with disabilities who have little or no access to it, and leaves lasting local capacity through training, partnership and permanent infrastructure.</p>
    <div class="actions"><a class="btn btn-primary" href="donate.html">Donate</a><a class="btn btn-secondary" href="reports.html">Read our reports</a></div>
  </div>
  <div class="card topline">
    <span class="eyebrow">Our promise</span>
    <p style="font-family:var(--serif);font-size:2rem;line-height:1.25;margin:0 0 var(--s2)">Disability care that is free, repeated and respectful.</p>
    <p class="small">Free for beneficiaries, always. Care for vulnerable people is never tied to ability to pay.</p>
  </div>
</div></section>

<section class="bg-ink"><div class="wrap">
  <span class="eyebrow">Since 2016</span>
  <div class="grid g4">
    {stat("96", "Missions")}{stat("636", "Volunteers")}{stat("5,511", "People treated")}{stat("9,547", "Clinical sessions")}
  </div>
  <p class="small" style="color:#cfcfcf;margin:var(--s3) 0 0">Cumulative figures since 2016. We report people and sessions separately because complex disability needs repeated care. See our <a href="reports.html">annual reports</a> for each year and how we calculate them.</p>
</div></section>

<section><div class="wrap split">
  <div><span class="eyebrow">Who we are</span><h2>Skill and dignity, together</h2></div>
  <div>
    <p>The name says what we bring: skilled hands, and the respect that should come with every act of care.</p>
    <p>The <strong>hands</strong> are the clinical work: osteopathy, physiotherapy, behavioural optometry and rehabilitation, delivered free by professionals who know what they are doing, and taught to the people who will keep doing it. The <strong>heart</strong> is how that care is offered. We listen before we act, and we seek to understand how each community sees disability before we add support.</p>
    <p>Hands With Heart began in Bali in 2016, with a simple decision: to respond to children with disabilities by offering what the team could offer best, which was free care, presence and persistence. Ten years later the same idea guides our work in Indonesia, Costa Rica, Ukraine, Romania and adaptive sport.</p>
    <p class="statement">We come back. We train the people who stay. And we build what remains when we leave.</p>
  </div>
</div></section>

<section class="bg-paper"><div class="wrap">
  <span class="eyebrow">Why we exist</span>
  <h2>Disability that systems overlook</h2>
  <p>Disability is a universal human reality, but the response to it is shaped by poverty, belief, geography, war and stigma. Across very different places we have seen the same pattern. Four gaps keep people from the care they need, and we respond to all four.</p>
  <div class="grid g4" style="margin-top:var(--s3)">
    <div class="card"><h3>Hidden and stigmatised</h3><p>In many communities disability is linked to shame or belief. Children are kept at home, out of school, so their needs are never assessed. We answer with home visits, trusted local partners and work with families, schools and media.</p></div>
    <div class="card"><h3>Care that comes and goes</h3><p>Complex disability needs repeated, adjusted care. Short visits create hope but rarely continuity. We return to the same people, year after year, and are building a permanent centre.</p></div>
    <div class="card"><h3>Thin local capacity</h3><p>Specialist paediatric and rehabilitation skills are scarce, and local therapists often lack mentoring and equipment. We offer hands-on training, university partnerships and, over time, employed local professionals.</p></div>
    <div class="card"><h3>Rebuilding forgets people</h3><p>War and disaster create new disabilities, while reconstruction focuses on roads and buildings. We provide rehabilitation in Ukraine and are developing a Human Recovery programme.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <span class="eyebrow">Our values</span><h2>Four pillars in everything we do</h2>
  <div class="grid g4">
    <div class="card redline"><h3>Dignity first</h3><p>Every person with a disability has inherent dignity. We understand the person, family and context before offering care, and we represent people with consent and respect.</p></div>
    <div class="card redline"><h3>Care that returns</h3><p>We go back to the same communities and to people who cannot reach us. Continuity is the core of our clinical value.</p></div>
    <div class="card redline"><h3>Capacity from within</h3><p>We train local therapists, families and carers, and strengthen local institutions so that knowledge and care remain in the community.</p></div>
    <div class="card redline"><h3>Honest impact</h3><p>We report clearly and conservatively: people separate from sessions, income separate from value, what we know separate from what we hope.</p></div>
  </div>
  <p class="note" style="margin-top:var(--s3)">Running through all four is cultural humility: we seek to understand before we act, and add support without erasing what is already there.</p>
</div></section>

<section class="bg-paper"><div class="wrap split">
  <div><span class="eyebrow">Ten years of proof</span><h2>How we got here</h2></div>
  <ol class="timeline">
    <li><strong class="yr">2016</strong>Hands With Heart begins in Bali. The volunteer and disability-care model takes shape.</li>
    <li><strong class="yr">2018</strong>The association is registered in Spain, giving the organisation a formal legal base.</li>
    <li><strong class="yr">2021</strong>Our Costa Rica work grows, and our contribution is recognised by the UN as an example of good practice for the SDGs.</li>
    <li><strong class="yr">2023</strong>First direct field work in Ukraine, an institutional agreement in Chaco, Argentina, and growing support for adaptive surfing.</li>
    <li><strong class="yr">2024</strong>Our US 501(c)(3) is established, opening US philanthropy and partnerships.</li>
    <li><strong class="yr">2025</strong>€16,000 of infrastructure support to partner centres in Bali, and renewed agreements with local partners.</li>
    <li class="next"><strong class="yr">2026–2029</strong>The shift from missions to permanent systems: Bahía de Niños in Bali, a local workforce, and Human Recovery.</li>
  </ol>
</div></section>

<section><div class="wrap">
  <span class="eyebrow">Our commitments</span><h2>Trust is what lets us work in people's homes, schools and hospitals</h2>
  <ol class="steps">
    <li><span><strong>Care is free for beneficiaries.</strong> Children, adults and families are never charged for our care, and core care is protected from any ability-to-pay model.</span></li>
    <li><span><strong>Local law comes first.</strong> We work within each country's licensing and professional rules, and prioritise local professionals.</span></li>
    <li><span><strong>Dignity and consent in every story.</strong> Images and testimonies are published only with consent, never to create pity.</span></li>
    <li><span><strong>Honest, conservative numbers.</strong> People are separate from sessions, and direct value is separate from income.</span></li>
    <li><span><strong>Planned is not secured.</strong> Emerging projects are labelled as emerging, and restricted gifts are used as promised and reported.</span></li>
  </ol>
</div></section>

<section class="bg-paper" id="founder"><div class="wrap split">
  <div>
    <div class="portrait">Portrait of Dr Jorge Aranda<br>(consented photograph to be added)</div>
  </div>
  <div>
    <span class="eyebrow">Our founder</span>
    <h2>Dr Jorge Aranda</h2>
    <p class="small" style="margin-bottom:var(--s2)">Founder and CEO</p>
    <p>Jorge is an osteopath and clinical teacher. He studied osteopathic medicine in London, completed a Master's in Paediatric Osteopathy in San Diego, California, and holds a PhD from Rome. He has taught at the British College of Osteopathic Medicine, the University of Murcia, the FICO School of Osteopathy in Warsaw and Universitas Dhyana Pura in Bali, among other schools.</p>
    <p>In 2016 he began Hands With Heart from a simple decision in Bali: to respond respectfully to the suffering of children with disabilities by offering what we could offer best, which was free healthcare, presence and care. He has led the Foundation since, continues to lead clinical teams in the field, including in Ukraine, and coordinates our Human Recovery work.</p>
    <p>He has spoken about disability and collective trauma to students and communities in Bali, represented the Foundation at international professional conferences, and was recognised at the Cadena 100 awards in December 2022 for his work with a child in Romania.</p>
    <blockquote class="quote" style="margin-top:var(--s3)">“Relieving pain is not enough. We must also be willing to be present where it hurts most.”<cite>Dr Jorge Aranda, 2024 Annual Report</cite></blockquote>
    <p class="todo" style="margin-top:var(--s3)">To confirm with Jorge: the training and teaching details above come from a public faculty profile, and he should check them and supply a consented portrait.</p>
  </div>
</div></section>

<section id="advisors"><div class="wrap">
  <span class="eyebrow">Our advisors</span><h2>People who guide us</h2>
  <p>Our advisors bring clinical, academic and institutional experience to the Foundation as it grows from missions to permanent systems of care.</p>
  {person_cards(ADVISORS, example=True)}
  <p class="todo" style="margin-top:var(--s3)"><strong>Examples only.</strong> These advisor profiles are placeholders to show the layout. Replace them with the real board of advisors.</p>
</div></section>

<section class="bg-paper" id="team"><div class="wrap">
  <span class="eyebrow">Our team</span><h2>A volunteer-powered team, built to last</h2>
  <p>Hands With Heart runs on the commitment of a small team and its volunteers. In 2025 the Spanish accounts recorded no salaried employees; 83 volunteers and clinical team members took part in our work in 2024. That keeps costs low, and it concentrates responsibility on a few people, so we are building the roles that will let the organisation last: programme leads, finance, monitoring and evaluation, safeguarding, and communications.</p>
  <p>Volunteers are part of our method, not its purpose. Osteopaths, physiotherapists, behavioural optometrists, students and recent graduates train before every programme and work under senior supervision, alongside local therapists.</p>
  {person_cards(TEAM)}
  <p class="todo" style="margin-top:var(--s3)">To complete: surnames, the remaining roles and consented portraits.</p>
</div></section>

<section id="team-leaders"><div class="wrap">
  <span class="eyebrow">Our team leaders</span><h2>Senior clinicians who keep care safe</h2>
  <p>Team leaders are senior clinicians with at least ten years of paediatric experience. They protect clinical quality, supervise volunteers, lead workshops and carry operational responsibility for each programme. They are the reason families can trust the team that arrives.</p>
  {person_cards(LEADERS, example=True)}
  <p class="todo" style="margin-top:var(--s3)"><strong>Examples only.</strong> We have between 10 and 15 team leaders. These twelve profiles are placeholders to show the layout. Replace them with the real team leaders.</p>
</div></section>

<section class="bg-red"><div class="wrap grid g2" style="align-items:center">
  <div><span class="eyebrow">Help us return</span><h2>Help build Bahía de Niños</h2><p>A permanent, locally led centre in Bali, where children with disabilities get free care every week, not once a year.</p></div>
  <div style="justify-self:end"><a class="btn btn-primary" href="donate.html">Donate</a></div>
</div></section>
"""

# ------------------------------------------------------------------ OBJECTIVES
OBJ = {
    "care": dict(
        code="ESO1 · Care", title="Free healthcare for people with disabilities", file="care.html",
        lede="Children and adults with disabilities in underserved settings receive the specialised care they need, free of charge, and receive it more than once.",
        problem="Children and adults with disabilities in underserved communities receive little or no specialised care. Poverty, distance and conflict keep them out of reach, and the care that does arrive is often a single visit.",
        what=["Since 2016 we have returned to the same communities in Bali, Costa Rica, Ukraine and Romania, and to the same athletes in adaptive sport.",
              "To scale this up, we protect what works: supervised multidisciplinary teams in osteopathy, physiotherapy, behavioural optometry and rehabilitation; home visits for those who cannot travel; and reporting of people and sessions separately, so that continuity is the measure of our clinical commitment."],
        inputs=["Volunteer clinicians, students and senior team leaders", "On-site supervision and clinical protocols", "Partner schools, yayasan, clinics and rehabilitation centres", "Translation and local coordination", "Volunteer fees, donations and organiser contributions", "Clinical equipment and transport for home visits"],
        outputs=["Free clinical sessions delivered by programme", "Home visits for people who cannot reach care", "Repeat care for the same people over years", "Healthcare teams at para surfing championships", "Annual reporting of people, sessions and value"],
        outcome="People with disabilities receive continuous, specialised care that is adjusted over time. Function, comfort and participation improve.",
        impact="People with disabilities in neglected settings live with greater health, autonomy and dignity.",
        assumptions=["Partners continue to grant access", "Enough qualified volunteers and team leaders", "Legal permission for each activity", "Security allows travel"],
        evidence="In 2025 we delivered 1,751 clinical sessions to 713 people across Bali, Costa Rica, Ukraine, adaptive sport and Romania.",
        links=[("Missions", "../projects/missions.html"), ("ParaSurf", "../projects/parasurf.html")]),
    "knowledge": dict(
        code="ESO2 · Knowledge", title="Training and mentorship for local healthcare professionals", file="knowledge.html",
        lede="Our goal is not only to provide care, but to leave knowledge behind.",
        problem="Specialist paediatric and rehabilitation skills are scarce where we work. Local therapists lack mentoring, equipment and access to training, and families are rarely shown how to continue care at home.",
        what=["Every programme combines patient care with education: international volunteers work alongside local therapists, universities, schools and community organisations, sharing practical skills that keep benefiting people after each visit ends.",
              "To scale this up, we are turning that practice into structured training: a mentoring ladder for local professionals, guidance for families and carers, university partnerships, and training exchange for Ukrainian rehabilitation teams. Volunteers are trained too, through our Training in Pediatric Disability before every programme."],
        inputs=["Senior clinicians with 10+ years' paediatric experience", "Training in Pediatric Disability curriculum", "University partners in Indonesia, Spain and the US", "Local therapists, carers and families", "Translation and teaching materials", "Funding for training and faculty time"],
        outputs=["Local professionals trained and mentored (58 capacity-building participants in 2025)", "Families and carers shown home routines", "Volunteers trained before every programme", "University placements, teaching and research", "Training modules for Ukrainian teams"],
        outcome="Local professionals deliver better disability care with more confidence, and families support care between visits. Knowledge stays when visiting teams leave.",
        impact="A stronger local workforce able to provide quality disability care without depending on outside teams.",
        assumptions=["Local professionals can take part", "Training is recognised locally", "Universities stay engaged", "Trainees remain in their communities"],
        evidence="We work with Universitas Dhyana Pura in Bali, whose agreement covers training, student participation and local capacity building, including its Faculty of Medicine, and with Western University of Health Sciences in California.",
        links=[("Partners", "../partners.html"), ("Bahía de Niños", "../projects/bahia-de-ninos.html")]),
    "permanence": dict(
        code="ESO3 · Permanence", title="Sustainable community-based healthcare solutions", file="permanence.html",
        lede="Our goal is to solve the structural weakness of mission-based care: continuity.",
        problem="Mission-based care cannot provide year-round continuity. Families face waiting lists, cost and transport barriers, and partner institutions lack the facilities to sustain care.",
        what=["Repeated missions have shown both the demand and the deeper problem: families need care all year round, in a place that remains after international teams leave.",
              "This is where scaling up is most visible. The flagship is Bahía de Niños, a permanent, Indonesian-led base in Bali for paediatric disability care, training and vocational inclusion. Alongside it: infrastructure support for partner institutions (€16,000 in Bali in 2025), home-care models for families, and community-based recovery pilots through Human Recovery."],
        inputs=["US$400,000 seed commitment and remaining capital (approx. US$250,000)", "Site in Sibang; land and legal agreements", "Indonesian yayasan and training structure", "Indonesian clinical staff", "Partner institutions and Ukrainian rehabilitation centres", "Safeguarding, clinical-governance and M&E systems"],
        outputs=["Bahía de Niños Phase 1 built, equipped and staffed", "Infrastructure improvements at partner institutions", "Pilot vocational pathways for young people", "One Human Recovery pilot with partners and budget", "Operating model with 24-month funding"],
        outcome="Year-round, locally led disability care in Bali, reaching approximately 600 children in its first three years, and community-based models that continue without visiting teams.",
        impact="Communities that sustain quality disability care themselves, and models that can be replicated elsewhere.",
        assumptions=["Land, entity and licensing finalised", "Capital gap closed", "Operating funding secured", "Local staff recruited and retained"],
        evidence="In 2025 our donors' trust let us fund bathroom renovations at SLB Negeri 1 Denpasar, swimming-pool support at Yayasan Legong and a roof renovation at Yayasan Mentari Fajar.",
        links=[("Bahía de Niños", "../projects/bahia-de-ninos.html"), ("Missions", "../projects/missions.html")]),
    "advocacy": dict(
        code="ESO4 · Advocacy", title="Change social perceptions and barriers towards people with disabilities", file="advocacy.html",
        lede="Care alone cannot reach a child who is kept at home. The barriers people with disabilities face are often social before they are clinical.",
        problem="Stigma, shame and exclusion keep many people with disabilities hidden from care, school and community life. Public and policy agendas rarely give disability and rehabilitation priority.",
        what=["In ten years of fieldwork we have seen disability hidden by shame and belief in Bali, isolated by geography in Costa Rica, multiplied by war in Ukraine, and celebrated as performance in adaptive sport. Each setting shows that perceptions decide who is brought for care, who goes to school and who is included.",
              "To scale our impact beyond the clinic, we work with families and communities to reduce stigma, support schools to include children with disabilities, tell consent-based stories that show agency rather than pity, use adaptive sport to show ability, and keep rehabilitation and inclusion visible in reconstruction and health policy, led by people with lived experience. This objective is new, and we will start with two or three focused workstreams, beginning with families in Bali."],
        inputs=["Ten years of field knowledge and stories", "People with lived experience, including peer experts", "Local partners, schools and community leaders", "Communications capacity and the brand manual", "Adaptive sport platforms", "Policy forums"],
        outputs=["Community awareness sessions in partner areas", "Inclusion support for partner schools", "Consent-based stories and campaigns", "Media and forum engagement", "Policy input on rehabilitation and inclusion"],
        outcome="Families are more willing to seek care and include their children; communities see people with disabilities as capable and entitled to take part; disability is more visible in policy.",
        impact="Societies where people with disabilities are seen, included and able to claim their rights.",
        assumptions=["Local and lived-experience voices lead", "Consent is in place", "Communities are open to dialogue", "Channels to policymakers exist"],
        evidence="We seek first to understand how each community sees disability, then add support without erasing what exists. People with disabilities and their families shape the message.",
        links=[("Stories", "../stories.html"), ("ParaSurf", "../projects/parasurf.html")]),
    "sustainability": dict(
        code="ESO5 · Sustainability", title="Diversify sources of funds and build strong partnerships for sustainability", file="sustainability.html",
        lede="Our goal is to fund the mission for the long term, while keeping care free for the people we serve.",
        problem="Project-based fundraising, dependence on a small team and limited unrestricted income leave the organisation fragile, and make it hard to sustain permanent solutions.",
        what=["We have operated with almost all resources going directly to programmes and no salaried staff in our Spanish accounts. That efficiency has a cost: fundraising is project by project, some programmes need ongoing subsidy, and growth depends on a few people.",
              "Scaling up needs a funding base to match. We are building a portfolio of capital philanthropy, institutional grants, corporate partnerships, university and research funding, organiser contributions and recurring unrestricted giving. We will become grant-ready, and turn our network into partnerships with a defined status, owner, role and value exchange."],
        inputs=["Fundraising, grants and compliance expertise", "CRM and partnership register", "Finance systems and programme budgets", "Verified figures and annual reporting", "Governance across Spain, the US, Costa Rica and Indonesia", "Board and donor networks"],
        outputs=["Funding strategy and qualified pipeline", "Named donor packages for Bahía de Niños", "Grant-ready compliance pack", "Recurring giving programme", "Partnership agreements with roles and value exchange"],
        outcome="More diversified and predictable income, including a growing unrestricted share, and long-term partnerships that strengthen delivery.",
        impact="A resilient, trusted organisation able to sustain care, training, permanent solutions and advocacy.",
        assumptions=["Donors value transparency and evidence", "Stable economic conditions", "We can show measurable impact", "Capacity to steward relationships"],
        evidence="In 2025 the Spanish accounts recorded €123,752.58 of income and a small surplus of €544.64; the US Form 990-EZ recorded $133,652 in revenue and $133,100 in expenses.",
        links=[("Reports", "../reports.html"), ("Partners", "../partners.html"), ("Donate", "../donate.html")]),
}


def objective_body(o):
    fl = lambda t, items: f"<h3>{t}</h3>{ul(items)}"
    links = " ".join(f'<a class="pill" href="{h}">{e(t)}</a>' for t, h in o["links"])
    return head(o["title"], o["lede"], o["code"],
                [("Our objectives", "index.html"), (o["code"], None)]) + f"""
<section><div class="wrap split">
  <div><span class="eyebrow">What this objective sets out to do</span>
  <div class="callout"><span class="eyebrow">The problem</span><p style="font-family:var(--serif);font-size:1.15rem">{e(o['problem'])}</p></div></div>
  <div>{''.join(f'<p>{e(p)}</p>' for p in o['what'])}
  <p class="note">{e(o['evidence'])}</p></div>
</div></section>
<section class="bg-paper"><div class="wrap">
  <span class="eyebrow">How we expect change to happen</span><h2>From inputs to impact</h2>
  <div class="flow">
    <div><span class="eyebrow">Inputs</span><h3>What we invest</h3>{ul(o['inputs'])}</div>
    <div><span class="eyebrow">Outputs</span><h3>What we deliver</h3>{ul(o['outputs'])}</div>
    <div class="mid"><span class="eyebrow">Outcome</span><h3>What changes</h3><p>{e(o['outcome'])}</p></div>
    <div class="final"><span class="eyebrow">Impact</span><h3 style="font-family:var(--serif);font-weight:400;font-size:1.35rem;line-height:1.35">{e(o['impact'])}</h3></div>
  </div>
  <div class="callout" style="margin-top:var(--s4)"><span class="eyebrow">Assumptions we monitor</span><p>{' · '.join(e(a) for a in o['assumptions'])}</p></div>
</div></section>
<section><div class="wrap"><h3>Related</h3><p>{links}</p>
<p class="note">This objective is part of our Strategic Direction 2026–2029. We test our theory of change every year, and name what did not work in our annual report.</p></div></section>
"""


def objectives_index():
    cards = "".join(
        f'<a class="card topline" href="{o["file"]}"><span class="eyebrow">{e(o["code"])}</span><h3>{e(o["title"])}</h3><p>{e(o["lede"])}</p></a>'
        for o in OBJ.values())
    return head("Five objectives. One set of systems to make them last.",
                "Between 2026 and 2029 our aim is to scale up free, repeated, respectful disability care, and the local capacity to sustain it, on systems strong enough to carry it.",
                "Our objectives") + f"""
<section><div class="wrap"><span class="eyebrow">External objectives</span><h2>What we will scale up for people and communities</h2>
<div class="grid g3">{cards}</div></div></section>
<section class="bg-paper"><div class="wrap grid g2" style="align-items:center">
 <div><span class="eyebrow">Internal objectives</span><h2>Systems for scale</h2>
 <p>Underneath all five sits the organisational capability that makes growth safe, fundable and sustainable: governance, safeguarding, evidence, people and communication. Every step up in scale must be matched by a step up in systems.</p>
 <a class="btn btn-secondary" href="systems-for-scale.html">Read about our systems</a></div>
 <div class="card"><h3>Our scaling principle</h3><p>We grow only as fast as our governance, safeguarding and evidence allow. We move to the next stage only when the systems for it are in place.</p></div>
</div></section>
<section><div class="wrap"><span class="eyebrow">Our theory of change</span><h2>Our aim, our condition, our first test</h2>
<div class="grid g3">
<div class="card redline"><h3>Our aim</h3><p>Scale up free, repeated, respectful disability care, and the local capacity to sustain it.</p></div>
<div class="card redline"><h3>Our condition</h3><p>Systems before scale. We grow only as fast as our governance, safeguarding and evidence allow.</p></div>
<div class="card redline"><h3>Our first test</h3><p>Can we launch Bahía de Niños on a legal, locally led and funded footing while missions continue?</p></div>
</div></div></section>
"""


systems_body = head("Systems for scale",
    "The internal objectives: the organisational capability that makes growth safe, fundable and sustainable.",
    "Internal objectives",
    [("Our objectives", "index.html"), ("Systems for scale", None)]) + """
<section><div class="wrap">
<p>Today Hands With Heart runs on the commitment of a small team and its volunteers. That has been enough to prove the model. It is not enough to run a permanent centre, manage restricted grants, safeguard children year-round or report to institutional funders. Growing without these systems would put children, partners, volunteers and the organisation's reputation at risk.</p>
<div class="grid g5" style="margin-top:var(--s4)">
 <div class="card topline"><span class="eyebrow">ISO1</span><h3>Strengthen governance across entities</h3><p>Clarify roles, approvals and reporting across the Spanish association, the US 501(c)(3), the Costa Rican foundation and, in future, the Indonesian <em>yayasan</em>. Keep brand and legal form distinct.</p></div>
 <div class="card topline"><span class="eyebrow">ISO2</span><h3>Make safeguarding and clinical governance funder-ready</h3><p>Child and vulnerable-adult safeguarding, consent, data protection, complaints and professional scope defined by jurisdiction.</p></div>
 <div class="card topline"><span class="eyebrow">ISO3</span><h3>Standardise evidence and learning</h3><p>Collect people, sessions, home visits, training, costs, stories and consent after every programme; add outcome measures and programme budgets.</p></div>
 <div class="card topline"><span class="eyebrow">ISO4</span><h3>Develop programme leadership and people</h3><p>Operational leads for each major programme; volunteer and team-leader standards; less dependence on a small number of people.</p></div>
 <div class="card topline"><span class="eyebrow">ISO5</span><h3>Professionalise communication</h3><p>One brand, one verified set of figures, consent-based storytelling and a website that matches our standards.</p></div>
</div></div></section>
<section class="bg-paper"><div class="wrap">
<span class="eyebrow">What scaling depends on</span><h2>Every step up in scale needs a step up in systems</h2>
""" + table(["Scaling step", "System it depends on", "Internal objective"], [
    ["Raise and manage institutional grants", "Governance, financial procedures, restricted-funds tracking, compliance pack", "ISO1 · ISO5"],
    ["Open and run Bahía de Niños", "Indonesian entity, licensing, safeguarding, clinical governance, operating budget", "ISO1 · ISO2"],
    ["Show impact to funders", "Evaluation framework, verified figures, outcome measures", "ISO3"],
    ["Run more programmes at once", "Programme leads, team-leader standards, delegation", "ISO4"],
    ["Grow public support and advocacy", "Brand, consent-based storytelling, one source of figures", "ISO5"],
]) + """
<div class="grid g3">
 <div class="card redline"><span class="eyebrow">What we control</span><h3>Quality of care and training</h3><p>Sessions, home visits and people by programme; training delivered; consent and safeguarding records.</p></div>
 <div class="card redline"><span class="eyebrow">What we influence</span><h3>Change for people and teams</h3><p>Continuity (sessions per person, return rates), functional and family-reported outcomes, local staff employed and retained.</p></div>
 <div class="card redline"><span class="eyebrow">What we contribute to</span><h3>Systems that last</h3><p>Communities sustaining care, human recovery in reconstruction policy, reduced stigma and wider inclusion.</p></div>
</div></div></section>
<section><div class="wrap"><div class="callout"><span class="eyebrow">Learning cycle</span><p><strong>We test this theory every year.</strong> After each programme, teams submit standard data within two weeks. Each year, the annual report compares results against our theory of change, names what did not work, and updates assumptions.</p></div></div></section>
"""

# ------------------------------------------------------------------ PROJECTS
projects_index = head("Our projects",
    "Three ways we put care, training and permanence into practice.", "Our projects") + """
<section><div class="wrap"><div class="grid g3">
 <a class="card topline" href="parasurf.html"><span class="tag sport">Adaptive Sport</span><h3>ParaSurf</h3><p>Healthcare teams at para surfing championships, keeping athletes mobile, pain-free and ready to compete.</p><span class="link-arrow">See ParaSurf →</span></a>
 <a class="card topline" href="bahia-de-ninos.html"><span class="tag bali">Bali</span><h3>Bahía de Niños</h3><p>A permanent home for free disability care, rehabilitation, training and inclusion for children in Bali. In development.</p><span class="link-arrow">See Bahía de Niños →</span></a>
 <a class="card topline" href="missions.html"><span class="tag ink">Global Health Programmes</span><h3>Missions</h3><p>Repeated free care in Bali, Costa Rica, Ukraine, Romania and Argentina, delivered with local partners.</p><span class="link-arrow">See our missions →</span></a>
</div></div></section>
<section class="bg-paper"><div class="wrap split"><div><span class="eyebrow">How they fit together</span><h2>Missions are the engine. Permanence is the shift.</h2></div>
<div><p>Field programmes deliver free care and training today, and build the trust that permanent solutions depend on. New investment goes first to Bahía de Niños and a defined Human Recovery pilot. Every programme contributes stories and evidence to our work on changing how disability is seen, with consent.</p></div></div></section>
"""

parasurf_body = head("ParaSurf",
    "Disability shown through performance, autonomy and sport, with healthcare teams that keep para surfers mobile, pain-free and ready to compete.",
    "Adaptive Sport · Our projects", [("Our projects", "index.html"), ("ParaSurf", None)]) + """
<section><div class="wrap split">
 <div><span class="tag sport">Adaptive Sport</span><h2>Healthcare at the water's edge</h2></div>
 <div>
  <p>Through the professional adaptive surfing community and international competition settings, Hands With Heart provides free healthcare teams for para surfers. The programme shows disability through performance, autonomy, sport and long-term health, rather than only vulnerability.</p>
  <p>Our teams support athletes between heats with osteopathy and rehabilitation, so that they can compete with less pain and recover well. In 2024 we worked alongside the International Surfing Association at its championships, and organisers increasingly recognise specialised healthcare as a necessary part of the adaptive sport ecosystem.</p>
 </div></div></section>
<section class="bg-ink"><div class="wrap"><span class="eyebrow">Adaptive sport · 2025</span>
 <div class="grid g4">""" + stat("106", "Athletes treated") + stat("252", "Clinical sessions") + stat("12", "Local professionals trained") + stat("US$9,000", "Contributed by organisers") + """</div>
 <p class="small" style="color:#cfcfcf;margin-top:var(--s3)">2025: Hawaii (59 athletes, 127 sessions) and California (47 athletes, 125 sessions, with 12 local professionals trained over three hours).</p></div></section>
<section><div class="wrap"><span class="eyebrow">Where we have worked</span><h2>Events and seasons</h2>
""" + table(["Year", "Events", "Athletes", "Sessions"], [
    ["2023", "Hawaii; California (two events)", "240", "527"],
    ["2024", "Byron Bay (Australia); Hawaii; Costa Rica Surf Adaptado; Stoke for Life (USA); ISA (USA)", "263", "456"],
    ["2025", "Hawaii; California", "106", "252"],
]) + """
<div class="grid g3">
 <div class="card redline"><h3>Care</h3><p>Specialised healthcare for professional adaptive athletes, delivered free by our teams.</p></div>
 <div class="card redline"><h3>Training</h3><p>Local professionals learn alongside our clinicians at each event.</p></div>
 <div class="card redline"><h3>Visibility</h3><p>Adaptive sport shows what people with disabilities achieve, and changes how disability is seen.</p></div>
</div>
<p class="note" style="margin-top:var(--s3)">ParaSurf contributes to our objectives on <a href="../objectives/care.html">free healthcare</a> and <a href="../objectives/advocacy.html">changing perceptions</a>. Photographs of athletes appear only with their consent and are credited to their photographers.</p>
</div></section>
<section class="bg-paper"><div class="wrap grid g2" style="align-items:center"><div><span class="eyebrow">Are you an organiser?</span><h2>Bring a healthcare team to your event</h2><p>Organisers who work with us help cover team costs. Get in touch to talk about your championship.</p></div><div style="justify-self:end"><a class="btn btn-secondary" href="../contact.html">Contact us</a></div></div></section>
"""

PACKAGES = [
    ("01", "Complete Pediatric Rehabilitation Gym", "Core for opening", "26,000", "50,000"),
    ("02", "Advanced Photobiomodulation / Therapeutic Laser System", "Therapy technology", "20,000", "40,000"),
    ("03", "Equipped Pediatric Treatment Rooms", "Core for opening", "21,000", "40,000"),
    ("04", "Sensory & Regulation Room", "Core for opening", "27,000", "50,000"),
    ("05", "Advanced Supported Gait Training System", "Therapy technology", "32,000", "75,000"),
    ("06", "Interactive Movement & Therapy Floor", "Therapy technology", "9,000", "25,000"),
    ("07", "Accessible Changing, Shower & Transfer Suite", "Core for opening", "26,000", "50,000"),
    ("08", "Digital Gait, Balance & Force-Plate System", "Therapy technology", "18,000", "45,000"),
    ("09", "Eye-Gaze Communication & AAC Station", "Therapy technology", "18,000", "30,000"),
    ("10", "3D Printing & Adaptive Equipment Workshop", "Therapy technology", "12,000", "30,000"),
    ("11", "Portable Clinical Ultrasound / POCUS System", "After clinical validation", "8,000", "20,000"),
    ("12", "Pressure Mapping & Seating Assessment System", "After clinical validation", "12,000", "25,000"),
    ("13", "Functional Electrical Stimulation (FES) Package", "After clinical validation", "14,000", "30,000"),
    ("14", "Robotic / Assisted Upper-Limb Rehabilitation System", "After clinical validation", "22,000", "40,000"),
    ("15", "Adaptive / Inclusive Playground", "Built environment & legacy", "55,000", "100,000"),
    ("16", "Covered Outdoor Therapy Pavilion", "Built environment & legacy", "30,000", "50,000"),
]

bahia_body = head("Bahía de Niños",
    "A permanent home for free disability care, rehabilitation, training and inclusion for children in Bali.",
    "Flagship project · Bali, Indonesia", [("Our projects", "index.html"), ("Bahía de Niños", None)]) + f"""
<section style="padding-top:var(--s4)"><div class="wrap">
 <figure><img src="../assets/img/bahia-aerial-concept.jpg" alt="Aerial concept image of the Bahía de Niños site, showing a care and coordination building, a rehabilitation pavilion with rows of treatment tables, gardens and parking" width="1400" height="976"><figcaption><span class="badge-ill">Illustrative concept image</span> Final layout will follow the architect's survey-based design.</figcaption></figure>
</div></section>
<section><div class="wrap">
 <span class="tag bali">Bali · In development</span>
 <div class="split"><div><h2>Children who need care every week, not once a year</h2></div>
 <div>
  <p>In Bali, disability can carry social shame and karmic interpretation. Many children with cerebral palsy, developmental delay and neurological conditions are kept at home, with little access to specialised therapy. Transport, cost and distance make regular clinic visits hard for families, and specialist paediatric rehabilitation skills remain scarce.</p>
  <p>Since 2016 we have returned to Bali again and again, working with local schools and foundations and visiting children at home. In 2025 alone, the Bali programme delivered <strong>879 clinical sessions to 190 children and adults</strong>, including 90 home visits, and trained 24 local participants.</p>
  <p>Those visits proved the demand and revealed the deeper problem: <strong>complex disability needs continuity</strong>. Visiting teams build trust, but they leave. Families need care that is there every week, local professionals who keep learning, and a place that remains.</p>
 </div></div>
 <div class="grid g3" style="margin-top:var(--s3)">{stat("~250", "Children with multiple disabilities treated at SLB Negeri 1 Denpasar")}{stat("600", "Children on Yayasan Legong's waiting list")}{stat("300", "Children on Yayasan Mentari Fajar's list")}</div>
 <p class="small" style="margin-top:var(--s2)">Figures as published by Hands With Heart for its Bali partners (up to).</p>
</div></section>

<section class="bg-ink"><div class="wrap"><span class="eyebrow">At a glance</span>
 <div class="grid g4">{stat("5,404 m²", "Surveyed site, Sibang")}{stat("~600", "Children in the first 3 years")}{stat("~300", "People trained in 3 years")}{stat("14", "Indonesian staff at opening")}</div>
 <p style="color:#e6e6e6;margin-top:var(--s3)"><strong>The gap Bahía de Niños closes:</strong> from periodic missions to year-round care; from visiting experts to a trained local team; from borrowed rooms to a place built for children with disabilities.</p></div></section>

<section><div class="wrap"><span class="eyebrow">Aim and strategy</span><h2>What Bahía de Niños will achieve</h2>
 <p class="lede">To give children with disabilities in Bali continuous, free, specialised care in a permanent, locally led centre, and to build the local capacity to sustain it.</p>
 <div class="grid g3">
 <div class="card redline"><span class="eyebrow">Care</span><h3>Free, continuous care</h3><p>Free or accessible paediatric disability and rehabilitation services, delivered by an Indonesian team in a compliant model. Core care is never tied to ability to pay.</p></div>
 <div class="card redline"><span class="eyebrow">Train</span><h3>Local capacity</h3><p>A training ladder for Indonesian physiotherapists and health professionals, families and carers, with international faculty and university partners.</p></div>
 <div class="card redline"><span class="eyebrow">Include</span><h3>Pathways to participation</h3><p>As the centre grows, vocational skills and work pathways for young people with disabilities: crafts, gardening, café and retail.</p></div></div>
 {table(["Our approach", ""], [
   ["Local first, legally compliant", "Delivery by Indonesian professionals within an Indonesian yayasan and training structure. Foreign clinical practice is never assumed; international input focuses on education and approved activities."],
   ["Built on trust", "Ten years of repeated work with SLB Negeri 1 Denpasar, Yayasan Legong and Yayasan Mentari Fajar, and a signed agreement with Universitas Dhyana Pura."],
   ["Simple, robust, Balinese", "Contemporary Balinese design: natural ventilation, deep roofs, locally repairable materials. Calm rather than luxurious, and easy to maintain."],
   ["Phased and gated", "Phase 1 is deliberately compact: two units that can open safely. Each next step proceeds only when design, legal, funding and operating conditions are met."],
   ["Funded to run, not only to build", "Capital fundraising is matched by a 24-month operating plan, so the building opens with a team and keeps running."]])}
</div></section>

<section class="bg-paper"><div class="wrap"><span class="eyebrow">Site and Phase 1 design</span><h2>A compact centre that can open safely</h2>
 <p>An officially surveyed site of 5,404 m² in Sibang, Badung Regency, with two functional units. The design is contemporary Balinese, not an institutional clinic.</p>
 <div class="grid g2" style="margin:var(--s3) 0">
  <figure><img src="../assets/img/bahia-concept-rehab-pavilion.jpg" alt="Concept render of the rehabilitation pavilion: a naturally ventilated open hall with a pitched tile roof, set in tropical garden" loading="lazy" width="1400" height="823"><figcaption><span class="badge-ill">Concept</span> Rehabilitation pavilion (Unit B)</figcaption></figure>
  <figure><img src="../assets/img/bahia-concept-care-unit.jpg" alt="Concept render of the care and coordination building with glazed doors opening onto a veranda" loading="lazy" width="1400" height="823"><figcaption><span class="badge-ill">Concept</span> Care and coordination (Unit A)</figcaption></figure>
 </div>
 <div class="grid g2">
  <div class="card topline"><span class="eyebrow">Unit A · 145–195 m²</span><h3>Care and coordination</h3>{ul(["Reception and family waiting", "Office, administration and records", "Meeting and training room", "Four private treatment-room shells; at least two fully fitted at opening", "Accessible toilet, storage and clinical support"])}</div>
  <div class="card topline"><span class="eyebrow">Unit B · 200–250 m²</span><h3>Rehabilitation and training pavilion</h3>{ul(["Naturally ventilated, weather-protected hall", "Up to 16 treatment tables used at the same time", "Space for two learners per table during training", "Lockable storage and accessible toilet", "Flexible for care, teaching and family workshops"])}</div>
 </div>
 <p class="note" style="margin-top:var(--s3)">Optional items are priced separately as Phase 1B: a salt-water therapy pool, an assisted changing and shower suite, enhanced enclosure and air conditioning, landscape and future vocational works.</p>
</div></section>

<section><div class="wrap split"><div><span class="eyebrow">Where we are now</span><h2>Design, pricing and legal set-up</h2>
 <p>Bahía de Niños is an advanced project, not an idea. The seed funding is committed and the site is surveyed. The current phase turns the concept into a measured, priced and legally sound project before construction begins.</p></div>
 <ol class="timeline">
  <li><strong class="yr">2016–2025 · Done</strong>Repeated missions in Bali; long-term relationships with SLB, Yayasan Legong, Yayasan Mentari Fajar and Universitas Dhyana Pura; €16,000 of infrastructure support to partner centres in 2025.</li>
  <li><strong class="yr">2025–2026 · Done</strong>US$400,000 seed commitment secured from a major donor.</li>
  <li><strong class="yr">June 2026 · Done</strong>Official boundary, topography and section surveys of the Sibang site.</li>
  <li><strong class="yr">Sept–Oct 2026 · Done</strong>Business plan, opening-year staffing and operating budget, equipment catalogue, and a consolidated architect and contractor design brief (5 October 2026).</li>
  <li class="next"><strong class="yr">Now · In progress</strong>Survey-based design, permit route, measured bill of quantities and at least two comparable contractor quotes.</li>
  <li class="next"><strong class="yr">Now · In progress</strong>Final land agreement and site control; Indonesian yayasan and training structure; written legal opinion on permitted activities and licensing.</li>
  <li class="next"><strong class="yr">Spring 2027 · Target</strong>Construction start of Phase 1, once the decision gate is met.</li>
 </ol></div></section>
<section class="bg-paper"><div class="wrap"><div class="callout" style="margin-top:0"><span class="eyebrow">Decision gate before construction</span><p>A construction deposit is only considered once there is a survey-based design, a coordinated structure and services, a confirmed permit route, a measured bill of quantities and at least two comparable contractor prices. Land and licensing are still being finalised, and we will tell you if timing changes.</p></div>
 <h3>From a two-unit centre to a campus</h3>
 {table(["Phase", "Scope", "Proceeds when"], [
  ["Phase 0 · 2026 – early 2027", "Design, bill of quantities, contractor selection, permits, land agreement, Indonesian entity, legal opinion, recruitment plan, policies (safeguarding, clinical governance, data).", "Decision gate met; capital committed for the base price."],
  ["Phase 1 · Build and open · 2027", "Unit A and Unit B, site works and access. Recruit and train 14 Indonesian staff. Open with 14–20 children per day; core equipment packages in place.", "Building handed over; team in post; 24 months of operating costs covered."],
  ["Phase 1B · Options", "Salt-water therapy pool, assisted changing suite, therapy technology packages, inclusive playground and outdoor pavilion.", "Separately priced and funded; clinical validation where needed."],
  ["Phase 2 · Grow · 2028–2029", "Expand training (around 300 people over three years), add treatment-room fit-out, start vocational pathways for young people, research with university partners.", "Phase 1 runs year-round with outcomes reported."],
  ["Long-term vision", "A campus-like inclusive environment: additional treatment pavilions, therapy pool and wellness pavilion, volunteer residence, community warung and expansion areas.", "Evaluation of Phases 1–2 and new funding."]])}
</div></section>

<section><div class="wrap"><span class="eyebrow">People and operations</span><h2>A local team to run the centre every day</h2>
 <p>The centre opens with 14 Indonesian employees: eight physiotherapists and six support and operations staff. International specialists contribute training and supervision; their costs are not included here.</p>
 <div class="grid g4" style="margin:var(--s3) 0">{stat("US$47,662", "Local team, per year (14 people)")}{stat("US$21,572", "Utilities, facility and mobility")}{stat("US$69,234", "Base annual cost")}{stat("US$83,081", "With a 20% reserve")}</div>
 <p class="note">Core operations include electricity, water, internet, cleaning, maintenance, insurance, accounting and legal compliance, booking and records software, and two adapted transport vehicles. Staff costs are loaded annual estimates, to be confirmed against the 2027 Badung wage floor by an Indonesian accountant.</p>
</div></section>

<section class="bg-paper" id="funding"><div class="wrap"><span class="eyebrow">What we need</span><h2>The funding picture</h2>
 <p>Bahía de Niños needs three kinds of support: capital to build Phase 1, equipment that makes the centre work for children, and operating funding so it runs from day one.</p>
 <div class="grid g3">
  <div class="card topline"><span class="eyebrow">A · Phase 1 capital</span><span class="num">~US$250k</span><p style="margin-top:12px">still to raise, of a US$650,000 Phase 1 ambition. US$400,000 is already committed.</p></div>
  <div class="card topline"><span class="eyebrow">B · Equipment and spaces</span><span class="num">16 packages</span><p style="margin-top:12px">US$20,000 to US$100,000 each. Estimated equipment cost US$350,000; full packages up to US$700,000.</p></div>
  <div class="card topline"><span class="eyebrow">C · Launch operations</span><span class="num">~US$166k</span><p style="margin-top:12px">for the first 24 months (US$83,081 per year), so the centre opens with a funded team.</p></div>
 </div>
 <div class="callout"><span class="eyebrow">Being re-priced</span><p>Our construction estimate was built on a 240 m² reference footprint. The current Phase 1 brief covers about 367–479 m² of covered area, so the measured bill of quantities from the architect and contractors will replace it. The split of the US$650,000 ambition between land and site, construction, equipment and set-up will be confirmed with that price.</p></div>
 <h3 style="margin-top:var(--s4)">Sixteen ways to equip the centre</h3>
 <p>Each opportunity is a complete package: equipment or space plus what it takes to use it well. The suggested gift covers the estimated equipment cost and, where needed, freight, installation, training, consumables, servicing and a replacement reserve. Final amounts are confirmed with current quotations and a donor agreement.</p>
 {table(["#", "Opportunity", "Tier", "Equipment est. (US$)", "Suggested gift (US$)"], [[a, b, c, d, f"<strong>{g}</strong>"] for a, b, c, d, g in PACKAGES])}
 <p class="small">Core for opening: needed for daily care from day one. Therapy technology: extends what therapists can do. After clinical validation: funded once clinical use is confirmed. Built environment and legacy: permanent, visible spaces.</p>
 <figure style="max-width:520px;margin-top:var(--s3)"><img src="../assets/img/bahia-treatment-room-illustrative.jpg" alt="Illustration of a child and a carer with a physiotherapist in a bright treatment room" loading="lazy" width="1400" height="1050"><figcaption><span class="badge-ill">Illustrative</span> Equipped paediatric treatment rooms (opportunity 03). Image for illustration only.</figcaption></figure>
</div></section>
<section class="bg-red"><div class="wrap grid g2" style="align-items:center"><div><span class="eyebrow">Be part of Bahía de Niños</span><h2>Help build a permanent home for care in Bali</h2><p>Recognition, transparent reporting against budget, and an invitation to visit the site and meet the team. Restricted gifts are tracked and reported against their agreed purpose.</p></div><div style="justify-self:end"><a class="btn btn-primary" href="../donate.html">Donate</a></div></div></section>
"""

missions_body = head("Missions",
    "Repeated, free care delivered with local partners. We return to the same people, and we leave skills behind.",
    "Global Health Programmes · Our projects", [("Our projects", "index.html"), ("Missions", None)]) + """
<section><div class="wrap split"><div><span class="eyebrow">How missions work</span><h2>Not a volunteer trip. A committed presence that treats, teaches and builds.</h2></div>
<div><p>Our field programmes send supervised multidisciplinary teams of osteopaths, physiotherapists, behavioural optometrists and students to the same places, year after year. Teams are led by senior clinicians, train before they travel, and work alongside local therapists, who are as visible as the international team.</p>
<p>Care is free for the people we serve. We reach people who cannot travel through home visits. We report people and sessions separately, because for complex disability, repeated care can be more meaningful than one-off intervention.</p>
<div class="actions"><a class="btn btn-secondary" href="../contact.html">Volunteer with a supervised team</a></div></div></div></section>

<section class="bg-paper" id="bali"><div class="wrap">
 <span class="tag bali">Bali · Indonesia</span><h2>Bali Global Health Programme</h2>
 <p class="lede">Where it began in 2016, and our anchor programme. Bahía de Niños is the permanent centre within it.</p>
 <div class="grid g4">""" + stat("190", "People treated · 2025") + stat("879", "Clinical sessions · 2025") + stat("90", "Home visits · 2025") + stat("€16,000", "Infrastructure support · 2025") + """</div>
 <p style="margin-top:var(--s3)">We work with SLB Negeri 1 Denpasar, Yayasan De Legong Anak Bangsa and Yayasan Mentari Fajar, and with Universitas Dhyana Pura, where agreements were renewed in 2025. In 2025 your support funded bathroom renovations at SLB, swimming-pool support at Yayasan Legong and a roof renovation at Yayasan Mentari Fajar. We trained 24 local participants alongside our clinical work.</p>
 <p><a class="link-arrow" href="bahia-de-ninos.html">See Bahía de Niños →</a></p>
</div></section>

<section id="costa-rica"><div class="wrap">
 <span class="tag costa">Costa Rica</span><h2>Costa Rica Global Health Programme</h2>
 <p class="lede">Accessible care in Cartago, and home visits in the Indigenous territories of Bribri and Talamanca.</p>
 <div class="grid g4">""" + stat("225", "People treated · 2025") + stat("300", "Clinical sessions · 2025") + stat("50", "Bribri/Talamanca home visits · 2025") + stat("22", "Capacity-building participants · 2025") + """</div>
 <p style="margin-top:var(--s3)">The Bribri work matters because access itself is part of the value: the team walks into remote areas, accepts difficult conditions, and builds trust through repeated presence. We work with Asociación Dawe Ese Wakpa Kimoie, which promotes projects for Indigenous people with disabilities in Talamanca. This programme has high community value and needs dedicated funding because of logistics, access and smaller teams.</p>
</div></section>

<section class="bg-paper" id="ukraine"><div class="wrap">
 <span class="tag ukraine">Ukraine · Human Recovery</span><h2>Ukraine and REpower</h2>
 <p class="lede">War creates new disabilities and reduces services for those already in need. Reconstruction should rebuild people, not only places.</p>
 <div class="grid g4">""" + stat("104", "People treated in Ukraine · 2025") + stat("188", "Sessions in Ukraine · 2025") + stat("86", "Combat medics treated abroad (REpower) · 2025") + stat("108", "REpower sessions · 2025") + """</div>
 <p style="margin-top:var(--s3)">Our direct field work in Ukraine began with an assessment visit in March 2023, followed by clinical missions. We now treat children with disabilities and soldiers with amputations inside Ukraine, and, through REpower, Ukrainian combat medics abroad. We work alongside the Halychyna Center of Complex Rehabilitation in Lviv and Novovolynsk Central City Hospital.</p>
 <p>This work taught us that care could not focus only on muscles and joints: it also required attention to regulation, safety and presence. In October 2026 we are taking part in the Rebuilding International Forum in Lorca, Spain, as we shape <strong>Human Recovery</strong>, an emerging programme. <span class="tag status">Emerging</span> No future funding or institutional partnership is described as secured until it has been formally agreed.</p>
</div></section>

<section id="romania"><div class="wrap">
 <span class="tag ink">Romania</span><h2>Romania</h2>
 <p>A small, repeated-care programme. In 2025 two people received repeated care across six trips, 24 sessions in all. Romania continues where volunteers and funding are secured.</p>
</div></section>

<section class="bg-paper" id="chaco"><div class="wrap">
 <span class="tag ink">Argentina · Chaco</span><h2>Argentina / Chaco</h2>
 <p>In 2023 we signed an agreement with the Vice-Government, the Ministry of Health, the Ministry of Environment and Territorial Development, and IPRODICH to provide free healthcare to children and people with disabilities in the province of Chaco, reaching 176 people that July and 118 in 2024. No mission was delivered in 2025. We remain committed to the region, and the year showed how hard it is to attract volunteers and funding to this mission area.</p>
</div></section>

<section><div class="wrap"><div class="callout"><span class="eyebrow">Where we go next</span><p>We add a new place only where a trusted local partner invites us and shares responsibility, we can return at least annually, the legal basis for our activity is clear, and the programme has a budget and a funding route. In 2023 we visited Dharamsala, India, and chose not to start a project there because our model was not clearly needed. Responsible growth means knowing where not to go.</p></div></div></section>
"""

# ------------------------------------------------------------------ STORIES
STORIES = [
    ("Bali", "bali", "Pools, roofs and bathrooms: trust turned into infrastructure",
     "In 2025 a donor believed in us because our years of commitment had created legitimacy. That trust became bathroom renovations at SLB Negeri 1 Denpasar, swimming-pool support at Yayasan Legong and a roof renovation at Yayasan Mentari Fajar, chosen with the partners who use these spaces every day.",
     "2025 Annual Report"),
    ("Costa Rica", "costa", "Walking into Bribri territory",
     "Care in the Bribri and Talamanca territories means walking into remote areas and accepting difficult conditions. Together with Asociación Dawe Ese Wakpa Kimoie, our team brings care to families at home, and returns, because trust is built through repeated presence.",
     "2025 Annual Report"),
    ("Ukraine", "ukraine", "Treating the nervous system, not only the body",
     "Treating combat medics, including some who had experienced captivity, and soldiers with severe amputations showed us that care could not focus only on muscles, scars, joints or pain. It also meant attention to regulation, safety, presence and co-regulation.",
     "2024 Annual Report"),
    ("Adaptive Sport", "sport", "Between heats",
     "At para surfing championships our team keeps athletes mobile, pain-free and ready to compete. Here disability is seen through performance, autonomy and sport, and organisers increasingly treat specialised healthcare as part of the event.",
     "Annual Reports 2023–2025"),
]
stories_body = head("Stories",
    "Real people, real places, told with consent. We show agency, never pity.",
    "Stories") + "".join([
    '<section><div class="wrap">',
    '<div class="filter" data-target="#story-list" role="group" aria-label="Filter stories"><button aria-pressed="true" data-filter="all">All</button>',
    '<button aria-pressed="false" data-filter="bali">Bali</button><button aria-pressed="false" data-filter="costa">Costa Rica</button>',
    '<button aria-pressed="false" data-filter="ukraine">Ukraine</button><button aria-pressed="false" data-filter="sport">Adaptive Sport</button></div>',
    '<div id="story-list">',
    "".join(f'<article class="story-item" data-cat="{c}"><div><span class="tag {c}">{e(t)}</span></div><div><h2 style="font-size:1.5rem">{e(h)}</h2><p>{e(p)}</p><p class="small">Source: {e(s)}</p></div></article>' for t, c, h, p, s in STORIES),
    '</div>',
    '<div class="callout"><span class="eyebrow">More stories</span><p>The stories above come from our annual reports. Our full set of impact stories is on our <a href="https://handswithheartfoundation.org/stories/" target="_blank" rel="noopener">current website</a>.</p></div>\n    <div class="todo" style="margin-top:var(--s3)">To add: copy each story from the current site into the <code>STORIES</code> list in <code>build.py</code> (title, text, photo, consent). I could not open that page from my environment, so none of its text has been copied.</div>',
    '</div></section>',
    '<section class="bg-ink"><div class="wrap"><span class="eyebrow">How we tell stories</span><h2>Would the person in this photo, or their family, be proud to see it on our homepage?</h2>',
    '<p>That is our test. We publish images and testimonies only with written consent, we avoid pity-based imagery, we show local therapists as visible as international volunteers, and we name vulnerable people only with explicit consent.</p></div></section>',
])

# ------------------------------------------------------------------ NEWS
NEWS = [
    ("2026-10-05", "5 October 2026", "Bahía de Niños: architect and contractor design brief issued",
     "We issued a consolidated design brief for the first phase of Bahía de Niños, our planned permanent centre in Bali, to the architect and contractors. Next: survey-based design, a measured bill of quantities and comparable contractor quotes.", "projects/bahia-de-ninos.html", "Read about Bahía de Niños"),
    ("2026-10-01", "October 2026", "Taking part in the Rebuilding International Forum, Lorca",
     "Hands With Heart is taking part in the Rebuilding International Forum in Lorca, Spain, as we develop Human Recovery: rebuilding people, not only places.", "projects/missions.html#ukraine", "Read about Ukraine and Human Recovery"),
    ("2026-06-19", "19 June 2026", "Official survey of the Bahía de Niños site completed",
     "The official boundary survey confirmed a 5,404 m² site in Sibang, Badung Regency, Bali.", "projects/bahia-de-ninos.html", "Read about Bahía de Niños"),
    ("2026-01-01", "2026", "2025 Annual Report published",
     "In 2025 we delivered 1,751 clinical sessions to 713 people and generated an estimated €252,450 of direct value. We report both numbers, and say where we need to improve.", "reports.html", "Read the report"),
    ("2026-01-02", "2026", "Public-utility status in Spain",
     "Our Spanish association now holds public-utility status, a step in strengthening our governance for the years ahead.", "objectives/systems-for-scale.html", "Read about our systems"),
    ("2025-12-01", "2025", "€16,000 of infrastructure support to our Bali partners",
     "Bathroom renovations at SLB Negeri 1 Denpasar, swimming-pool support at Yayasan Legong and a roof renovation at Yayasan Mentari Fajar.", "projects/missions.html#bali", "Read about Bali"),
]
news_body = head("News",
    "What is happening at Hands With Heart: milestones, field updates and announcements.", "News") + '<section><div class="wrap">' + "".join(
    f'<article class="news-item"><time datetime="{d}">{e(dl)}</time><div><h2 style="font-size:1.5rem">{e(t)}</h2><p>{e(b)}</p><a class="link-arrow" href="{h}">{e(hl)} →</a></div></article>'
    for d, dl, t, b, h, hl in sorted(NEWS, reverse=True)) + """
<div class="todo" style="margin-top:var(--s4)">To add: new items go in the <code>NEWS</code> list in <code>build.py</code> (date, headline, summary, link). Check these items before publishing.</div>
</div></section>"""

# ------------------------------------------------------------------ REPORTS
REPORTS = [
    ("2025", "Help, Share, and Learn · Since 2016", "Strengthening foundations: stronger reporting, a stronger financial base and a clearer path from missions to permanent infrastructure.",
     [("713", "People"), ("1,751", "Sessions"), ("€123,752.58", "Official income"), ("€252,450", "Direct value")], "reports/hwh-annual-report-2025.pdf"),
    ("2024", "Growing Through Challenge", "Expanding our reach, learning from pressure, and strengthening the foundations of disability care.",
     [("1,326", "People"), ("1,849", "Sessions"), ("€63,939.15", "Official income"), ("€268,110", "Direct value")], "reports/hwh-annual-report-2024.pdf"),
    ("2023", "Opening Doors", "A year of new frontiers, careful growth and international visibility.",
     [("1,012", "People"), ("1,688", "Sessions"), ("€41,630.56", "Official income"), ("€244,230", "Direct value")], "reports/hwh-annual-report-2023.pdf"),
]
reports_body = head("Reports",
    "Honest impact, clearly reported. We publish an annual report every year, and we separate people from sessions, and income from value.",
    "Transparency") + '<section><div class="wrap"><div class="grid">' + "".join(
    f"""<article class="card topline"><div class="grid g2" style="align-items:start"><div><span class="eyebrow">Annual report {y}</span><h2>{e(t)}</h2><p>{e(s)}</p>
<p><a class="btn btn-secondary" href="{f}" download>Download the {y} report (PDF)</a></p></div>
<div class="grid g2" style="gap:var(--s2)">{''.join(stat(n, l) for n, l in st)}</div></div></article>"""
    for y, t, s, st, f in REPORTS) + """</div>
<h2 style="margin-top:var(--s5)">How we calculate our numbers</h2>
<div class="grid g3">
 <div class="card redline"><h3>People and sessions</h3><p>A person is someone we reached. A session is a treatment or clinical encounter. Complex disability needs repeated care, so we report both.</p></div>
 <div class="card redline"><h3>Direct value</h3><p>A conservative estimate of what the care, training or support would reasonably have cost, in euros. It is not revenue, profit or an audited social return.</p></div>
 <div class="card redline"><h3>Official income</h3><p>Taken from the accounts of our Spanish association, with the US Form 990-EZ as supporting documentation. Volunteer fees are treated as income, not as value.</p></div>
</div>
<p class="note" style="margin-top:var(--s3)">The Spanish accounts record no salaried employees in 2023, 2024 or 2025.</p>
</div></section>"""

# ------------------------------------------------------------------ PARTNERS
PARTNERS = [
    ("SLB Negeri 1 Denpasar", "indonesia", "Denpasar, Bali", "Public special-education school", "Signed agreement",
     "SLB Negeri 1 Denpasar is a public special-education school in Bali. Since our first missions, we have provided free therapy for its students and training for its staff.", None),
    ("Yayasan De Legong Anak Bangsa", "indonesia", "Gianyar, Bali", "Foundation (yayasan)", "Signed agreement",
     "Yayasan De Legong Anak Bangsa in Gianyar, Bali, cares for children with disabilities, especially cerebral palsy. Together we provide free therapy, family support and better facilities.", None),
    ("Yayasan Mentari Fajar", "indonesia", "Jimbaran, Bali", "Foundation (yayasan) and inclusive school", "Signed agreement",
     "Yayasan Mentari Fajar runs an inclusive school and therapy programme for children with special needs in Jimbaran, Bali. Our teams provide therapy and training alongside its staff.", "https://yayasanmentarifajar.wordpress.com"),
    ("Universitas Dhyana Pura", "indonesia", "Badung, Bali", "Private university", "Signed agreement",
     "Universitas Dhyana Pura is a university in Bali. Through a signed agreement, we work together on training, student participation and building local rehabilitation capacity.", "https://undhirabali.ac.id"),
    ("Center of Complex Rehabilitation “Halychyna”", "ukraine", "Lviv", "State rehabilitation centre", "Collaboration",
     "The Halychyna Center of Complex Rehabilitation in Lviv is a state rehabilitation centre for veterans and civilians. Our teams work alongside its professionals during our rehabilitation missions in Ukraine.", "https://reabl.lviv.ua"),
    ("Novovolynsk Central City Hospital", "ukraine", "Novovolynsk, Volyn", "Municipal public hospital", "Collaboration",
     "Novovolynsk Central City Hospital is a municipal hospital in Volyn, Ukraine. It collaborates with Hands With Heart on rehabilitation care for people affected by disability and war.", "https://ncml.com.ua"),
    ("Asociación Dawe Ese Wakpa Kimoie", "costa", "Talamanca, Limón", "Indigenous civil association", "Signed agreement",
     "Asociación Dawe Ese Wakpa Kimoie promotes projects for Indigenous people with disabilities in Talamanca, Costa Rica. Together we bring care to families in remote Bribri communities.", None),
    ("Western University of Health Sciences", "usa", "Pomona, California", "Private university", "Collaboration",
     "Western University of Health Sciences is a graduate university of health professions in California. We collaborate on osteopathic education, student participation and adaptive sport.", "https://westernu.edu"),
]
COUNTRY = {"indonesia": "Indonesia", "ukraine": "Ukraine", "costa": "Costa Rica", "usa": "United States"}
partners_body = head("Our partners",
    "Our work is only possible with local schools, foundations, hospitals, universities and associations who welcome us, work alongside us and continue the care when we leave. These are the partners who stand with us.",
    "Partners") + """
<section><div class="wrap">
<div class="filter" data-target="#partner-list" role="group" aria-label="Filter partners by country"><button aria-pressed="true" data-filter="all">All</button><button aria-pressed="false" data-filter="indonesia">Bali · Indonesia</button><button aria-pressed="false" data-filter="ukraine">Ukraine</button><button aria-pressed="false" data-filter="costa">Costa Rica</button><button aria-pressed="false" data-filter="usa">United States</button></div>
<div class="grid g2" id="partner-list">""" + "".join(
    f'''<article class="card topline" data-cat="{c}"><span class="rel {'signed' if rel == 'Signed agreement' else ''}">{rel}</span>
<p class="partner-name" style="font-size:1.2rem">{e(n)}</p><p class="small">{e(kind)} · {e(loc)}, {COUNTRY[c]}</p><p>{e(txt)}</p>
{f'<a class="link-arrow" href="{u}" target="_blank" rel="noopener">Visit website ↗</a>' if u else ''}</article>'''
    for n, c, loc, kind, rel, txt, u in PARTNERS) + """</div>
<p class="note" style="margin-top:var(--s3)">We list partners only where there is a signed agreement or a documented collaboration, and we say which. Logos are added as each partner gives permission.</p>
</div></section>
<section class="bg-paper"><div class="wrap grid g2" style="align-items:center"><div><span class="eyebrow">Become a partner</span><h2>Are you a school, hospital, university or company that shares our mission?</h2><p>Partner with us. We work on defined problems, with clear roles, and never in a way that influences how we care for people.</p></div><div style="justify-self:end"><a class="btn btn-primary" href="contact.html?topic=partner">Become a partner</a></div></div></section>"""

# ------------------------------------------------------------------ CONTACT
contact_body = head("Contact",
    "Questions, partnerships, volunteering or press. We read every message.", "Contact") + f"""
<section><div class="wrap split">
 <div><h2>Get in touch</h2>
  <p>Email us at <a href="mailto:{EMAIL}">{EMAIL}</a>, or use the form.</p>
  <h3 style="margin-top:var(--s3)">Volunteering</h3>
  <p>We welcome osteopaths, physiotherapists, optometrists, students and recent graduates who can join a supervised clinical team that returns to the same people every year. Tell us about your training and experience.</p>
  <h3>Partnerships</h3>
  <p>Schools, yayasan, hospitals, universities, organisers and companies are welcome to get in touch about working together.</p></div>
 <form id="contact-form" data-to="{EMAIL}">
  <label for="name">Your name</label><input id="name" name="name" required autocomplete="name">
  <label for="email">Your email</label><input id="email" name="email" type="email" required autocomplete="email">
  <label for="topic">What is this about?</label>
  <select id="topic" name="topic"><option value="general">General question</option><option value="volunteer">Volunteering</option><option value="partner">Becoming a partner</option><option value="donate">Donating</option><option value="press">Press</option></select>
  <label for="message">Message</label><textarea id="message" name="message" required></textarea>
  <button class="btn btn-primary" type="submit">Send message</button>
  <p class="small" style="margin-top:12px">This opens your email app with the message ready to send.</p>
 </form>
</div></section>
<script>
(function(){{var t=new URLSearchParams(location.search).get('topic');var s=document.getElementById('topic');if(t&&s){{s.value=t;}}}})();
</script>"""

# ------------------------------------------------------------------ DONATE
donate_body = head("Donate",
    "Your gift keeps care free for children and adults with disabilities, and helps us leave skills and places of care that last.",
    "Donate") + f"""
<section><div class="wrap grid g2" style="align-items:start">
 <div>
  <h2>Where your gift goes</h2>
  <p>Care is free for the people we serve, always. Gifts to our field programmes pay for travel, equipment, local coordination and training, and gifts to Bahía de Niños build a permanent centre. Restricted gifts are used as promised and reported.</p>
  <a class="btn btn-primary" href="{DONATE_URL}">Donate</a>
  <p class="small" style="margin-top:12px">Online giving is being set up. For now, email us and we will send you our bank details and the right receipt for your country.</p>
 </div>
 <div class="callout" style="margin-top:0"><span class="eyebrow">How to give</span><p>Gifts can be made through Hands With Heart's Spanish association (public-utility status) or its US 501(c)(3), depending on your country and tax situation. Tell us where you are and we will point you to the right route.</p></div>
</div></section>
<section class="bg-paper"><div class="wrap"><span class="eyebrow">Ways to give</span><h2>Choose how you want to help</h2>
{table(["Gift", "What it funds", "Indicative amount"], [
  ["Lead and legacy gifts", "A major part of the Bahía de Niños Phase 1 capital gap: a building unit, the rehabilitation and training pavilion, or a named programme.", "US$50,000 – 250,000"],
  ["Built-environment gifts", "Inclusive playground, outdoor therapy pavilion, salt-water therapy pool (once priced).", "US$50,000 – 100,000"],
  ["Equipment packages", "Any of the <a href='projects/bahia-de-ninos.html#funding'>16 opportunities</a> to equip the centre.", "US$20,000 – 75,000"],
  ["Launch operations", "The first 24 months of the local team and centre operations.", "US$83,081 per year"],
  ["Sponsor a physiotherapist", "One Indonesian physiotherapist for a year, fully loaded.", "≈ US$3,600 per year"],
  ["Keep families moving", "Running costs of one adapted transport vehicle for a year.", "≈ US$3,350 per year"],
  ["Monthly giving", "Unrestricted support that keeps care free and the organisation resilient.", "Any amount"]])}
<p class="small">Per-role and per-vehicle figures are derived from the opening-year operating budget at IDR 17,912 per US$.</p></div></section>
<section><div class="wrap"><span class="eyebrow">What donors receive</span><div class="grid g3">
 <div class="card topline"><h3>Recognition</h3><p>Naming of spaces and packages where appropriate, agreed in writing, and recognition on site and online.</p></div>
 <div class="card topline"><h3>Transparent reporting</h3><p>Progress updates through design and construction, and annual reports with people, sessions, training and spending against budget.</p></div>
 <div class="card topline"><h3>A visit</h3><p>An invitation to see the site, meet the team and, with consent, the families the centre serves.</p></div></div>
 <p class="note" style="margin-top:var(--s3)">In 2025, every €1 of official income was transformed into approximately €2.04 of direct measurable value. This is a conservative replacement-value estimate, not a social return on investment. <a href="reports.html">Read how we calculate it</a>.</p>
</div></section>
<section class="bg-ink"><div class="wrap"><span class="eyebrow">Never for sale</span><p class="quote" style="color:#fff">Free care for vulnerable people, consent, and the facts in our reports.</p></div></section>
"""

# ------------------------------------------------------------------ build
def main():
    page("index.html", "About us", "Hands With Heart provides free, repeated and respectful disability care, and leaves lasting local capacity through training, partnership and permanent infrastructure.", about_body)
    page("objectives/index.html", "Our objectives", "Five external objectives and one set of internal systems that guide Hands With Heart from 2026 to 2029.", objectives_index())
    for o in OBJ.values():
        page(f"objectives/{o['file']}", o["title"], o["lede"], objective_body(o), current="objectives/index.html")
    page("objectives/systems-for-scale.html", "Systems for scale", "The internal objectives that make growth safe, fundable and sustainable.", systems_body, current="objectives/index.html")
    page("projects/index.html", "Our projects", "ParaSurf, Bahía de Niños and our missions in Bali, Costa Rica, Ukraine, Romania and Argentina.", projects_index)
    page("projects/parasurf.html", "ParaSurf", "Free healthcare teams for para surfers at international championships.", parasurf_body, current="projects/index.html")
    page("projects/bahia-de-ninos.html", "Bahía de Niños", "A permanent home for free disability care, rehabilitation, training and inclusion for children in Bali.", bahia_body, current="projects/index.html")
    page("projects/missions.html", "Missions", "Repeated, free care with local partners in Bali, Costa Rica, Ukraine, Romania and Argentina.", missions_body, current="projects/index.html")
    page("stories.html", "Stories", "Real people, real places, told with consent.", stories_body)
    page("news.html", "News", "News and updates from Hands With Heart Foundation.", news_body)
    page("reports.html", "Reports", "Annual reports 2023, 2024 and 2025 from Hands With Heart Foundation.", reports_body)
    page("partners.html", "Partners", "The schools, foundations, hospitals and universities that stand with Hands With Heart.", partners_body)
    page("contact.html", "Contact", "Contact Hands With Heart Foundation.", contact_body)
    page("donate.html", "Donate", "Support free, repeated and respectful disability care.", donate_body)


if __name__ == "__main__":
    main()
