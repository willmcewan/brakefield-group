#!/usr/bin/env python3
"""Generates the whole Brakefield Group site from this one file.

Edit content here, run `python3 build.py`, commit, push. Every page shares one
header, footer and stylesheet, so the site cannot drift page to page.
"""
import os, re, json

ROOT = os.path.dirname(os.path.abspath(__file__))
PHONE_H = "662.715.4477"
PHONE   = "+16627154477"
EMAIL   = "booking@brakefieldtrans.com"
DOMAIN  = "https://brakefieldgroup.com"     # LAUNCH: set the real domain
NOINDEX = True                              # LAUNCH: set False on the real domain

# ----------------------------------------------------------------- navigation
SERVICES = [
    ("gameday",      "Ole Miss Gameday",        "services/gameday.html"),
    ("airport",      "Airport Transportation",  "services/airport.html"),
    ("corporate",    "Corporate &amp; Executive",   "services/corporate.html"),
    ("celebrations", "Celebrations",            "services/celebrations.html"),
    ("charters",     "Group Charters",          "services/charters.html"),
    ("students",     "Students &amp; Parents",      "services/students.html"),
]
AREAS = [
    ("memphis-airport", "Memphis Airport",  "areas/memphis-airport.html"),
    ("oxford",          "Oxford",           "areas/oxford.html"),
    ("tupelo",          "Tupelo",           "areas/tupelo.html"),
    ("southaven",       "Southaven &amp; DeSoto","areas/southaven.html"),
    ("batesville",      "Batesville",       "areas/batesville.html"),
    ("new-albany",      "New Albany",       "areas/new-albany.html"),
    ("holly-springs",   "Holly Springs",    "areas/holly-springs.html"),
    ("starkville",      "Starkville",       "areas/starkville.html"),
]

def icon(p, extra=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (extra, p))
I_PHONE = icon('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>')
I_SMS   = icon('<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>')
I_MAIL  = icon('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 6L2 7"/>')
I_INFO  = icon('<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>')

def pic(r, name, alt, cls="", w=1600, h=1000, lazy=True):
    return ('<picture><source srcset="%sassets/%s.webp" type="image/webp">'
            '<img src="%sassets/%s.jpg" alt="%s" class="%s" width="%d" height="%d"%s></picture>'
            % (r, name, r, name, alt, cls, w, h, ' loading="lazy" decoding="async"' if lazy else ''))

def head(r, title, desc, canon, extra_ld=None):
    ld = {"@context":"https://schema.org","@type":["LocalBusiness","TaxiService"],
      "name":"The Brakefield Group","telephone":"+1-662-715-4477","email":EMAIL,
      "url":DOMAIN+"/","image":DOMAIN+"/assets/hero-sprinter.jpg","priceRange":"$$$",
      "slogan":"Trusted Service. Professional Results.",
      "address":{"@type":"PostalAddress","addressLocality":"Oxford","addressRegion":"MS","addressCountry":"US"},
      "areaServed":[{"@type":"AdministrativeArea","name":"North Mississippi"},
                    {"@type":"City","name":"Oxford, MS"},{"@type":"City","name":"Memphis, TN"}],
      "sameAs":["https://www.instagram.com/thebrakegroup/","https://linktr.ee/brakefieldgroup"]}
    blocks = '<script type="application/ld+json">%s</script>' % json.dumps(ld)
    if extra_ld:
        blocks += '\n<script type="application/ld+json">%s</script>' % json.dumps(extra_ld)
    robots = '\n<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#08080a">{robots}
<link rel="canonical" href="{DOMAIN}/{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="The Brakefield Group">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{canon}">
<meta property="og:image" content="{DOMAIN}/assets/share.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}assets/favicon.png" sizes="32x32">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow:ital,wght@0,400;0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/site.css">
{blocks}
<script>document.documentElement.className+=" js";</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>'''

def header(r, active=""):
    svc = "".join('<a href="%s%s">%s</a>' % (r, u, n) for _, n, u in SERVICES)
    ara = "".join('<a href="%s%s">%s</a>' % (r, u, n) for _, n, u in AREAS)
    def cls(k): return ' class="on"' if k == active else ''
    return f'''
<header>
  <div class="wrap nav">
    <a class="brand" href="{r}index.html" aria-label="The Brakefield Group, home">
      <img src="{r}assets/logo-lockup.png" alt="The Brakefield Group" width="476" height="155">
    </a>
    <nav class="navlinks" aria-label="Primary">
      <div class="drop">
        <a href="{r}services/gameday.html"{cls('services')} aria-haspopup="true">Services</a>
        <div class="menu">{svc}</div>
      </div>
      <div class="drop">
        <a href="{r}areas/memphis-airport.html"{cls('areas')} aria-haspopup="true">Service Area</a>
        <div class="menu">{ara}</div>
      </div>
      <a href="{r}fleet.html"{cls('fleet')}>Fleet</a>
      <a href="{r}about.html"{cls('about')}>About</a>
      <a href="{r}faq.html"{cls('faq')}>FAQ</a>
      <a href="{r}reserve.html"{cls('reserve')}>Reserve</a>
    </nav>
    <a class="btn btn-primary" href="tel:{PHONE}">{I_PHONE}{PHONE_H}</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mobilenav" aria-label="Open menu">
      {icon('<path d="M3 6h18M3 12h18M3 18h18"/>')}
    </button>
  </div>
  <div id="mobilenav">
    <span class="mlabel">Services</span>{svc}
    <span class="mlabel">Service area</span>{ara}
    <span class="mlabel">More</span>
    <a href="{r}fleet.html">Fleet</a><a href="{r}about.html">About</a>
    <a href="{r}faq.html">FAQ</a><a href="{r}reserve.html">Reserve a date</a>
    <a href="{r}contact.html">Contact</a>
  </div>
</header>
<main id="main">'''

def cta_band(r, title="Ready when you are", sub="Send the date, the headcount and where you're headed. We'll come straight back with a rate."):
    return f'''
<section class="band">
  <div class="wrap band-in">
    <div>
      <h2 class="chrome">{title}</h2>
      <p>{sub}</p>
    </div>
    <div class="band-cta">
      <a class="btn btn-primary" href="tel:{PHONE}">{I_PHONE}Call {PHONE_H}</a>
      <a class="btn btn-ghost" href="{r}reserve.html">Reserve a date</a>
    </div>
  </div>
</section>'''

def footer(r):
    svc = "".join('<li><a href="%s%s">%s</a></li>' % (r, u, n) for _, n, u in SERVICES)
    ara = "".join('<li><a href="%s%s">%s</a></li>' % (r, u, n) for _, n, u in AREAS)
    return f'''</main>
<footer>
  <div class="wrap">
    <div class="f-top">
      <div>
        <a class="brand" href="{r}index.html" style="display:inline-flex">
          <img src="{r}assets/logo-lockup.png" alt="The Brakefield Group" width="476" height="155" style="width:186px" loading="lazy">
        </a>
        <p class="f-blurb">Private chauffeured transportation based in Oxford, Mississippi, serving North Mississippi and the Mid-South.</p>
        <div class="social">
          <a href="https://www.instagram.com/thebrakegroup/" aria-label="Instagram" target="_blank" rel="noopener">{icon('<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>')}</a>
          <a href="https://linktr.ee/brakefieldgroup" aria-label="Linktree" target="_blank" rel="noopener">{icon('<path d="M12 3v18M12 9L6 4M12 9l6-5M12 14l-6 5M12 14l6 5"/>')}</a>
        </div>
      </div>
      <div><h4>Services</h4><ul class="f-list">{svc}</ul></div>
      <div><h4>Service area</h4><ul class="f-list">{ara}</ul></div>
      <div><h4>Company</h4><ul class="f-list">
        <li><a href="{r}fleet.html">The fleet</a></li>
        <li><a href="{r}about.html">About us</a></li>
        <li><a href="{r}faq.html">FAQ</a></li>
        <li><a href="{r}reserve.html">Reserve a date</a></li>
        <li><a href="{r}contact.html">Contact</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul class="f-list">
        <li><a href="tel:{PHONE}">{PHONE_H}</a></li>
        <li><a href="sms:{PHONE}">Text us</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul></div>
    </div>
    <div class="f-bot">
      <span>&copy; <span id="yr">2026</span> The Brakefield Group. All rights reserved.</span>
      <span class="f-legal"><a href="{r}privacy.html">Privacy</a> · <a href="{r}terms.html">Terms</a></span>
      <span class="sp">Oxford, Mississippi · Serving the Mid-South</span>
    </div>
  </div>
</footer>
<div class="callbar">
  <a class="btn btn-primary" href="tel:{PHONE}">Call now</a>
  <a class="btn btn-ghost" href="sms:{PHONE}">Text us</a>
</div>
<script src="{r}assets/site.js"></script>
</body>
</html>'''

def crumbs(r, trail):
    out = ['<a href="%sindex.html">Home</a>' % r]
    for label, href in trail[:-1]:
        out.append('<a href="%s%s">%s</a>' % (r, href, label))
    out.append('<span>%s</span>' % trail[-1][0])
    return '<nav class="crumbs wrap" aria-label="Breadcrumb">%s</nav>' % "".join(out)

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return path

# ---------------------------------------------------------------------- CSS
CSS = r"""
:root{
  --ink:#08080a; --ink-2:#0e0f12; --ink-3:#15161a;
  --line:rgba(255,255,255,.13); --line-2:rgba(255,255,255,.07);
  --mute:#8f959d; --mute-2:#c2c7ce; --chrome-3:#9aa0a6; --chrome-2:#e4e7ea;
  --maxw:1220px; --pad:clamp(20px,5vw,52px); --r:14px;
  --ease:cubic-bezier(.22,.61,.36,1);
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--ink);color:var(--mute-2);
  font-family:"Barlow",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block;height:auto}
a{color:inherit}
h1,h2,h3{font-family:"Anton",Impact,"Arial Narrow Bold",sans-serif;font-weight:400;
  text-transform:uppercase;line-height:.95;color:#fff;margin:0;text-wrap:balance}
p{margin:0}
.wrap{max-width:var(--maxw);margin-inline:auto;padding-inline:var(--pad)}
.eyebrow{font-size:11.5px;letter-spacing:.28em;text-transform:uppercase;color:var(--chrome-3);
  font-weight:600;margin:0 0 20px}
.chrome{color:#eef0f2}
@supports (-webkit-background-clip:text) or (background-clip:text){
 .chrome{background:linear-gradient(178deg,#fff 0%,#e9ecef 34%,#8e959c 50%,#fbfcfd 62%,#b9c0c7 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-weight:700;
  font-size:14px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;
  padding:16px 28px;border-radius:999px;border:1px solid transparent;cursor:pointer;
  font-family:inherit;white-space:nowrap;
  transition:transform .25s var(--ease),background .25s var(--ease),border-color .25s var(--ease)}
.btn:active{transform:translateY(1px)}
.btn-primary{background:linear-gradient(180deg,#fff,#d5d9dd);color:#08080a;
  box-shadow:0 1px 0 rgba(255,255,255,.7) inset,0 14px 34px -14px rgba(255,255,255,.4)}
.btn-primary:hover{background:#fff}
.btn-ghost{border-color:var(--line);color:#fff;background:rgba(255,255,255,.03)}
.btn-ghost:hover{border-color:rgba(255,255,255,.42);background:rgba(255,255,255,.08)}
.btn svg{width:16px;height:16px;flex:none}

header{position:sticky;top:0;z-index:60;background:rgba(8,8,10,.76);
  backdrop-filter:saturate(150%) blur(14px);-webkit-backdrop-filter:saturate(150%) blur(14px);
  border-bottom:1px solid var(--line-2)}
.nav{display:flex;align-items:center;gap:22px;height:78px}
.brand{display:flex;align-items:center;margin-right:auto;text-decoration:none}
.brand img{width:172px}
.navlinks{display:flex;gap:28px;align-items:center}
.navlinks a{text-decoration:none;font-size:12.5px;font-weight:600;letter-spacing:.15em;
  text-transform:uppercase;color:var(--mute);transition:color .2s}
.navlinks a:hover,.navlinks a.on{color:#fff}
.drop{position:relative}
.menu{position:absolute;top:100%;left:-18px;padding:10px 0;min-width:250px;display:none;
  background:#101116;border:1px solid var(--line);border-radius:12px;
  box-shadow:0 26px 60px -20px rgba(0,0,0,.9);margin-top:14px}
.menu::before{content:"";position:absolute;top:-14px;left:0;right:0;height:14px}
.drop:hover .menu,.drop:focus-within .menu{display:block}
.menu a{display:block;padding:11px 20px;font-size:12.5px;color:var(--mute-2);letter-spacing:.1em}
.menu a:hover{color:#fff;background:rgba(255,255,255,.05)}
.nav>.btn{padding:12px 22px;font-size:12.5px}
.burger{display:none;background:none;border:1px solid var(--line);border-radius:10px;
  width:44px;height:44px;color:#fff;cursor:pointer;align-items:center;justify-content:center}
.burger svg{width:20px;height:20px}
#mobilenav{display:none;border-top:1px solid var(--line-2);background:var(--ink-2);
  max-height:76vh;overflow-y:auto}
#mobilenav.open{display:block}
#mobilenav a{display:block;padding:14px var(--pad);text-decoration:none;color:#fff;
  font-weight:600;letter-spacing:.1em;text-transform:uppercase;font-size:13px;
  border-bottom:1px solid var(--line-2)}
.mlabel{display:block;padding:16px var(--pad) 8px;font-size:10.5px;letter-spacing:.24em;
  text-transform:uppercase;color:var(--chrome-3);font-weight:700}

.crumbs{display:flex;flex-wrap:wrap;gap:10px;align-items:center;padding-top:24px;
  font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
.crumbs a{text-decoration:none;color:var(--mute)}
.crumbs a:hover{color:#fff}
.crumbs a::after{content:"›";margin-left:10px;color:var(--chrome-3)}
.crumbs span{color:#fff}

.hero{position:relative;padding:clamp(52px,7vw,92px) 0 0;overflow:hidden}
.hero::before{content:"";position:absolute;inset:-45% -20% auto;height:150%;
  background:radial-gradient(58% 48% at 50% 0%,rgba(255,255,255,.11),transparent 70%);pointer-events:none}
.hero .wrap{position:relative;z-index:1}
h1{font-size:clamp(38px,6.6vw,82px);max-width:15ch}
.lede{margin-top:26px;max-width:58ch;font-size:clamp(17px,2.1vw,20px);color:var(--mute-2)}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}
.trust{display:flex;flex-wrap:wrap;gap:10px 30px;margin-top:42px;padding-top:26px;
  border-top:1px solid var(--line-2);list-style:none;padding-left:0}
.trust li{display:flex;align-items:center;gap:9px;font-size:14px;color:var(--mute);font-weight:500}
.trust svg{width:16px;height:16px;color:var(--chrome-3);flex:none}

.shot{position:relative;margin-top:clamp(30px,5vw,56px);border-radius:var(--r);overflow:hidden;
  border:1px solid var(--line)}
.shot img{width:100%;object-fit:cover;aspect-ratio:16/9}
.shot::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 55%,rgba(8,8,10,.55))}
.shot.tall img{aspect-ratio:4/5}
.shot.free img{aspect-ratio:auto}

.ticker{border-block:1px solid var(--line-2);background:var(--ink-2);overflow:hidden;padding:16px 0;margin-top:clamp(46px,7vw,86px)}
.ticker-track{display:flex;width:max-content;animation:slide 40s linear infinite}
@keyframes slide{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.ticker-track span{display:inline-flex;align-items:center;gap:36px;padding-right:36px;font-size:12.5px;
  font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--chrome-3);white-space:nowrap}
.ticker-track span::after{content:"";width:4px;height:4px;border-radius:50%;background:var(--chrome-3);opacity:.5}
@media (prefers-reduced-motion:reduce){.ticker-track{animation:none}.ticker{overflow-x:auto}}

.sec{padding:clamp(64px,9vw,116px) 0}
.sec.alt{background:var(--ink-2);border-block:1px solid var(--line-2)}
.sec-head{max-width:58ch;margin-bottom:clamp(36px,5vw,58px)}
h2{font-size:clamp(30px,5vw,54px)}
.sec-head p{margin-top:20px;color:var(--mute)}
.prose{max-width:68ch;display:grid;gap:20px}
.prose p{color:var(--mute)}
.prose h3{font-size:clamp(21px,3vw,28px);margin-top:14px}
/* Service pages wrap each block in a div, which made it a single grid child —
   its heading and paragraphs collapsed together. Space them as their own stack. */
.prose>div{display:grid;gap:16px}
.prose>div>h3{margin-top:0}
.prose ul{margin:0;padding:0;list-style:none;display:grid;gap:11px}
.prose li{color:var(--mute);display:flex;gap:12px;font-size:16px}
.prose li::before{content:"";width:4px;height:4px;border-radius:50%;background:var(--chrome-3);margin-top:11px;flex:none}

.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,5vw,66px);align-items:center}
.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(20px,3vw,34px)}
.svc{display:grid;gap:16px;grid-template-columns:repeat(2,1fr)}
.card{border:1px solid var(--line);border-radius:var(--r);
  background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.014));
  padding:clamp(26px,3.2vw,38px);text-decoration:none;display:block;
  transition:border-color .3s var(--ease),transform .3s var(--ease),background .3s var(--ease)}
a.card:hover,.card:hover{border-color:rgba(255,255,255,.28);transform:translateY(-3px);
  background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.02))}
.card h3{font-size:clamp(21px,2.7vw,28px);margin-bottom:13px}
.card p{color:var(--mute);font-size:16px}
.card ul{margin:18px 0 0;padding:0;list-style:none;display:grid;gap:10px}
.card li{font-size:14.5px;color:var(--mute);display:flex;gap:11px;align-items:flex-start}
.card li::before{content:"";width:4px;height:4px;border-radius:50%;background:var(--chrome-3);margin-top:9px;flex:none}
.card .more{display:inline-flex;align-items:center;gap:8px;margin-top:20px;color:#fff;
  font-size:12.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}
.card .more::after{content:"→";transition:transform .25s var(--ease)}
a.card:hover .more::after{transform:translateX(4px)}
.card.wide{grid-column:1/-1}

.spec{margin:28px 0 0;padding:0;list-style:none;border-top:1px solid var(--line-2)}
.spec div{display:flex;justify-content:space-between;gap:20px;align-items:baseline;
  padding:15px 0;border-bottom:1px solid var(--line-2)}
.spec dt{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--chrome-3);font-weight:700}
.spec dd{margin:0;color:#fff;font-size:15.5px;text-align:right}

.gd{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--ink-2)}
.gd-row{display:grid;grid-template-columns:auto 1fr auto;gap:clamp(14px,3vw,32px);align-items:center;
  padding:21px clamp(18px,3vw,32px);border-bottom:1px solid var(--line-2);transition:background .25s var(--ease)}
.gd-row:last-child{border-bottom:0}
.gd-row:hover{background:rgba(255,255,255,.035)}
.gd-date{font-family:"Anton",sans-serif;font-size:15px;letter-spacing:.09em;color:#fff;min-width:6.5ch;line-height:1.25}
.gd-date small{display:block;font-family:"Barlow",sans-serif;font-size:11px;letter-spacing:.16em;
  color:var(--chrome-3);font-weight:600;margin-top:3px}
.gd-opp{font-family:"Anton",sans-serif;font-size:clamp(19px,2.9vw,27px);color:#fff;line-height:1.05}
.gd-opp em{display:block;font-family:"Barlow",sans-serif;font-style:normal;font-size:12px;letter-spacing:.15em;
  text-transform:uppercase;color:var(--chrome-3);font-weight:600;margin-top:6px}
.gd-row .btn{padding:11px 21px;font-size:12px}
.gd-row.past{opacity:.32}.gd-row.past .btn{display:none}
.gd-row.past .gd-opp em::after{content:" · completed"}
.gd-row.next{background:linear-gradient(90deg,rgba(255,255,255,.1),rgba(255,255,255,.02))}
.gd-row.next .gd-date::before{content:"Next up";display:block;font-family:"Barlow",sans-serif;font-size:10px;
  letter-spacing:.2em;text-transform:uppercase;color:#fff;font-weight:700;margin-bottom:6px}
.note{margin-top:20px;font-size:13.5px;color:var(--mute);display:flex;gap:10px;align-items:flex-start}
.note svg{width:15px;height:15px;flex:none;margin-top:4px;color:var(--chrome-3)}

.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;counter-reset:s}
.step{border:1px solid var(--line);border-radius:var(--r);padding:clamp(24px,3vw,34px);
  background:linear-gradient(180deg,rgba(255,255,255,.045),transparent);counter-increment:s}
.step::before{content:counter(s,decimal-leading-zero);font-family:"Anton",sans-serif;font-size:32px;
  color:transparent;-webkit-text-stroke:1px var(--chrome-3);display:block;margin-bottom:18px;opacity:.8}
.step h3{font-size:21px;margin-bottom:12px}
.step p{font-size:15.5px;color:var(--mute)}
.why-item h3{font-size:19px;margin-bottom:11px}
.why-item p{font-size:15px;color:var(--mute)}
.why-item .mk{width:28px;height:2px;background:linear-gradient(90deg,#fff,var(--chrome-3));
  margin-bottom:20px;border-radius:2px}

.band{background:var(--ink-2);border-block:1px solid var(--line-2);padding:clamp(44px,6vw,72px) 0}
.band-in{display:flex;gap:30px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.band-in h2{font-size:clamp(26px,3.6vw,40px)}
.band-in p{color:var(--mute);margin-top:12px;max-width:52ch}
.band-cta{display:flex;gap:12px;flex-wrap:wrap}

details{border-bottom:1px solid var(--line-2)}
summary{list-style:none;cursor:pointer;padding:25px 46px 25px 0;position:relative;
  font-family:"Anton",sans-serif;text-transform:uppercase;color:#fff;font-size:clamp(16px,2.2vw,21px);line-height:1.3}
summary::-webkit-details-marker{display:none}
summary::after{content:"";position:absolute;right:6px;top:50%;width:11px;height:11px;
  border-right:2px solid var(--chrome-3);border-bottom:2px solid var(--chrome-3);
  transform:translateY(-70%) rotate(45deg);transition:transform .28s var(--ease)}
details[open] summary::after{transform:translateY(-30%) rotate(225deg)}
details p{padding:0 0 27px;color:var(--mute);max-width:70ch}
summary:focus-visible{outline:2px solid var(--chrome-3);outline-offset:4px;border-radius:4px}
.faq{max-width:880px}

.contact-grid{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(30px,5vw,66px);align-items:start}
.dial{display:grid;gap:12px;margin-top:30px}
.dial a{display:flex;align-items:center;gap:17px;text-decoration:none;border:1px solid var(--line);
  border-radius:var(--r);padding:19px 23px;transition:border-color .25s var(--ease),background .25s var(--ease)}
.dial a:hover{border-color:rgba(255,255,255,.35);background:rgba(255,255,255,.05)}
.dial svg{width:21px;height:21px;color:var(--chrome-2);flex:none}
.dial b{display:block;color:#fff;font-family:"Anton",sans-serif;font-weight:400;font-size:19px;
  letter-spacing:.03em;text-transform:uppercase}
.dial small{display:block;color:var(--mute);font-size:13px;margin-top:3px}
form{border:1px solid var(--line);border-radius:var(--r);padding:clamp(26px,3.4vw,38px);
  background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.012))}
.f2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
label{display:block;font-size:11.5px;letter-spacing:.17em;text-transform:uppercase;
  color:var(--chrome-3);font-weight:700;margin:0 0 8px}
.field{margin-bottom:16px}
input,select,textarea{width:100%;background:rgba(0,0,0,.45);border:1px solid var(--line);border-radius:10px;
  padding:13px 14px;color:#fff;font-family:inherit;font-size:16px;transition:border-color .2s,background .2s}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--chrome-3);background:rgba(0,0,0,.62)}
textarea{resize:vertical;min-height:96px}
select{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%239aa0a6' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 14px center;padding-right:38px}
form .btn{width:100%;margin-top:6px}
.formnote{font-size:12.5px;color:var(--mute);margin-top:15px;text-align:center}

footer{border-top:1px solid var(--line-2);background:var(--ink-2);padding:clamp(52px,6vw,78px) 0 42px}
.f-top{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr 1fr;gap:clamp(24px,3vw,44px);
  padding-bottom:40px;border-bottom:1px solid var(--line-2)}
.f-top h4{font-size:11.5px;letter-spacing:.2em;color:var(--chrome-3);margin:0 0 18px;
  text-transform:uppercase;font-weight:700}
.f-blurb{color:var(--mute);font-size:15px;max-width:34ch;margin-top:20px}
.f-list{list-style:none;margin:0;padding:0;display:grid;gap:11px}
.f-list a{text-decoration:none;color:var(--mute);font-size:14.5px;transition:color .2s}
.f-list a:hover{color:#fff}
.f-bot{display:flex;flex-wrap:wrap;gap:14px 26px;align-items:center;padding-top:28px;font-size:13px;color:var(--mute)}
.f-bot .sp{margin-left:auto}
.f-legal a{color:var(--mute);text-decoration:none}
.f-legal a:hover{color:#fff}
.social{display:flex;gap:10px;margin-top:22px}
.social a{width:40px;height:40px;border:1px solid var(--line);border-radius:10px;display:grid;place-items:center;
  color:var(--mute);transition:color .2s,border-color .2s,background .2s}
.social a:hover{color:#fff;border-color:rgba(255,255,255,.35);background:rgba(255,255,255,.05)}
.social svg{width:18px;height:18px}

.callbar{position:fixed;left:0;right:0;bottom:0;z-index:70;display:none;gap:10px;
  padding:10px var(--pad) calc(10px + env(safe-area-inset-bottom));background:rgba(8,8,10,.92);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-top:1px solid var(--line)}
.callbar .btn{flex:1;padding:14px 10px}

.js .rv{opacity:0;transform:translateY(18px);transition:opacity .75s var(--ease),transform .75s var(--ease)}
.js .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.js .rv{opacity:1;transform:none;transition:none}}
:focus-visible{outline:2px solid var(--chrome-2);outline-offset:3px}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:#000;padding:12px 18px;z-index:99;
  font-weight:700;border-radius:0 0 8px 0}
.skip:focus{left:0}

@media (max-width:1080px){.f-top{grid-template-columns:1fr 1fr 1fr}}
@media (max-width:980px){
  .grid-2{grid-template-columns:1fr}.grid-4{grid-template-columns:repeat(2,1fr)}
  .grid-3,.steps{grid-template-columns:1fr}
  .contact-grid{grid-template-columns:1fr}
}
@media (max-width:760px){
  body{font-size:16px}
  .navlinks,.nav>.btn{display:none}
  .burger{display:inline-flex}
  .brand img{width:148px}
  .svc{grid-template-columns:1fr}
  .callbar{display:flex}
  main{padding-bottom:84px}
  .gd-row{grid-template-columns:auto 1fr;row-gap:14px}
  .gd-row .btn{grid-column:1/-1;justify-self:start}
  .f2{grid-template-columns:1fr}
  .trust{gap:10px 20px}
  .f-top{grid-template-columns:1fr 1fr}
  .band-in{flex-direction:column;align-items:flex-start}
}
@media (max-width:520px){
  .grid-4,.f-top{grid-template-columns:1fr}
  h1{font-size:clamp(34px,10vw,54px)}
}
"""

JS = r"""(function(){"use strict";
var y=document.getElementById("yr"); if(y) y.textContent=new Date().getFullYear();

var burger=document.getElementById("burger"), mnav=document.getElementById("mobilenav");
if(burger&&mnav){
  burger.addEventListener("click",function(){
    var open=mnav.classList.toggle("open");
    burger.setAttribute("aria-expanded",open?"true":"false");
    burger.setAttribute("aria-label",open?"Close menu":"Open menu");
  });
}
var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// gameday: gray out past games, mark the next one
var today=new Date(); today.setHours(0,0,0,0); var found=false;
Array.prototype.forEach.call(document.querySelectorAll(".gd-row[data-date]"),function(row){
  var p=row.getAttribute("data-date").split("-");
  var d=new Date(+p[0],+p[1]-1,+p[2]);
  if(d<today) row.classList.add("past");
  else if(!found){ row.classList.add("next"); found=true; }
});

// Reveal on scroll. Deliberately not IntersectionObserver: it never fires in
// some webviews, which would leave sections hidden for good. Polling a rect
// cannot be missed, and a zero-height viewport reveals rather than hides.
var rvEls=Array.prototype.slice.call(document.querySelectorAll(".rv"));
var raf=window.requestAnimationFrame||function(f){return setTimeout(f,16)};
if(reduce){ rvEls.forEach(function(el){el.classList.add("in")}); }
else{
  rvEls.forEach(function(el,i){ el.style.transitionDelay=(Math.min(i,3)*55)+"ms"; });
  var ticking=false,onScroll,poll;
  var stop=function(){clearInterval(poll);window.removeEventListener("scroll",onScroll);window.removeEventListener("resize",onScroll)};
  var check=function(){
    ticking=false;
    var h=window.innerHeight||document.documentElement.clientHeight;
    if(!h){ rvEls.forEach(function(el){el.classList.add("in")}); rvEls.length=0; stop(); return; }
    for(var i=rvEls.length-1;i>=0;i--){
      if(rvEls[i].getBoundingClientRect().top<h*0.92){ rvEls[i].classList.add("in"); rvEls.splice(i,1); }
    }
    if(!rvEls.length) stop();
  };
  onScroll=function(){ if(!ticking){ticking=true;raf(check)} };
  window.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",onScroll);
  poll=setInterval(check,200); check();
}

// quote form -> pre-filled email. Swap for a real backend by putting
// action/method on the <form> and deleting this listener.
var form=document.getElementById("quote");
if(form) form.addEventListener("submit",function(e){
  e.preventDefault();
  var v=function(id){var el=document.getElementById(id);return el&&el.value?el.value.trim():"—"};
  var lines=["Name: "+v("name"),"Phone: "+v("phone"),"Email: "+v("email"),"Service: "+v("service"),
    "Date: "+v("date"),"Passengers: "+v("pax"),"Pickup: "+v("from"),"Drop-off: "+v("to"),"","Details:",v("notes")];
  window.location.href="mailto:booking@brakefieldtrans.com?subject="+
    encodeURIComponent("Reservation request — "+v("service")+" — "+v("date"))+
    "&body="+encodeURIComponent(lines.join("\n"));
});
})();"""

# ------------------------------------------------------------------- content
GAMES = [("2026-09-12","Sep 12","Sat","Charlotte","Home opener"),
         ("2026-09-19","Sep 19","Sat","LSU","SEC opener"),
         ("2026-10-17","Oct 17","Sat","Missouri","SEC"),
         ("2026-10-31","Oct 31","Sat","Auburn","SEC · Halloween"),
         ("2026-11-07","Nov 7","Sat","Georgia","SEC"),
         ("2026-11-21","Nov 21","Sat","Wofford","Non-conference"),
         ("2026-11-27","Nov 27","Fri","Mississippi State","The Egg Bowl")]

def schedule(r):
    rows = "".join(f'''<div class="gd-row" data-date="{d}">
        <div class="gd-date">{lbl}<small>{dow}</small></div>
        <div class="gd-opp">{opp}<em>{note}</em></div>
        <a class="btn btn-ghost" href="{r}reserve.html">Reserve</a></div>''' for d,lbl,dow,opp,note in GAMES)
    return f'''<div class="gd rv">{rows}</div>
    <p class="note rv">{I_INFO} Kickoff times are set by the conference and released closer to each game; we build your pickup around the announced time. The Brakefield Group is an independent transportation company and is not affiliated with or endorsed by the University of Mississippi.</p>'''

TRUST = f'''<ul class="trust">
  <li>{icon('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>')}Licensed &amp; insured</li>
  <li>{icon('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>')}Reserved in advance, never on demand</li>
  <li>{icon('<path d="M20 6L9 17l-5-5"/>')}Your rate agreed before you ride</li>
  <li>{icon('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>')}Locally owned &amp; operated</li>
</ul>'''

SERVICE = {
 "gameday": dict(
  nav="Ole Miss Gameday", img="hero-sprinter",
  title="Ole Miss Gameday Transportation in Oxford, MS | The Brakefield Group",
  desc="Private gameday transportation for Ole Miss home games in Oxford. Door-to-door to The Grove and Vaught-Hemingway in a black Mercedes-Benz Sprinter.",
  h1="Ole Miss gameday transportation",
  lede="Door-to-door to The Grove and back, in a black Mercedes-Benz Sprinter, on the seven busiest Saturdays of the year in Oxford.",
  body=[("Why people book us for gamedays",
    ["Oxford on a home weekend is not a normal driving day. Streets close, the square fills, lots sell out by mid-morning, and the walk back to wherever you parked is longer than anyone remembers.",
     "We stage before kickoff, we know which routes hold up and which ones don't, and we move your group from the house or the hotel to the tailgate and back. Nobody circles for parking. Nobody draws the short straw and stays sober to drive."]),
   ("What a gameday booking usually looks like",
    ["Morning pickup from a house, hotel or rental to the tailgate.",
     "Held on-call through the game, or released and re-scheduled for pickup afterward.",
     "Dinner on the square afterward, then home.",
     "Round-trip and by-the-hour both work — tell us the shape of the day and we'll build the run sheet."]),
   ("Book early, genuinely",
    ["Home weekends are the first dates to go, and the Egg Bowl and the LSU game go first of all. If you already know your weekend, get it on the calendar now — we would rather turn down a late request than have you find out in November."])]),
 "airport": dict(
  nav="Airport Transportation", img="sprinter-exterior",
  title="Memphis &amp; Oxford Airport Transportation | The Brakefield Group",
  desc="Airport transportation between Oxford, Mississippi and Memphis International (MEM), University-Oxford (UOX) and Tupelo Regional (TUP). Flight-tracked, booked in advance.",
  h1="Airport transportation",
  lede="Memphis International is the run we make most. We plan around your flight rather than the other way around.",
  body=[("Airports we serve",
    ["<strong>Memphis International (MEM)</strong> — about 70 miles from Oxford, usually an hour and fifteen each way, longer in Memphis rush hour. Our most requested run by a distance.",
     "<strong>University-Oxford Airport (UOX)</strong> — minutes from campus and the square. Common for private and charter arrivals.",
     "<strong>Tupelo Regional (TUP)</strong> — about an hour east.",
     "Going somewhere else — Golden Triangle, Jackson, Nashville, Birmingham? Ask us."]),
   ("How we handle flights",
    ["Give us the flight number when you book and we watch it. If you land late, we already know; if you land early, we adjust. You are not standing at the curb explaining a delay to a driver who is somewhere else.",
     "For departures we build in a cushion for the drive and for security, and we agree the pickup time with you rather than guessing at it."]),
   ("Luggage and groups",
    ["A high-roof Sprinter takes the bags and the people together. No one is negotiating over a trunk, and a family or a team travels as one group rather than split across separate cars that arrive ten minutes apart."])]),
 "corporate": dict(
  nav="Corporate &amp; Executive", img="interior-seats",
  title="Corporate &amp; Executive Car Service, Oxford MS | The Brakefield Group",
  desc="Executive and corporate transportation in North Mississippi — client visits, site tours, team travel and conference movements, arranged once and handled quietly.",
  h1="Corporate &amp; executive travel",
  lede="Client visits, site tours, recruiting weekends and team movements — arranged once, handled quietly, invoiced clean.",
  body=[("What we handle",
    ["Executive and client transportation to and from Memphis International.",
     "Multi-stop days: office, site, lunch, airport, in one booking.",
     "Team and group movements where everyone needs to arrive together and on time.",
     "Recurring and contracted routes for companies running the same trip regularly."]),
   ("Why it works for business travel",
    ["One point of contact from the first message to the final drop-off. You are not managing a roster of drivers or reconciling a dozen separate receipts.",
     "The rate is agreed in writing before the trip, which makes it something you can approve and expense without a surprise at the end."]),
   ("Discretion",
    ["A professional at the wheel, a clean vehicle, and a driver who understands that a conversation in the back of the van is not his business."])]),
 "celebrations": dict(
  nav="Celebrations", img="interior-door",
  title="Celebrations &amp; Nights Out — Private Transportation | The Brakefield Group",
  desc="Private group transportation for birthdays, anniversaries, dinners, concerts and nights out across North Mississippi.",
  h1="Celebrations &amp; nights out",
  lede="Birthdays, anniversaries, dinners, concerts and family occasions — with a driver who stays with the group.",
  body=[("The point of booking a driver",
    ["The evening ends the way it was planned instead of in a parking lot, at midnight, watching a rideshare estimate climb.",
     "We build the run sheet with you ahead of time — pickup windows, the stops, who is getting collected where — so the logistics are settled before anyone puts a dress on."]),
   ("Occasions we regularly run",
    ["Milestone birthdays and anniversary dinners.",
     "Concerts and events in Memphis, Tupelo and across the Mid-South.",
     "Family celebrations where the grandparents and the kids all need to travel together.",
     "Nights out on the Oxford square where nobody should be driving home."]),
   ("Hourly works best",
    ["For an evening with more than one stop, book us by the hour. Your driver stays with the group for the window you have booked rather than being dispatched somewhere else between stops."])]),
 "charters": dict(
  nav="Group Charters", img="interior-seats",
  title="Sprinter Charters &amp; Group Transportation, North Mississippi | The Brakefield Group",
  desc="Private Sprinter charters and group transportation across North Mississippi and the Mid-South — by the hour, by the day, or point to point.",
  h1="Group charters",
  lede="By the hour, by the day, or point to point — private Sprinter charters across North Mississippi and the Mid-South.",
  body=[("How charters are priced",
    ["Hourly, with a minimum, for days with several stops or a lot of waiting.",
     "Point to point, at a flat rate, when it is a straightforward run.",
     "Day rates for longer itineraries or out-of-market travel.",
     "We will tell you which of these is cheaper for what you are actually doing, rather than quoting whichever is highest."]),
   ("Typical charter work",
    ["Wedding-party and guest movements between hotel, venue and reception.",
     "Corporate offsites, plant tours and recruiting weekends.",
     "Group travel to games, concerts and events across the Mid-South.",
     "Multi-day itineraries where the same group needs the same vehicle each day."]),
   ("Out-of-market travel",
    ["Memphis, Tupelo, Jackson, Starkville, Nashville, Birmingham and the wider Mid-South are all within reach. If your itinerary leaves the region, tell us the plan and we will tell you plainly whether we are the right fit."])]),
 "students": dict(
  nav="Students &amp; Parents", img="sprinter-exterior",
  title="Ole Miss Student &amp; Parent Airport Transportation | The Brakefield Group",
  desc="Airport transportation for Ole Miss students and visiting parents between Oxford and Memphis International — booked in advance by a parent, driven by a professional.",
  h1="Students &amp; parents",
  lede="Getting an Ole Miss student to Memphis and back, booked by a parent who is four states away.",
  body=[("Booked by one person, ridden by another",
    ["Most of these bookings are made by a parent for a student. You reserve it, you approve the rate, and we confirm with you — and with them — so nobody is coordinating a pickup by text at 5am on the morning of a flight.",
     "We will confirm the pickup with you once the trip is done, so you know it happened."]),
   ("The runs we make most",
    ["Oxford to Memphis International at the start and end of every break.",
     "Move-in and move-out weekends.",
     "Parents' weekend, graduation and family visits.",
     "Return trips from MEM back to campus, dorm or off-campus housing."]),
   ("Book breaks early",
    ["Thanksgiving, winter break and the end of the spring semester all move a lot of students at once, in the same two or three days. Those dates fill well ahead — get them on the calendar as soon as the academic calendar is out."])]),
}

AREA = {
 "memphis-airport": dict(nav="Memphis Airport", img="sprinter-exterior",
  title="Memphis Airport to Oxford MS Car Service | The Brakefield Group",
  desc="Private car service between Memphis International Airport (MEM) and Oxford, Mississippi. Flight-tracked, booked in advance, rate agreed up front.",
  h1="Memphis Airport to Oxford",
  lede="About 70 miles and roughly an hour and fifteen, in a black Mercedes-Benz Sprinter with your flight already being watched.",
  facts=[("Distance","About 70 miles"),("Typical drive","1 hr 15 min each way"),
         ("Airport code","MEM"),("Flight tracking","Included")],
  body=["Memphis International is the gateway to Oxford, and the drive down I-55 and MS-314 is the single most common trip we make. It is also the trip most worth booking properly: it is long enough that a no-show is a real problem, and it usually lands at the end of a travel day when nobody wants to negotiate.",
        "Give us the flight number and we watch it. A delay is our problem to solve, not something you explain at the curb. For departures we agree the pickup time with you and build in a cushion for both the drive and the terminal.",
        "The Sprinter matters more on this run than almost any other. It is an hour and a quarter with the luggage, and a high-roof van means the bags and the people travel together rather than one family split across two cars."]),
 "oxford": dict(nav="Oxford", img="hero-sprinter",
  title="Oxford MS Private Car Service &amp; Chauffeur | The Brakefield Group",
  desc="Private chauffeured car service in Oxford, Mississippi — gameday, airport, corporate and evening transportation in a black Mercedes-Benz Sprinter.",
  h1="Oxford, Mississippi",
  lede="Our home market — the square, the campus, The Grove, and everything that runs between them.",
  facts=[("Base","Oxford, MS"),("Ole Miss campus","Minutes"),("Nearest airport","UOX"),("Main hub","MEM, about 70 miles")],
  body=["Oxford is where we are based and where most of our work happens: gameday runs to The Grove and Vaught-Hemingway, airport transfers to Memphis, dinners on the square, move-in and graduation weekends, and the steady rhythm of a college town that empties and fills a dozen times a year.",
        "Knowing Oxford is the actual service. Which streets close on a home Saturday, where a Sprinter can turn around, which entrance to a venue is not blocked at 6pm — none of that comes from a map app, and all of it is the difference between arriving well and arriving frustrated.",
        "We cover residential pickups, hotels and rentals, campus, the square and the surrounding county."]),
 "tupelo": dict(nav="Tupelo", img="sprinter-exterior",
  title="Tupelo MS Car Service &amp; Airport Transportation | The Brakefield Group",
  desc="Private car service to and from Tupelo, Mississippi and Tupelo Regional Airport (TUP), including transfers to Memphis International.",
  h1="Tupelo",
  lede="About an hour east of Oxford, with its own regional airport and a steady run to Memphis.",
  facts=[("From Oxford","About an hour"),("Airport","Tupelo Regional (TUP)"),("To MEM","Roughly 1 hr 45 min"),("Service","Airport, corporate, events")],
  body=["Tupelo sits about an hour east of Oxford and is a regular part of our map — corporate travel, regional flights out of Tupelo Regional, and longer transfers up to Memphis International when the schedule out of TUP does not work.",
        "For business travel between Tupelo and Memphis, an agreed flat rate and a professional driver usually costs less trouble than the alternatives, particularly when the arrival time actually matters.",
        "We also run Tupelo for events and celebrations where a group wants to travel together and nobody wants to drive home afterward."]),
 "southaven": dict(nav="Southaven &amp; DeSoto County", img="sprinter-exterior",
  title="Southaven &amp; DeSoto County Car Service | The Brakefield Group",
  desc="Private car service in Southaven, Olive Branch, Hernando and DeSoto County, Mississippi — airport transfers to Memphis International and group transportation.",
  h1="Southaven &amp; DeSoto County",
  lede="The northern edge of Mississippi, minutes from Memphis International and the whole Memphis metro.",
  facts=[("Towns","Southaven, Olive Branch, Hernando"),("To MEM","Under half an hour"),("From Oxford","About an hour"),("Service","Airport, corporate, events")],
  body=["DeSoto County sits right on the Tennessee line, which makes it the shortest airport run on our map — Southaven and Olive Branch are both well under half an hour from Memphis International in normal traffic.",
        "It is also the natural staging point for anything happening in the Memphis metro: concerts, games, downtown dinners and corporate travel that starts or ends in Mississippi but happens in Tennessee.",
        "We run DeSoto County both as a destination and as part of longer trips between Oxford and Memphis."]),
 "batesville": dict(nav="Batesville", img="sprinter-exterior",
  title="Batesville MS Car Service &amp; Airport Transportation | The Brakefield Group",
  desc="Private car service in Batesville and Panola County, Mississippi — Memphis airport transfers, gameday transportation to Oxford and group travel.",
  h1="Batesville",
  lede="About half an hour from Oxford, right on the I-55 corridor to Memphis.",
  facts=[("From Oxford","About 30 minutes"),("To MEM","About an hour"),("Corridor","I-55"),("Service","Airport, gameday, events")],
  body=["Batesville sits on I-55 between Oxford and Memphis, which makes it a straightforward and frequently requested pickup — both for airport runs north and for gameday travel east into Oxford.",
        "For Ole Miss home weekends, Batesville and Panola County are common staging points for families who stay outside Oxford to avoid the weekend rates, then need a way in and out that does not involve parking.",
        "Airport transfers from Batesville to Memphis International run about an hour in normal traffic."]),
 "new-albany": dict(nav="New Albany", img="sprinter-exterior",
  title="New Albany MS Car Service &amp; Airport Transportation | The Brakefield Group",
  desc="Private car service in New Albany and Union County, Mississippi — airport transfers, gameday transportation to Oxford and private group travel.",
  h1="New Albany",
  lede="Half an hour east of Oxford, on the road between the campus and Tupelo.",
  facts=[("From Oxford","About 30 minutes"),("To Tupelo","About 30 minutes"),("To MEM","Around 1 hr 45 min"),("Service","Airport, gameday, events")],
  body=["New Albany sits between Oxford and Tupelo, which puts it comfortably inside our regular map for airport transfers, gameday travel and evening bookings.",
        "Most New Albany work is either a run up to Memphis International or a run into Oxford for a home game or a graduation weekend.",
        "For groups, travelling together from New Albany into Oxford removes the parking problem entirely on the weekends when parking is the whole problem."]),
 "holly-springs": dict(nav="Holly Springs", img="sprinter-exterior",
  title="Holly Springs MS Car Service &amp; Airport Transportation | The Brakefield Group",
  desc="Private car service in Holly Springs and Marshall County, Mississippi — Memphis airport transfers, gameday travel to Oxford and group transportation.",
  h1="Holly Springs",
  lede="Between Oxford and Memphis, and closer to the airport than most of our map.",
  facts=[("From Oxford","About 40 minutes"),("To MEM","Around 45 minutes"),("County","Marshall"),("Service","Airport, gameday, events")],
  body=["Holly Springs sits north of Oxford on the way to Memphis, which makes for a short and predictable airport transfer — usually around forty-five minutes to Memphis International.",
        "It is also a regular gameday pickup for families who keep a place in Marshall County and want a way into Oxford on a home Saturday.",
        "We cover Holly Springs for airport runs, gameday travel, and private group bookings across Marshall County."]),
 "starkville": dict(nav="Starkville", img="hero-sprinter",
  title="Starkville MS Car Service &amp; Group Transportation | The Brakefield Group",
  desc="Private group transportation between Oxford and Starkville, Mississippi, including Egg Bowl travel and Mississippi State game weekends.",
  h1="Starkville",
  lede="The other end of the rivalry, and a run we make most often in late November.",
  facts=[("From Oxford","Roughly 1 hr 45 min"),("Campus","Mississippi State"),("Peak","Egg Bowl weekend"),("Service","Game travel, charters")],
  body=["Starkville is a charter run more than a commuter one: a group heading across the state for a game, a graduation or a family weekend, wanting to travel together and not wanting anyone to drive back at night.",
        "Egg Bowl weekend is the obvious one. When the game is in Starkville, that trip books out well in advance — if you want it, ask early rather than in the week of.",
        "Because it is a longer run, Starkville trips are usually quoted as a day rate or a flat point-to-point rather than hourly. We will tell you which is cheaper for your plan."]),
}

# ------------------------------------------------------------------- builders
def form_block(r):
    return f'''<form id="quote">
      <div class="f2">
        <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
      <div class="f2">
        <div class="field"><label for="date">Date of trip</label><input id="date" name="date" type="date"></div>
        <div class="field"><label for="pax">Passengers</label><input id="pax" name="pax" type="number" min="1" max="60" inputmode="numeric"></div>
      </div>
      <div class="field"><label for="service">Service</label>
        <select id="service" name="service">
          <option>Ole Miss gameday</option><option>Airport transfer</option>
          <option>Corporate / executive</option><option>Celebration / night out</option>
          <option>Group charter</option><option>Student / parent travel</option>
          <option>Something else</option>
        </select></div>
      <div class="f2">
        <div class="field"><label for="from">Pickup</label><input id="from" name="from" type="text" placeholder="Address, hotel or airport"></div>
        <div class="field"><label for="to">Drop-off</label><input id="to" name="to" type="text" placeholder="Where you're headed"></div>
      </div>
      <div class="field"><label for="notes">Details</label><textarea id="notes" name="notes" placeholder="Times, stops, flight number, luggage, anything else we should know"></textarea></div>
      <button class="btn btn-primary" type="submit">Send request</button>
      <p class="formnote">This opens your email app with the details filled in. Prefer to talk? <a href="tel:{PHONE}" style="color:var(--chrome-2)">Call {PHONE_H}</a>.</p>
    </form>'''

def dial_block(r):
    return f'''<div class="dial">
      <a href="tel:{PHONE}">{I_PHONE}<span><b>{PHONE_H}</b><small>Call us</small></span></a>
      <a href="sms:{PHONE}">{I_SMS}<span><b>Text {PHONE_H}</b><small>Quickest for quick questions</small></span></a>
      <a href="mailto:{EMAIL}">{I_MAIL}<span><b>{EMAIL}</b><small>Email us</small></span></a>
    </div>'''

def service_cards(r, limit=None):
    out=[]
    for key,nav,url in (SERVICES[:limit] if limit else SERVICES):
        s=SERVICE[key]
        out.append(f'''<a class="card rv" href="{r}{url}"><h3 class="chrome">{s["h1"]}</h3>
          <p>{s["lede"]}</p><span class="more">See details</span></a>''')
    return '<div class="svc">%s</div>' % "".join(out)

def build_service(key):
    s=SERVICE[key]; r="../"; url="services/%s.html"%key
    ld={"@context":"https://schema.org","@type":"Service","serviceType":re.sub("<[^>]+>","",s["h1"]),
        "provider":{"@type":"LocalBusiness","name":"The Brakefield Group","telephone":"+1-662-715-4477"},
        "areaServed":{"@type":"AdministrativeArea","name":"North Mississippi"}}
    secs=""
    for h,items in s["body"]:
        if isinstance(items[0],str) and len(items)>1 and all(len(i)<170 for i in items):
            inner="<ul>%s</ul>"%"".join("<li>%s</li>"%i for i in items)
        else:
            inner="".join("<p>%s</p>"%i for i in items)
        secs+=f'<div class="rv"><h3 class="chrome">{h}</h3>{inner}</div>'
    extra = ('<section class="sec alt"><div class="wrap"><div class="sec-head rv">'
             '<p class="eyebrow">2026 home schedule · Vaught-Hemingway Stadium</p>'
             '<h2 class="chrome">Seven Saturdays in Oxford</h2></div>'+schedule(r)+'</div></section>') if key=="gameday" else ""
    return write(url, head(r,s["title"],s["desc"],url,ld)+header(r,"services")+f'''
{crumbs(r,[("Services","services/gameday.html"),(s["nav"],url)])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)">
  <div class="wrap">
    <p class="eyebrow">Service</p>
    <h1 class="chrome">{s["h1"]}</h1>
    <p class="lede">{s["lede"]}</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{r}reserve.html">Reserve a date</a>
      <a class="btn btn-ghost" href="tel:{PHONE}">{I_PHONE}{PHONE_H}</a>
    </div>
  </div>
  <div class="wrap"><div class="shot free rv">{pic(r,s["img"],re.sub("<[^>]+>","",s["h1"])+" — black Mercedes-Benz Sprinter",lazy=False)}</div></div>
</section>
<section class="sec"><div class="wrap"><div class="prose">{secs}</div></div></section>
{extra}
<section class="sec {'' if key=='gameday' else 'alt'}"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">Also available</p><h2 class="chrome">Other ways we run</h2></div>
  {service_cards(r)}
</div></section>
{cta_band(r)}
'''+footer(r))

def build_area(key):
    a=AREA[key]; r="../"; url="areas/%s.html"%key
    facts="".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k,v in a["facts"])
    body="".join("<p>%s</p>"%p for p in a["body"])
    ld={"@context":"https://schema.org","@type":"Service","serviceType":"Private car service",
        "provider":{"@type":"LocalBusiness","name":"The Brakefield Group","telephone":"+1-662-715-4477"},
        "areaServed":{"@type":"Place","name":re.sub("<[^>]+>","",a["h1"])}}
    return write(url, head(r,a["title"],a["desc"],url,ld)+header(r,"areas")+f'''
{crumbs(r,[("Service area","areas/memphis-airport.html"),(a["nav"],url)])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)">
  <div class="wrap">
    <p class="eyebrow">Service area</p>
    <h1 class="chrome">{a["h1"]}</h1>
    <p class="lede">{a["lede"]}</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{r}reserve.html">Reserve a date</a>
      <a class="btn btn-ghost" href="tel:{PHONE}">{I_PHONE}{PHONE_H}</a>
    </div>
  </div>
</section>
<section class="sec"><div class="wrap grid-2">
  <div class="rv"><div class="prose">{body}</div><dl class="spec">{facts}</dl></div>
  <div class="shot tall rv">{pic(r,a["img"],"Black Mercedes-Benz Sprinter serving "+re.sub("<[^>]+>","",a["h1"]))}</div>
</div></section>
<section class="sec alt"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">Nearby</p><h2 class="chrome">Everywhere else we run</h2></div>
  <div class="grid-4">{"".join(f'<a class="card rv" href="{r}{u}"><h3 class="chrome" style="font-size:20px">{n}</h3><span class="more">View</span></a>' for k,n,u in AREAS if k!=key)}</div>
</div></section>
{cta_band(r)}
'''+footer(r))

FAQS = [
 ("How far in advance should I book?",
  "As early as you can. Ole Miss home weekends, graduation and the holiday break move a lot of people on the same few days, and those go first. If it's last minute, call or text {p} anyway — we'll tell you straight away whether the date is open."),
 ("What will you arrive in?",
  "A black high-roof Mercedes-Benz Sprinter. High roof means you walk in rather than climb in, and there's room for the luggage and the coolers alongside the people."),
 ("Do you run to Memphis International?",
  "Yes — it's our most requested run, about 70 miles and roughly an hour and fifteen from Oxford. We also serve University-Oxford (UOX) and Tupelo Regional (TUP). Give us your flight number and we'll watch it."),
 ("How do you price a trip?",
  "Every trip is quoted individually on distance, duration and timing, so we don't post a number that would be wrong for most people. You'll have the full rate in writing before you commit, and it doesn't change on the day."),
 ("Can you handle multiple stops or wait time?",
  "Yes. Hourly and multi-stop bookings are common for gamedays and evenings out — your driver stays with the group for the window you've booked rather than being sent elsewhere between stops."),
 ("What areas do you serve?",
  "We're based in Oxford and regularly run Tupelo, Southaven and DeSoto County, Batesville, New Albany, Holly Springs and Starkville, plus Memphis and the wider Mid-South. Going further? Ask us."),
 ("Do you track flights?",
  "Yes, when you give us the flight number at booking. A delay becomes our problem to solve rather than something you explain at the curb."),
 ("Can I book on someone else's behalf?",
  "Often that's exactly what happens — a parent booking for a student, an assistant booking for an executive. You reserve it and approve the rate; we'll confirm with you and with whoever is actually riding."),
]

def build_home():
    r=""
    lede=("Chauffeured travel across North Mississippi in a black Mercedes-Benz Sprinter. Gameday, airport "
          "and private group transportation — arranged in advance, priced in advance, and driven by someone "
          "who does this for a living.")
    return write("index.html", head(r,"The Brakefield Group | Private Chauffeured Transportation — Oxford, MS",
      "Trusted transportation. Professional service. Private chauffeured travel across North Mississippi in a black Mercedes-Benz Sprinter. Gameday, airport, corporate and group transportation. Call or text 662.715.4477.",
      "")+header(r)+f'''
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Private car service · Oxford, Mississippi</p>
    <h1><span class="chrome">Trusted transportation.</span><span class="chrome" style="display:block">Professional service.</span></h1>
    <p class="lede">{lede}</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="{r}reserve.html">Reserve your date</a>
      <a class="btn btn-ghost" href="sms:{PHONE}">{I_SMS}Text us</a>
    </div>
    {TRUST}
  </div>
  <div class="wrap"><div class="shot free">{pic(r,"hero-sprinter","Black high-roof Mercedes-Benz Sprinter, front three-quarter view",lazy=False)}</div></div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">
  {"".join("<span>%s</span>"%t for t in ["Oxford","The Grove","Vaught-Hemingway","Memphis Intl (MEM)","University-Oxford (UOX)","Tupelo","Southaven","Batesville","New Albany","Holly Springs","Starkville","Tunica"]*2)}
</div></div>

<section class="sec"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">The service</p><h2 class="chrome">Chauffeured, end to end</h2>
  <p>One point of contact from the first message to the last drop-off. Nothing about the day is left to an app.</p></div>
  {service_cards(r)}
</div></section>

<section class="sec alt"><div class="wrap grid-2">
  <div class="rv">
    <p class="eyebrow">The fleet</p>
    <h2 class="chrome">Black Sprinters, kept immaculate</h2>
    <p style="margin-top:20px;color:var(--mute)">We run black Mercedes-Benz Sprinters — high roof, so you walk in rather than climb in, with leather seating and room for the luggage alongside the people.</p>
    <p style="margin-top:16px;color:var(--mute)">Every vehicle is detailed before it goes out. Your group travels together instead of splitting across separate cars that arrive ten minutes apart.</p>
    <dl class="spec">
      <div><dt>Vehicle</dt><dd>Mercedes-Benz Sprinter</dd></div>
      <div><dt>Configuration</dt><dd>High-roof executive</dd></div>
      <div><dt>Finish</dt><dd>Black, detailed before every trip</dd></div>
      <div><dt>Group size</dt><dd>Tell us your headcount — we'll confirm the fit</dd></div>
    </dl>
    <div class="cta-row"><a class="btn btn-ghost" href="{r}fleet.html">See the fleet</a></div>
  </div>
  <div class="shot tall rv">{pic(r,"interior-seats","Leather captain's chairs inside a Mercedes-Benz Sprinter")}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">2026 home schedule · Vaught-Hemingway Stadium</p>
  <h2 class="chrome">Seven Saturdays in Oxford</h2>
  <p>Home weekends are the first dates to go. Reserve the one you need and we'll confirm the details with you directly.</p></div>
  {schedule(r)}
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">How it works</p><h2 class="chrome">Booked in three steps</h2></div>
  <div class="steps">
    <div class="step rv"><h3 class="chrome">Tell us the trip</h3><p>Call, text, or send the reservation form with your date, headcount, pickup point and destination. Thirty seconds is enough to start.</p></div>
    <div class="step rv"><h3 class="chrome">Get your rate</h3><p>We come back with the timing and a flat rate in writing. No meter, no moving target, no renegotiating at the curb.</p></div>
    <div class="step rv"><h3 class="chrome">We handle the rest</h3><p>Your driver arrives early, tracks flights and traffic, and stays in contact with you from pickup to drop-off.</p></div>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">Service area</p><h2 class="chrome">Where we run</h2>
  <p>Based in Oxford, working across North Mississippi and the Mid-South.</p></div>
  <div class="grid-4">{"".join(f'<a class="card rv" href="{r}{u}"><h3 class="chrome" style="font-size:20px">{n}</h3><span class="more">View</span></a>' for k,n,u in AREAS)}</div>
</div></section>

<section class="sec alt"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">The standard</p><h2 class="chrome">Why people book us twice</h2>
  <p>We're a North Mississippi company, and most of our work comes from someone who rode once and passed the number along.</p></div>
  <div class="grid-4">
    <div class="why-item rv"><div class="mk"></div><h3 class="chrome">A professional at the wheel</h3><p>Vetted, licensed and presentable. Knowing Oxford on a game weekend matters more than any map app does.</p></div>
    <div class="why-item rv"><div class="mk"></div><h3 class="chrome">Immaculate, every time</h3><p>Detailed before it goes out, with the whole group riding together rather than scattered across separate cars.</p></div>
    <div class="why-item rv"><div class="mk"></div><h3 class="chrome">One rate, agreed up front</h3><p>You approve the price before the trip. It doesn't move because it's raining or because kickoff just ended.</p></div>
    <div class="why-item rv"><div class="mk"></div><h3 class="chrome">A real person answers</h3><p>Call or text {PHONE_H} and you reach us — not a queue, an app, or a call center three states away.</p></div>
  </div>
</div></section>
{cta_band(r)}
'''+footer(r))

def build_fleet():
    r=""
    return write("fleet.html", head(r,"The Fleet — Mercedes-Benz Sprinter | The Brakefield Group",
      "Black high-roof Mercedes-Benz Sprinters with leather seating, detailed before every trip. The fleet behind The Brakefield Group.","fleet.html")
      +header(r,"fleet")+f'''
{crumbs(r,[("The fleet","fleet.html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">The fleet</p>
  <h1 class="chrome">Black Sprinters, kept immaculate</h1>
  <p class="lede">High-roof Mercedes-Benz Sprinters with leather seating — the group and the luggage travelling together, in something you're happy to be seen arriving in.</p>
  <div class="cta-row"><a class="btn btn-primary" href="{r}reserve.html">Reserve a date</a>
  <a class="btn btn-ghost" href="tel:{PHONE}">{I_PHONE}{PHONE_H}</a></div>
</div>
<div class="wrap"><div class="shot free">{pic(r,"hero-sprinter","Black high-roof Mercedes-Benz Sprinter",lazy=False)}</div></div>
</section>
<section class="sec"><div class="wrap grid-2">
  <div class="rv"><h2 class="chrome">Why a Sprinter</h2>
    <div class="prose" style="margin-top:20px">
      <p>A high-roof Sprinter is the vehicle that actually solves the problem most groups have: everyone, plus everything they brought, in one vehicle, arriving at the same time.</p>
      <p>You walk in standing up rather than folding yourself into a back seat. Luggage rides with you rather than being negotiated into a trunk. And a party of eight is one booking rather than three cars and a group text trying to work out who got where.</p>
      <p>It is also, quietly, the reason the day runs on time. One vehicle leaving one address beats three vehicles leaving three addresses, every single time.</p>
    </div>
    <dl class="spec">
      <div><dt>Vehicle</dt><dd>Mercedes-Benz Sprinter</dd></div>
      <div><dt>Configuration</dt><dd>High-roof executive</dd></div>
      <div><dt>Seating</dt><dd>Leather, forward-facing</dd></div>
      <div><dt>Finish</dt><dd>Black, detailed before every trip</dd></div>
      <div><dt>Luggage</dt><dd>Travels with the passengers</dd></div>
      <div><dt>Group size</dt><dd>Tell us your headcount — we'll confirm the fit</dd></div>
    </dl>
  </div>
  <div class="shot tall rv">{pic(r,"interior-seats","Leather captain's chairs inside the Sprinter")}</div>
</div></section>
<section class="sec alt"><div class="wrap grid-2">
  <div class="shot rv">{pic(r,"interior-door","Sprinter side door open, showing the cabin and step")}</div>
  <div class="rv"><h2 class="chrome">Arriving well</h2>
    <div class="prose" style="margin-top:20px">
      <p>The door opens, the step lights, and your group steps out at the front of the venue rather than at the far end of a parking lot.</p>
      <p>It is a small thing that turns out to matter on the nights that matter — a milestone birthday, a rehearsal dinner, a client you are trying to impress, or a grandmother who should not be walking six blocks in the rain.</p>
    </div>
    <div class="cta-row"><a class="btn btn-primary" href="{r}reserve.html">Reserve a date</a></div>
  </div>
</div></section>
<section class="sec"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">Put it to work</p><h2 class="chrome">What we run it for</h2></div>
  {service_cards(r)}
</div></section>
{cta_band(r)}
'''+footer(r))

def build_about():
    r=""
    return write("about.html", head(r,"About The Brakefield Group | Oxford, MS Car Service",
      "The Brakefield Group is a locally owned private transportation company based in Oxford, Mississippi, serving North Mississippi and the Mid-South.","about.html")
      +header(r,"about")+f'''
{crumbs(r,[("About","about.html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">About us</p>
  <h1 class="chrome">Trusted service.<span style="display:block">Professional results.</span></h1>
  <p class="lede">A locally owned transportation company based in Oxford, Mississippi, built around doing the ordinary things properly.</p>
</div></section>
<section class="sec"><div class="wrap grid-2">
  <div class="prose rv">
    <p>The Brakefield Group is a private transportation company in Oxford, Mississippi. We run black Mercedes-Benz Sprinters across North Mississippi and the Mid-South — airports, gamedays, corporate travel and the evenings people plan for months.</p>
    <h3 class="chrome">What we're actually selling</h3>
    <p>Not a car. Anyone can get a car. What we sell is the part where you stop thinking about it: the driver is early, the vehicle is clean, the flight is being watched, the price was agreed a week ago, and nobody in your group has to volunteer to stay sober and drive.</p>
    <h3 class="chrome">Local, on purpose</h3>
    <p>We live here. We know which streets close on a home Saturday, which venue entrance is blocked at six, and how long the drive to Memphis really takes when it's raining and it's a Friday. That knowledge is not available from an app, and it is most of the job.</p>
    <h3 class="chrome">How we grow</h3>
    <p>Almost entirely by referral. Someone rides once, it goes the way it was supposed to, and they pass the number along. That is a slow way to build a business and the only one that produces the kind we want.</p>
  </div>
  <div class="shot tall rv">{pic(r,"sprinter-exterior","Black Mercedes-Benz Sprinter")}</div>
</div></section>
<section class="sec alt"><div class="wrap">
  <div class="sec-head rv"><p class="eyebrow">Reach us</p><h2 class="chrome">Talk to a person</h2>
  <p>Call or text {PHONE_H}. It reaches us, not a queue.</p></div>
  {dial_block(r)}
</div></section>
{cta_band(r)}
'''+footer(r))

def build_faq():
    r=""
    items="".join(f"<details><summary>{q}</summary><p>{a.format(p=PHONE_H)}</p></details>" for q,a in FAQS)
    ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a.format(p=PHONE_H))}} for q,a in FAQS]}
    return write("faq.html", head(r,"FAQ | The Brakefield Group",
      "Common questions about booking private transportation with The Brakefield Group — lead times, pricing, airports, group sizes and service area.","faq.html",ld)
      +header(r,"faq")+f'''
{crumbs(r,[("FAQ","faq.html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">Questions</p><h1 class="chrome">Before you book</h1>
  <p class="lede">The things people ask most. If yours isn't here, call or text {PHONE_H} and ask.</p>
</div></section>
<section class="sec"><div class="wrap"><div class="faq rv">{items}</div></div></section>
{cta_band(r)}
'''+footer(r))

def build_reserve():
    r=""
    return write("reserve.html", head(r,"Reserve a Date | The Brakefield Group",
      "Reserve private chauffeured transportation in North Mississippi. Send your date, headcount and route and we'll come back with a flat rate in writing.","reserve.html")
      +header(r,"reserve")+f'''
{crumbs(r,[("Reserve","reserve.html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">Reservations</p><h1 class="chrome">Let's get it on the calendar</h1>
  <p class="lede">The fastest way to reach us is a call or a text. Send the date, the headcount and where you're headed, and we'll come straight back with a rate.</p>
</div></section>
<section class="sec"><div class="wrap contact-grid">
  <div class="rv">
    <h2 class="chrome" style="font-size:clamp(24px,3.2vw,34px)">Straight to us</h2>
    {dial_block(r)}
    <div class="prose" style="margin-top:34px">
      <h3 class="chrome">What to include</h3>
      <ul>
        <li>Date, and the times you need to be somewhere</li>
        <li>How many people are travelling</li>
        <li>Pickup address and where you're going</li>
        <li>Flight number, if it's an airport run</li>
        <li>Any stops along the way</li>
      </ul>
    </div>
  </div>
  {form_block(r)}
</div></section>
{cta_band(r,"Prefer to talk it through?","Some trips are easier to explain than to type. Call and we'll work it out with you.")}
'''+footer(r))

def build_contact():
    r=""
    return write("contact.html", head(r,"Contact | The Brakefield Group",
      "Call or text 662.715.4477, or email booking@brakefieldtrans.com. Private transportation based in Oxford, Mississippi.","contact.html")
      +header(r)+f'''
{crumbs(r,[("Contact","contact.html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">Contact</p><h1 class="chrome">Talk to a person</h1>
  <p class="lede">Call or text {PHONE_H}. It reaches us directly — not a queue, an app, or a call center three states away.</p>
</div></section>
<section class="sec"><div class="wrap grid-2">
  <div class="rv">{dial_block(r)}</div>
  <div class="rv"><div class="prose">
    <h3 class="chrome">Where we are</h3>
    <p>Based in Oxford, Mississippi. We work across North Mississippi and the Mid-South — Memphis, Tupelo, DeSoto County, Batesville, New Albany, Holly Springs and Starkville among them.</p>
    <h3 class="chrome">When to reach us</h3>
    <p>Bookings are by reservation rather than on demand, so the earlier you call the better we can help. For same-day questions, text is quickest.</p>
    <h3 class="chrome">Follow along</h3>
    <p>We post the current schedule and recent trips on <a href="https://www.instagram.com/thebrakegroup/" target="_blank" rel="noopener" style="color:var(--chrome-2)">Instagram</a>.</p>
  </div></div>
</div></section>
{cta_band(r)}
'''+footer(r))

def build_legal(slug, title, blocks):
    r=""
    body="".join(f'<h3 class="chrome">{h}</h3>'+"".join(f"<p>{p}</p>" for p in ps) for h,ps in blocks)
    return write(slug+".html", head(r,f"{title} | The Brakefield Group",
      f"{title} for The Brakefield Group.",slug+".html")+header(r)+f'''
{crumbs(r,[(title,slug+".html")])}
<section class="hero" style="padding-top:clamp(30px,4vw,54px)"><div class="wrap">
  <p class="eyebrow">Legal</p><h1 class="chrome">{title}</h1></div></section>
<section class="sec"><div class="wrap"><div class="prose">{body}</div></div></section>
'''+footer(r))

PRIVACY = [
 ("What this site collects",
  ["This website does not use analytics, advertising trackers or cookies. Nothing you do on these pages is recorded by us.",
   "The reservation form does not submit data to a server. It opens your own email application with the details filled in, so nothing is sent until you press send in your own mail app, and it arrives as an ordinary email."]),
 ("What we do with what you send",
  ["When you call, text or email us, we keep what we need to arrange and carry out your trip — your name, contact details, and the details of the journey.",
   "We do not sell your information, and we do not share it with anyone except where it is necessary to carry out your booking or where the law requires it."]),
 ("Fonts and hosting",
  ["Typefaces on this site are served by Google Fonts, which means your browser makes a request to Google to fetch them. That request is subject to Google's own privacy policy."]),
 ("Getting in touch",
  ["To ask what we hold about you, or to have it deleted, email booking@brakefieldtrans.com or call 662.715.4477."]),
]
TERMS = [
 ("Quotes and bookings",
  ["Rates are quoted individually for each trip based on distance, duration and timing. A quote is confirmed in writing before your trip, and the confirmed rate is the rate you pay.",
   "A booking is reserved once we have confirmed it to you directly. A request submitted through this website is a request, not a confirmed reservation, until we come back to you."]),
 ("Changes, cancellations and payment",
  ["Cancellation, change and payment terms are set out in your written confirmation for the specific booking. If anything there is unclear, ask us before you confirm."]),
 ("Our responsibilities",
  ["We will arrive at the agreed time and carry out the journey as described. Where circumstances outside our control — weather, road closures, mechanical failure — affect a trip, we will tell you as early as we can and work out the best available alternative with you."]),
 ("Conduct",
  ["We ask that passengers travel safely and treat the vehicle and the driver with respect. We reserve the right to end a journey where behaviour puts the safety of passengers, the driver or the public at risk."]),
 ("Independence",
  ["The Brakefield Group is an independent transportation company. We are not affiliated with, endorsed by, or sponsored by the University of Mississippi, any athletics conference, or any airport, airline or venue named on this site. Those names are used only to describe where we travel."]),
 ("Governing law",
  ["These terms are governed by the laws of the State of Mississippi."]),
]

def build_sitemap(pages):
    urls="".join(f"<url><loc>{DOMAIN}/{p}</loc></url>" for p in pages)
    write("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    write("robots.txt", ("User-agent: *\nDisallow: /\n" if NOINDEX
        else f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"))

def main():
    os.makedirs(os.path.join(ROOT,"assets"), exist_ok=True)
    write("assets/site.css", CSS)
    write("assets/site.js", JS)
    pages=[build_home(), build_fleet(), build_about(), build_faq(),
           build_reserve(), build_contact(),
           build_legal("privacy","Privacy Policy",PRIVACY),
           build_legal("terms","Terms of Service",TERMS)]
    pages += [build_service(k) for k in SERVICE]
    pages += [build_area(k)    for k in AREA]
    build_sitemap(pages)
    print("built %d pages" % len(pages))
    for p in sorted(pages): print("  ", p)
    print("robots: %s" % ("NOINDEX (preview)" if NOINDEX else "indexable"))

if __name__ == "__main__":
    main()
