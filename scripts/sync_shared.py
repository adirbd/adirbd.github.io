#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_URL = 'https://www.adirbd.com'


def e(value: object) -> str:
    """HTML-escape a value for safe interpolation into element text or a
    double-quoted attribute (escapes & < > " '). Use for every dynamic,
    user-facing string; do NOT use inside JSON-LD (json.dumps escapes that)."""
    return html.escape(str(value), quote=True)


def _asset_ver(name: str) -> str:
    """Short content hash so browsers refetch index.css/js after any change
    (cache-busting). Changes to those files re-version every page on sync."""
    path = REPO / name
    return hashlib.md5(path.read_bytes()).hexdigest()[:8] if path.exists() else '1'


CSS_VER = _asset_ver('index.css')
JS_VER = _asset_ver('index.js')
# Stable "last meaningfully updated" marker for the sitemap. Bump by hand
# when the site changes substantively. Deliberately NOT derived from git
# commit dates: the sitemap is committed in the same commit whose date it
# would record, so a derived value can never match what CI regenerates
# across a midnight boundary (it drifts and fails the sync check).
LASTMOD = '2026-06-17'
# Applied before first paint so dark-mode visitors never flash light.
THEME_BOOT_SCRIPT = (
    "<script>(function(){try{var t=localStorage.getItem('adirbd-theme');"
    "if(t!=='light'&&t!=='dark'){t=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}"
    "document.documentElement.dataset.theme=t;}catch(e){}})();</script>"
)


def absolute_url(href: str) -> str:
    return href if href.startswith('http') else f'{SITE_URL}{href}'


PERSON_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': f'{SITE_URL}/#person',
    'name': 'Adir Ben David',
    'alternateName': ['Adirbd', 'אדיר בן דוד'],
    'jobTitle': 'DevOps Engineer',
    'description': (
        'Adir Ben David is a DevOps engineer at Check Point Software Technologies in Tel Aviv, working on the '
        'cloud side, building and managing infrastructure on AWS and Azure with Terraform, Terragrunt, and '
        'Crossplane, running Kubernetes across staging, production, and new regions, and building out observability '
        'with Grafana, VictoriaMetrics, and OpenTelemetry. He works on FedRAMP-compliant infrastructure and CI/CD, '
        'and co-led a migration of 1,000+ users to GitHub Enterprise. He joined Check Point in December 2019; '
        'before DevOps he led a six-person team that built and operated complex on-prem environments (servers, '
        'networking, firewalls, and ESXi virtualization) from 2021 to 2024. Earlier he was a Tier-2 networking '
        'engineer at Bezeq (2017-2019) working with multi-vendor Layer 2/3 networks, routers, and switches, and a '
        'communications network technician in the Communications and Computers Corps (Tikshuv) during military '
        'service (2014-2017). Having worked both on-prem data centers and the cloud shapes how he approaches systems.'
    ),
    'worksFor': {'@type': 'Organization', 'name': 'Check Point Software Technologies', 'url': 'https://www.checkpoint.com/'},
    'hasOccupation': {
        '@type': 'Occupation',
        'name': 'DevOps Engineer',
        'occupationLocation': {'@type': 'City', 'name': 'Tel Aviv'},
        'skills': 'DevOps, AWS, Azure, Kubernetes, Terraform, Terragrunt, Crossplane, Helm, Docker, CI/CD, '
                  'GitHub Actions, GitHub Enterprise, Infrastructure as Code, Linux, Bash, Python, observability, '
                  'Grafana, OpenTelemetry, FedRAMP compliance, on-prem infrastructure, systems integration, '
                  'virtualization (ESXi), firewalls, networking (Layer 2/3)',
    },
    'alumniOf': [
        {'@type': 'Organization', 'name': 'Bezeq'},
        {'@type': 'Organization', 'name': 'Communications and Computers Corps (Tikshuv)'},
    ],
    'hasCredential': [
        {'@type': 'EducationalOccupationalCredential', 'name': 'Check Point Certified Security Expert (CCSE)',
         'credentialCategory': 'certificate', 'recognizedBy': {'@type': 'Organization', 'name': 'Check Point Software Technologies'}},
        {'@type': 'EducationalOccupationalCredential', 'name': 'Check Point Certified Security Administrator (CCSA)',
         'credentialCategory': 'certificate', 'recognizedBy': {'@type': 'Organization', 'name': 'Check Point Software Technologies'}},
        {'@type': 'EducationalOccupationalCredential', 'name': 'Cisco Certified Network Professional (CCNP) Routing and Switching',
         'credentialCategory': 'certificate', 'recognizedBy': {'@type': 'Organization', 'name': 'Cisco'}},
        {'@type': 'EducationalOccupationalCredential', 'name': 'Cisco Certified Network Associate (CCNA) Routing and Switching',
         'credentialCategory': 'certificate', 'recognizedBy': {'@type': 'Organization', 'name': 'Cisco'}},
        {'@type': 'EducationalOccupationalCredential', 'name': 'Cisco Certified Entry Networking Technician (CCENT)',
         'credentialCategory': 'certificate', 'recognizedBy': {'@type': 'Organization', 'name': 'Cisco'}},
    ],
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Tel Aviv'},
    'url': f'{SITE_URL}/',
    'sameAs': [
        'https://github.com/adirbd',
        'https://www.linkedin.com/in/adirbd/',
        'https://www.instagram.com/adirbd/',
        'https://www.facebook.com/adirbd/',
        'https://www.youtube.com/@adirbd',
        'https://x.com/adirbd',
        'https://en.wikipedia.org/wiki/User:Adirbd',
    ],
    'knowsAbout': [
        'DevOps', 'Infrastructure', 'Cloud', 'AWS', 'Azure', 'On-premises infrastructure',
        'Systems integration', 'Virtualization', 'Firewalls', 'Automation', 'CI/CD', 'GitHub Actions',
        'Infrastructure as Code', 'Kubernetes', 'Terraform', 'Terragrunt', 'Crossplane', 'Helm', 'Docker',
        'GitHub Enterprise', 'Linux', 'Bash', 'Python', 'Observability', 'Grafana', 'OpenTelemetry',
        'FedRAMP compliance', 'Networking', 'Systems', 'Transportation', 'Urban systems',
    ],
}

# Nav order is the site's story arc: work (credibility) -> now (momentum)
# -> journeys (personality) -> links (presence) -> contact (the close).
# The "about" page was merged into the home page (the brand link).
EN_NAV = [
    ('/', 'Home'),
    ('work.html', 'Work'),
    ('now.html', 'Now'),
    ('journeys.html', 'Journeys'),
    ('connect.html', 'Connect'),
]
# Same reading order as EN_NAV; dir="rtl" already mirrors the visual layout.
HE_NAV = [
    ('/he/', 'בית'),
    ('/he/work.html', 'עבודה'),
    ('/he/now.html', 'עכשיו'),
    ('/he/journeys.html', 'מסעות'),
    ('/he/connect.html', 'בואו נדבר'),
]
SOCIALS = [
    ('https://www.linkedin.com/in/adirbd/', 'LinkedIn', '/images/linkedin.svg', 'LinkedIn'),
    ('https://www.instagram.com/adirbd/', 'Instagram', '/images/instagram.svg', 'Instagram'),
    ('https://www.facebook.com/adirbd/', 'Facebook', '/images/facebook.svg', 'Facebook'),
    ('https://x.com/adirbd', 'X', '/images/twitter.svg', 'X'),
    ('https://www.youtube.com/@adirbd', 'YouTube', '/images/youtube.svg', 'YouTube'),
    ('https://github.com/adirbd', 'GitHub', '/images/github.svg', 'GitHub'),
    ('https://en.wikipedia.org/wiki/User:Adirbd', 'Wikipedia', '/images/wikipedia.svg', 'Wikipedia'),
]
PAGES = {
    'index.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': '/', 'page_type': 'ProfilePage', 'switch': '/he/', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Adir Ben David - Work, projects, and contact',
        'description': 'A place to explore my work, projects, useful links, and easy ways to get in touch.',
        'slug': '', 'en_href': f'{SITE_URL}/', 'he_href': '/he/', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'work.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'work.html', 'switch': '/he/work.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Work | Adir Ben David',
        'description': 'Professional experience, working style, and systems-minded infrastructure work by Adir Ben David.',
        'slug': 'work.html', 'en_href': f'{SITE_URL}/work.html', 'he_href': '/he/work.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'now.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'now.html', 'switch': '/he/now.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Now | Adir Ben David',
        'description': 'What Adir Ben David is currently building and into: AI projects, a self-hosted home server, and a Home Assistant smart home, plus a long-standing interest in transit and cities.',
        'slug': 'now.html', 'en_href': f'{SITE_URL}/now.html', 'he_href': '/he/now.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'journeys.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'journeys.html', 'switch': '/he/journeys.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Journeys | Adir Ben David',
        'description': 'Places, movement, and selected photos from trips by Adir Ben David: Japan, the Alps, Thailand, and more.',
        'slug': 'journeys.html', 'en_href': f'{SITE_URL}/journeys.html', 'he_href': '/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'connect.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'connect.html', 'switch': '/he/connect.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Connect | Adir Ben David',
        'description': 'Reach Adir Ben David on LinkedIn, Instagram, Facebook, X, YouTube, GitHub, Wikipedia, or by email, for collaboration, ideas, or a thoughtful hello.',
        'slug': 'connect.html', 'en_href': f'{SITE_URL}/connect.html', 'he_href': '/he/connect.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'he/index.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/', 'page_type': 'ProfilePage', 'switch': '/', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'אדיר בן דוד - עבודה, פרויקטים ויצירת קשר',
        'description': 'מקום להכיר את העבודה, הפרויקטים והדרך שלי, למצוא קישורים שימושיים וליצור קשר בקלות.',
        'slug': 'he/', 'en_href': '/', 'he_href': f'{SITE_URL}/he/', 'x_default': '/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/work.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/work.html', 'switch': '/work.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'עבודה | אדיר בן דוד',
        'description': 'ניסיון מקצועי, סגנון עבודה וחשיבה מערכתית של אדיר בן דוד.',
        'slug': 'he/work.html', 'en_href': '/work.html', 'he_href': f'{SITE_URL}/he/work.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/now.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/now.html', 'switch': '/now.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'עכשיו | אדיר בן דוד',
        'description': 'במה אדיר בן דוד עוסק עכשיו: פרויקטים עם AI, שרת ביתי עצמאי ובית חכם מבוסס Home Assistant, לצד עניין מתמשך בתחבורה ובערים.',
        'slug': 'he/now.html', 'en_href': '/now.html', 'he_href': f'{SITE_URL}/he/now.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/journeys.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/journeys.html', 'switch': '/journeys.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'מסעות | אדיר בן דוד',
        'description': 'מקומות, תנועה ותמונות נבחרות מהטיולים של אדיר בן דוד: יפן, האלפים, תאילנד ועוד.',
        'slug': 'he/journeys.html', 'en_href': '/journeys.html', 'he_href': f'{SITE_URL}/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/connect.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/connect.html', 'switch': '/connect.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'בואו נדבר | אדיר בן דוד',
        'description': 'איך ליצור קשר עם אדיר בן דוד: ב־LinkedIn, Instagram, Facebook, X, YouTube, GitHub, ויקיפדיה או באימייל, לשיתופי פעולה, רעיונות או סתם שלום.',
        'slug': 'he/connect.html', 'en_href': '/connect.html', 'he_href': f'{SITE_URL}/he/connect.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
}


def json_script(data: dict) -> str:
    # Escape the characters that could otherwise break out of the surrounding
    # <script type="application/ld+json"> element (e.g. a literal "</script>"
    # in a value). The \uXXXX forms are valid JSON and parse identically.
    return (json.dumps(data, ensure_ascii=False, indent=6)
            .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))


def render_nav(items: list[tuple[str, str]], active: str) -> str:
    rendered = []
    for href, label in items:
        current = ' aria-current="page"' if href == active else ''
        rendered.append(f'<li><a href="{href}"{current}>{e(label)}</a></li>')
    return ''.join(rendered)


def render_head(meta: dict[str, str]) -> str:
    # Relative depth to the site root: one '../' per directory in the slug.
    # '' -> './', 'work.html' -> './', 'he/work.html' -> '../',
    # 'trips/japan.html' -> '../', 'he/trips/japan.html' -> '../../'.
    prefix = '../' * meta['slug'].count('/') or './'
    canonical = f'{SITE_URL}/{meta["slug"]}' if meta['slug'] else f'{SITE_URL}/'
    og_image = absolute_url(meta.get('og_image', '/images/og-image.png'))
    og_image_alt = meta.get('og_image_alt', 'Adir Ben David')
    # Default share image (og-image.png) is 1200x630; album pages override with
    # their cover, whose real dimensions come through the meta dict.
    og_image_w = meta.get('og_image_w', 1200)
    og_image_h = meta.get('og_image_h', 630)
    og_image_type = 'image/png' if og_image.lower().endswith('.png') else 'image/jpeg'
    webpage_schema = {
        '@context': 'https://schema.org',
        '@type': meta.get('page_type', 'WebPage'),
        'url': canonical,
        'name': meta['title'],
        'inLanguage': meta['lang'],
        'description': meta['description'],
        'isPartOf': {'@type': 'WebSite', 'url': f'{SITE_URL}/', 'name': 'Adir Ben David'},
        'about': {'@id': f'{SITE_URL}/#person'},
    }
    if webpage_schema['@type'] == 'ProfilePage':
        webpage_schema['mainEntity'] = {'@id': f'{SITE_URL}/#person'}
    if meta.get('og_image'):
        webpage_schema['primaryImageOfPage'] = {'@type': 'ImageObject', 'url': og_image}
    return f'''<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(meta['title'])}</title>
  <meta name="description" content="{e(meta['description'])}" />
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#f6f8fc" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#0d1320" media="(prefers-color-scheme: dark)" />
  <link rel="alternate" hreflang="en" href="{absolute_url(meta['en_href'])}" />
  <link rel="alternate" hreflang="en-US" href="{absolute_url(meta['en_href'])}" />
  <link rel="alternate" hreflang="he" href="{absolute_url(meta['he_href'])}" />
  <link rel="alternate" hreflang="he-IL" href="{absolute_url(meta['he_href'])}" />
  <link rel="alternate" hreflang="x-default" href="{absolute_url(meta['x_default'])}" />
  <link rel="icon" type="image/svg+xml" href="{prefix}images/favicon-transit.svg" />
  <link rel="alternate icon" type="image/png" href="{prefix}images/favicon.png" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="Adir Ben David" />
  <meta property="og:locale" content="{meta['locale']}" />
  <meta property="og:locale:alternate" content="{meta['locale_alt']}" />
  <meta property="og:title" content="{e(meta['title'])}" />
  <meta property="og:description" content="{e(meta['description'])}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:image:alt" content="{e(og_image_alt)}" />
  <meta property="og:image:width" content="{og_image_w}" />
  <meta property="og:image:height" content="{og_image_h}" />
  <meta property="og:image:type" content="{og_image_type}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@adirbd" />
  <meta name="twitter:creator" content="@adirbd" />
  <meta name="twitter:title" content="{e(meta['title'])}" />
  <meta name="twitter:description" content="{e(meta['description'])}" />
  <meta name="twitter:image" content="{og_image}" />
  <meta name="twitter:image:alt" content="{e(og_image_alt)}" />
  <script type="application/ld+json">{json_script(PERSON_SCHEMA)}</script>
  <script type="application/ld+json">{json_script(webpage_schema)}</script>
  {THEME_BOOT_SCRIPT}
  <link rel="preload" href="{prefix}fonts/HKGrotesk-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}fonts/Jost-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{prefix}index.css?v={CSS_VER}" />
</head>'''


def render_header(meta: dict[str, str]) -> str:
    is_he = meta['lang'] == 'he'
    nav_items = HE_NAV if is_he else EN_NAV
    # Pages below the site root (e.g. /trips/japan.html) can't use the EN nav's
    # page-relative hrefs ('work.html' would resolve to /trips/work.html), so
    # absolutise them. HE nav hrefs are already root-relative.
    if meta.get('abs_nav') and not is_he:
        nav_items = [(h if h.startswith('/') else f'/{h}', label) for h, label in nav_items]
    nav = render_nav(nav_items, meta['active'])
    nav_label = 'ראשי' if is_he else 'Primary'
    nav_toggle_label = 'פתח ניווט' if is_he else 'Open navigation'
    theme_label = 'מעבר למצב בהיר או כהה' if is_he else 'Toggle theme'
    theme_text = 'כהה' if is_he else 'Dark'
    switch_lang = 'en' if is_he else 'he'
    # Show just the language code you'll switch TO (EN page -> HE, HE page -> EN).
    switch_name = meta['switch_to']
    switch_aria = 'מעבר לאנגלית' if is_he else 'Switch to Hebrew'
    skip_text = 'דלג לתוכן' if is_he else 'Skip to content'
    return f'''<header class="site-header">
  <a class="skip-link" href="#main">{skip_text}</a>
  <div class="site-shell header-inner">
    <a class="brand" href="{meta['home']}">
      <span class="brand-mark" aria-hidden="true"></span>
      <span>Adir Ben David</span>
    </a>
    <button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-label="{nav_toggle_label}">
      ☰
    </button>
    <div class="nav-area">
      <nav class="site-nav" aria-label="{nav_label}">
        <ul>
          {nav}
        </ul>
      </nav>
      <div class="header-tools">
        <a class="lang-switch" href="{meta['switch']}" hreflang="{switch_lang}" lang="{switch_lang}" aria-label="{switch_aria}">{switch_name}</a>
        <button class="toggle" type="button" data-theme-toggle aria-label="{theme_label}"><span>◐</span><span data-theme-label>{theme_text}</span></button>
      </div>
    </div>
  </div>
</header>'''


def render_footer(lang: str) -> str:
    is_he = lang == 'he'
    line = ('תל אביב · © <span data-year>2026</span> אדיר בן דוד' if is_he
            else 'Tel Aviv · © <span data-year>2026</span> Adir Ben David')
    # Footer mirrors the full primary nav (absolute hrefs so it resolves from
    # subdirectory pages like /trips/ too).
    nav_items = HE_NAV if is_he else EN_NAV
    footer_nav = ''.join(
        f'<a href="{h if h.startswith("/") else f"/{h}"}">{e(label)}</a>'
        for h, label in nav_items
    )
    socials = ''.join(
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" aria-label="{e(aria)}"><img src="{icon}" alt="{e(alt)}"></a>'
        for href, aria, icon, alt in SOCIALS
    )
    return f'''<footer class="site-footer">
  <div class="site-shell footer-inner">
    <div>
      <strong>Adir Ben David</strong>
      <div class="muted">{line}</div>
    </div>
    <nav class="footer-nav">{footer_nav}</nav>
    <div class="socials">{socials}</div>
  </div>
</footer>'''


# Trip albums are fully generated (like the sitemap) from this data model:
# add a trip here + its photos under images/journeys/, run this script, and the
# Journeys index preview card and the /trips/<slug>.html album are produced for
# both languages. Section types: 'story' (narrative text), 'photo', 'clip'.
IMG = '/images/journeys'
TRIPS = [
    {
        'slug': 'japan', 'dates': '2026', 'featured': True,
        'state_en': 'Completed', 'state_he': 'הסתיים',
        'kicker_en': 'Completed journey', 'kicker_he': 'מסע שהושלם',
        'title_en': 'Japan', 'title_he': 'יפן',
        'meta_en': 'Osaka · Nara · Kyoto · Tokyo · Fuji', 'meta_he': 'אוסקה · נארה · קיוטו · טוקיו · פוג\'י',
        'tags_en': ['Rail', 'City', 'Fuji', 'Rome'], 'tags_he': ['רכבות', 'עיר', 'פוג\'י', 'רומא'],
        'teaser_en': 'A long rail loop through Osaka, Nara, Kyoto and Tokyo, out to the lakes under Mount Fuji, then a Rome finale before the flight home.',
        'teaser_he': 'מסע ארוך ברכבות דרך אוסקה, נארה, קיוטו וטוקיו, ומשם לאגמים שמתחת להר פוג\'י, וסיום ברומא לפני הטיסה הביתה.',
        'cover': 'japan-fuji-blossoms.jpg', 'cover_w': 768, 'cover_h': 1024,
        'cover_alt_en': 'Mount Fuji rising above cherry blossoms',
        'cover_alt_he': 'הר פוג\'י מעל פריחת הדובדבן',
        'intro_en': 'Japan was a long loop by rail: Osaka, Nara, Kyoto, Tokyo, and the lakes under Mount Fuji. It ended, unexpectedly, with a layover in Rome on the way home.',
        'intro_he': 'יפן היה מסע ארוך ברכבות: אוסקה, נארה, קיוטו, טוקיו, והאגמים שמתחת להר פוג\'י. הוא הסתיים, באופן לא צפוי, בעצירת ביניים ברומא בדרך הביתה.',
        # Photos run in travel order: Kyoto -> Tokyo -> Fuji -> Rome. Osaka and
        # Nara photos will be added at the front when they arrive.
        'sections': [
            {'type': 'story', 'en': 'After Osaka and Nara, Kyoto slowed things down: the bamboo paths of Arashiyama, a good bowl of ramen, and a detour to the Nintendo Museum just outside the city.',
             'he': 'אחרי אוסקה ונארה, קיוטו האטה את הקצב: שבילי הבמבוק של אראשיאמה, קערת ראמן טובה, וקפיצה למוזיאון נינטנדו ממש מחוץ לעיר.'},
            {'type': 'photo', 'src': 'bamboo-grove.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir walking through a towering bamboo grove', 'alt_he': 'אדיר הולך בשביל בתוך יער במבוק',
             'cap_en': 'Walking through the bamboo at Arashiyama.', 'cap_he': 'הליכה בין הבמבוק באראשיאמה.'},
            {'type': 'photo', 'src': 'japan-bamboo-path.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The bamboo grove path at Arashiyama', 'alt_he': 'שביל יער הבמבוק באראשיאמה',
             'cap_en': 'The Arashiyama bamboo path, busy as ever.', 'cap_he': 'שביל הבמבוק באראשיאמה, שוקק כתמיד.'},
            {'type': 'photo', 'src': 'japan-ramen.jpg', 'w': 1024, 'h': 768,
             'alt_en': 'A bowl of ramen with gyoza on the side', 'alt_he': 'קערת ראמן עם גיוזה בצד',
             'cap_en': 'Ramen and gyoza in Kyoto.', 'cap_he': 'ראמן וגיוזה בקיוטו.'},
            {'type': 'photo', 'src': 'japan-nintendo.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The Nintendo Museum entrance', 'alt_he': 'הכניסה למוזיאון נינטנדו',
             'cap_en': 'The Nintendo Museum, just outside Kyoto.', 'cap_he': 'מוזיאון נינטנדו, ממש מחוץ לקיוטו.'},
            {'type': 'photo', 'src': 'japan-nintendo-controllers.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Giant plush Wii and N64 controllers at the Nintendo Museum', 'alt_he': 'בקרי Wii ו־N64 ענקיים מבד במוזיאון נינטנדו',
             'cap_en': 'Giant plush Wii and N64 controllers from the museum gift shop.', 'cap_he': 'שלטי Wii ו־N64 ענקיים מבד מחנות המזכרות של המוזיאון.'},
            {'type': 'story', 'en': 'Then Tokyo: fast, loud, and easy to love. Tokyo Tower up close, and a written wish left at a shrine.',
             'he': 'אחר כך טוקיו: מהירה, רועשת וקל להתאהב בה. מגדל טוקיו מקרוב, ומשאלה כתובה שהשארתי במקדש.'},
            {'type': 'photo', 'src': 'tokyo-tower.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir below the orange lattice of Tokyo Tower', 'alt_he': 'אדיר מתחת לשלד הכתום של מגדל טוקיו',
             'cap_en': 'Under the orange lattice of Tokyo Tower.', 'cap_he': 'מתחת לשלד הכתום של מגדל טוקיו.'},
            {'type': 'photo', 'src': 'shrine-wish.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir holding a written wish envelope at a shrine in Tokyo', 'alt_he': 'אדיר מחזיק מעטפת משאלה במקדש בטוקיו',
             'cap_en': 'A written wish at a Tokyo shrine.', 'cap_he': 'משאלה כתובה במקדש בטוקיו.'},
            {'type': 'story', 'en': 'Out to Mount Fuji: the little Fujikyu line, a clear day by Lake Kawaguchi, and the Chureito pagoda above the blossoms.',
             'he': 'ומשם להר פוג\'י: קו הפוג\'יקיו הקטן, יום בהיר על שפת אגם קוואגוצ\'י, ופגודת צ\'וריטו מעל הפריחה.'},
            {'type': 'clip', 'src': 'japan-rail.mp4', 'poster': 'japan-rail-poster.jpg', 'w': 540, 'h': 960,
             'alt_en': 'An orange Mt Fuji line train arriving at a platform', 'alt_he': 'רכבת כתומה של קו הר פוג\'י נכנסת לתחנה',
             'cap_en': 'Waiting on the platform for the Fujikyu line.', 'cap_he': 'ממתין על הרציף לרכבת הפוג\'יקיו.'},
            {'type': 'photo', 'src': 'fuji-lakeside.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir at a lakeside with Mount Fuji behind him', 'alt_he': 'אדיר על שפת אגם כשהר פוג\'י מאחוריו',
             'cap_en': 'A clear day across Lake Kawaguchi from Mount Fuji.', 'cap_he': 'יום בהיר מעבר לאגם קוואגוצ\'י מול הר פוג\'י.'},
            {'type': 'photo', 'src': 'japan-pagoda.jpg', 'w': 360, 'h': 480,
             'alt_en': 'The Chureito pagoda framed by cherry blossoms', 'alt_he': 'פגודת צ\'וריטו ממוסגרת בפריחת דובדבן',
             'cap_en': 'The Chureito pagoda, framed by cherry blossoms.', 'cap_he': 'פגודת צ\'וריטו, ממוסגרת בפריחת דובדבן.'},
            {'type': 'story', 'en': 'The flight home routed through Rome, so the trip ended at the Colosseum at golden hour, an unplanned last chapter.',
             'he': 'הטיסה הביתה עברה דרך רומא, אז הטיול הסתיים מול הקולוסיאום בשעת הזהב, פרק אחרון לא מתוכנן.'},
            {'type': 'photo', 'src': 'rome-colosseum.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir in front of the Colosseum in Rome at golden hour', 'alt_he': 'אדיר מול הקולוסיאום ברומא בשעת שקיעה',
             'cap_en': 'Golden hour at the Colosseum, Rome.', 'cap_he': 'שעת הזהב מול הקולוסיאום, רומא.'},
        ],
    },
    {
        'slug': 'avoriaz', 'dates': '2026',
        'state_en': 'Completed', 'state_he': 'הסתיים',
        'kicker_en': 'Snowboard trip', 'kicker_he': 'טיול סנובורד',
        'title_en': 'Avoriaz', 'title_he': 'אבוריאז',
        'meta_en': 'French Alps · Portes du Soleil', 'meta_he': 'האלפים הצרפתיים · Portes du Soleil',
        'tags_en': ['Snow', 'Snowboard', 'French Alps'], 'tags_he': ['שלג', 'סנובורד', 'האלפים הצרפתיים'],
        'teaser_en': 'A snowboard trip in Avoriaz, in the French Alps. Chairlifts, long runs, and mountain light from first lift to last.',
        'teaser_he': 'טיול סנובורד באבוריאז שבאלפים הצרפתיים. רכבלים, מסלולים ארוכים, ואור הרים מהרכבל הראשון עד האחרון.',
        'cover': 'snowboard-valley.jpg', 'cover_w': 1024, 'cover_h': 768,
        'cover_alt_en': 'A snowboard resting above a snowy alpine valley and village',
        'cover_alt_he': 'סנובורד מונח מעל עמק וכפר מושלגים',
        'intro_en': 'A week on the snow in Avoriaz, up in the French Alps, part of the huge Portes du Soleil area that spills across into Switzerland.',
        'intro_he': 'שבוע על השלג באבוריאז, גבוה באלפים הצרפתיים, חלק מאזור Portes du Soleil הענק שנמתח עד שווייץ.',
        'sections': [
            {'type': 'photo', 'src': 'snowboard-chairlift.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'View from a chairlift over the snowy Avoriaz slopes', 'alt_he': 'מבט מרכבל על מדרונות אבוריאז המושלגים',
             'cap_en': 'Above the slopes on the way up.', 'cap_he': 'מעל המדרונות בדרך למעלה.'},
            {'type': 'photo', 'src': 'avoriaz-sign.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The Avoriaz deer sign in the snow', 'alt_he': 'שלט האייל של אבוריאז בשלג',
             'cap_en': 'The Avoriaz deer, half in the snow.', 'cap_he': 'האייל של אבוריאז, חצי בשלג.'},
            {'type': 'photo', 'src': 'avoriaz-snow.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir beside the Avoriaz sign in the snow, chairlift overhead', 'alt_he': 'אדיר ליד שלט אבוריאז בשלג, רכבל מעל',
             'cap_en': 'Suited up, chairlift overhead.', 'cap_he': 'מצויד ומוכן, רכבל מעל הראש.'},
            {'type': 'story', 'en': 'Long runs, first lift to last, and the kind of cold that clears your head.',
             'he': 'ירידות ארוכות, מהרכבל הראשון עד האחרון, וקור שמנקה את הראש.'},
            {'type': 'photo', 'src': 'snowboard-summit.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir holding his snowboard overhead at sunset on the mountain', 'alt_he': 'אדיר מרים את הסנובורד מעל הראש בשקיעה על ההר',
             'cap_en': 'Last light at the top.', 'cap_he': 'אור אחרון בפסגה.'},
        ],
    },
    {
        'slug': 'matterhorn', 'dates': '2025',
        'state_en': 'Completed', 'state_he': 'הסתיים',
        'kicker_en': 'Snowboard trip', 'kicker_he': 'טיול סנובורד',
        'title_en': 'The Matterhorn', 'title_he': 'המטרהורן',
        'meta_en': 'Zermatt & Cervinia · Switzerland & Italy', 'meta_he': 'צרמט וצ\'רוויניה · שווייץ ואיטליה',
        'tags_en': ['Snow', 'Alps', 'Matterhorn'], 'tags_he': ['שלג', 'אלפים', 'מטרהורן'],
        'teaser_en': 'Riding the Matterhorn from both sides, Zermatt in Switzerland and Cervinia in Italy, under one of the most recognizable peaks in the Alps.',
        'teaser_he': 'גלישה על המטרהורן משני הצדדים, צרמט בשווייץ וצ\'רוויניה באיטליה, מתחת לאחת הפסגות המזוהות ביותר באלפים.',
        'cover': 'matterhorn-zermatt.jpg', 'cover_w': 768, 'cover_h': 1024,
        'cover_alt_en': 'The Matterhorn seen from Zermatt, Switzerland',
        'cover_alt_he': 'פסגת המטרהורן מצרמט שבשווייץ',
        'intro_en': 'Riding the Matterhorn from both sides, Zermatt in Switzerland and Cervinia in Italy, under one of the most recognizable peaks in the Alps. You can cross the border mid-mountain and ride down into a different country for lunch.',
        'intro_he': 'גלישה על המטרהורן משני הצדדים, צרמט בשווייץ וצ\'רוויניה באיטליה, מתחת לאחת הפסגות המוכרות באלפים. אפשר לחצות את הגבול באמצע ההר ולגלוש למדינה אחרת בשביל ארוחת צהריים.',
        'sections': [
            {'type': 'photo', 'src': 'matterhorn-zermatt.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The Matterhorn seen from Zermatt, Switzerland', 'alt_he': 'פסגת המטרהורן מצרמט שבשווייץ',
             'cap_en': 'The Matterhorn from the Zermatt side, Switzerland.', 'cap_he': 'המטרהורן מצד צרמט, שווייץ.'},
            {'type': 'photo', 'src': 'matterhorn-cervinia.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The Matterhorn above the slopes at Cervinia, Italy', 'alt_he': 'המטרהורן מעל המדרונות בצ\'רוויניה שבאיטליה',
             'cap_en': 'The same peak above Cervinia, Italy.', 'cap_he': 'אותה פסגה מעל צ\'רוויניה, איטליה.'},
            {'type': 'photo', 'src': 'alpine-village.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A snow-covered alpine village street', 'alt_he': 'רחוב כפרי מושלג באלפים',
             'cap_en': 'A snowed-in village street at the bottom.', 'cap_he': 'רחוב כפרי מושלג למטה.'},
        ],
    },
    {
        'slug': 'thailand', 'dates': '2024',
        'state_en': 'Completed', 'state_he': 'הסתיים',
        'kicker_en': 'Completed trip', 'kicker_he': 'טיול שהושלם',
        'title_en': 'Thailand', 'title_he': 'תאילנד',
        'meta_en': 'Chiang Mai · Chiang Rai · Pai · islands · Bangkok', 'meta_he': 'צ\'יאנג מאי · צ\'יאנג ראי · פאי · האיים · בנגקוק',
        'tags_en': ['Jungle', 'Islands', 'Warm weather', 'Elephants'], 'tags_he': ['ג\'ונגל', 'איים', 'מזג אוויר חם', 'פילים'],
        'teaser_en': 'The green, misty north around Chiang Mai and Pai, then the southern islands, ending in Bangkok. A warm, easy pace the whole way.',
        'teaser_he': 'הצפון הירוק והערפילי סביב צ\'יאנג מאי ופאי, ואז האיים בדרום, וסיום בבנגקוק. קצב חמים ונינוח לכל אורך הדרך.',
        'cover': 'thailand-kohtao-viewpoint.jpg', 'cover_w': 1024, 'cover_h': 1280,
        'cover_alt_en': 'A high viewpoint over a turquoise bay with green hills on Ko Tao',
        'cover_alt_he': 'תצפית גבוהה מעל מפרץ טורקיז עם גבעות ירוקות בקו טאו',
        'intro_en': 'Thailand was really two trips in one: the green, misty north around Chiang Mai and Pai, then the southern islands, winding up in Bangkok before the flight home.',
        'intro_he': 'תאילנד הייתה שני טיולים באחד: הצפון הירוק והערפילי סביב צ\'יאנג מאי ופאי, ואז האיים בדרום, וסיום בבנגקוק לפני הטיסה הביתה.',
        # Travel order: north (Chiang Mai -> Pai -> Chiang Mai) -> southern islands -> Bangkok.
        'sections': [
            {'type': 'story', 'en': 'It started up north around Chiang Mai: buzzing night markets, a morning with elephants, white-water rafting, jungle waterfalls and a hill-tribe village, plus a side trip up to the tea hills of Chiang Rai.',
             'he': 'זה התחיל בצפון, סביב צ\'יאנג מאי: שווקי לילה שוקקים, בוקר ליד פילים, רפטינג, מפלים בג\'ונגל וכפר שבטי, ובנוסף קפיצה צפונה לגבעות התה של צ\'יאנג ראי.'},
            {'type': 'photo', 'src': 'thailand-night-market.jpg', 'w': 960, 'h': 1280,
             'alt_en': 'The lit Chill Square sign over the Anusarn night market in Chiang Mai', 'alt_he': 'שלט Chill Square מואר מעל שוק הלילה אנוסארן בצ\'יאנג מאי',
             'cap_en': 'Chill Square at the Anusarn night market, Chiang Mai.', 'cap_he': 'Chill Square בשוק הלילה אנוסארן, צ\'יאנג מאי.'},
            {'type': 'photo', 'src': 'thailand-elephants-river.jpg', 'w': 1200, 'h': 900,
             'alt_en': 'Two elephants by a river with green hills behind, Adir standing nearby', 'alt_he': 'שני פילים על גדת נהר עם גבעות ירוקות מאחור, אדיר עומד בקרבת מקום',
             'cap_en': 'Elephants by the river at a sanctuary near Chiang Mai.', 'cap_he': 'פילים על גדת הנהר בשמורה ליד צ\'יאנג מאי.'},
            {'type': 'photo', 'src': 'thailand-elephants.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir reaching out to an elephant by a river near Chiang Mai', 'alt_he': 'אדיר מושיט יד לפיל על גדת נהר ליד צ\'יאנג מאי',
             'cap_en': 'Up close with one of them.', 'cap_he': 'מקרוב מול אחד מהם.'},
            {'type': 'clip', 'src': 'thailand-rafting.mp4', 'poster': 'thailand-rafting-poster.jpg', 'w': 960, 'h': 540,
             'alt_en': 'A GoPro view from a raft splashing through river rapids', 'alt_he': 'מבט גו-פרו מתוך רפסודה חוצה אשדות נהר',
             'cap_en': 'White-water rafting down a river near Chiang Mai.', 'cap_he': 'רפטינג במורד נהר ליד צ\'יאנג מאי.'},
            {'type': 'story', 'en': 'The days swung between adrenaline and calm: rafting and waterfalls one minute, a village loom or a quiet tea hillside the next.',
             'he': 'הימים התנדנדו בין אדרנלין לרוגע: רפטינג ומפלים ברגע אחד, נול בכפר או מדרון תה שקט ברגע הבא.'},
            {'type': 'photo', 'src': 'thailand-bua-tong.jpg', 'w': 900, 'h': 1200,
             'alt_en': 'Water running over the limestone Bua Tong sticky waterfalls in the jungle', 'alt_he': 'מים זורמים על מפלי הדבק בואה טונג בג\'ונגל',
             'cap_en': 'The Bua Tong "sticky" waterfalls you can walk straight up.', 'cap_he': 'מפלי הדבק בואה טונג שאפשר לטפס עליהם ישר למעלה.'},
            {'type': 'photo', 'src': 'thailand-waterfall.jpg', 'w': 886, 'h': 886,
             'alt_en': 'Adir climbing a waterfall by rope, jungle all around', 'alt_he': 'אדיר מטפס על מפל בעזרת חבל, ג\'ונגל מסביב',
             'cap_en': 'Climbing them by rope.', 'cap_he': 'טיפוס עליהם בעזרת חבל.'},
            {'type': 'photo', 'src': 'thailand-longneck.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A Kayan woman with brass neck rings weaving at a loom in a village', 'alt_he': 'אישה מבני קאיאן עם טבעות צוואר מפליז אורגת בנול בכפר',
             'cap_en': 'A Kayan weaver at a hill-tribe village near Chiang Mai.', 'cap_he': 'אורגת מבני קאיאן בכפר שבטי ליד צ\'יאנג מאי.'},
            {'type': 'story', 'en': 'Then up to Chiang Rai for a day of temples and color: a hillside tea estate, the red pagoda and giant white Guan Yin of Wat Huay Pla Kang, and a night market glowing pink. The drive even threw in a steaming roadside hot spring and a temple the monkeys had taken over.',
             'he': 'ואז צפונה לצ\'יאנג ראי, ליום של מקדשים וצבע: מטע תה על מדרון, הפגודה האדומה ופסל הגואן יין הלבן הענק של ואט הואי פלא קאנג, ושוק לילה שזוהר בוורוד. הדרך אפילו זרקה פנימה מעיין חם מהביל ומקדש שהקופים השתלטו עליו.'},
            {'type': 'photo', 'src': 'thailand-tea.jpg', 'w': 1200, 'h': 900,
             'alt_en': 'Rolling rows of tea bushes at a plantation in Chiang Rai', 'alt_he': 'שורות מתפתלות של שיחי תה במטע בצ\'יאנג ראי',
             'cap_en': 'The Choui Fong tea plantation up in Chiang Rai.', 'cap_he': 'מטע התה צ\'וי פונג בצ\'יאנג ראי.'},
            {'type': 'photo', 'src': 'thailand-wphk-pagoda.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'The red and gold nine-tier pagoda and white temple of Wat Huay Pla Kang at dusk', 'alt_he': 'הפגודה האדומה-זהובה בת תשע הקומות והמקדש הלבן של ואט הואי פלא קאנג בין הערביים',
             'cap_en': 'The pagoda and temple at Wat Huay Pla Kang, Chiang Rai.', 'cap_he': 'הפגודה והמקדש בוואט הואי פלא קאנג, צ\'יאנג ראי.'},
            {'type': 'photo', 'src': 'thailand-guan-yin.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The giant white Guan Yin statue towering over the steps at Wat Huay Pla Kang', 'alt_he': 'פסל הגואן יין הלבן הענק מתנשא מעל המדרגות בוואט הואי פלא קאנג',
             'cap_en': 'The giant white Guan Yin above the steps.', 'cap_he': 'הגואן יין הלבן הענק מעל המדרגות.'},
            {'type': 'photo', 'src': 'thailand-pink-trees.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Trees covered in bright pink lights at a night market in Chiang Rai', 'alt_he': 'עצים עטופים באורות ורודים זוהרים בשוק לילה בצ\'יאנג ראי',
             'cap_en': 'Glowing pink trees at a Chiang Rai night market.', 'cap_he': 'עצים ורודים זוהרים בשוק לילה בצ\'יאנג ראי.'},
            {'type': 'story', 'en': 'The White Temple, Wat Rong Khun, was the strangest of all: bright white and mirror-flecked, with a field of reaching hands at the bridge and silver wish plaques jingling overhead.',
             'he': 'המקדש הלבן, ואט רונג חון, היה המוזר מכולם: לבן בוהק ומנוצץ בשברי מראה, עם שדה של ידיים מושטות לפני הגשר ולוחיות משאלה מכסף שמצלצלות מעל.'},
            {'type': 'photo', 'src': 'thailand-white-temple.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The all-white Wat Rong Khun temple reflected across its pond', 'alt_he': 'מקדש ואט רונג חון הלבן כולו משתקף מעבר לבריכה שלפניו',
             'cap_en': 'Wat Rong Khun, the White Temple of Chiang Rai.', 'cap_he': 'ואט רונג חון, המקדש הלבן של צ\'יאנג ראי.'},
            {'type': 'photo', 'src': 'thailand-wish-plaques.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Silver heart-shaped wish plaques hanging at the White Temple', 'alt_he': 'לוחיות משאלה מכסף בצורת לב תלויות במקדש הלבן',
             'cap_en': 'Silver wish plaques hung around the temple.', 'cap_he': 'לוחיות משאלה מכסף תלויות סביב המקדש.'},
            {'type': 'photo', 'src': 'thailand-white-temple-hands.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A sea of sculpted reaching hands at the entrance bridge of the White Temple', 'alt_he': 'ים של ידיים מושטות מפוסלות בגשר הכניסה של המקדש הלבן',
             'cap_en': 'The field of reaching hands at the entrance.', 'cap_he': 'שדה הידיים המושטות בכניסה.'},
            {'type': 'clip', 'src': 'thailand-hot-spring.mp4', 'poster': 'thailand-hot-spring-poster.jpg', 'w': 540, 'h': 960,
             'alt_en': 'Steam rising from a roadside hot spring at Wiang Pa Pao', 'alt_he': 'אדים עולים ממעיין חם בצד הדרך בוויאנג פא פאו',
             'cap_en': 'A steaming hot spring at Wiang Pa Pao, on the road to Chiang Rai.', 'cap_he': 'מעיין חם מהביל בוויאנג פא פאו, בדרך לצ\'יאנג ראי.'},
            {'type': 'clip', 'src': 'thailand-monkeys.mp4', 'poster': 'thailand-monkeys-poster.jpg', 'w': 540, 'h': 960,
             'alt_en': 'A troop of macaques roaming the ground at a roadside temple', 'alt_he': 'להקת קופי מקוק משוטטת על הקרקע במקדש בצד הדרך',
             'cap_en': 'Macaques running the show at a roadside temple.', 'cap_he': 'קופי מקוק מנהלים את המקום במקדש בצד הדרך.'},
            {'type': 'story', 'en': 'Then a run up to Pai, slower and greener: rice fields, a misty valley, a rainy walking street, and a scooter ride out to a steaming hot spring.',
             'he': 'ואז קפיצה לפאי, איטית וירוקה יותר: שדות אורז, עמק ערפילי, רחוב מטיילים גשום, ונסיעה על קטנוע אל מעיין חם מהביל.'},
            {'type': 'photo', 'src': 'thailand-rice-bridge.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir with arms spread on a bamboo bridge over rice paddies in Pai', 'alt_he': 'אדיר בידיים פתוחות על גשר במבוק מעל שדות אורז בפאי',
             'cap_en': 'The bamboo bridge over the rice fields in Pai.', 'cap_he': 'גשר הבמבוק מעל שדות האורז בפאי.'},
            {'type': 'photo', 'src': 'thailand-pai-view.jpg', 'w': 1500, 'h': 704,
             'alt_en': 'A green, misty valley and hills seen from a hillside balcony above Pai', 'alt_he': 'עמק ירוק וערפילי וגבעות, נראים ממרפסת על מדרון מעל פאי',
             'cap_en': 'A misty valley view from a hillside spot above Pai.', 'cap_he': 'נוף עמק ערפילי ממקום על מדרון מעל פאי.'},
            {'type': 'photo', 'src': 'thailand-pai-street.jpg', 'w': 960, 'h': 1280,
             'alt_en': 'A wet Pai walking street lined with hanging paper lanterns under grey skies', 'alt_he': 'רחוב המטיילים הרטוב של פאי עם פנסי נייר תלויים תחת שמיים אפורים',
             'cap_en': "Pai's walking street in the rain.", 'cap_he': 'רחוב המטיילים של פאי בגשם.'},
            {'type': 'photo', 'src': 'thailand-pai-scooter.jpg', 'w': 960, 'h': 1280,
             'alt_en': 'Adir on a white Honda Click scooter parked under a carport in Pai', 'alt_he': 'אדיר על קטנוע הונדה קליק לבן חונה תחת סככה בפאי',
             'cap_en': 'The scooter I rented to get around Pai.', 'cap_he': 'הקטנוע ששכרתי כדי להסתובב בפאי.'},
            {'type': 'photo', 'src': 'thailand-mueng-pang.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The Mueng Pang Hot Spring entrance sign with steam rising behind it near Pai', 'alt_he': 'שלט הכניסה של מעיין החם מואנג פאנג עם אדים עולים מאחוריו ליד פאי',
             'cap_en': 'Mueng Pang hot spring, a scooter ride out from Pai.', 'cap_he': 'מעיין החם מואנג פאנג, נסיעת קטנוע מפאי.'},
            {'type': 'story', 'en': 'Between the big sights, the small stuff was half the fun: night markets, trays of mochi, flower stalls, and slow evenings by the river with friends.',
             'he': 'בין האתרים הגדולים, דווקא הדברים הקטנים היו חצי מהכיף: שווקי לילה, מגשי מוצ\'י, דוכני פרחים, וערבים נינוחים על שפת הנהר עם חברים.'},
            {'type': 'photo', 'src': 'thailand-river-night.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir with a baby in a carrier and two friends on a lit bridge over a river at night, a colorful market glowing across the water', 'alt_he': 'אדיר עם תינוק במנשא ושני חברים על גשר מואר מעל נהר בלילה, שוק צבעוני זוהר מעבר למים',
             'cap_en': 'A night by the river with friends.', 'cap_he': 'ערב על שפת הנהר עם חברים.'},
            {'type': 'photo', 'src': 'thailand-mochi.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Trays of colorful mochi (strawberry, green tea, chocolate, salted egg) at a night-market stall', 'alt_he': 'מגשי מוצ\'י צבעוניים (תות, תה ירוק, שוקולד, חלמון מלוח) בדוכן בשוק לילה',
             'cap_en': 'Mochi stacked up at a night market.', 'cap_he': 'מוצ\'י ערוך בערימות בשוק לילה.'},
            {'type': 'photo', 'src': 'thailand-flower-market.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Buckets of marigolds, roses, and dyed chrysanthemums with jasmine garlands at a Thai flower market', 'alt_he': 'דליים של ציפורני חתול, ורדים וחרציות צבועות עם זרי יסמין בשוק פרחים תאילנדי',
             'cap_en': 'A flower and garland stall at the market.', 'cap_he': 'דוכן פרחים וזרים בשוק.'},
            {'type': 'story', 'en': 'Then south to the islands, starting with a short flight into Koh Samui\'s little garden airport.',
             'he': 'ואז דרומה לאיים, שמתחילים בטיסה קצרה לשדה התעופה הקטן והירוק של קו סמוי.'},
            {'type': 'clip', 'src': 'thailand-samui-aerial.mp4', 'poster': 'thailand-samui-aerial-poster.jpg', 'w': 540, 'h': 960,
             'alt_en': 'Aerial view from a plane window of a green headland and turquoise sea at Koh Samui', 'alt_he': 'מבט אווירי מחלון מטוס על לשון יבשה ירוקה וים טורקיז בקו סמוי',
             'cap_en': 'Coming in over Koh Samui.', 'cap_he': 'מתקרבים מעל קו סמוי.'},
            {'type': 'photo', 'src': 'thailand-samui-airport.jpg', 'w': 665, 'h': 1182,
             'alt_en': 'The orange Samui Airport sign in a tropical garden', 'alt_he': 'שלט שדה התעופה הכתום של קו סמוי בגן טרופי',
             'cap_en': "Koh Samui's open-air garden airport.", 'cap_he': 'שדה התעופה הפתוח והירוק של קו סמוי.'},
            {'type': 'story', 'en': 'A ferry over to Ko Tao, then island time: a climb to a viewpoint over a turquoise bay, palms down to the water, a sunset swim, fresh coconuts, and a fire show on the beach after dark.',
             'he': 'מעבורת לקו טאו, ואז זמן אי: טיפוס לתצפית מעל מפרץ טורקיז, דקלים עד המים, שחייה בשקיעה, קוקוסים טריים, ומופע אש על החוף אחרי רדת החשכה.'},
            {'type': 'photo', 'src': 'thailand-kohtao-viewpoint.jpg', 'w': 1024, 'h': 1280,
             'alt_en': 'A high viewpoint over a turquoise bay with green hills and resorts on Ko Tao', 'alt_he': 'תצפית גבוהה מעל מפרץ טורקיז עם גבעות ירוקות ובתי נופש בקו טאו',
             'cap_en': 'A viewpoint over a turquoise bay on Ko Tao.', 'cap_he': 'תצפית מעל מפרץ טורקיז בקו טאו.'},
            {'type': 'photo', 'src': 'thailand-kohtao-palms.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Tall coconut palms framing a turquoise bay on Ko Tao', 'alt_he': 'דקלי קוקוס גבוהים ממסגרים מפרץ טורקיז בקו טאו',
             'cap_en': 'Palms running down to the water.', 'cap_he': 'דקלים יורדים עד המים.'},
            {'type': 'photo', 'src': 'thailand-kohtao-sunset.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Sunset over the sea with longtail boats and swimmers off a Ko Tao beach', 'alt_he': 'שקיעה מעל הים עם סירות לונגטייל ומתרחצים מול חוף בקו טאו',
             'cap_en': 'A sunset swim off the beach.', 'cap_he': 'שחייה בשקיעה מול החוף.'},
            {'type': 'photo', 'src': 'thailand-kohtao-coconut.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Adir smiling at a beach restaurant with a fresh young coconut and a green smoothie', 'alt_he': 'אדיר מחייך במסעדת חוף עם קוקוס צעיר טרי ושייק ירוק',
             'cap_en': 'Fresh coconut at a beach restaurant.', 'cap_he': 'קוקוס טרי במסעדת חוף.'},
            {'type': 'clip', 'src': 'thailand-kohtao-fire.mp4', 'poster': 'thailand-kohtao-fire-poster.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Fire dancers spinning flaming poi on a beach at night while a crowd watches', 'alt_he': 'רקדני אש מסובבים כדורי אש על החוף בלילה בעוד קהל צופה',
             'cap_en': 'A fire show on the beach after dark.', 'cap_he': 'מופע אש על החוף אחרי רדת החשכה.'},
            {'type': 'story', 'en': 'Ko Tao had a boat day in it too: out by longtail to snorkel among the granite boulders and pull up on quiet beaches, then sunset drinks at a hilltop bar.',
             'he': 'בקו טאו היה גם יום סירה: יציאה בלונגטייל לשנורקל בין סלעי הגרניט ועצירה בחופים שקטים, ואז דרינקים בשקיעה בבר על הגבעה.'},
            {'type': 'photo', 'src': 'thailand-kohtao-boattrip.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Adir and a friend on a red longtail boat at a wooden pier under a moody sky on Ko Tao', 'alt_he': 'אדיר וחבר על סירת לונגטייל אדומה ברציף עץ תחת שמיים מעוננים בקו טאו',
             'cap_en': 'Heading out on a boat trip from Ko Tao.', 'cap_he': 'יוצאים לטיול סירה מקו טאו.'},
            {'type': 'photo', 'src': 'thailand-kohtao-boat-beach.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'View from a boat of a palm-backed beach in clear shallow turquoise water', 'alt_he': 'מבט מהסירה על חוף מוקף דקלים במים רדודים, צלולים וטורקיז',
             'cap_en': 'Pulling up to a quiet beach.', 'cap_he': 'עוגנים מול חוף שקט.'},
            {'type': 'photo', 'src': 'thailand-kohtao-snorkel.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A beach with big granite boulders and snorkellers in turquoise water on Ko Tao', 'alt_he': 'חוף עם סלעי גרניט גדולים ושנורקלרים במים טורקיז בקו טאו',
             'cap_en': 'Snorkelling among the granite boulders.', 'cap_he': 'שנורקל בין סלעי הגרניט.'},
            {'type': 'clip', 'src': 'thailand-kohtao-bar.mp4', 'poster': 'thailand-kohtao-bar-poster.jpg', 'w': 960, 'h': 540,
             'alt_en': 'A pink and orange sunset over the sea and jungle from a hilltop bar on Ko Tao', 'alt_he': 'שקיעה ורודה וכתומה מעל הים והג\'ונגל מבר על גבעה בקו טאו',
             'cap_en': 'Sunset from a hilltop bar.', 'cap_he': 'שקיעה מבר על הגבעה.'},
            {'type': 'story', 'en': 'Back on Ko Samui, the day was all jet skis: a tour out across a calm green bay, opening it up on the open water, and dinner to finish.',
             'he': 'בחזרה בקו סמוי, היום היה כולו אופנועי ים: סיור על פני מפרץ ירוק ורגוע, פתיחת גז על המים הפתוחים, וארוחת ערב לסיום.'},
            {'type': 'photo', 'src': 'thailand-samui-jetski-group.jpg', 'w': 1182, 'h': 666,
             'alt_en': 'A group lined up on a row of jet skis in a calm green bay off Ko Samui', 'alt_he': 'קבוצה על שורת אופנועי ים במפרץ ירוק ורגוע מול קו סמוי',
             'cap_en': 'The jet ski tour lined up off Ko Samui.', 'cap_he': 'סיור אופנועי הים מסודר בשורה מול קו סמוי.'},
            {'type': 'photo', 'src': 'thailand-jetski.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir on a jet ski in clear blue water by Ko Samui', 'alt_he': 'אדיר על אופנוע ים במים כחולים ליד קו סמוי',
             'cap_en': 'Out on the water off Ko Samui.', 'cap_he': 'על המים מול קו סמוי.'},
            {'type': 'photo', 'src': 'thailand-samui-jetski-solo.jpg', 'w': 666, 'h': 1182,
             'alt_en': 'Adir riding a jet ski fast across open blue water with spray flying', 'alt_he': 'אדיר דוהר על אופנוע ים על מים כחולים פתוחים, התזה עפה',
             'cap_en': 'Opening it up on the open water.', 'cap_he': 'פותח גז על המים הפתוחים.'},
            {'type': 'photo', 'src': 'thailand-samui-dinner.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Adir smiling over fresh coconuts at a restaurant table at night', 'alt_he': 'אדיר מחייך מעל קוקוסים טריים בשולחן מסעדה בלילה',
             'cap_en': 'Dinner and fresh coconuts.', 'cap_he': 'ארוחת ערב וקוקוסים טריים.'},
            {'type': 'story', 'en': 'Then over to Phuket, the big-island version of all this: driving everywhere, long beaches, and even a water park.',
             'he': 'ואז לפוקט, הגרסה של האי הגדול לכל זה: נסיעות לכל מקום, חופים ארוכים, ואפילו פארק מים.'},
            {'type': 'photo', 'src': 'thailand-phuket-driving.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'View from inside a car driving down a Phuket road at golden hour', 'alt_he': 'מבט מתוך רכב נוסע בכביש בפוקט בשעת הזהב',
             'cap_en': 'Driving around Phuket.', 'cap_he': 'נסיעה ברחבי פוקט.'},
            {'type': 'photo', 'src': 'thailand-kata-beach.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Kata Beach at dusk with loungers and two small islands offshore', 'alt_he': 'חוף קאטה בין הערביים עם מיטות שיזוף ושני איים קטנים ברקע',
             'cap_en': 'Kata Beach at dusk.', 'cap_he': 'חוף קאטה בין הערביים.'},
            {'type': 'photo', 'src': 'thailand-phuket-beach-steps.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Stone steps leading down to a busy Phuket beach with longtail boats', 'alt_he': 'מדרגות אבן יורדות לחוף שוקק בפוקט עם סירות לונגטייל',
             'cap_en': 'Steps down to the beach.', 'cap_he': 'מדרגות יורדות לחוף.'},
            {'type': 'photo', 'src': 'thailand-phuket-waterpark.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A big wave pool with rock formations and slides at a Phuket water park', 'alt_he': 'בריכת גלים גדולה עם תצורות סלע ומגלשות בפארק מים בפוקט',
             'cap_en': 'The wave pool at a Phuket water park.', 'cap_he': 'בריכת הגלים בפארק מים בפוקט.'},
            {'type': 'story', 'en': 'A day out into Phang Nga Bay: a speedboat through the limestone karsts, kayaking under the cliffs, and a roadside fruit stop.',
             'he': 'יום בשייט אל מפרץ פאנג נגה: סירת מהירות בין צוקי הגיר, קייאקים מתחת למצוקים, ועצירת פירות בצד הדרך.'},
            {'type': 'photo', 'src': 'thailand-phangnga-boat.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'View from a speedboat of limestone cliffs and a floating village in Phang Nga Bay', 'alt_he': 'מבט מסירת מהירות על צוקי גיר וכפר צף במפרץ פאנג נגה',
             'cap_en': 'Into Phang Nga Bay by speedboat.', 'cap_he': 'אל מפרץ פאנג נגה בסירת מהירות.'},
            {'type': 'photo', 'src': 'thailand-phangnga-kayak.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Tall limestone karsts rising from green water in Phang Nga Bay, seen from a kayak', 'alt_he': 'צוקי גיר גבוהים מתנשאים ממים ירוקים במפרץ פאנג נגה, ממבט קייאק',
             'cap_en': 'Kayaking under the cliffs of Phang Nga Bay.', 'cap_he': 'קייאק מתחת למצוקים של מפרץ פאנג נגה.'},
            {'type': 'photo', 'src': 'thailand-phuket-fruit-stall.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A roadside stall with pineapples, watermelons and coconuts under bunting', 'alt_he': 'דוכן בצד הדרך עם אננסים, אבטיחים וקוקוסים תחת שרשרת דגלים',
             'cap_en': 'A roadside fruit stop.', 'cap_he': 'עצירת פירות בצד הדרך.'},
            {'type': 'story', 'en': 'And the nights: the Naka weekend market, the neon of Patong\'s Bangla Road, and a quieter clifftop sunset to balance it out.',
             'he': 'והלילות: שוק סוף השבוע נאקה, הניאון של רחוב באנגלה בפטונג, ושקיעה שקטה על צוק לאיזון.'},
            {'type': 'photo', 'src': 'thailand-phuket-naka-market.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The lit entrance arch of the Naka weekend night market in Phuket', 'alt_he': 'שער הכניסה המואר של שוק הלילה נאקה בפוקט',
             'cap_en': 'The Naka weekend market.', 'cap_he': 'שוק סוף השבוע נאקה.'},
            {'type': 'photo', 'src': 'thailand-patong-bangla.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'The neon Patong Beach welcome arch over Bangla Road at night', 'alt_he': 'שער הניאון של פטונג מעל רחוב באנגלה בלילה',
             'cap_en': 'Bangla Road, Patong, after dark.', 'cap_he': 'רחוב באנגלה, פטונג, אחרי החשכה.'},
            {'type': 'photo', 'src': 'thailand-phuket-sunset-bar.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A red sun setting over the sea from a clifftop bar with rattan chairs and a palm', 'alt_he': 'שמש אדומה שוקעת מעל הים מבר על צוק עם כיסאות ראטאן ודקל',
             'cap_en': 'A clifftop sunset to wind down.', 'cap_he': 'שקיעה על צוק לסיום היום.'},
            {'type': 'story', 'en': 'A boat over to Koh Phi Phi: clear turquoise under the cliffs, longtails everywhere, kayaks on the sand, and the bay hemmed in by karsts.',
             'he': 'סירה לקו פי פי: מים טורקיז צלולים מתחת למצוקים, סירות לונגטייל בכל מקום, קייאקים על החול, והמפרץ מוקף בצוקי גיר.'},
            {'type': 'photo', 'src': 'thailand-phiphi-pileh.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Turquoise water and a towering limestone cliff seen from a longtail at Koh Phi Phi', 'alt_he': 'מים טורקיז וצוק גיר מתנשא, ממבט סירת לונגטייל בקו פי פי',
             'cap_en': 'Clear turquoise water under the Phi Phi cliffs.', 'cap_he': 'מים טורקיז צלולים מתחת למצוקי פי פי.'},
            {'type': 'photo', 'src': 'thailand-longtail.jpg', 'w': 880, 'h': 1100,
             'alt_en': 'Adir on a longtail boat between limestone cliffs at Koh Phi Phi', 'alt_he': 'אדיר על סירת לונגטייל בין צוקי גיר בקו פי פי',
             'cap_en': 'A longtail boat between the cliffs at Koh Phi Phi.', 'cap_he': 'סירת לונגטייל בין הצוקים בקו פי פי.'},
            {'type': 'photo', 'src': 'thailand-phiphi-bay.jpg', 'w': 1280, 'h': 960,
             'alt_en': 'Many longtail and speed boats moored in Phi Phi bay under the twin karst headland', 'alt_he': 'סירות לונגטייל וסירות מהירות רבות עוגנות במפרץ פי פי מתחת לראש הצוק הכפול',
             'cap_en': 'Longtails lined up in the bay.', 'cap_he': 'סירות לונגטייל מסודרות במפרץ.'},
            {'type': 'photo', 'src': 'thailand-phiphi-kayaks.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Colorful kayaks on the sand with longtail boats and karst behind at Koh Phi Phi', 'alt_he': 'קייאקים צבעוניים על החול עם סירות לונגטייל וצוקי גיר מאחור בקו פי פי',
             'cap_en': 'Kayaks on the beach at Phi Phi.', 'cap_he': 'קייאקים על החוף בפי פי.'},
            {'type': 'clip', 'src': 'thailand-phiphi-beach.mp4', 'poster': 'thailand-phiphi-beach-poster.jpg', 'w': 720, 'h': 960,
             'alt_en': 'Longtail boats moored along a Phi Phi beach under cloudy cliffs', 'alt_he': 'סירות לונגטייל עוגנות לאורך חוף בפי פי תחת מצוקים מעוננים',
             'cap_en': 'A quiet stretch of Phi Phi beach.', 'cap_he': 'מתחם חוף שקט בפי פי.'},
            {'type': 'story', 'en': 'And the rest of it: coconuts on the walking street, lanterns over the lanes at night, and a fire show on the beach.',
             'he': 'וכל השאר: קוקוסים ברחוב המטיילים, פנסים מעל הסמטאות בלילה, ומופע אש על החוף.'},
            {'type': 'photo', 'src': 'thailand-phiphi-coconut.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A hand holding a fresh green coconut on the Phi Phi walking street', 'alt_he': 'יד מחזיקה קוקוס ירוק טרי ברחוב המטיילים של פי פי',
             'cap_en': 'A coconut on the walking street.', 'cap_he': 'קוקוס ברחוב המטיילים.'},
            {'type': 'photo', 'src': 'thailand-phiphi-lanterns.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Colorful paper lanterns strung over a Phi Phi walkway at night', 'alt_he': 'פנסי נייר צבעוניים תלויים מעל שביל בפי פי בלילה',
             'cap_en': 'Lanterns over the lanes at night.', 'cap_he': 'פנסים מעל הסמטאות בלילה.'},
            {'type': 'clip', 'src': 'thailand-phiphi-fire.mp4', 'poster': 'thailand-phiphi-fire-poster.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A fire performer making a flaming heart with poi on a Phi Phi beach at night', 'alt_he': 'אמן אש יוצר לב להבות עם כדורי אש על חוף בפי פי בלילה',
             'cap_en': 'A fire show on the beach.', 'cap_he': 'מופע אש על החוף.'},
            {'type': 'story', 'en': 'The last stretch was Bangkok, a loud, sprawling city to land in after weeks of beaches and mountains.',
             'he': 'הקטע האחרון היה בנגקוק, עיר רועשת ומשתרעת לנחות בה אחרי שבועות של חופים והרים.'},
            {'type': 'photo', 'src': 'thailand-bangkok-aerial.jpg', 'w': 720, 'h': 1280,
             'alt_en': "View of Bangkok's outskirts and an AirAsia wingtip from the plane window on approach", 'alt_he': 'מבט על פאתי בנגקוק וכנף מטוס של AirAsia מחלון המטוס בזמן הגישה לנחיתה',
             'cap_en': 'Coming back into Bangkok from the islands.', 'cap_he': 'חוזרים לבנגקוק מהאיים.'},
            {'type': 'photo', 'src': 'thailand-bangkok-watarun.jpg', 'w': 1024, 'h': 768,
             'alt_en': 'The spires of Wat Arun across the Chao Phraya river with longtail boats passing', 'alt_he': "צריחי ואט ארון מעבר לנהר צ'או פראיה עם סירות לונגטייל חולפות",
             'cap_en': 'Wat Arun across the Chao Phraya.', 'cap_he': "ואט ארון מעבר לנהר צ'או פראיה."},
            {'type': 'photo', 'src': 'thailand-bangkok-lumphini.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'A lake at Lumphini Park reflecting a tall glass tower, framed by trees', 'alt_he': 'אגם בפארק לומפיני משקף מגדל זכוכית גבוה, ממוסגר בעצים',
             'cap_en': 'Lumphini Park, green in the middle of the city.', 'cap_he': 'פארק לומפיני, ירוק בלב העיר.'},
            {'type': 'photo', 'src': 'thailand-bangkok-monitor.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A large water monitor lizard resting on rocks by the lake at Lumphini Park', 'alt_he': 'ורן מים גדול נח על סלעים ליד האגם בפארק לומפיני',
             'cap_en': 'A water monitor sunning itself by the lake.', 'cap_he': 'ורן מתחמם בשמש ליד האגם.'},
            {'type': 'story', 'en': 'Lumphini is a piece of green dropped into the middle of the towers, and the water monitors wander it like they own the place.',
             'he': 'לומפיני הוא פיסת ירוק בלב המגדלים, והוורנים מטיילים בו כמו בבית.'},
            {'type': 'photo', 'src': 'thailand-bangkok-skyline.jpg', 'w': 1024, 'h': 768,
             'alt_en': 'Bangkok skyline over a stadium and rail tracks, towers fading into haze', 'alt_he': 'קו הרקיע של בנגקוק מעל אצטדיון ומסילות, מגדלים נמוגים באובך',
             'cap_en': 'The city stacked up, all the way to the horizon.', 'cap_he': 'העיר נערמת עד האופק.'},
            {'type': 'photo', 'src': 'thailand-bangkok-iconsiam.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'Colorful light installations reflected in water by the ICONSIAM riverside at night', 'alt_he': 'מיצגי אור צבעוניים משתקפים במים ליד אייקונסיאם על גדת הנהר בלילה',
             'cap_en': 'ICONSIAM lit up along the river at night.', 'cap_he': 'אייקונסיאם מואר לאורך הנהר בלילה.'},
            {'type': 'photo', 'src': 'thailand-bangkok-mbk.jpg', 'w': 720, 'h': 1280,
             'alt_en': 'The illuminated facade of MBK Center shopping mall in Bangkok at night', 'alt_he': 'החזית המוארת של קניון MBK בבנגקוק בלילה',
             'cap_en': 'MBK Center after dark.', 'cap_he': 'מרכז MBK אחרי רדת החשכה.'},
            {'type': 'photo', 'src': 'thailand-bangkok-7eleven.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'A brightly lit 7-Eleven storefront on a Bangkok street at night with scooters parked outside', 'alt_he': 'חזית מוארת של חנות 7-Eleven ברחוב בבנגקוק בלילה עם קטנועים חונים בחוץ',
             'cap_en': 'And, of course, the 7-Eleven on every corner.', 'cap_he': 'וכמובן, ה־7-Eleven שבכל פינה.'},
            {'type': 'story', 'en': 'And then the flight home.',
             'he': 'ואז הטיסה הביתה.'},
        ],
    },
]


def album_meta(trip: dict, lang: str) -> dict[str, str]:
    is_he = lang == 'he'
    slug = f'he/trips/{trip["slug"]}.html' if is_he else f'trips/{trip["slug"]}.html'
    en_href = f'/trips/{trip["slug"]}.html'
    he_href = f'/he/trips/{trip["slug"]}.html'
    title_word = trip['title_he'] if is_he else trip['title_en']
    name = f'אדיר בן דוד' if is_he else 'Adir Ben David'
    title = f'{title_word} {trip["dates"]} | {name}'
    description = trip['teaser_he'] if is_he else trip['teaser_en']
    return {
        'lang': lang, 'dir': 'rtl' if is_he else 'ltr',
        'home': '/he/' if is_he else '/',
        'active': '/he/journeys.html' if is_he else '/journeys.html',
        'abs_nav': True,
        'switch': he_href if not is_he else en_href,
        'switch_from': 'HE' if is_he else 'EN', 'switch_to': 'EN' if is_he else 'HE',
        'title': title, 'description': description,
        'slug': slug, 'en_href': en_href, 'he_href': he_href, 'x_default': en_href,
        'locale': 'he_IL' if is_he else 'en_US', 'locale_alt': 'en_US' if is_he else 'he_IL',
        'og_image': f'{IMG}/{trip["cover"]}',
        'og_image_alt': trip['cover_alt_he'] if is_he else trip['cover_alt_en'],
        'og_image_w': trip['cover_w'], 'og_image_h': trip['cover_h'],
    }


def render_tags(tags: list[str]) -> str:
    return ''.join(f'<span>{e(t)}</span>' for t in tags)


def render_album_main(trip: dict, lang: str) -> str:
    is_he = lang == 'he'
    back = 'חזרה למסעות' if is_he else 'Back to Journeys'
    arrow = '→' if is_he else '←'
    journeys_href = '/he/journeys.html' if is_he else '/journeys.html'
    title = trip['title_he'] if is_he else trip['title_en']
    kicker = trip['kicker_he'] if is_he else trip['kicker_en']
    meta_line = trip['meta_he'] if is_he else trip['meta_en']
    intro = trip['intro_he'] if is_he else trip['intro_en']
    cover_alt = trip['cover_alt_he'] if is_he else trip['cover_alt_en']
    tags = render_tags(trip['tags_he'] if is_he else trip['tags_en'])

    def figure(s: dict) -> str:
        alt = e(s['alt_he'] if is_he else s['alt_en'])
        cap = e(s['cap_he'] if is_he else s['cap_en'])
        if s['type'] == 'clip':
            media = (f'<video data-clip muted loop playsinline preload="none" '
                     f'poster="{IMG}/{s["poster"]}" width="{s["w"]}" height="{s["h"]}" '
                     f'aria-label="{alt}"><source src="{IMG}/{s["src"]}" type="video/mp4" /></video>')
            cls = 'album-figure album-figure-clip'
        else:
            media = f'<img src="{IMG}/{s["src"]}" alt="{alt}" loading="lazy" decoding="async" width="{s["w"]}" height="{s["h"]}">'
            cls = 'album-figure'
        return (f'        <figure class="{cls}">\n          {media}\n'
                f'          <figcaption>{cap}</figcaption>\n        </figure>')

    # Group consecutive photos/clips into a gallery (a single one shows at a
    # natural size); story blocks break the groups and span full width.
    blocks = []
    run: list[dict] = []

    def flush_run() -> None:
        if not run:
            return
        figs = '\n'.join(figure(s) for s in run)
        if len(run) == 1:
            blocks.append(f'      <div class="album-solo">\n{figs}\n      </div>')
        else:
            blocks.append(f'      <div class="album-gallery">\n{figs}\n      </div>')
        run.clear()

    for s in trip['sections']:
        if s['type'] == 'story':
            flush_run()
            text = e(s['he'] if is_he else s['en'])
            blocks.append(f'      <section class="album-story">\n        <p>{text}</p>\n      </section>')
        else:
            run.append(s)
    flush_run()
    sections_html = '\n'.join(blocks)

    return f'''<main id="main" tabindex="-1" class="site-shell album">
  <a class="album-back" href="{journeys_href}">{arrow} {back}</a>
  <header class="album-hero">
    <div class="album-hero-media">
      <img src="{IMG}/{trip['cover']}" alt="{e(cover_alt)}" width="{trip['cover_w']}" height="{trip['cover_h']}" fetchpriority="high">
    </div>
    <div class="album-hero-copy">
      <span class="kicker">{e(kicker)}</span>
      <h1>{e(title)} · {e(trip['dates'])}</h1>
      <p class="album-intro">{e(intro)}</p>
      <div class="meta-line">{e(meta_line)}</div>
      <div class="tags">{tags}</div>
    </div>
  </header>
  <div class="album-body">
{sections_html}
  </div>
  <a class="album-back album-back-end" href="{journeys_href}">{arrow} {back}</a>
</main>'''


def render_album_page(trip: dict, lang: str) -> str:
    meta = album_meta(trip, lang)
    prefix = '../' * meta['slug'].count('/') or './'
    return f'''<!DOCTYPE html>
<html lang="{meta['lang']}" dir="{meta['dir']}">
{render_head(meta)}
<body>

{render_header(meta)}


{render_album_main(trip, lang)}


{render_footer(meta['lang'])}

<script src="{prefix}index.js?v={JS_VER}" defer></script>
</body>
</html>
'''


def render_trip_previews(lang: str) -> str:
    is_he = lang == 'he'
    view = 'לאלבום המלא' if is_he else 'View album'
    arrow = '←' if is_he else '→'
    cards = []
    for trip in TRIPS:
        href = f'/he/trips/{trip["slug"]}.html' if is_he else f'/trips/{trip["slug"]}.html'
        title = trip['title_he'] if is_he else trip['title_en']
        kicker = trip['kicker_he'] if is_he else trip['kicker_en']
        state = trip['state_he'] if is_he else trip['state_en']
        teaser = trip['teaser_he'] if is_he else trip['teaser_en']
        meta_line = trip['meta_he'] if is_he else trip['meta_en']
        cover_alt = trip['cover_alt_he'] if is_he else trip['cover_alt_en']
        tags = render_tags(trip['tags_he'] if is_he else trip['tags_en'])
        cls = 'surface-card trip-card trip-card-featured' if trip.get('featured') else 'surface-card trip-card'
        open_label = f'{title} {trip["dates"]}'
        cards.append(f'''        <article class="{cls}">
          <a class="trip-cover" href="{href}" aria-label="{e(open_label)}">
            <img src="{IMG}/{trip['cover']}" alt="{e(cover_alt)}" loading="lazy" decoding="async" width="{trip['cover_w']}" height="{trip['cover_h']}">
          </a>
          <div class="trip-copy">
            <div class="trip-headline">
              <div>
                <span class="kicker">{e(kicker)}</span>
                <h3>{e(title)} · {e(trip['dates'])}</h3>
              </div>
              <span class="trip-state trip-state-archive">{e(state)}</span>
            </div>
            <p class="trip-teaser">{e(teaser)}</p>
            <div class="meta-line">{e(meta_line)}</div>
            <div class="tags">{tags}</div>
            <a class="trip-album-link" href="{href}">{view} <span aria-hidden="true">{arrow}</span></a>
          </div>
        </article>''')
    return '\n\n'.join(cards)


def render_sitemap() -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<?xml-stylesheet type="text/xsl" href="sitemap.xsl"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    album_metas = [album_meta(trip, lang) for trip in TRIPS for lang in ('en', 'he')]
    for meta in list(PAGES.values()) + album_metas:
        canonical = f'{SITE_URL}/{meta["slug"]}' if meta['slug'] else f'{SITE_URL}/'
        lines.extend([
            '  <url>',
            f'    <loc>{canonical}</loc>',
            f'    <lastmod>{LASTMOD}</lastmod>',
            f'    <xhtml:link rel="alternate" hreflang="en" href="{absolute_url(meta["en_href"])}"/>',
            f'    <xhtml:link rel="alternate" hreflang="en-US" href="{absolute_url(meta["en_href"])}"/>',
            f'    <xhtml:link rel="alternate" hreflang="he" href="{absolute_url(meta["he_href"])}"/>',
            f'    <xhtml:link rel="alternate" hreflang="he-IL" href="{absolute_url(meta["he_href"])}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{absolute_url(meta["x_default"])}"/>',
            '  </url>',
        ])
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def replace_section(text: str, start_tag: str, end_tag: str, replacement: str, where: str = '') -> str:
    start = text.find(start_tag)
    if start == -1:
        raise ValueError(f'marker {start_tag!r} not found in {where or "page"}')
    end = text.find(end_tag, start)
    if end == -1:
        raise ValueError(f'closing marker {end_tag!r} not found after {start_tag!r} in {where or "page"}')
    return text[:start] + replacement + text[end + len(end_tag):]


def sync_page(path_str: str, meta: dict[str, str]) -> bool:
    path = REPO / path_str
    original = path.read_text()
    updated = replace_section(original, '<head>', '</head>', render_head(meta), where=path_str)
    updated = replace_section(updated, '<header class="site-header">', '</header>', render_header(meta), where=path_str)
    updated = replace_section(updated, '<footer class="site-footer">', '</footer>', render_footer(meta['lang']), where=path_str)
    if path_str in ('journeys.html', 'he/journeys.html'):
        previews = render_trip_previews(meta['lang'])
        block = f'<!-- TRIPS:START -->\n{previews}\n        <!-- TRIPS:END -->'
        updated = replace_section(updated, '<!-- TRIPS:START -->', '<!-- TRIPS:END -->', block, where=path_str)
    html_open = f'<html lang="{meta["lang"]}" dir="{meta["dir"]}">'
    for line in original.splitlines():
        if line.startswith('<html '):
            updated = updated.replace(line, html_open, 1)
            break
    if updated != original:
        path.write_text(updated)
        return True
    return False


def write_if_changed(path: Path, content: str) -> bool:
    old = path.read_text() if path.exists() else None
    if old != content:
        path.write_text(content)
        return True
    return False


# Keys every trip must define so BOTH the album page and the journeys preview
# card render. Without this check a trip missing, say, 'state_en' builds its
# album fine but throws a cryptic KeyError when journeys.html regenerates.
_REQUIRED_TRIP_KEYS = (
    'slug', 'dates', 'title_en', 'title_he', 'kicker_en', 'kicker_he',
    'state_en', 'state_he', 'teaser_en', 'teaser_he', 'meta_en', 'meta_he',
    'intro_en', 'intro_he', 'cover', 'cover_w', 'cover_h',
    'cover_alt_en', 'cover_alt_he', 'tags_en', 'tags_he', 'sections',
)


def validate_trips() -> None:
    for trip in TRIPS:
        missing = [k for k in _REQUIRED_TRIP_KEYS if k not in trip]
        if missing:
            slug = trip.get('slug', '<no slug>')
            raise ValueError(
                f"trip {slug!r} is missing required key(s): {', '.join(missing)}")


def main() -> int:
    validate_trips()
    changed = []
    for path_str, meta in PAGES.items():
        if sync_page(path_str, meta):
            changed.append(path_str)
    for trip in TRIPS:
        for lang in ('en', 'he'):
            meta = album_meta(trip, lang)
            target = REPO / meta['slug']
            target.parent.mkdir(parents=True, exist_ok=True)
            if write_if_changed(target, render_album_page(trip, lang)):
                changed.append(meta['slug'])
    sitemap = render_sitemap()
    if write_if_changed(REPO / 'sitemap.xml', sitemap):
        changed.append('sitemap.xml')
    if changed:
        print('Updated:')
        for item in changed:
            print(f'  - {item}')
    else:
        print('No changes needed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
