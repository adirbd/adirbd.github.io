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
