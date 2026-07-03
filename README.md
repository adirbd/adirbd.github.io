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
It also appends a content-hash query to the asset links (`index.css?v=…`,
`index.js?v=…`) on every page so browsers fetch the latest CSS/JS after a
change; the version updates automatically whenever those files change. The 404
page's theme-boot script and stylesheet link are kept in sync too.

Image assets are validated with:

```bash
bash scripts/check_assets.sh
```

This rejects oversized files (images > 400KB, videos > 3MB) and files whose
extension doesn't match their real type (e.g. an HTML error page saved as `.jpg`).

## Trip albums

Each trip on the Journeys page has its own album page under `/trips/<slug>.html`
(and `/he/trips/<slug>.html`). Both the album pages and the preview cards on the
Journeys index are **generated** from the `TRIPS` list in
`scripts/sync_shared.py` — they are not hand-edited.

To add or change a trip:

1. Add the photos to `images/journeys/` (compress them; see the asset guard).
2. Add or edit the trip's entry in `TRIPS` (bilingual title/teaser/intro, cover,
   and an ordered `sections` list of `story` / `photo` / `clip` blocks).
3. Run `python3 scripts/sync_shared.py`.

This writes the EN + HE album pages, the Journeys preview cards (between the
`<!-- TRIPS:START -->` / `<!-- TRIPS:END -->` markers), and the sitemap entries.

## Video clips in albums

A trip's `sections` can hold a short looping clip instead of a photo — a
`{'type': 'clip', ...}` block with `src` (an `.mp4` in `images/journeys/`),
`poster`, `w`/`h`, and bilingual `alt`/`cap`. The generator emits a muted,
looping `<video preload="none">` that only downloads and plays once it scrolls
into view (`index.js`); under `prefers-reduced-motion` it stays on its poster.

Encode a source clip to a muted, web-friendly MP4 (needs `ffmpeg`; keep it short
and under the 3MB asset-guard cap), then grab a poster frame:

```bash
# Portrait clip → 720 wide (use scale=960:-2 for a landscape clip)
ffmpeg -i in.mov -an -vf "scale=720:-2,fps=30" -c:v libx264 -profile:v main \
  -crf 30 -preset veryfast -movflags +faststart -pix_fmt yuv420p \
  images/journeys/CLIP.mp4
# Poster frame — size-checked like any image (< 400KB)
ffmpeg -ss 1 -i in.mov -frames:v 1 -vf "scale=720:-2" -q:v 5 \
  images/journeys/CLIP-poster.jpg
```

Match the source's native width where possible (phone clips are usually 720px
wide) so the clip stays sharp at the column width. Then reference `CLIP.mp4` /
`CLIP-poster.jpg` from a `clip` block in `TRIPS` and run
`python3 scripts/sync_shared.py`.

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
