# CV Management

- [WORKFLOW.md](./WORKFLOW.md): flujo de la hoja de vida por casos de uso (solicitud `.md`/`.txt` → backend Python `apps/api` → Word/PDF + `cv/output/cv-data.json` → web).

## Dueño y herramientas

El dueño es `portfolio-cv-manager` (`.github/agents/portfolio-cv-manager.agent.md`); sus reglas están en `.github/instructions/cv-management.instructions.md`. Las herramientas MCP son `cv-status`, `cv-apply` y `cv-generate` (servidor `maestro`), que delegan en el CLI del backend.
