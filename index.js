
const root = document.documentElement;
const themeToggle = document.querySelector('[data-theme-toggle]');
const navToggle = document.querySelector('[data-nav-toggle]');
const body = document.body;
const storageKey = 'adirbd-theme';
const isHebrew = (root.lang || '').toLowerCase().startsWith('he');
const themeText = isHebrew
  ? { light: 'בהיר', dark: 'כהה', toLight: 'מעבר למצב בהיר', toDark: 'מעבר למצב כהה' }
  : { light: 'Light', dark: 'Dark', toLight: 'Switch to light mode', toDark: 'Switch to dark mode' };

// Storage can throw (blocked cookies, some private modes); one unguarded call
// at the top level would kill the whole script — nav, theme, clips and all.
const safeGet = (key) => {
  try { return localStorage.getItem(key); } catch (e) { return null; }
};
const safeSet = (key, value) => {
  try { localStorage.setItem(key, value); } catch (e) {}
};

const getPreferredTheme = () => {
  const saved = safeGet(storageKey);
  if (saved === 'light' || saved === 'dark') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

// Persist only an explicit toggle: saving the OS-derived theme on first load
// would freeze it, so the site would stop following later OS theme changes.
const setTheme = (theme, persist = false) => {
  root.dataset.theme = theme;
  if (persist) safeSet(storageKey, theme);
  const themeColor = theme === 'dark' ? '#0d1320' : '#f6f8fc';
  document.querySelectorAll('meta[name="theme-color"]').forEach((node) => {
    node.setAttribute('content', themeColor);
    node.removeAttribute('media');
  });
  if (themeToggle) {
    themeToggle.setAttribute('aria-label', theme === 'dark' ? themeText.toLight : themeText.toDark);
    themeToggle.querySelector('[data-theme-label]').textContent = theme === 'dark' ? themeText.light : themeText.dark;
  }
};

setTheme(getPreferredTheme());

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
  });
}

if (navToggle) {
  const closeNav = () => {
    if (!body.classList.contains('nav-open')) return;
    // If focus is inside the menu when it closes, it would be stranded on a
    // hidden element — hand it back to the toggle button.
    const navArea = document.querySelector('.nav-area');
    if (navArea && navArea.contains(document.activeElement)) navToggle.focus();
    body.classList.remove('nav-open');
    navToggle.setAttribute('aria-expanded', 'false');
  };

  navToggle.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (!body.classList.contains('nav-open')) return;
    const insideMenu = event.target.closest('.nav-area') || event.target.closest('[data-nav-toggle]');
    if (!insideMenu) {
      closeNav();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });

  window.addEventListener('resize', () => {
    if (window.matchMedia('(min-width: 921px)').matches) closeNav();
  });
}

document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

// Short gallery clips: load and play only while on screen, and only if the
// visitor is OK with motion. Until then they show their poster and cost nothing.
const clips = document.querySelectorAll('video[data-clip]');
const motionOK = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (clips.length && motionOK && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      const video = entry.target;
      if (entry.isIntersecting) {
        if (video.preload !== 'auto') video.preload = 'auto';
        video.play().catch(() => {});
      } else {
        video.pause();
      }
    }
  }, { threshold: 0.25 });
  clips.forEach((video) => io.observe(video));
}
