# @mportafolio/core

Data and types the web renders. The web imports the TypeScript source through the
`@mportafolio/core` alias (Vite, Vitest and tsconfig), so there is no build step.

| Module | Contents |
| --- | --- |
| `src/data/cv-data.ts` | `CV_DATA`, `CV_DOCUMENTS`, `CV_FINGERPRINT` and certificate helpers, read from `cv/output/cv-data.json` (written by the CV backend in `apps/api`) |
| `src/data/projects.ts` | `PROJECTS`: the catalog of technical demos shown on `/demos` |
| `src/types/` | `CVData`, `CVDocument`, `Project` and related types |

## Changing the data

- **CV:** never edit it here. Add a request to `cv/input/requests/` and run `pnpm cv:apply`; the backend
  regenerates Word/PDF and `cv-data.json` together ([workflow](../../docs/CV_MANAGEMENT/WORKFLOW.md)).
- **Demos:** edit `src/data/projects.ts`; `apps/web/src/utils/__tests__/projects.test.ts` guards unique ids
  and the featured demos.

Then `pnpm lint:all` and `pnpm test`.
