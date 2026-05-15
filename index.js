
const root = document.documentElement;
const themeToggle = document.querySelector('[data-theme-toggle]');
const navToggle = document.querySelector('[data-nav-toggle]');
const body = document.body;
const storageKey = 'adirbd-theme';

const getPreferredTheme = () => {
  const saved = localStorage.getItem(storageKey);
  if (saved === 'light' || saved === 'dark') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

const setTheme = (theme) => {
  root.dataset.theme = theme;
  localStorage.setItem(storageKey, theme);
  if (themeToggle) {
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
    themeToggle.querySelector('[data-theme-label]').textContent = theme === 'dark' ? 'Light' : 'Dark';
  }
};

setTheme(getPreferredTheme());

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    setTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
  });
}

if (navToggle) {
  navToggle.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (!body.classList.contains('nav-open')) return;
    const insideMenu = event.target.closest('.nav-area') || event.target.closest('[data-nav-toggle]');
    if (!insideMenu) {
      body.classList.remove('nav-open');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

document.querySelectorAll('[data-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});
