#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

EN_NAV = [
    ("about.html", "About"),
    ("work.html", "Work"),
    ("now.html", "Now"),
    ("journeys.html", "Journeys"),
    ("links.html", "Links"),
    ("contact.html", "Contact"),
]

HE_NAV = [
    ("/he/contact.html", "יצירת קשר"),
    ("/he/links.html", "קישורים"),
    ("/he/journeys.html", "מסעות"),
    ("/he/now.html", "עכשיו"),
    ("/he/work.html", "עבודה"),
    ("/he/about.html", "אודות"),
]

SOCIALS = [
    ("https://github.com/adirbd", "GitHub", "/images/github.svg", "GitHub"),
    ("https://www.linkedin.com/in/adirbd/", "LinkedIn", "/images/linkedin.svg", "LinkedIn"),
    ("https://x.com/adirbd", "X", "/images/twitter.svg", "X"),
    ("https://www.instagram.com/adirbd/", "Instagram", "/images/instagram.svg", "Instagram"),
    ("https://www.youtube.com/@adirbd", "YouTube", "/images/youtube.svg", "YouTube"),
]

PAGES = {
    "index.html": {"lang": "en", "home": "/", "active": "index.html", "switch": "/he/", "switch_from": "EN", "switch_to": "HE"},
    "about.html": {"lang": "en", "home": "/", "active": "about.html", "switch": "/he/about.html", "switch_from": "EN", "switch_to": "HE"},
    "work.html": {"lang": "en", "home": "/", "active": "work.html", "switch": "/he/work.html", "switch_from": "EN", "switch_to": "HE"},
    "now.html": {"lang": "en", "home": "/", "active": "now.html", "switch": "/he/now.html", "switch_from": "EN", "switch_to": "HE"},
    "journeys.html": {"lang": "en", "active": "journeys.html", "home": "/", "switch": "/he/journeys.html", "switch_from": "EN", "switch_to": "HE"},
    "links.html": {"lang": "en", "home": "/", "active": "links.html", "switch": "/he/links.html", "switch_from": "EN", "switch_to": "HE"},
    "contact.html": {"lang": "en", "home": "/", "active": "contact.html", "switch": "/he/contact.html", "switch_from": "EN", "switch_to": "HE"},
    "he/index.html": {"lang": "he", "home": "/he/", "active": "/he/index.html", "switch": "/", "switch_from": "HE", "switch_to": "EN"},
    "he/about.html": {"lang": "he", "home": "/he/", "active": "/he/about.html", "switch": "/about.html", "switch_from": "HE", "switch_to": "EN"},
    "he/work.html": {"lang": "he", "home": "/he/", "active": "/he/work.html", "switch": "/work.html", "switch_from": "HE", "switch_to": "EN"},
    "he/now.html": {"lang": "he", "home": "/he/", "active": "/he/now.html", "switch": "/now.html", "switch_from": "HE", "switch_to": "EN"},
    "he/journeys.html": {"lang": "he", "home": "/he/", "active": "/he/journeys.html", "switch": "/journeys.html", "switch_from": "HE", "switch_to": "EN"},
    "he/links.html": {"lang": "he", "home": "/he/", "active": "/he/links.html", "switch": "/links.html", "switch_from": "HE", "switch_to": "EN"},
    "he/contact.html": {"lang": "he", "home": "/he/", "active": "/he/contact.html", "switch": "/contact.html", "switch_from": "HE", "switch_to": "EN"},
}


def render_nav(items: list[tuple[str, str]], active: str) -> str:
    rendered = []
    for href, label in items:
        current = ' aria-current="page"' if href == active else ''
        rendered.append(f'<li><a href="{href}"{current}>{label}</a></li>')
    return ''.join(rendered)


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
    updated = replace_section(original, '<header class="site-header">', '</header>', render_header(meta))
    updated = replace_section(updated, '<footer class="site-footer">', '</footer>', render_footer(meta['lang']))
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
