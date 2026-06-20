const { test, expect } = require('@playwright/test');

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
