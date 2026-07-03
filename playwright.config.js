const { defineConfig } = require('@playwright/test');

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:8000';
const { hostname, port } = new URL(baseURL);

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 0,
  webServer: {
    command: `python3 -m http.server ${port || 8000} --bind ${hostname || '127.0.0.1'} -d .`,
    url: baseURL,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
  use: {
    baseURL,
    trace: 'on-first-retry',
  },
});
