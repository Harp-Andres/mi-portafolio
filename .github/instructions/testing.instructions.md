---
applyTo: "apps/web/tests/e2e/**,apps/web/src/**/__tests__/**,apps/web/vitest.config.ts,apps/web/playwright.config.ts,apps/api/tests/**"
---

# Testing skill (unit + E2E)

Role: `portfolio-test-manager` / `sdet-quality-manager` (see `.github/agents/`).

- Prefer semantic selectors (`getByRole`, accessible names) over `data-testid` in Playwright specs.
- `playwright.config.ts` already runs 2 workers in CI (`PLAYWRIGHT_WORKERS` overridable) and generates html/json/junit reports — don't lower parallelism or drop a reporter without a reason.
- Verify things that actually cross the network/filesystem for real (e.g. use Playwright's `page.waitForEvent('download')` + `download.failure()`, not just checking a static file exists on disk) — filesystem-only checks can mask real bugs (e.g. wrong base path).
- The app uses `BrowserRouter` (base `/mi-portafolio/`); section navigation scrolls via `useSectionNavigation`, not URL hashes. Assert on heading visibility/`toBeInViewport()` and `window.scrollY`, never on a `#hash`. Unit tests may wrap components in `HashRouter`/`MemoryRouter`, which is fine for isolation.
- `baseURL` is `http://localhost:5173/mi-portafolio/`. For sub-routes use **relative** paths: `page.goto('demos')`. A leading slash (`page.goto('/demos')`) resolves against the origin and drops `/mi-portafolio/`; only `'/'` happens to work because Vite redirects the root to its base.
- Smooth scrolling (`behavior: 'smooth'`) barely advances in hidden/background tabs. Poll or use `toBeInViewport()` instead of a fixed short timeout.
- If Playwright fails with `Executable doesn't exist … chrome-headless-shell`, install the browsers (`pnpm -F @mportafolio/web exec playwright install chromium`) before concluding anything. Where installing isn't possible (sandboxed agent), verify manually in the IDE browser and state that E2E will run in CI.
- Run web tests with `pnpm -F @mportafolio/web test` (unit) / `pnpm -F @mportafolio/web test:e2e` (E2E) / `pnpm -F @mportafolio/web test:coverage` (coverage).
- Run API tests with `cd apps/api && uv run pytest`.
- Before declaring a fix done, re-run the affected suite and confirm the previously-failing test now passes — don't rely solely on lint/type-check.
