
const root = document.documentElement;
const themeToggle = document.querySelector('[data-theme-toggle]');
const navToggle = document.querySelector('[data-nav-toggle]');
const body = document.body;
const storageKey = 'adirbd-theme';
const isHebrew = (root.lang || '').toLowerCase().startsWith('he');
const themeText = isHebrew
  ? { light: 'בהיר', dark: 'כהה', toLight: 'מעבר למצב בהיר', toDark: 'מעבר למצב כהה' }
  : { light: 'Light', dark: 'Dark', toLight: 'Switch to light mode', toDark: 'Switch to dark mode' };

const getPreferredTheme = () => {
  const saved = localStorage.getItem(storageKey);
  if (saved === 'light' || saved === 'dark') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const setTheme = (theme) => {
  root.dataset.theme = theme;
  localStorage.setItem(storageKey, theme);
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
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
  });
}

if (navToggle) {
  const closeNav = () => {
    if (!body.classList.contains('nav-open')) return;
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
