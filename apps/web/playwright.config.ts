import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 0 : 0,
  workers: process.env.CI ? Number(process.env.PLAYWRIGHT_WORKERS ?? 2) : undefined,
  timeout: 30000, // 30 seconds per test
  expect: {
    timeout: 10000, // 10 seconds for assertions
  },
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'playwright-report/results.json' }],
    ['junit', { outputFile: 'playwright-report/results.xml' }],
    ['list'],
    ['github']
  ],
  use: {
    baseURL: 'http://localhost:5173/mi-portafolio/',
    trace: 'on-first-retry',
    screenshot: 'on',
    navigationTimeout: 10000, // 10 seconds for navigation
    acceptDownloads: true,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  webServer: {
    // Not `pnpm dev`: pnpm 12 does not forward teardown signals, so vite outlives the run.
    command: 'node ../../scripts/hv/sync-cv-downloads.mjs && vite',
    url: 'http://localhost:5173/mi-portafolio/',
    timeout: 120000, // 120 seconds to start server
    reuseExistingServer: !process.env.CI,
  },

  globalTimeout: 600000, // 10 minute global timeout for all tests
})
