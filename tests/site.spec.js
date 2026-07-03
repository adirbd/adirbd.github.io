const { test, expect } = require('@playwright/test');
const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const pages = [
  '/',
  '/work.html',
  '/now.html',
  '/journeys.html',
  '/connect.html',
  '/he/',
  '/he/work.html',
  '/he/now.html',
  '/he/journeys.html',
  '/he/connect.html',
  '/trips/japan.html',
  '/trips/avoriaz.html',
  '/trips/matterhorn.html',
  '/trips/thailand.html',
  '/he/trips/japan.html',
  '/he/trips/avoriaz.html',
  '/he/trips/matterhorn.html',
  '/he/trips/thailand.html',
];

const SITE_URL = 'https://www.adirbd.com';

const isSkippableHref = (href) =>
  !href ||
  href.startsWith('#') ||
  href.startsWith('mailto:') ||
  href.startsWith('tel:') ||
  href.startsWith('javascript:') ||
  href.startsWith('http://') ||
  href.startsWith('https://');

test.describe('site pages', () => {
  for (const path of pages) {
    test(`loads ${path}`, async ({ page }) => {
      const response = await page.goto(path);
      expect(response, `expected ${path} to return a response`).not.toBeNull();
      expect(response.status(), `expected ${path} to load successfully`).toBeLessThan(400);
      await expect(page.locator('main')).toBeVisible();
      await expect(page.locator('h1').first()).toBeVisible();
      await expect(page.locator('form')).toHaveCount(0);
    });
  }

  test('desktop theme toggle persists across reload', async ({ page }) => {
    await page.goto('/');

    const themeToggle = page.locator('[data-theme-toggle]');
    const initialTheme = await page.evaluate(() => document.documentElement.dataset.theme);

    await themeToggle.click();
    const toggledTheme = await page.evaluate(() => document.documentElement.dataset.theme);
    expect(toggledTheme).not.toBe(initialTheme);

    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-theme', toggledTheme);
  });

  test('mobile nav opens and closes cleanly', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/');

    const navToggle = page.locator('[data-nav-toggle]');
    await navToggle.click();
    await expect(page.locator('body')).toHaveClass(/nav-open/);

    await page.keyboard.press('Escape');
    await expect(page.locator('body')).not.toHaveClass(/nav-open/);
  });

  test('no duplicate journey media files', () => {
    const dir = path.join(__dirname, '..', 'images', 'journeys');
    const files = fs.readdirSync(dir).filter((f) => /\.(jpg|jpeg|png|webp|mp4)$/i.test(f));
    const byHash = {};
    for (const f of files) {
      const h = crypto.createHash('md5').update(fs.readFileSync(path.join(dir, f))).digest('hex');
      (byHash[h] = byHash[h] || []).push(f);
    }
    const dups = Object.values(byHash).filter((g) => g.length > 1);
    expect(dups, `duplicate journey media: ${JSON.stringify(dups)}`).toEqual([]);
  });

  test('album media is complete (dims + alt, lazy imgs, poster+source clips)', async ({ page }) => {
    const albums = pages.filter((p) => p.includes('/trips/'));
    for (const path of albums) {
      await page.goto(path);
      const imgs = await page.$$eval('.album-figure img', (els) =>
        els.map((e) => ({ w: e.getAttribute('width'), h: e.getAttribute('height'), alt: e.getAttribute('alt'), loading: e.getAttribute('loading') })),
      );
      expect(imgs.length, `expected album figures on ${path}`).toBeGreaterThan(0);
      for (const im of imgs) {
        expect(Boolean(im.w && im.h), `gallery img needs width+height on ${path}`).toBe(true);
        expect((im.alt || '').length, `gallery img needs alt on ${path}`).toBeGreaterThan(3);
        expect(im.loading, `gallery img should be lazy on ${path}`).toBe('lazy');
      }
      const vids = await page.$$eval('.album-figure video', (els) =>
        els.map((e) => ({ poster: e.getAttribute('poster'), w: e.getAttribute('width'), h: e.getAttribute('height'), src: e.querySelector('source')?.getAttribute('src'), label: e.getAttribute('aria-label') })),
      );
      for (const v of vids) {
        expect(Boolean(v.poster), `clip needs poster on ${path}`).toBe(true);
        expect(Boolean(v.src), `clip needs <source> on ${path}`).toBe(true);
        expect(Boolean(v.w && v.h), `clip needs width+height on ${path}`).toBe(true);
        expect((v.label || '').length, `clip needs aria-label on ${path}`).toBeGreaterThan(3);
      }
    }
  });

  test('no horizontal overflow at mobile width', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const path of pages) {
      await page.goto(path);
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
      );
      expect(overflow, `expected ${path} to have no horizontal overflow at 390px`).toBeLessThanOrEqual(1);
    }
  });

  test('album gallery collapses to one column on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const path of pages.filter((p) => p.includes('/trips/'))) {
      await page.goto(path);
      const gallery = page.locator('.album-gallery').first();
      if (await gallery.count()) {
        const cols = await gallery.evaluate((el) => getComputedStyle(el).columnCount);
        expect(cols, `expected single-column album gallery on mobile for ${path}`).toBe('1');
      }
    }
  });

  test('sitemap.xml lists every content page', async ({ request }) => {
    const res = await request.get('/sitemap.xml');
    expect(res.status(), 'sitemap.xml should be served').toBeLessThan(400);
    const xml = await res.text();
    const SITE = 'https://www.adirbd.com';
    for (const path of pages) {
      expect(xml, `sitemap should list ${SITE}${path}`).toContain(`<loc>${SITE}${path}</loc>`);
    }
  });

  test('legacy compatibility URLs stay healthy', async ({ request }) => {
    const heLegacy = await request.get('/he.html');
    expect(heLegacy.status(), 'legacy he.html should not 404').toBeLessThan(400);
    expect(await heLegacy.text(), 'legacy he.html should point to canonical /he/').toContain('/he/');

    const oldProfile = await request.get('/images/profile-photo.webp');
    expect(oldProfile.status(), 'legacy profile-photo.webp should remain reachable').toBeLessThan(400);
    expect(oldProfile.headers()['content-type'] || '').toContain('image/webp');
  });

  test('valid JSON-LD and SEO basics on every page', async ({ page }) => {
    for (const path of pages) {
      await page.goto(path);

      const blocks = await page.$$eval('script[type="application/ld+json"]', (nodes) =>
        nodes.map((n) => n.textContent),
      );
      expect(blocks.length, `expected JSON-LD on ${path}`).toBeGreaterThan(0);
      for (const block of blocks) {
        expect(() => JSON.parse(block), `expected valid JSON-LD on ${path}`).not.toThrow();
      }

      await expect(page.locator('h1'), `expected exactly one <h1> on ${path}`).toHaveCount(1);

      const desc = await page.getAttribute('meta[name="description"]', 'content');
      expect(desc, `expected meta description on ${path}`).toBeTruthy();
      expect(desc.trim().length, `expected non-empty description on ${path}`).toBeGreaterThan(20);
    }
  });

  test('pages load with no console errors or failed requests', async ({ page }) => {
    const problems = [];
    page.on('console', (m) => { if (m.type() === 'error') problems.push(`console: ${m.text()}`); });
    page.on('pageerror', (e) => problems.push(`pageerror: ${e.message}`));
    page.on('requestfailed', (r) => problems.push(`requestfailed: ${r.url()}`));
    page.on('response', (r) => { if (r.status() >= 400) problems.push(`http ${r.status()}: ${r.url()}`); });
    for (const path of [...pages, '/404.html']) {
      await page.goto(path, { waitUntil: 'networkidle' });
    }
    expect(problems, `runtime problems: ${JSON.stringify(problems, null, 2)}`).toEqual([]);
  });

  test('hreflang alternates resolve locally and are reciprocal', async ({ request }) => {
    const altsOf = (html) => {
      const out = {};
      const re = /<link rel="alternate" hreflang="([^"]+)" href="([^"]+)" \/>/g;
      let m;
      while ((m = re.exec(html))) out[m[1]] = m[2];
      return out;
    };
    for (const pagePath of pages) {
      const html = await (await request.get(pagePath)).text();
      const alts = altsOf(html);
      for (const lang of ['en', 'en-US', 'he', 'he-IL', 'x-default']) {
        expect(alts[lang], `expected hreflang=${lang} on ${pagePath}`).toBeTruthy();
      }
      for (const [lang, href] of Object.entries(alts)) {
        const local = href.replace(SITE_URL, '') || '/';
        const res = await request.get(local);
        expect(res.status(), `hreflang ${lang} -> ${href} from ${pagePath} should resolve`).toBeLessThan(400);
      }
      // The Hebrew alternate must point back at the same English URL (and itself).
      const heHtml = await (await request.get(alts.he.replace(SITE_URL, ''))).text();
      const heAlts = altsOf(heHtml);
      expect(heAlts.en, `he alternate of ${pagePath} should point back to the same en URL`).toBe(alts.en);
      expect(heAlts.he, `he alternate of ${pagePath} should self-reference`).toBe(alts.he);
    }
  });

  test('css/js references carry the current content-hash version', async ({ request }) => {
    const hashOf = (name) =>
      crypto.createHash('md5').update(fs.readFileSync(path.join(__dirname, '..', name))).digest('hex').slice(0, 8);
    const cssVer = hashOf('index.css');
    const jsVer = hashOf('index.js');
    for (const pagePath of [...pages, '/404.html']) {
      const html = await (await request.get(pagePath)).text();
      expect(html, `stylesheet on ${pagePath} should carry ?v=${cssVer}`).toContain(`index.css?v=${cssVer}`);
      if (pagePath !== '/404.html') {
        expect(html, `script on ${pagePath} should carry ?v=${jsVer}`).toContain(`index.js?v=${jsVer}`);
      }
    }
  });

  test('sitemap lists every album image for Google Images', async ({ page, request }) => {
    const xml = await (await request.get('/sitemap.xml')).text();
    expect(xml, 'sitemap should declare the image namespace').toContain(
      'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"',
    );
    for (const pagePath of pages.filter((p) => p.includes('/trips/'))) {
      await page.goto(pagePath);
      const media = await page.$$eval('.album-hero-media img, .album-figure img, .album-figure video', (els) =>
        els.map((el) => (el.tagName === 'VIDEO' ? el.getAttribute('poster') : el.getAttribute('src'))),
      );
      expect(media.length, `expected album media on ${pagePath}`).toBeGreaterThan(0);
      for (const src of media) {
        expect(xml, `sitemap should list ${src} (shown on ${pagePath})`).toContain(
          `<image:loc>${SITE_URL}${src}</image:loc>`,
        );
      }
    }
  });

  test('album pages carry ImageGallery JSON-LD covering all their media', async ({ page }) => {
    for (const pagePath of pages.filter((p) => p.includes('/trips/'))) {
      await page.goto(pagePath);
      const blocks = await page.$$eval('script[type="application/ld+json"]', (nodes) =>
        nodes.map((n) => n.textContent),
      );
      const gallery = blocks.map((b) => JSON.parse(b)).find((b) => b['@type'] === 'ImageGallery');
      expect(gallery, `expected ImageGallery JSON-LD on ${pagePath}`).toBeTruthy();
      expect(Array.isArray(gallery.hasPart), `expected hasPart images on ${pagePath}`).toBe(true);
      for (const img of gallery.hasPart) {
        expect(img['@type']).toBe('ImageObject');
        expect(img.contentUrl, `ImageObject needs contentUrl on ${pagePath}`).toContain(`${SITE_URL}/images/journeys/`);
        expect(Boolean(img.width && img.height), `ImageObject needs dims on ${pagePath}`).toBe(true);
      }
      // Every photo/clip figure must be represented (cover may merge with a photo).
      const figures = await page.$$eval('.album-figure img, .album-figure video', (els) => els.length);
      expect(gallery.hasPart.length, `hasPart should cover the album media on ${pagePath}`).toBeGreaterThanOrEqual(figures);
    }
  });

  test('canonical URL matches the page path', async ({ page }) => {
    for (const pagePath of pages) {
      await page.goto(pagePath);
      const canonical = await page.getAttribute('link[rel="canonical"]', 'href');
      expect(canonical, `canonical on ${pagePath}`).toBe(`${SITE_URL}${pagePath}`);
    }
  });

  test('every page has an og:image with a non-empty og:image:alt', async ({ page }) => {
    for (const path of pages) {
      await page.goto(path);
      const img = await page.getAttribute('meta[property="og:image"]', 'content');
      expect(img, `expected og:image on ${path}`).toBeTruthy();
      const alt = await page.getAttribute('meta[property="og:image:alt"]', 'content');
      expect((alt || '').trim().length, `expected non-empty og:image:alt on ${path}`).toBeGreaterThan(3);
      const talt = await page.getAttribute('meta[name="twitter:image:alt"]', 'content');
      expect((talt || '').trim().length, `expected non-empty twitter:image:alt on ${path}`).toBeGreaterThan(3);
    }
  });

  test('external links are secure (https + rel=noopener on _blank)', async ({ page }) => {
    for (const path of pages) {
      await page.goto(path);
      const links = await page.$$eval('a[href]', (anchors) =>
        anchors.map((a) => ({
          href: a.getAttribute('href'),
          target: a.getAttribute('target'),
          rel: a.getAttribute('rel') || '',
        })),
      );
      for (const { href, target, rel } of links) {
        expect(href.startsWith('http://'), `insecure http:// link on ${path}: ${href}`).toBe(false);
        if (target === '_blank') {
          expect(rel, `target=_blank without rel=noopener on ${path}: ${href}`).toContain('noopener');
        }
      }
    }
  });

  test('skip-to-content link targets a real main on every page', async ({ page }) => {
    for (const path of pages) {
      await page.goto(path);
      const skip = page.locator('a.skip-link[href="#main"]');
      await expect(skip, `expected a skip link on ${path}`).toHaveCount(1);
      await expect(page.locator('main#main'), `expected <main id=main> on ${path}`).toHaveCount(1);
    }
    // first Tab focuses the skip link (it must be the first focusable element)
    await page.goto('/');
    await page.keyboard.press('Tab');
    const cls = await page.evaluate(() => document.activeElement.className);
    expect(cls).toContain('skip-link');
  });

  test('no skipped heading levels', async ({ page }) => {
    for (const path of pages) {
      await page.goto(path);
      const levels = await page.$$eval('h1,h2,h3,h4,h5,h6', (nodes) =>
        nodes.map((n) => Number(n.tagName[1])),
      );
      let prev = 0;
      for (const lvl of levels) {
        if (prev) {
          expect(lvl, `expected no heading-level skip (after h${prev}) on ${path}`).toBeLessThanOrEqual(prev + 1);
        }
        prev = lvl;
      }
    }
  });

  test('text colors meet WCAG AA contrast in both themes', async ({ page }) => {
    await page.goto('/');
    const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
    const lum = (hex) => { const h = hex.replace('#', ''); const [r, g, b] = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b); };
    const ratio = (a, b) => { const la = lum(a), lb = lum(b); return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05); };
    for (const theme of ['light', 'dark']) {
      await page.evaluate((t) => { document.documentElement.dataset.theme = t; }, theme);
      const v = await page.evaluate(() => {
        const s = getComputedStyle(document.documentElement);
        const g = (n) => s.getPropertyValue(n).trim();
        return { text: g('--text'), soft: g('--text-soft'), heading: g('--heading'), bg: g('--bg'), strong: g('--bg-strong') };
      });
      for (const fg of [v.text, v.soft, v.heading]) {
        for (const bg of [v.bg, v.strong]) {
          expect(ratio(fg, bg), `${theme}: ${fg} on ${bg} should meet AA`).toBeGreaterThanOrEqual(4.5);
        }
      }
    }
  });

  test('internal links resolve across the site', async ({ page, request }) => {
    for (const path of pages) {
      await page.goto(path);

      const hrefs = await page.$$eval('a[href]', (anchors) =>
        anchors.map((anchor) => anchor.getAttribute('href')).filter(Boolean),
      );

      const checked = new Set();

      for (const href of hrefs) {
        if (isSkippableHref(href)) continue;
        const resolved = new URL(href, page.url()).toString();
        if (checked.has(resolved)) continue;
        checked.add(resolved);

        const response = await request.get(resolved);
        expect(
          response.status(),
          `expected internal link ${href} from ${path} to resolve`,
        ).toBeLessThan(400);
      }
    }
  });
});
