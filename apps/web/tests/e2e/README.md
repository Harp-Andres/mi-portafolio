# E2E tests (Playwright)

Chromium against the dev server at `http://localhost:5173/mi-portafolio/` (started by Playwright, or
reused if already running). Configuration: `apps/web/playwright.config.ts`.

| Spec | Covers |
| --- | --- |
| `01-navigation.spec.ts` | Home sections, `/demos` opening at the top, legacy `/proyectos` redirect, scroll to top |
| `02-cv-download.spec.ts` | CV download dialog: ATS and Visual PDF downloads, format options, closing |
| `03-responsiveness.spec.ts` | iPhone 12, 360×780, iPad and 1920×1080: landmarks, font sizes, touch targets, no horizontal overflow; 360×780 hamburger, course carousel and skill cards |
| `04-accessibility.spec.ts` | Headings, alt text, contrast, keyboard navigation and traps, focus styles, ARIA landmarks |
| `05-certificate-download.spec.ts` | Certificate PDFs download under the `/mi-portafolio/` base path |

## Run

```bash
pnpm exec playwright install chromium   # once per machine
pnpm test:e2e                           # from the repo root
pnpm test:e2e:ui                        # interactive runner
pnpm test:e2e -- 02-cv-download.spec.ts # one spec
```

Reports go to `apps/web/playwright-report/` (gitignored). In CI (`test-e2e` job in
`.github/workflows/deploy.yml`) the suite runs with 2 workers and the report is uploaded as an artifact.

## Conventions

- Prefer role/text locators (`getByRole`, `getByText`) and web-first assertions (`toBeVisible`), never fixed waits.
- Viewport rules for mobile (360×780) live in `.github/instructions/responsive-mobile.instructions.md`.
- Local timeouts on `page.goto` usually mean a slow machine; CI is the reference.
