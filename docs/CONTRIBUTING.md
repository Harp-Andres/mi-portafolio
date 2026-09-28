# Contributing

## Flujo

1. Rama desde `main` actualizado: `feat/...`, `fix/...`, `refactor/...`, `chore/...` o `docs/...`. Nunca se hace push a `main`.
2. Cambios pequeños y enfocados; un PR por tema.
3. Antes del PR: `pnpm release` (type-check, tests unitarios, backend, agente, sincronía de la HV y build).
4. `gh pr create --base main --body-file body.md` (en Windows usa siempre `--body-file`).
5. Merge solo con CI en verde (`.github/workflows/deploy.yml`); el merge a `main` publica en GitHub Pages.

## Commits

[Conventional Commits](https://www.conventionalcommits.org/) en inglés: `feat(web): ...`, `fix(cv): ...`,
`refactor(agent): ...`, `chore: ...`, `docs: ...`. Añade al stage archivos concretos, no `git add .`.

## Reglas

- La hoja de vida se cambia solo con solicitudes en `cv/input/requests/` + `pnpm cv:apply`; nunca a mano en `cv/output/`.
- Ningún secreto, `.env`, log, reporte, `dist/` ni `coverage/` en el repo.
- En la raíz solo va `README.md`; la documentación va en `docs/` o en el `README.md` de cada paquete.
- Código, commits y ramas en inglés; el contenido de la web y de la HV en español.
- Tests: Vitest para la web (`apps/web/src/**/__tests__`), Playwright para E2E (`apps/web/tests/e2e`),
  pytest para `apps/api/tests` y `agent/tests`.
