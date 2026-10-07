#!/usr/bin/env python3
"""Pitch prototype generator for Pinheiro's Cleaning (Deerfield Beach, FL).

Plain HTML built from WordPress core block markup (Twenty Twenty-Five layout, Literata + Ysabeau Office
from the TT25 font collection). Every fact comes from pinheiroscleaning.com and its Google reviews.
Run:  python3 tools/build_site.py .
"""
import hashlib, json, os, sys, time
from urllib.parse import quote_plus

# ---- CONFIG ----
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
BASE_URL = "https://pinheiros.whitephoenixconsulting.com/"
NAME = "Pinheiro&rsquo;s Cleaning"
PHONE = "(561) 929-0067"
TEL = "+15619290067"
EMAIL = "contact@pinheiroscleaning.com"
TOWN = "Deerfield Beach, FL 33442"
GOOGLE = "https://www.google.com/search?q=" + quote_plus("Pinheiro's Cleaning Deerfield Beach FL reviews")
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote_plus("Pinheiro's Cleaning, Deerfield Beach, FL 33442")
DIM = "#16241a"

BUILD = time.strftime("%Y%m%d%H%M%S")
SELF_HEAL = ('<script>(function(){if(!window.fetch)return;fetch("ROOTversion.json",{cache:"no-store"})'
             '.then(function(r){return r.json()}).then(function(v){if(v.build&&v.build!=="BUILD"){var k="reload-"+v.build;'
             'try{if(sessionStorage.getItem(k))return;sessionStorage.setItem(k,"1")}catch(e){}location.reload()}}).catch(function(){})})();</script>')


def ver(rel):
    with open(os.path.join(OUT, rel), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


IMGS = {
    "hero": ([800, 1280], 1280, 725),
    "residential": ([600], 600, 340), "commercial": ([600], 600, 340), "move": ([600], 600, 340),
    "construction": ([600], 600, 340), "rental": ([600], 600, 340),
    "details": ([980], 980, 555), "palms": ([980], 980, 555), "carpet": ([980], 980, 555),
}

SVG = {
    "phone": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "arrow": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M5 5v1.5h14V5H5zm0 7.8h14v-1.5H5v1.5zM5 19h14v-1.5H5V19z"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="m13.06 12 6.47-6.47-1.06-1.06L12 10.94 5.53 4.47 4.47 5.53 10.94 12l-6.47 6.47 1.06 1.06L12 13.06l6.47 6.47 1.06-1.06L13.06 12Z"/></svg>',
    "expand": '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="none" viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path fill="#fff" d="M2 0a2 2 0 0 0-2 2v2h1.5V2a.5.5 0 0 1 .5-.5h2V0H2Zm2 10.5H2a.5.5 0 0 1-.5-.5V8H0v2a2 2 0 0 0 2 2h2v-1.5ZM8 12v-1.5h2a.5.5 0 0 0 .5-.5V8H12v2a2 2 0 0 1-2 2H8Zm2-12a2 2 0 0 1 2 2v2h-1.5V2a.5.5 0 0 0-.5-.5H8V0h2Z"/></svg>',
}
CUR = ' aria-current="page"'


def srcset(root, name):
    widths, w, h = IMGS[name]
    return ", ".join(f"{root}assets/img/{name}-{x}.webp {x}w" for x in widths)


def src(root, name):
    widths = IMGS[name][0]
    return f"{root}assets/img/{name}-{widths[-1]}.webp"


def img(root, name, alt, sizes, cls="", eager=False, extra=""):
    widths, w, h = IMGS[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{src(root, name)}" srcset="{srcset(root, name)}" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{extra}>')


def lightbox_figure(root, name, alt, sizes, cls="wp-block-image size-large"):
    return (f'<figure class="{cls} wp-lightbox-container">{img(root, name, alt, sizes)}'
            f'<button class="lightbox-trigger" type="button" aria-haspopup="dialog" aria-label="Enlarge: {alt}">{SVG["expand"]}</button></figure>')


def button(href, label, style="", icon=None, attrs=""):
    cls = "wp-block-button" + (f" is-style-{style}" if style else "")
    ic = SVG[icon] if icon else ""
    lead = ic if icon == "phone" else ""
    trail = ic if icon == "arrow" else ""
    return f'<div class="{cls}"><a class="wp-block-button__link wp-element-button" href="{href}"{attrs}>{lead}{label}{trail}</a></div>'


def buttons(*items, center=False):
    j = " is-content-justification-center" if center else ""
    return f'<div class="wp-block-buttons is-layout-flex{j}">{"".join(items)}</div>'


def quote_link(root, service=None):
    return f"{root}quote/" + (f"?service={service}" if service else "")


def reveal(i=0):
    return f' style="--reveal-delay:{i * 0.08:.2f}s"' if i else ""


NAV = [("Home", ""), ("Services", "services/"), ("Reviews", "#reviews"), ("Contact", "contact/")]
SPECULATION = {"prerender": [{"source": "document", "where": {"and": [{"href_matches": "/*"},
               {"not": {"href_matches": "/*\\?*"}}, {"not": {"selector_matches": "a[rel~=nofollow]"}}]}, "eagerness": "moderate"}]}


def head(root, title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Prototype preview. Remove this noindex line at launch. -->
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#faf8f3">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_URL}{path}">
<meta property="og:image" content="{BASE_URL}assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,300..600&amp;family=Ysabeau+Office:wght@400..700&amp;display=swap">
<link rel="stylesheet" id="wp-block-library-css" href="{root}assets/css/wp-blocks.css?ver=11.2.0">
<link rel="stylesheet" id="theme-style-css" href="{root}assets/css/site.css?ver={ver('assets/css/site.css')}">
<meta name="site-build" content="{BUILD}">
<script>document.documentElement.classList.add("js");</script>
{SELF_HEAL.replace("ROOT", root).replace("BUILD", BUILD)}
<script type="speculationrules">{json.dumps(SPECULATION)}</script>
{extra}<script src="{root}assets/js/site.js?ver={ver('assets/js/site.js')}" defer></script>
</head>"""


def href(root, h):
    if h.startswith("#"):
        return (root or "./") + h
    return (root + h) or "./"


CHEVRON = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" focusable="false"><path d="M1.50002 4L6.00002 8L10.5 4" stroke-width="1.5"></path></svg>'


def mega_menu(root):
    cards = "".join(
        f'<a class="mega-card" href="{root}services/#{s["id"]}">'
        f'<img src="{src(root, s["img"])}" width="600" height="340" alt="" loading="lazy" decoding="async">'
        f'<span class="mega-card__title">{s["name"]}</span><span class="mega-card__text">{s["card"]}</span></a>'
        for s in SERVICES)
    return (f'<div class="mega-menu" id="mega-services"><div class="mega-menu__inner">'
            f'<div class="mega-menu__grid">{cards}</div>'
            f'<div class="mega-menu__foot"><span>Not sure which one fits? Tell us about the place and we&rsquo;ll suggest one.</span>'
            f'<a class="more-link" href="{root}services/">All services {SVG["arrow"]}</a></div></div></div>')


def header(root, active):
    home = root or "./"
    items = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        link = f'<a class="wp-block-navigation-item__content" href="{href(root, h)}"{cur}>{l}</a>'
        if h == "services/":
            items.append(f'<li class="wp-block-navigation-item has-child open-on-hover-click wp-block-navigation-submenu has-mega-menu">{link}'
                         f'<button class="wp-block-navigation__submenu-icon wp-block-navigation-submenu__toggle" type="button" aria-expanded="false" aria-controls="mega-services" aria-label="Services submenu">{CHEVRON}</button>'
                         f'{mega_menu(root)}</li>')
        else:
            items.append(f'<li class="wp-block-navigation-item">{link}</li>')
    sub = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    overlay = []
    for l, h in NAV:
        cur = CUR if active == h else ""
        extra = f'<ul class="overlay-sub">{sub}</ul>' if h == "services/" else ""
        overlay.append(f'<li><a href="{href(root, h)}"{cur}>{l}</a>{extra}</li>')
    return f"""<a class="skip-link screen-reader-text" href="#wp--skip-link--target">Skip to content</a>
<header class="wp-block-template-part site-header has-global-padding">
  <div class="site-header__inner">
    <div class="wp-block-site-logo"><a href="{home}" rel="home" aria-label="{NAME}, home"><img src="{root}assets/img/logo.webp" width="287" height="70" alt="Pinheiro&rsquo;s, cleaning that makes the difference"></a></div>
    <nav class="wp-block-navigation" aria-label="Main"><ul class="wp-block-navigation__container">{"".join(items)}</ul></nav>
    <div class="header-tools">
      <a class="header-phone" href="tel:{TEL}">{SVG["phone"].replace("<svg ", '<svg width="18" height="18" ')}{PHONE}</a>
      <a class="icon-button header-call" href="tel:{TEL}" aria-label="Call {PHONE}">{SVG["phone"]}</a>
      <div class="wp-block-button header-quote"><a class="wp-block-button__link wp-element-button" href="{root}quote/">Get a quote</a></div>
      <button class="wp-block-navigation__responsive-container-open icon-button" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="Open menu">{SVG["menu"]}</button>
    </div>
  </div>
  <div class="wp-block-navigation__responsive-container" role="dialog" aria-modal="true" aria-label="Menu">
    <button class="wp-block-navigation__responsive-container-close icon-button" type="button" aria-label="Close menu">{SVG["close"]}</button>
    <ul>{"".join(overlay)}</ul>
    {buttons(button(root + "quote/", "Get a quote"), button("tel:" + TEL, "Call " + PHONE, "outline"))}
  </div>
</header>"""


def footer(root):
    home = root or "./"
    links = "".join(f'<li><a href="{root}services/#{s["id"]}">{s["name"]}</a></li>' for s in SERVICES)
    return f"""<footer class="wp-block-template-part site-footer has-global-padding">
  <div class="site-footer__inner">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="footer-logo" href="{home}"><img src="{root}assets/img/logo-white.webp" width="287" height="70" alt="Pinheiro&rsquo;s Cleaning" loading="lazy"></a>
        <p>Home, office and vacation rental cleaning across Palm Beach County and Broward. Locally owned since 2019.</p>
      </div>
      <div><h2>Services</h2><ul>{links}</ul></div>
      <div><h2>Company</h2><ul>
        <li><a href="{home}#reviews">Reviews</a></li>
        <li><a href="{root}quote/">Get a quote</a></li>
        <li><a href="{root}contact/">Contact</a></li>
        <li><a href="{GOOGLE}" target="_blank" rel="noopener">Google reviews</a></li>
      </ul></div>
      <div><h2>Get in touch</h2><ul>
        <li><a href="tel:{TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>{TOWN}</li>
      </ul></div>
    </div>
    <div class="footer-bottom"><p>&copy; 2019 to <span data-year>2026</span> {NAME}</p><p><button class="dusted" type="button" data-dusted>Last dusted <span>a moment</span> ago</button></p></div>
  </div>
</footer>"""


def mobile_actions(root):
    return f"""<div class="mobile-actions" role="region" aria-label="Quick actions">
  {button("tel:" + TEL, "Call", "outline", "phone")}
  {button(root + "quote/", "Get a quote", "", "arrow")}
</div>"""


def page(depth, path, title, desc, active, main, extra_head="", actions=True, body_class="page"):
    root = "../" * depth
    html = f"""{head(root, title, desc, path, extra_head)}
<body class="{body_class}{" has-mobile-actions" if actions else ""}">
<div class="wp-site-blocks">
{header(root, active)}
<main class="wp-block-group" id="wp--skip-link--target">
{main(root)}
</main>
{footer(root)}
</div>
{mobile_actions(root) if actions else ""}
</body>
</html>
"""
    target = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w") as f:
        f.write(html)
    print("wrote", os.path.relpath(target, OUT))


# ---------- content (all from pinheiroscleaning.com and its Google reviews) ----------

SERVICES = [
    {"id": "residential", "name": "House cleaning", "img": "residential",
     "alt": "Gloved hand wiping down an oven door",
     "card": "Kitchens, bathrooms, tile, floors, dust in the corners. Regular cleans or a deep clean."},
    {"id": "vacation-rental", "name": "Rental and vacation homes", "img": "rental",
     "alt": "A tidy living room ready for guests",
     "card": "Turnovers between guests, so the place is ready when they walk in."},
    {"id": "move-in-out", "name": "Move in and move out", "img": "move",
     "alt": "Cleaners wiping down a window",
     "card": "A deep clean of the empty place, before you move in or after you move out."},
    {"id": "commercial", "name": "Office and commercial", "img": "commercial",
     "alt": "Office floor being cleaned beside a wet floor sign",
     "card": "Offices, restaurants and medical spaces. A clean front door says a lot."},
    {"id": "post-construction", "name": "Post-construction", "img": "construction",
     "alt": "Broom and debris bags on a dusty floor after building work",
     "card": "When the builders leave, we clear the dust and debris so you can use the space."},
]

REVIEWS = [
    ("Marisela Campbell", "August 2024",
     "I enjoy getting my house cleaned by Pinheiros cleaning teams. They pay attention to what you want done and will redo any area that you want cleaned more extensively. They bring they&rsquo;re own equipment and go out of their way to please you. Roses or vows on toilet paper, hotel towel folds and all details that make your house look outstanding!"),
    ("Micahela Myrie-Lowe", "May 2025",
     "I&rsquo;ve been using them for years and they&rsquo;ve always done a good job. always ask me to check before they leave and clean where i ask them too. i continue to use them because they are kind and respectful and work efficiently."),
    ("Jennifer Jeanette", "June 2024",
     "Did an amazing job, very professional and thorough. I was so relieved when I came home bc I have been too busy to clean. Amazing service! Went above and beyond."),
    ("Ileana Simpatico", "August 2024",
     "My experience with Pinheiros cleaning service has been exceptional. The have a cleaning team that is friendly. cooperative and their work is exceptional. I would recommend Pinheiros to everyone."),
    ("Veronica Lynne", "August 2024",
     "I have had great experiences with this company, they&rsquo;re very quick to respond and professional, do a great job. Would recommend."),
    ("Shari Remland", "June 2024",
     "It&rsquo;s difficult to find a great cleaning service and I&rsquo;m so happy I finally did! A+. Highly recommend!"),
]

TRUST = [
    ("111 Google reviews", "From homes and offices nearby",
     '<path d="M13 14h30a4 4 0 0 1 4 4v17a4 4 0 0 1-4 4H27l-7.5 6.5V39H13a4 4 0 0 1-4-4V18a4 4 0 0 1 4-4z" fill="#23452b"/><path d="M28 19.5l2 4.4 4.8.5-3.6 3.2 1 4.7-4.2-2.4-4.2 2.4 1-4.7-3.6-3.2 4.8-.5z" fill="#f4e9f1"/><circle class="trust-art__spark" cx="46" cy="10" r="3" fill="#8a3a7d"/>'),
    ("Licensed and insured", "You&rsquo;re letting us into your place",
     '<path d="M28 9c4.5 3.4 9.2 5 14 5v11c0 10-6.2 16.4-14 20-7.8-3.6-14-10-14-20V14c4.8 0 9.5-1.6 14-5z" fill="#23452b"/><path d="m21.5 27.5 4.5 4.5 9-9.5" fill="none" stroke="#f4e9f1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'),
    ("We bring the supplies", "Equipment and products included",
     '<path d="M20 22h16l-2 22a3 3 0 0 1-3 2.7h-6a3 3 0 0 1-3-2.7z" fill="#23452b"/><path d="M23 22v-5h10v5" fill="none" stroke="#23452b" stroke-width="2.5"/><path d="M33 17h6l3 3" fill="none" stroke="#8a3a7d" stroke-width="2.5" stroke-linecap="round"/><circle class="trust-art__spark" cx="45" cy="25" r="1.6" fill="#8a3a7d"/><circle class="trust-art__spark" cx="47" cy="20" r="1.3" fill="#8a3a7d"/><rect x="24" y="30" width="8" height="8" rx="1.5" fill="#f4e9f1"/>'),
    ("Locally owned since 2019", "Palm Beach County and Broward",
     '<path class="trust-art__pin" d="M28 9a10 10 0 0 1 10 10c0 7.6-10 17-10 17s-10-9.4-10-17A10 10 0 0 1 28 9z" fill="#23452b"/><path d="M28 14c2.6 1.8 3.6 4.4 2.6 7.4-.6 1.6-1.5 2.4-2.6 2.9-1.1-.5-2-1.3-2.6-2.9-1-3 0-5.6 2.6-7.4z" fill="#f4e9f1"/><path d="M12 44c6-3 10 0 16-2s10-3 16 0" fill="none" stroke="#8a3a7d" stroke-width="2.2" stroke-linecap="round"/>'),
]

FAQS = [
    ("Which areas do you cover?", "Palm Beach County and Broward. We&rsquo;re based in Deerfield Beach. If you&rsquo;re not sure we come out your way, call and ask."),
    ("Do I need to provide cleaning supplies?", "No. The team brings its own equipment and products."),
    ("What if I want something cleaned again?", "Tell the team before they leave. They ask you to check the place, and they&rsquo;ll go back over anything you point out."),
    ("Are you licensed and insured?", "Yes. Ask us for the details when you book."),
    ("Do you clean offices and other businesses?", "Yes. Offices, restaurants, medical spaces and sites after construction, as well as homes."),
    ("Can you turn over a vacation rental between guests?", "Yes. We clean rental and vacation homes so they&rsquo;re ready when the next guests arrive."),
]

CHOICES = [
    ("home", "House cleaning", "Regular or one-time",
     '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>'),
    ("deep", "Deep clean", "Every corner, top to bottom",
     '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>'),
    ("move-in-out", "Move in or out", "The empty place, start to finish",
     '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5"/><path d="M12 13v8"/>'),
    ("vacation-rental", "Vacation rental", "Turnovers between guests",
     '<circle cx="7.5" cy="15.5" r="4.5"/><path d="M10.7 12.3 20 3"/><path d="m16 7 3 3"/><path d="m14 9 2 2"/>'),
    ("commercial", "Office or business", "Offices, restaurants, medical",
     '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 21v-4h6v4"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2"/>'),
    ("post-construction", "After construction", "Dust and debris cleared",
     '<path d="M2 18h20"/><path d="M4 18v-2a8 8 0 0 1 16 0v2"/><path d="M10 8V5h4v3"/>'),
]
TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M20 6 9 17l-5-5"/></svg>'


def choice_cards(input_type, large=False):
    items = []
    for v, l, d, icon in CHOICES:
        svg = f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{icon}</svg>'
        desc = f'<span class="gcard__desc">{d}</span>' if large else ""
        items.append(f'<li><label class="gcard"><input type="{input_type}" name="service" value="{v}">'
                     f'<span class="gcard__box"><span class="gcard__icon">{svg}</span><span class="gcard__text">{l}{desc}</span>'
                     f'<span class="gcard__tick">{TICK}</span></span></label></li>')
    cls = "gchoice-cards gchoice-cards--3" + (" gchoice-cards--lg" if large else "")
    return f'<ul class="{cls}">{"".join(items)}</ul>'


def gfield(label, inner, required=False, half=False, stack=True, desc="", group=False, cls=""):
    req = '<span class="gfield_required" aria-hidden="true">*</span>' if required else ""
    width = " gfield--width-half" + (" stack-sm" if stack else "") if half else ""
    grp = " data-group-required" if group and required else ""
    d = f'<div class="gfield_description">{desc}</div>' if desc else ""
    if group:
        return (f'<fieldset class="gfield{width} {cls}"{grp} style="border:0;margin:0;padding:0;min-width:0"><legend class="gfield_label">{label}{req}</legend>'
                f'{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></fieldset>')
    return f'<div class="gfield{width} {cls}">{label.format(req=req)}{d}<div class="ginput_container">{inner}</div><div class="validation_message" aria-live="polite"></div></div>'


def lab(for_id, text):
    return f'<label class="gfield_label" for="{for_id}">{text}{{req}}</label>'


def radios(name, vals):
    return '<ul class="gfield_radio inline">' + "".join(
        f'<li><label class="gchoice"><input type="radio" name="{name}" value="{v}"> {v}</label></li>' for v in vals) + "</ul>"


def select(id_, name, vals, required=False):
    opts = '<option value="">Select</option>' + "".join(f"<option>{v}</option>" for v in vals)
    return f'<select id="{id_}" name="{name}"{" required" if required else ""}>{opts}</select>'


# ---------- shared sections ----------

def service_cards(root, link_to_anchor=True):
    cards = []
    for i, s in enumerate(SERVICES):
        h = f"{root}services/#{s['id']}" if link_to_anchor else f"#{s['id']}"
        cards.append(f"""<div class="wp-block-group service-card wp-reveal"{reveal(i)}>
  <a href="{h}">
    <figure class="wp-block-image size-large">{img(root, s["img"], s["alt"], "(min-width: 782px) 33vw, 50vw")}</figure>
    <h3 class="wp-block-heading">{s["name"]}</h3>
    <p>{s["card"]}</p>
    <span class="more-link">Learn more {SVG["arrow"]}</span>
  </a>
</div>""")
    cards.append(f"""<div class="wp-block-group service-card service-card--note wp-reveal"{reveal(5)}>
  <h3 class="wp-block-heading">Not on the list?</h3>
  <p>Tile and grout, a fridge or oven, a one-off before a party. Tell us what you need and we&rsquo;ll say if it&rsquo;s something we do.</p>
  {buttons(button(quote_link(root), "Ask us", "outline"))}
</div>""")
    return f'<div class="wp-block-group is-layout-grid columns-3 service-grid">{"".join(cards)}</div>'


def review_card(r, i=0):
    n, d, t = r
    return (f'<figure class="review-card wp-reveal"{reveal(i)}><blockquote class="wp-block-quote is-style-plain"><p>&ldquo;{t}&rdquo;</p></blockquote>'
            f'<figcaption><strong>{n}</strong><span>Google review, {d}</span></figcaption></figure>')


def cta(root, title="Tell us about the place", text="Send the form or give us a call. We&rsquo;ll get back to you with a price."):
    return f"""<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding">
  <div class="wp-block-group has-text-align-center wp-reveal" style="max-width:680px;margin:0 auto">
    <h2 class="wp-block-heading has-text-align-center" style="font-size:var(--wp--preset--font-size--xx-large)">{title}</h2>
    <p class="has-text-align-center cta-lede">{text}</p>
    <div style="margin-top:28px">{buttons(button(root + "quote/", "Get a quote", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}</div>
  </div>
</section>"""


def banner(root, crumb, title, lede):
    return f"""<section class="wp-block-group alignfull page-banner has-global-padding">
  <div class="page-banner__inner">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{root or './'}">Home</a> / {crumb}</nav>
    <h1 class="wp-block-heading">{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


# ---------- Home ----------

def home(root):
    trust = "".join(
        f'<div class="trust-item wp-reveal"{reveal(i)}><svg class="trust-art" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#e9eee7"/>{art}</svg><p><strong>{t}</strong><span>{s}</span></p></div>'
        for i, (t, s, art) in enumerate(TRUST))
    half = (len(FAQS) + 1) // 2
    col = lambda items: "".join(f'<details class="wp-block-details"><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
    reviews = "".join(review_card(r, i % 3) for i, r in enumerate(REVIEWS))
    return f"""
<div class="wp-block-media-text alignfull has-media-on-the-right is-stacked-on-mobile is-image-fill-element hero-split">
  <div class="wp-block-media-text__content">
    <div class="hero-copy">
      <p class="hero-kicker">Locally owned in Deerfield Beach since 2019</p>
      <h1 class="wp-block-heading">Home and office cleaning in Palm Beach County and Broward</h1>
      <p class="hero-lede">Houses, vacation rentals, offices and new builds. We bring the supplies, and we don&rsquo;t leave until you&rsquo;ve had a look.</p>
      <div class="quote-box" data-hero-cta>
        <div class="gform_wrapper">
          <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
          <form method="post" novalidate>
            <!-- Prototype: the form validates and confirms but sends nothing. Wire a form service in here at launch. -->
            <div class="gform_fields">
              {gfield("What needs cleaning?", choice_cards("radio"), True, group=True)}
              {gfield(lab("h-name", "Name"), '<input id="h-name" name="name" type="text" autocomplete="name" required>', True, True)}
              {gfield(lab("h-phone", "Phone"), '<input id="h-phone" name="phone" type="tel" autocomplete="tel" required>', True, True)}
            </div>
            <div class="gform_footer gform_footer--inline">
              {gfield(lab("h-zip", "ZIP code"), '<input id="h-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True)}
              <button class="wp-element-button" type="submit">Get my price</button>
            </div>
          </form>
          <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! We got your request.</h3><p>We&rsquo;ll call you back with a price. Need us sooner? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
        </div>
      </div>
      <p class="hero-meta">Rather talk? <a href="tel:{TEL}">{PHONE}</a></p>
    </div>
  </div>
  <figure class="wp-block-media-text__media">
    {img(root, "hero", "Cleaning a glass balcony screen beside potted plants", "(min-width: 782px) 50vw, 100vw", eager=True)}
    <figcaption class="hero-review"><span>&ldquo;They pay attention to what you want done and will redo any area that you want cleaned more extensively.&rdquo;</span><strong>Marisela Campbell, Google review</strong></figcaption>
  </figure>
</div>

<section class="wp-block-group alignfull trust-row has-global-padding" aria-label="Why people book us">
  <div class="wp-block-group is-layout-grid columns-4">{trust}</div>
</section>

<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="services-title">
  <div class="wide">
    <div class="section-head wp-reveal">
      <h2 class="wp-block-heading" id="services-title">What we clean</h2>
      <p>Homes and businesses, one-off or on a schedule.</p>
    </div>
    {service_cards(root)}
  </div>
</section>

<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding" aria-labelledby="details-title">
  <div class="wp-block-media-text alignwide wide is-stacked-on-mobile wp-reveal" style="grid-template-columns:46% auto">
    {lightbox_figure(root, "details", "Gloved hands cleaning a window with a spray bottle", "(min-width: 782px) 46vw, 100vw", "wp-block-media-text__media")}
    <div class="wp-block-media-text__content">
      <h2 class="wp-block-heading is-style-text-annotation">The details</h2>
      <h2 class="wp-block-heading" id="details-title">Finished like a hotel room</h2>
      <p>Customers tell us it&rsquo;s the small things they notice. Towels folded the way a hotel does it. The end of the toilet roll folded into a rose. A team that asks you to look around before they pack up.</p>
      <ul class="wp-block-list is-style-checks">
        <li>We walk through with you before we leave</li>
        <li>Anything you point out, we go back over</li>
        <li>We bring our own equipment and products</li>
        <li>Tile, grout, bathrooms and kitchens done properly</li>
      </ul>
    </div>
  </div>
</section>

<section class="wp-block-group alignfull section has-global-padding" id="reviews" aria-labelledby="reviews-title">
  <div class="wide">
    <div class="section-head section-head--split wp-reveal">
      <div><h2 class="wp-block-heading" id="reviews-title">In their words</h2>
      <p>From our 111 reviews on Google. Copied as written.</p></div>
      {buttons(button(GOOGLE, "Read them on Google", "outline", "arrow", ' target="_blank" rel="noopener"'))}
    </div>
    <div class="review-grid">{reviews}</div>
  </div>
</section>

<section class="wp-block-group alignfull section has-accent-5-background-color has-global-padding" aria-labelledby="how-title">
  <div class="wide">
    <div class="section-head wp-reveal"><h2 class="wp-block-heading" id="how-title">How booking works</h2></div>
    <div class="wp-block-columns steps is-layout-flex">
      <div class="wp-block-column wp-reveal"><span class="step-number">1</span><h3 class="wp-block-heading">Tell us about the place</h3><p>Fill in the form or call. House, rental, office or a site after building work.</p></div>
      <div class="wp-block-column wp-reveal"{reveal(1)}><span class="step-number">2</span><h3 class="wp-block-heading">Get your price</h3><p>We come back to you with a price and a day that suits you.</p></div>
      <div class="wp-block-column wp-reveal"{reveal(2)}><span class="step-number">3</span><h3 class="wp-block-heading">Check it with us</h3><p>Before the team leaves, walk round with them. If something needs another go, it gets one.</p></div>
    </div>
  </div>
</section>

<div class="wp-block-cover alignfull has-parallax band-cover" style="min-height:420px">
  <div role="img" aria-label="Palm trees against a blue sky" class="wp-block-cover__image-background has-parallax" style="background-position:50% 50%;background-image:url({root}assets/img/palms-980.webp)"></div>
  <span aria-hidden="true" class="wp-block-cover__background has-background-dim-60 has-background-dim" style="background-color:{DIM}"></span>
  <div class="wp-block-cover__inner-container has-text-align-center wp-reveal">
    <h2 class="wp-block-heading">Local since 2019</h2>
    <p>We&rsquo;re based in Deerfield Beach and clean homes and businesses from Palm Beach County down through Broward.</p>
    {buttons(button(root + "quote/", "Get a quote", "", "arrow"), center=True)}
  </div>
</div>

<section class="wp-block-group alignfull section has-global-padding" aria-labelledby="faq-title">
  <div class="wide">
    <div class="section-head wp-reveal">
      <h2 class="wp-block-heading" id="faq-title">Questions people ask</h2>
    </div>
    <div class="faq-grid wp-reveal"><div>{col(FAQS[:half])}</div><div>{col(FAQS[half:])}</div></div>
  </div>
</section>

{cta(root)}
"""


# ---------- Services ----------

DETAIL = {
    "residential": (["Dust on the shelves, dirt in the corners, a bathroom that never quite gets done. We take care of it, top to bottom.",
                     "Book a regular clean to keep on top of things, or a deep clean when the house needs a proper reset: tile and grout, bathrooms, the kitchen, the spots behind things."],
                    ["You&rsquo;ve been too busy to keep up", "Guests are coming and the house isn&rsquo;t ready"]),
    "vacation-rental": (["Guests notice everything, and they write reviews. We clean rental and vacation homes between stays so the place is ready when they arrive.",
                         "Towels folded the hotel way, bathrooms and kitchens spotless, floors done."],
                        ["Back-to-back bookings", "Reviews mention cleanliness"]),
    "move-in-out": (["Moving is a fresh start, and it&rsquo;s easier to clean a place when it&rsquo;s empty. We deep clean before you move in or after you move out.",
                     "Inside cabinets, behind where the fridge stood, bathrooms, floors. The parts nobody sees until the furniture is gone."],
                    ["You&rsquo;re handing back keys", "You want to start clean in the new place"]),
    "commercial": (["First impressions count. A clean office tells clients you mean business, and your staff will be glad to come in.",
                    "We clean offices and other workplaces, including restaurants and medical spaces."],
                   ["Clients visit your office", "The current cleaner keeps missing things"]),
    "post-construction": (["After the builders leave, the real clean-up starts. Fine dust gets everywhere and debris gets left behind.",
                           "We clear it out so you can move in, open up or hand the space over."],
                          ["A renovation just finished", "A new build is ready to hand over"]),
}


def services(root):
    rows = []
    for i, s in enumerate(SERVICES):
        body, signs = DETAIL[s["id"]]
        flip = " svc-row--flip" if i % 2 else ""
        bg = " has-accent-5-background-color" if i % 2 else ""
        rows.append(f"""<section class="wp-block-group alignfull section has-global-padding{bg}" id="{s["id"]}" aria-labelledby="{s["id"]}-title">
  <div class="svc-row{flip} wide wp-reveal">
    {lightbox_figure(root, s["img"], s["alt"], "(min-width: 782px) 50vw, 40vw", "wp-block-image svc-row__media")}
    <div class="svc-row__head"><h2 class="wp-block-heading" id="{s["id"]}-title">{s["name"]}</h2></div>
    <div class="svc-row__body">
      {"".join(f"<p>{p}</p>" for p in body)}
      <div class="signs"><h3 class="wp-block-heading">Good time to call</h3><ul class="wp-block-list is-style-checks">{"".join(f"<li>{x}</li>" for x in signs)}</ul></div>
      {buttons(button(quote_link(root, s["id"]), "Get a quote", "", "arrow"), button("tel:" + TEL, "Call us", "outline", "phone"))}
    </div>
  </div>
</section>""")
    return f"""
{banner(root, "Services", "What we clean", "Homes, vacation rentals, offices and new builds across Palm Beach County and Broward.")}
<section class="wp-block-group alignfull section has-global-padding" style="padding-bottom:0" aria-label="Jump to a service">
  <div class="wide">{service_cards(root, link_to_anchor=False)}</div>
</section>
{"".join(rows)}
{cta(root, "Not sure which clean you need?", "Tell us about the place. We&rsquo;ll suggest the right one and give you a price.")}
"""


# ---------- Contact ----------

def contact(root):
    return f"""
{banner(root, "Contact", "Get in touch", "Call, email or send a message. We&rsquo;ll get back to you.")}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="contact-layout wide">
    <div class="contact-cols wp-reveal">
      <div><h3 class="wp-block-heading">Phone</h3><p><a href="tel:{TEL}">{PHONE}</a></p></div>
      <div><h3 class="wp-block-heading">Based in</h3><p>{TOWN}<br><a href="{MAPS}" target="_blank" rel="noopener">Open in Maps</a></p></div>
      <div class="span-2"><h3 class="wp-block-heading">Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="span-2"><h3 class="wp-block-heading">Where we clean</h3><p>Palm Beach County and Broward.</p></div>
    </div>
    <div class="form-panel wp-reveal"{reveal(1)}>
      <div class="gform_wrapper">
        <div class="gform_heading"><h2 class="gform_title">Send us a message</h2><span class="gform_description">Want a price? The <a href="{root}quote/">quote form</a> is quicker.</span></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <div class="gform_fields">
            {gfield(lab("c-name", "Name"), '<input id="c-name" name="name" type="text" autocomplete="name" required>', True, True)}
            {gfield(lab("c-phone", "Phone"), '<input id="c-phone" name="phone" type="tel" autocomplete="tel" required>', True, True)}
            {gfield(lab("c-email", "Email"), '<input id="c-email" name="email" type="email" autocomplete="email" required>', True)}
            {gfield(lab("c-msg", "Message"), '<textarea id="c-msg" name="message" rows="5" required></textarea>', True)}
          </div>
          <div class="gform_footer"><button class="wp-element-button" type="submit">Send message</button></div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks for getting in touch!</h3><p>We&rsquo;ll get back to you soon. In a hurry? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
  </div>
</section>
"""


# ---------- Quote ----------

def quote(root):
    prev_btn = '<button class="wp-element-button gform_previous_button" type="button">Previous</button>'
    nav = lambda prev, nxt: f'<div class="gform_page_footer">{prev_btn if prev else ""}{nxt}</div>'
    nxt = '<button class="wp-element-button gform_next_button" type="button">Next</button>'
    sub = '<button class="wp-element-button" type="submit">Send request</button>'
    lede = f'Three short steps. Prefer to talk? Call <a href="tel:{TEL}">{PHONE}</a>.'
    r = REVIEWS[1]
    return f"""
{banner(root, "Get a quote", "Get a price for your clean", lede)}
<section class="wp-block-group alignfull section has-global-padding">
  <div class="quote-layout">
    <div class="form-panel">
      <div class="gform_wrapper">
        <div class="gf_progressbar_wrapper"><p class="gf_progressbar_title">Step 1 of 3 - The clean</p><div class="gf_progressbar" aria-hidden="true"><div class="gf_progressbar_percentage" style="width:33%"><span>33%</span></div></div></div>
        <div class="gform_validation_errors" role="alert" hidden>There was a problem with your submission. Please review the fields below.</div>
        <form method="post" novalidate>
          <!-- Prototype: the form validates and confirms but sends nothing. Wire a form service in here at launch. -->
          <div class="gform_page" data-title="The clean">
            <div class="gform_fields">
              {gfield("What needs cleaning?", choice_cards("checkbox", large=True), True, group=True, desc="Pick all that apply.")}
              {gfield("How often?", radios("frequency", ["One time", "Weekly", "Every two weeks", "Monthly", "Between guests"]), True, group=True)}
            </div>
            {nav(False, nxt)}
          </div>
          <div class="gform_page" data-title="The place" hidden>
            <div class="gform_fields">
              {gfield(lab("q-beds", "Bedrooms"), select("q-beds", "bedrooms", ["Studio", "1", "2", "3", "4", "5 or more", "Not a home"]), False, True)}
              {gfield(lab("q-baths", "Bathrooms"), select("q-baths", "bathrooms", ["1", "1.5", "2", "2.5", "3", "4 or more"]), False, True)}
              {gfield(lab("q-zip", "ZIP code"), '<input id="q-zip" name="zip" type="text" inputmode="numeric" maxlength="5" autocomplete="postal-code" required>', True, True)}
              {gfield(lab("q-date", "Preferred date"), '<input id="q-date" name="date" type="date">', False, True)}
              {gfield(lab("q-details", "Anything we should know?"), '<textarea id="q-details" name="details" rows="4" placeholder="For example: a dog at home, the oven needs doing, guests check in at 4pm"></textarea>')}
            </div>
            {nav(True, nxt)}
          </div>
          <div class="gform_page" data-title="Your details" hidden>
            <div class="gform_fields">
              {gfield(lab("q-name", "Name"), '<input id="q-name" name="name" type="text" autocomplete="name" required>', True, True)}
              {gfield(lab("q-phone", "Phone"), '<input id="q-phone" name="phone" type="tel" autocomplete="tel" required>', True, True)}
              {gfield(lab("q-email", "Email"), '<input id="q-email" name="email" type="email" autocomplete="email">')}
              {gfield("Best way to reach you", radios("contact_pref", ["Phone call", "Text", "Email"]), group=True)}
            </div>
            {nav(True, sub)}
          </div>
        </form>
        <div class="gform_confirmation_wrapper" hidden><div class="gform_confirmation_message" role="status"><h3 class="wp-block-heading">Thanks<span data-first-name></span>! Your request is in.</h3><p>We&rsquo;ll get back to you with a price. In a hurry? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div></div>
      </div>
    </div>
    <aside class="widget-area" aria-label="Sidebar">
      <section class="widget widget--dark">
        <h2 class="widget-title">Rather talk?</h2>
        <a class="widget-phone" href="tel:{TEL}">{PHONE}</a>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </section>
      <section class="widget">
        <h2 class="widget-title">From a customer</h2>
        <p>&ldquo;{r[2]}&rdquo;</p>
        <p class="widget-cite">{r[0]}, Google review</p>
      </section>
      <section class="widget">
        <h2 class="widget-title">Before we leave</h2>
        <p>We ask you to look around. Anything you point out, we go back over.</p>
      </section>
    </aside>
  </div>
</section>
"""


def notfound(root):
    return f"""
<section class="wp-block-group alignfull notfound has-global-padding">
  <h1 class="wp-block-heading">We looked under the couch cushions</h1>
  <p>This page isn&rsquo;t there. Try the homepage or give us a call.</p>
  {buttons(button(root, "Go to the homepage", "", "arrow"), button("tel:" + TEL, "Call " + PHONE, "outline"), center=True)}
</section>
"""


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "HouseCleaningService", "name": "Pinheiro's Cleaning",
        "url": "https://pinheiroscleaning.com/", "logo": BASE_URL + "assets/img/logo.png", "image": BASE_URL + "assets/img/og-image.jpg",
        "telephone": "+1-561-929-0067", "email": EMAIL, "foundingDate": "2019",
        "address": {"@type": "PostalAddress", "addressLocality": "Deerfield Beach", "addressRegion": "FL", "postalCode": "33442", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": "Palm Beach County"}, {"@type": "AdministrativeArea", "name": "Broward County"}],
    }
    return f'<script type="application/ld+json">{json.dumps(data, separators=(",", ":"))}</script>\n'


if __name__ == "__main__":
    preload = ('<link rel="preload" as="image" href="assets/img/hero-1280.webp" '
               'imagesrcset="assets/img/hero-800.webp 800w, assets/img/hero-1280.webp 1280w" imagesizes="(min-width: 782px) 50vw, 100vw" fetchpriority="high">\n')
    page(0, "", "House &amp; Office Cleaning in Palm Beach County and Broward | Pinheiro&rsquo;s Cleaning",
         f"Home, vacation rental, move-out, office and post-construction cleaning from Deerfield Beach. Locally owned since 2019. Call {PHONE}.",
         "", home, extra_head=preload + jsonld(), body_class="home page")
    page(1, "services/", "Cleaning Services | Pinheiro&rsquo;s Cleaning, Deerfield Beach FL",
         "House cleaning, vacation rentals, move in and move out, offices and post-construction cleaning in Palm Beach County and Broward.", "services/", services)
    page(1, "contact/", f"Contact | Pinheiro&rsquo;s Cleaning | {PHONE}",
         f"Call {PHONE}, email or send a message to Pinheiro's Cleaning in Deerfield Beach, FL.", "contact/", contact)
    page(1, "quote/", "Get a Quote | Pinheiro&rsquo;s Cleaning",
         "Get a price for house, rental, office or post-construction cleaning in Palm Beach County and Broward.", None, quote, actions=False)
    out = f"""{head(BASE_URL, "Page not found | Pinheiro&rsquo;s Cleaning", "This page could not be found.", "404.html")}
<body class="error404 has-mobile-actions">
<div class="wp-site-blocks">
{header(BASE_URL, None)}
<main class="wp-block-group" id="wp--skip-link--target">{notfound(BASE_URL)}</main>
{footer(BASE_URL)}
</div>
{mobile_actions(BASE_URL)}
</body>
</html>
"""
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(out)
    print("wrote 404.html")
    with open(os.path.join(OUT, "version.json"), "w") as f:
        json.dump({"build": BUILD}, f)
    print("wrote version.json", BUILD)
