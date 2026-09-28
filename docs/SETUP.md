# Setup

## Requisitos

| Herramienta | Versión | Para qué |
| --- | --- | --- |
| Node.js | 20+ (CI usa 24) | Web |
| pnpm | 12+ | Monorepo JS |
| [uv](https://docs.astral.sh/uv/) | reciente | Backend de la HV (`apps/api`) y agente maestro (`agent/`); cada uno instala sus dependencias la primera vez |
| GitHub CLI (`gh`) | reciente, autenticado | PRs y skills de GitHub del agente |

## Instalación

```bash
git clone https://github.com/Harp-Andres/mi-portafolio.git
cd mi-portafolio
pnpm install
pnpm exec playwright install chromium   # solo para los tests E2E
```

No hace falta ninguna variable de entorno.

## Día a día

```bash
pnpm dev            # web en http://localhost:5173/mi-portafolio/
pnpm lint           # TypeScript (tsc --noEmit)
pnpm test           # tests unitarios (Vitest)
pnpm test:e2e       # Playwright
pnpm build          # build de producción (apps/web/dist)
pnpm release        # todo lo que corre CI, antes de abrir un PR
```

## Hoja de vida

```bash
pnpm cv:status      # ¿Word/PDF y datos de la web están sincronizados? ¿hay solicitudes pendientes?
pnpm cv:apply       # aplica cv/input/requests/*.md y regenera Word/PDF + cv/output/cv-data.json
pnpm test:backend   # tests del backend (pytest)
```

Detalle en [CV_MANAGEMENT/WORKFLOW.md](CV_MANAGEMENT/WORKFLOW.md).

## Agente maestro (MCP)

Cursor, VS Code y Claude Code ya lo tienen registrado (`.cursor/mcp.json`, `.vscode/mcp.json`, `.mcp.json`).
Actívalo una vez en el IDE (Cursor: Settings → MCP → `maestro`). Verifícalo con `pnpm test:agent`.
Referencia en [agent/README.md](../agent/README.md).

## Problemas conocidos

| Síntoma | Solución |
| --- | --- |
| `uv`: `invalid peer certificate` (proxy corporativo) | `$env:UV_SYSTEM_CERTS='1'` (PowerShell) o `export UV_SYSTEM_CERTS=1` |
| `tsc`/`vitest`: "Cannot find module" tras clonar, mover o renombrar la carpeta | `pnpm install` desde la raíz |
| Playwright no encuentra Chromium | `pnpm exec playwright install chromium` |
| PowerShell muestra `NativeCommandError` con pnpm | Es stderr informativo de pnpm; revisa el exit code |
