# Adir Ben David - Personal Portfolio

Bilingual (English/Hebrew) personal portfolio website.

## Live Site

- English: https://www.adirbd.com/
- Hebrew: https://www.adirbd.com/he/

## Features

- Bilingual support (English/Hebrew) with separate pages
- RTL support for Hebrew
- SEO optimized with hreflang tags
- Responsive design
- Clean and minimal design

## Technology

- Pure HTML, CSS, and JavaScript
- No frameworks or runtime dependencies
- GitHub Pages hosting
- Playwright for smoke and link checks

## Maintenance

Shared head/header/footer markup (and the sitemap) is synced with:

```bash
python3 scripts/sync_shared.py
```

Run it after editing any page; CI fails if pages drift from the script's output.

Image assets are validated with:

```bash
bash scripts/check_assets.sh
```

This rejects files over 400KB and files whose extension doesn't match their
real type (e.g. an HTML error page saved as `.jpg`).

## Validation

Install the test dependency once:

```bash
npm install
```

Run the site smoke tests and internal link checks:

```bash
npm run test:e2e
```

The Playwright config starts a local static server from the repository root. Set
`BASE_URL` to override the default `http://127.0.0.1:8000`.

## CI

`.github/workflows/ci.yml` runs on every push and pull request:

1. Sync drift check (`sync_shared.py` + clean `git diff`)
2. Asset guard (`check_assets.sh`)
3. Playwright smoke and link tests
