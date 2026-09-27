---
applyTo: "apps/web/src/**,apps/web/tests/e2e/**"
---

# Frontend UI & routing skill (apps/web)

Role: frontend maintainers + `portfolio-test-manager` (see `.github/agents/`). Mobile layout rules live in `responsive-mobile.instructions.md`.

## Tailwind CSS v4

- v4 preflight no longer sets `cursor: pointer` on `<button>`. `index.css` restores it globally (`button:not(:disabled), [role="button"]:not(:disabled)`), so don't add `cursor-pointer` per button and don't remove that base rule.
- Config lives in CSS (`@import "tailwindcss"` + `@layer`), not in a v3-style JS preset. Check the v4 docs before assuming a v3 utility or default still exists.

## Routing (`App.tsx`)

- `BrowserRouter` with `basename={import.meta.env.BASE_URL}` (Vite `base: '/mi-portafolio/'`). GitHub Pages deep links go through `public/404.html`.
- Routes: `/` (Home, one-page sections) and `/demos` (`pages/Portfolio.tsx`). Legacy `/proyectos` must keep redirecting to `/demos` (`<Navigate replace />`) because it was shared publicly.
- `<ScrollToTop />` resets scroll on every pathname change so new pages open at the top. It skips navigations that carry `state.scrollTo`.
- Section links (Sobre Mi, Habilidades, …) use `useSectionNavigation().goToSection(id)`: on `/` they scroll directly; from other routes they call `navigate('/', { state: { scrollTo } })` and `Home.tsx` scrolls after mount. New sections need a matching `id` on their `<section>`.
- When adding or renaming a route, update `Navigation.tsx` (desktop + mobile lists), `Footer.tsx`, and `tests/e2e/01-navigation.spec.ts`, and add a redirect for the old path.

## Naming (Spanish UI copy)

- The projects page is branded **"Demos Técnicas"** (nav, h1, footer), with **"Demos Destacadas"** and **"Otras Demos"** as subsections. These are demos/frameworks, not production products, so don't reintroduce "Proyectos" or "Portfolio de Proyectos".

## Verification

- Unit: class-based assertions for layout contracts (e.g. `h-auto sm:h-80`) plus `data-testid` hooks where a semantic role doesn't exist.
- E2E/browser: assert real behavior — `window.scrollY === 0` after route change, `getComputedStyle(el).cursor === 'pointer'`, redirect URL.
