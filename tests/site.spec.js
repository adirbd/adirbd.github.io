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
    for (const path of pages) {
      await page.goto(path, { waitUntil: 'networkidle' });
    }
    expect(problems, `runtime problems: ${JSON.stringify(problems, null, 2)}`).toEqual([]);
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
