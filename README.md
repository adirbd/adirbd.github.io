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

This rejects oversized files (images > 400KB, videos > 3MB) and files whose
extension doesn't match their real type (e.g. an HTML error page saved as `.jpg`).

## Short video clips in Journeys

A trip gallery cell can hold a short looping clip instead of a photo. Clips are
muted, loop, and only download + play once they scroll into view (handled by
`index.js`); under `prefers-reduced-motion` they stay paused on their poster.

Drop-in markup (replace an image `<div>` in a `.trip-gallery`):

```html
<div>
  <video data-clip muted loop playsinline preload="none"
         poster="/images/journeys/CLIP-poster.jpg" width="768" height="1024">
    <source src="/images/journeys/CLIP.webm" type="video/webm" />
    <source src="/images/journeys/CLIP.mp4" type="video/mp4" />
  </video>
</div>
```

Encode a source clip (needs `ffmpeg`; keep it ~10–15s, 720p, **no audio**):

```bash
# MP4 (H.264) — universal fallback
ffmpeg -i in.mov -t 15 -an -vf "scale=-2:720" -c:v libx264 -profile:v main -crf 28 -movflags +faststart images/journeys/CLIP.mp4
# WebM (VP9) — smaller, modern browsers
ffmpeg -i in.mov -t 15 -an -vf "scale=-2:720" -c:v libvpx-vp9 -crf 34 -b:v 0 images/journeys/CLIP.webm
# Poster (first frame), then compress like any photo
ffmpeg -i in.mov -vframes 1 -q:v 3 images/journeys/CLIP-poster.jpg
```

Keep each clip under the 3MB asset-guard cap.

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
