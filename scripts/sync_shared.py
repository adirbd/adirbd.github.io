#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_URL = 'https://www.adirbd.com'
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
        'cloud side — building and managing infrastructure on AWS and Azure with Terraform, Terragrunt, and '
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
    ('https://github.com/adirbd', 'GitHub', '/images/github.svg', 'GitHub'),
    ('https://www.linkedin.com/in/adirbd/', 'LinkedIn', '/images/linkedin.svg', 'LinkedIn'),
    ('https://x.com/adirbd', 'X', '/images/twitter.svg', 'X'),
    ('https://www.instagram.com/adirbd/', 'Instagram', '/images/instagram.svg', 'Instagram'),
    ('https://www.facebook.com/adirbd/', 'Facebook', '/images/facebook.svg', 'Facebook'),
    ('https://www.youtube.com/@adirbd', 'YouTube', '/images/youtube.svg', 'YouTube'),
]
PAGES = {
    'index.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': '/', 'page_type': 'ProfilePage', 'switch': '/he/', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Adir Ben David (Adirbd)',
        'description': 'Personal website of Adir Ben David — DevOps engineer focused on practical infrastructure, systems thinking, and long-term value.',
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
        'description': 'A current snapshot of work, interests, and attention right now.',
        'slug': 'now.html', 'en_href': f'{SITE_URL}/now.html', 'he_href': '/he/now.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'journeys.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'journeys.html', 'switch': '/he/journeys.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Journeys | Adir Ben David',
        'description': 'Places, movement, and selected photos from trips by Adir Ben David — Japan, the Alps, Thailand, and more.',
        'slug': 'journeys.html', 'en_href': f'{SITE_URL}/journeys.html', 'he_href': '/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'connect.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'connect.html', 'switch': '/he/connect.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Connect | Adir Ben David',
        'description': 'Reach Adir Ben David — on GitHub, LinkedIn, X, Instagram, YouTube, or by email — for collaboration, ideas, or a thoughtful hello.',
        'slug': 'connect.html', 'en_href': f'{SITE_URL}/connect.html', 'he_href': '/he/connect.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'he/index.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/', 'page_type': 'ProfilePage', 'switch': '/', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'אדיר בן דוד (Adirbd)',
        'description': 'האתר האישי של אדיר בן דוד — DevOps, תשתיות, חשיבה מערכתית ועניין במערכות גדולות לאורך זמן.',
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
        'description': 'צילום מצב עדכני של עבודה, תחומי עניין ומה תופס את תשומת הלב עכשיו.',
        'slug': 'he/now.html', 'en_href': '/now.html', 'he_href': f'{SITE_URL}/he/now.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/journeys.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/journeys.html', 'switch': '/journeys.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'מסעות | אדיר בן דוד',
        'description': 'מקומות, תנועה ותמונות נבחרות מהטיולים של אדיר בן דוד — יפן, האלפים, תאילנד ועוד.',
        'slug': 'he/journeys.html', 'en_href': '/journeys.html', 'he_href': f'{SITE_URL}/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/connect.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/connect.html', 'switch': '/connect.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'בואו נדבר | אדיר בן דוד',
        'description': 'איך ליצור קשר עם אדיר בן דוד — ב־GitHub, LinkedIn, X, Instagram, YouTube או באימייל — לשיתופי פעולה, רעיונות או סתם שלום.',
        'slug': 'he/connect.html', 'en_href': '/connect.html', 'he_href': f'{SITE_URL}/he/connect.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
}


def json_script(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=6)


def render_nav(items: list[tuple[str, str]], active: str) -> str:
    rendered = []
    for href, label in items:
        current = ' aria-current="page"' if href == active else ''
        rendered.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return ''.join(rendered)


def render_head(meta: dict[str, str]) -> str:
    # Relative depth to the site root: one '../' per directory in the slug.
    # '' -> './', 'work.html' -> './', 'he/work.html' -> '../',
    # 'trips/japan.html' -> '../', 'he/trips/japan.html' -> '../../'.
    prefix = '../' * meta['slug'].count('/') or './'
    canonical = f'{SITE_URL}/{meta["slug"]}' if meta['slug'] else f'{SITE_URL}/'
    og_image = absolute_url(meta.get('og_image', '/images/og-image.png'))
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
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />
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
  <meta property="og:title" content="{meta['title']}" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:site" content="@adirbd" />
  <meta name="twitter:creator" content="@adirbd" />
  <meta name="twitter:title" content="{meta['title']}" />
  <meta name="twitter:description" content="{meta['description']}" />
  <meta name="twitter:image" content="{og_image}" />
  <script type="application/ld+json">{json_script(PERSON_SCHEMA)}</script>
  <script type="application/ld+json">{json_script(webpage_schema)}</script>
  {THEME_BOOT_SCRIPT}
  <link rel="preload" href="{prefix}fonts/HKGrotesk-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="{prefix}fonts/Jost-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="{prefix}index.css" />
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
    return f'''<header class="site-header">
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
        <a class="lang-switch" href="{meta['switch']}" hreflang="{switch_lang}" lang="{switch_lang}"><span class="muted">{meta['switch_from']}</span><span>→</span><strong>{meta['switch_to']}</strong></a>
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
        f'<a href="{h if h.startswith("/") else f"/{h}"}">{label}</a>'
        for h, label in nav_items
    )
    socials = ''.join(
        f'<a href="{href}" target="_blank" rel="noopener noreferrer" aria-label="{aria}"><img src="{icon}" alt="{alt}"></a>'
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
        'teaser_en': 'A long rail loop through Osaka, Nara, Kyoto and Tokyo, out to the lakes under Mount Fuji — and a Rome finale before the flight home.',
        'teaser_he': 'מסע ארוך ברכבות דרך אוסקה, נארה, קיוטו וטוקיו, ומשם לאגמים שמתחת להר פוג\'י — וסיום ברומא לפני הטיסה הביתה.',
        'cover': 'japan-fuji-blossoms.jpg', 'cover_w': 768, 'cover_h': 1024,
        'cover_alt_en': 'Mount Fuji rising above cherry blossoms',
        'cover_alt_he': 'הר פוג\'י מעל פריחת הדובדבן',
        'intro_en': 'Japan was a long loop by rail — Osaka, Nara, Kyoto, Tokyo, and the lakes under Mount Fuji — and it ended, unexpectedly, with a layover in Rome on the way home.',
        'intro_he': 'יפן היה מסע ארוך ברכבות — אוסקה, נארה, קיוטו, טוקיו, והאגמים שמתחת להר פוג\'י — והוא הסתיים, באופן לא צפוי, בעצירת ביניים ברומא בדרך הביתה.',
        # Photos run in travel order: Kyoto -> Tokyo -> Fuji -> Rome. Osaka and
        # Nara photos will be added at the front when they arrive.
        'sections': [
            {'type': 'story', 'en': 'After Osaka and Nara, Kyoto slowed things down — the bamboo paths of Arashiyama, a good bowl of ramen, and a detour to the Nintendo Museum just outside the city.',
             'he': 'אחרי אוסקה ונארה, קיוטו האטה את הקצב — שבילי הבמבוק של אראשיאמה, קערת ראמן טובה, וקפיצה למוזיאון נינטנדו ממש מחוץ לעיר.'},
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
            {'type': 'story', 'en': 'Then Tokyo — fast, loud, and easy to love. Tokyo Tower up close, and a written wish left at a shrine.',
             'he': 'אחר כך טוקיו — מהירה, רועשת וקל להתאהב בה. מגדל טוקיו מקרוב, ומשאלה כתובה שהשארתי במקדש.'},
            {'type': 'photo', 'src': 'tokyo-tower.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir below the orange lattice of Tokyo Tower', 'alt_he': 'אדיר מתחת לשלד הכתום של מגדל טוקיו',
             'cap_en': 'Under the orange lattice of Tokyo Tower.', 'cap_he': 'מתחת לשלד הכתום של מגדל טוקיו.'},
            {'type': 'photo', 'src': 'shrine-wish.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir holding a written wish envelope at a shrine in Tokyo', 'alt_he': 'אדיר מחזיק מעטפת משאלה במקדש בטוקיו',
             'cap_en': 'A written wish at a Tokyo shrine.', 'cap_he': 'משאלה כתובה במקדש בטוקיו.'},
            {'type': 'story', 'en': 'Out to Mount Fuji — the little Fujikyu line, a clear day by Lake Kawaguchi, and the Chureito pagoda above the blossoms.',
             'he': 'ומשם להר פוג\'י — קו הפוג\'יקיו הקטן, יום בהיר על שפת אגם קוואגוצ\'י, ופגודת צ\'וריטו מעל הפריחה.'},
            {'type': 'clip', 'src': 'japan-rail.mp4', 'poster': 'japan-rail-poster.jpg', 'w': 540, 'h': 960,
             'alt_en': 'An orange Mt Fuji line train arriving at a platform', 'alt_he': 'רכבת כתומה של קו הר פוג\'י נכנסת לתחנה',
             'cap_en': 'Waiting on the platform for the Fujikyu line.', 'cap_he': 'ממתין על הרציף לרכבת הפוג\'יקיו.'},
            {'type': 'photo', 'src': 'fuji-lakeside.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir at a lakeside with Mount Fuji behind him', 'alt_he': 'אדיר על שפת אגם כשהר פוג\'י מאחוריו',
             'cap_en': 'A clear day across Lake Kawaguchi from Mount Fuji.', 'cap_he': 'יום בהיר מעבר לאגם קוואגוצ\'י מול הר פוג\'י.'},
            {'type': 'photo', 'src': 'japan-pagoda.jpg', 'w': 360, 'h': 480,
             'alt_en': 'The Chureito pagoda framed by cherry blossoms', 'alt_he': 'פגודת צ\'וריטו ממוסגרת בפריחת דובדבן',
             'cap_en': 'The Chureito pagoda, framed by cherry blossoms.', 'cap_he': 'פגודת צ\'וריטו, ממוסגרת בפריחת דובדבן.'},
            {'type': 'story', 'en': 'The flight home routed through Rome, so the trip ended at the Colosseum at golden hour — an unplanned last chapter.',
             'he': 'הטיסה הביתה עברה דרך רומא, אז הטיול הסתיים מול הקולוסיאום בשעת הזהב — פרק אחרון לא מתוכנן.'},
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
        'teaser_en': 'A snowboard trip in Avoriaz, in the French Alps — chairlifts, long runs, and mountain light from first lift to last.',
        'teaser_he': 'טיול סנובורד באבוריאז שבאלפים הצרפתיים — רכבלים, מסלולים ארוכים, ואור הרים מהרכבל הראשון עד האחרון.',
        'cover': 'snowboard-valley.jpg', 'cover_w': 1024, 'cover_h': 768,
        'cover_alt_en': 'A snowboard resting above a snowy alpine valley and village',
        'cover_alt_he': 'סנובורד מונח מעל עמק וכפר מושלגים',
        'intro_en': 'A week on the snow in Avoriaz, up in the French Alps — part of the huge Portes du Soleil area that spills across into Switzerland.',
        'intro_he': 'שבוע על השלג באבוריאז, גבוה באלפים הצרפתיים — חלק מאזור Portes du Soleil הענק שנמתח עד שווייץ.',
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
        'teaser_en': 'Riding the Matterhorn from both sides — Zermatt in Switzerland and Cervinia in Italy — under one of the most recognizable peaks in the Alps.',
        'teaser_he': 'גלישה על המטרהורן משני הצדדים — צרמט בשווייץ וצ\'רוויניה באיטליה — מתחת לאחת הפסגות המזוהות ביותר באלפים.',
        'cover': 'matterhorn-zermatt.jpg', 'cover_w': 768, 'cover_h': 1024,
        'cover_alt_en': 'The Matterhorn seen from Zermatt, Switzerland',
        'cover_alt_he': 'פסגת המטרהורן מצרמט שבשווייץ',
        'intro_en': 'Riding the Matterhorn from both sides — Zermatt in Switzerland and Cervinia in Italy — under one of the most recognizable peaks in the Alps. You can cross the border mid-mountain and ride down into a different country for lunch.',
        'intro_he': 'גלישה על המטרהורן משני הצדדים — צרמט בשווייץ וצ\'רוויניה באיטליה — מתחת לאחת הפסגות המוכרות באלפים. אפשר לחצות את הגבול באמצע ההר ולגלוש למדינה אחרת בשביל ארוחת צהריים.',
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
        'kicker_en': 'Completed trip', 'kicker_he': 'טיול שכבר קרה',
        'title_en': 'Thailand', 'title_he': 'תאילנד',
        'meta_en': 'Chiang Mai · Pai · the islands · Bangkok', 'meta_he': 'צ\'יאנג מאי · פאי · האיים · בנגקוק',
        'tags_en': ['Jungle', 'Islands', 'Warm weather', 'Elephants'], 'tags_he': ['ג\'ונגל', 'איים', 'מזג אוויר חם', 'פילים'],
        'teaser_en': 'The green, misty north around Chiang Mai and Pai, then the southern islands, ending in Bangkok — a warm, easy pace the whole way.',
        'teaser_he': 'הצפון הירוק והערפילי סביב צ\'יאנג מאי ופאי, ואז האיים בדרום, וסיום בבנגקוק — בקצב חמים ונינוח לכל אורך הדרך.',
        'cover': 'thailand-longtail.jpg', 'cover_w': 880, 'cover_h': 1100,
        'cover_alt_en': 'Adir on a longtail boat between limestone cliffs in Thailand',
        'cover_alt_he': 'אדיר על סירת לונגטייל בין צוקי גיר בתאילנד',
        'intro_en': 'Thailand was really two trips in one — the green, misty north around Chiang Mai and Pai, then the southern islands, winding up in Bangkok before the flight home.',
        'intro_he': 'תאילנד הייתה שני טיולים באחד — הצפון הירוק והערפילי סביב צ\'יאנג מאי ופאי, ואז האיים בדרום, וסיום בבנגקוק לפני הטיסה הביתה.',
        # Travel order: north (Chiang Mai -> Pai -> Chiang Mai) -> southern islands -> Bangkok.
        'sections': [
            {'type': 'story', 'en': 'It started up north — Chiang Mai first, with a morning with elephants and a waterfall you climb by rope, then a run up to Pai for the rice fields.',
             'he': 'זה התחיל בצפון — קודם צ\'יאנג מאי, עם בוקר ליד פילים ומפל שמטפסים עליו עם חבל, ואז קפיצה לפאי בשביל שדות האורז.'},
            {'type': 'photo', 'src': 'thailand-waterfall.jpg', 'w': 886, 'h': 886,
             'alt_en': 'Adir climbing a waterfall by rope, jungle all around', 'alt_he': 'אדיר מטפס על מפל בעזרת חבל, ג\'ונגל מסביב',
             'cap_en': 'Climbing the Sticky Waterfalls near Chiang Mai.', 'cap_he': 'טיפוס על מפלי הדבק ליד צ\'יאנג מאי.'},
            {'type': 'photo', 'src': 'thailand-elephants.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir reaching out to an elephant by a river near Chiang Mai', 'alt_he': 'אדיר מושיט יד לפיל על גדת נהר ליד צ\'יאנג מאי',
             'cap_en': 'Elephants by the river in Mae Taeng, near Chiang Mai.', 'cap_he': 'פילים על גדת הנהר ליד צ\'יאנג מאי.'},
            {'type': 'photo', 'src': 'thailand-rice-bridge.jpg', 'w': 768, 'h': 1024,
             'alt_en': 'Adir with arms spread on a bamboo bridge over rice paddies in Pai', 'alt_he': 'אדיר בידיים פתוחות על גשר במבוק מעל שדות אורז בפאי',
             'cap_en': 'The bamboo bridge over the rice fields in Pai.', 'cap_he': 'גשר הבמבוק מעל שדות האורז בפאי.'},
            {'type': 'story', 'en': 'Then south to the islands — Ko Tao, Phuket, and Koh Phi Phi: blue water, limestone cliffs, and long days on and around the sea.',
             'he': 'ואז דרומה לאיים — קו טאו, פוקט וקו פי פי: מים כחולים, צוקי גיר, וימים ארוכים על הים ולצדו.'},
            {'type': 'photo', 'src': 'thailand-jetski.jpg', 'w': 619, 'h': 1100,
             'alt_en': 'Adir on a jet ski in clear blue water by an island', 'alt_he': 'אדיר על אופנוע ים במים כחולים ליד אי',
             'cap_en': 'Jet ski off the islands.', 'cap_he': 'אופנוע ים מול האיים.'},
            {'type': 'photo', 'src': 'thailand-longtail.jpg', 'w': 880, 'h': 1100,
             'alt_en': 'Adir on a longtail boat between limestone cliffs at Koh Phi Phi', 'alt_he': 'אדיר על סירת לונגטייל בין צוקי גיר בקו פי פי',
             'cap_en': 'A longtail boat between the cliffs at Koh Phi Phi.', 'cap_he': 'סירת לונגטייל בין הצוקים בקו פי פי.'},
            {'type': 'story', 'en': 'A few last days in Bangkok, then the flight home.',
             'he': 'עוד כמה ימים אחרונים בבנגקוק, ואז הטיסה הביתה.'},
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
    }


def render_tags(tags: list[str]) -> str:
    return ''.join(f'<span>{t}</span>' for t in tags)


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
        alt = s['alt_he'] if is_he else s['alt_en']
        cap = s['cap_he'] if is_he else s['cap_en']
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
            text = s['he'] if is_he else s['en']
            blocks.append(f'      <section class="album-story">\n        <p>{text}</p>\n      </section>')
        else:
            run.append(s)
    flush_run()
    sections_html = '\n'.join(blocks)

    return f'''<main class="site-shell album">
  <a class="album-back" href="{journeys_href}">{arrow} {back}</a>
  <header class="album-hero">
    <div class="album-hero-media">
      <img src="{IMG}/{trip['cover']}" alt="{cover_alt}" width="{trip['cover_w']}" height="{trip['cover_h']}" fetchpriority="high">
    </div>
    <div class="album-hero-copy">
      <span class="kicker">{kicker}</span>
      <h1>{title} · {trip['dates']}</h1>
      <p class="album-intro">{intro}</p>
      <div class="meta-line">{meta_line}</div>
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

<script src="{prefix}index.js" defer></script>
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
          <a class="trip-cover" href="{href}" aria-label="{open_label}">
            <img src="{IMG}/{trip['cover']}" alt="{cover_alt}" loading="lazy" decoding="async" width="{trip['cover_w']}" height="{trip['cover_h']}">
          </a>
          <div class="trip-copy">
            <div class="trip-headline">
              <div>
                <span class="kicker">{kicker}</span>
                <h3>{title} · {trip['dates']}</h3>
              </div>
              <span class="trip-state trip-state-archive">{state}</span>
            </div>
            <p class="trip-teaser">{teaser}</p>
            <div class="meta-line">{meta_line}</div>
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


def replace_section(text: str, start_tag: str, end_tag: str, replacement: str) -> str:
    start = text.index(start_tag)
    end = text.index(end_tag, start) + len(end_tag)
    return text[:start] + replacement + text[end:]


def sync_page(path_str: str, meta: dict[str, str]) -> bool:
    path = REPO / path_str
    original = path.read_text()
    updated = replace_section(original, '<head>', '</head>', render_head(meta))
    updated = replace_section(updated, '<header class="site-header">', '</header>', render_header(meta))
    updated = replace_section(updated, '<footer class="site-footer">', '</footer>', render_footer(meta['lang']))
    if path_str in ('journeys.html', 'he/journeys.html'):
        previews = render_trip_previews(meta['lang'])
        block = f'<!-- TRIPS:START -->\n{previews}\n        <!-- TRIPS:END -->'
        updated = replace_section(updated, '<!-- TRIPS:START -->', '<!-- TRIPS:END -->', block)
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


def main() -> int:
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
    if write_if_changed(REPO / 'sitemap', sitemap):
        changed.append('sitemap')
    if changed:
        print('Updated:')
        for item in changed:
            print(f'  - {item}')
    else:
        print('No changes needed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
