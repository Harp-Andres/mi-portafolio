---
applyTo: "apps/web/src/components/**,apps/web/src/index.css,apps/web/tests/e2e/03-responsiveness.spec.ts"
---

# Responsive mobile (Galaxy S24 / 360px) skill

Role: `portfolio-test-manager` + frontend maintainers (see `.github/agents/`).

Target compact viewport: **360×780** (Galaxy S24 compact). Live site base path / Pages URL:
`https://harp-andres.github.io/mi-portafolio/`

## Layout rules

- **No horizontal page overflow**: `html, body { overflow-x: clip; max-width: 100%; }`. Prefer `overflow-x-clip` on wide sections (e.g. Hero) instead of letting long titles expand the page.
- **Hero**: use `break-words`, smaller mobile type (`text-3xl` name / `text-base` title), full wrapping of long professional titles.
- **Navigation**: hamburger must stay fully visible on 360px — `min-h-11 min-w-11`, `flex-shrink-0`, reduce horizontal padding on narrow screens (`px-3` mobile). Touch target ≥ 44px.
- **Skills**: on mobile (1 column) cards use `h-auto` so each box fits its content — no fixed height and no `auto-rows-fr`. From `sm:` keep uniform cards (`sm:h-80`, `sm:auto-rows-fr`, list `sm:overflow-y-auto`). Cards expose `data-testid="skill-card"`.
- **Certificates → Cursos de Formación**: on mobile, horizontal snap carousel — one card ≈ **85%** width, `overflow-x-auto snap-x snap-mandatory`, cards `snap-center`. From `md:` use `grid md:grid-cols-2 lg:grid-cols-3`. Official certs: `grid-cols-1 sm:grid-cols-2`. Expose `data-testid="courses-carousel"` and `data-testid="course-category-card"`. Show a mobile-only hint (e.g. “Desliza horizontalmente…”).

## Verification

- Unit: carousel classes, hamburger touch-target classes, Hero `break-words`, cv-data portfolio URL.
- E2E (`03-responsiveness`): 360×780 viewport — hamburger in viewport, no body overflow, carousel shows one primary card (~85% width).
- Playwright `baseURL` / webServer URL must include the Vite base: `http://localhost:5173/mi-portafolio/`.
