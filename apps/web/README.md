# @mportafolio/web

Portfolio site: React 19, TypeScript 7, Vite 8 and Tailwind CSS 4, deployed to
[GitHub Pages](https://harp-andres.github.io/mi-portafolio/) under the base `/mi-portafolio/`.

## Routes

| Route | Page |
| --- | --- |
| `/` | `pages/Home.tsx`: hero, about, skills, experience, education and certificates |
| `/demos` | `pages/Portfolio.tsx`: catalog of technical demos (`/proyectos` redirects here) |

## Commands

Run from the repo root (`pnpm dev`, `pnpm test`, ...) or here with `pnpm -F @mportafolio/web <script>`.

| Script | What it does |
| --- | --- |
| `dev` | Syncs the CV files into `public/cv/`, then starts Vite on port 5173 |
| `build` / `preview` | Same sync, type check and production build / serve `dist/` |
| `lint` | `tsc --noEmit` |
| `test` / `test:watch` / `test:ui` | Vitest once / in watch mode / with the UI |
| `test:coverage` | Vitest with v8 coverage (what CI runs) |
| `test:e2e` / `test:e2e:ui` | Playwright (Chromium); starts Vite itself ([specs](tests/e2e/README.md)) |

## Structure

```
src/
├── components/   sections, Navigation, CVDownloads, Footer, ScrollToTop (+ __tests__)
├── hooks/        useAge, useScrollPosition, useSectionNavigation, useCopyClean
├── pages/        Home, Portfolio
├── utils/        cv-data, cv-document (CV PDF URLs), public-asset (base-aware assets)
└── index.css     Tailwind import, theme (slideUp animation) and base styles
```

## Data

The web only displays data. `CV_DATA` and `PROJECTS` come from `@mportafolio/core`; the CV part is
`cv/output/cv-data.json`, written by the Python backend together with the Word/PDF. Change the CV with a
request and `pnpm cv:apply` ([workflow](../../docs/CV_MANAGEMENT/WORKFLOW.md)).

Assets under `public/` must be resolved with `resolvePublicAssetUrl` so they work under the Pages base path.
