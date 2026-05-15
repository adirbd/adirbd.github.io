#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SITE_URL = 'https://www.adirbd.com'
PERSON_SCHEMA = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    'name': 'Adir Ben David',
    'alternateName': ['Adirbd', 'אדיר בן דוד'],
    'jobTitle': 'DevOps Engineer',
    'worksFor': {'@type': 'Organization', 'name': 'Check Point'},
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Tel Aviv', 'addressCountry': 'IL'},
    'url': f'{SITE_URL}/',
    'sameAs': [
        'https://github.com/adirbd',
        'https://www.linkedin.com/in/adirbd/',
        'https://www.instagram.com/adirbd/',
        'https://www.youtube.com/@adirbd',
        'https://x.com/adirbd',
    ],
    'knowsAbout': ['DevOps', 'Infrastructure', 'Systems', 'Automation', 'Cloud', 'Kubernetes', 'Terraform', 'Transportation', 'Urban systems'],
}

EN_NAV = [
    ('about.html', 'About'),
    ('work.html', 'Work'),
    ('now.html', 'Now'),
    ('journeys.html', 'Journeys'),
    ('links.html', 'Links'),
    ('contact.html', 'Contact'),
]
HE_NAV = [
    ('/he/contact.html', 'יצירת קשר'),
    ('/he/links.html', 'קישורים'),
    ('/he/journeys.html', 'מסעות'),
    ('/he/now.html', 'עכשיו'),
    ('/he/work.html', 'עבודה'),
    ('/he/about.html', 'אודות'),
]
SOCIALS = [
    ('https://github.com/adirbd', 'GitHub', '/images/github.svg', 'GitHub'),
    ('https://www.linkedin.com/in/adirbd/', 'LinkedIn', '/images/linkedin.svg', 'LinkedIn'),
    ('https://x.com/adirbd', 'X', '/images/twitter.svg', 'X'),
    ('https://www.instagram.com/adirbd/', 'Instagram', '/images/instagram.svg', 'Instagram'),
    ('https://www.youtube.com/@adirbd', 'YouTube', '/images/youtube.svg', 'YouTube'),
]
PAGES = {
    'index.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'index.html', 'switch': '/he/', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Adir Ben David (Adirbd)',
        'description': 'Personal website of Adir Ben David — DevOps engineer focused on practical infrastructure, systems thinking, and long-term value.',
        'slug': '', 'en_href': f'{SITE_URL}/', 'he_href': '/he/', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'about.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'about.html', 'switch': '/he/about.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'About | Adir Ben David',
        'description': 'About Adir Ben David: DevOps, infrastructure, systems thinking, transportation, and public-scale curiosity.',
        'slug': 'about.html', 'en_href': f'{SITE_URL}/about.html', 'he_href': '/he/about.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
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
        'description': 'A warmer future home for places, movement, selected photos, and travel notes by Adir Ben David.',
        'slug': 'journeys.html', 'en_href': f'{SITE_URL}/journeys.html', 'he_href': '/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'links.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'links.html', 'switch': '/he/links.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Links | Adir Ben David',
        'description': 'Useful links and public profiles for Adir Ben David.',
        'slug': 'links.html', 'en_href': f'{SITE_URL}/links.html', 'he_href': '/he/links.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'contact.html': {
        'lang': 'en', 'dir': 'ltr', 'home': '/', 'active': 'contact.html', 'switch': '/he/contact.html', 'switch_from': 'EN', 'switch_to': 'HE',
        'title': 'Contact | Adir Ben David',
        'description': 'Contact Adir Ben David for collaboration, ideas, or professional conversations.',
        'slug': 'contact.html', 'en_href': f'{SITE_URL}/contact.html', 'he_href': '/he/contact.html', 'x_default': f'{SITE_URL}/', 'locale': 'en_US', 'locale_alt': 'he_IL'
    },
    'he/index.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/index.html', 'switch': '/', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'אדיר בן דוד (Adirbd)',
        'description': 'האתר האישי של אדיר בן דוד — DevOps, תשתיות, חשיבה מערכתית ועניין במערכות גדולות לאורך זמן.',
        'slug': 'he/', 'en_href': '/', 'he_href': f'{SITE_URL}/he/', 'x_default': '/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/about.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/about.html', 'switch': '/about.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'אודות | אדיר בן דוד',
        'description': 'על אדיר בן דוד: DevOps, תשתיות, חשיבה מערכתית, תחבורה וסקרנות בקנה מידה ציבורי.',
        'slug': 'he/about.html', 'en_href': '/about.html', 'he_href': f'{SITE_URL}/he/about.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
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
        'description': 'בית חם יותר למקומות, לתנועה, לתמונות נבחרות ולרשמי דרך של אדיר בן דוד.',
        'slug': 'he/journeys.html', 'en_href': '/journeys.html', 'he_href': f'{SITE_URL}/he/journeys.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/links.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/links.html', 'switch': '/links.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'קישורים | אדיר בן דוד',
        'description': 'קישורים שימושיים ופרופילים ציבוריים של אדיר בן דוד.',
        'slug': 'he/links.html', 'en_href': '/links.html', 'he_href': f'{SITE_URL}/he/links.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
    },
    'he/contact.html': {
        'lang': 'he', 'dir': 'rtl', 'home': '/he/', 'active': '/he/contact.html', 'switch': '/contact.html', 'switch_from': 'HE', 'switch_to': 'EN',
        'title': 'יצירת קשר | אדיר בן דוד',
        'description': 'צרו קשר עם אדיר בן דוד לשיתופי פעולה, רעיונות או שיחות מקצועיות.',
        'slug': 'he/contact.html', 'en_href': '/contact.html', 'he_href': f'{SITE_URL}/he/contact.html', 'x_default': f'{SITE_URL}/', 'locale': 'he_IL', 'locale_alt': 'en_US'
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
    prefix = '../' if meta['lang'] == 'he' else './'
    canonical = f'{SITE_URL}/{meta["slug"]}' if meta['slug'] else f'{SITE_URL}/'
    webpage_schema = {
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        'url': canonical,
        'name': meta['title'],
        'inLanguage': meta['lang'],
        'description': meta['description'],
        'isPartOf': {'@type': 'WebSite', 'url': f'{SITE_URL}/', 'name': 'Adir Ben David'},
    }
    return f'''<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['description']}" />
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
  <link rel="canonical" href="{canonical}" />
  
  <link rel="alternate" hreflang="en" href="{meta['en_href']}" />
  <link rel="alternate" hreflang="en-US" href="{meta['en_href']}" />
  <link rel="alternate" hreflang="he" href="{meta['he_href']}" />
  <link rel="alternate" hreflang="he-IL" href="{meta['he_href']}" />
  <link rel="alternate" hreflang="x-default" href="{meta['x_default']}" />
  <link rel="icon" type="image/svg+xml" href="{prefix}images/favicon-transit.svg" />
  <link rel="alternate icon" type="image/png" href="{prefix}images/favicon.png" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="Adir Ben David" />
  <meta property="og:locale" content="{meta['locale']}" />
  <meta property="og:locale:alternate" content="{meta['locale_alt']}" />
  <meta property="og:title" content="{meta['title']}" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:image" content="{SITE_URL}/images/og-image.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{meta['title']}" />
  <meta name="twitter:description" content="{meta['description']}" />
  <meta name="twitter:image" content="{SITE_URL}/images/og-image.png" />
  <script type="application/ld+json">{json_script(PERSON_SCHEMA)}</script>
  <script type="application/ld+json">{json_script(webpage_schema)}</script>
  <link rel="preload" href="{prefix}fonts/HKGrotesk-Regular.woff" as="font" type="font/woff" crossorigin />
  <link rel="preload" href="{prefix}fonts/Jost-Regular.ttf" as="font" type="font/truetype" crossorigin />
  <link rel="stylesheet" href="{prefix}index.css" />
</head>'''


def render_header(meta: dict[str, str]) -> str:
    is_he = meta['lang'] == 'he'
    nav = render_nav(HE_NAV if is_he else EN_NAV, meta['active'])
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
    if lang == 'he':
        home = '/he/'
        about = '/he/about.html'
        contact = '/he/contact.html'
        line = 'נבנה כך שיישאר פשוט, דו־לשוני וקל לתחזוקה.'
        labels = ('בית', 'אודות', 'יצירת קשר')
    else:
        home = '/'
        about = '/about.html'
        contact = '/contact.html'
        line = 'Built to stay simple, bilingual, and easy to maintain.'
        labels = ('Home', 'About', 'Contact')
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
    <nav class="footer-nav"><a href="{home}">{labels[0]}</a><a href="{about}">{labels[1]}</a><a href="{contact}">{labels[2]}</a></nav>
    <div class="socials">{socials}</div>
  </div>
</footer>'''


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
    html_open = f'<html lang="{meta["lang"]}" dir="{meta["dir"]}">'
    for line in original.splitlines():
        if line.startswith('<html '):
            updated = updated.replace(line, html_open, 1)
            break
    if updated != original:
        path.write_text(updated)
        return True
    return False


def main() -> int:
    changed = []
    for path_str, meta in PAGES.items():
        if sync_page(path_str, meta):
            changed.append(path_str)
    if changed:
        print('Updated:')
        for item in changed:
            print(f'  - {item}')
    else:
        print('No changes needed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
