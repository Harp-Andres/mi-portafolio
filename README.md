# Andrés Rodríguez Pisa — SDET Senior | QA Automation Engineer

[![Build & Deploy](https://img.shields.io/github/actions/workflow/status/Harp-Andres/mi-portafolio/deploy.yml?branch=main&label=Build%20%26%20Deploy)](https://github.com/Harp-Andres/mi-portafolio/actions/workflows/deploy.yml)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/tests-Vitest%20%2B%20Playwright%20%2B%20pytest-45BA4B?logo=playwright&logoColor=white)](docs/SETUP.md)

**[🌐 Ver el portafolio](https://harp-andres.github.io/mi-portafolio/)** · Hoja de vida y demos técnicas de automatización.

## Qué hay aquí

- **Web** (`apps/web`): hoja de vida interactiva (`/`) y demos técnicas (`/demos`). React 19, TypeScript, Tailwind v4 y Vite, publicada en GitHub Pages.
- **Backend de la HV** (`apps/api`, Python): una sola fuente de datos. Una solicitud `.md` en `cv/input/requests/` genera la HV en Word y PDF (versiones ATS y Visual) y `cv/output/cv-data.json`, que es lo que muestra la web. La descarga y la página siempre dicen lo mismo.
- **Agente maestro** (`agent/`, MCP): conecta los agentes de `.github/agents/` con las skills del repo (tests, build, sincronía de la HV, PRs) desde Cursor, VS Code o Claude Code.
- **Calidad**: tests unitarios con Vitest, E2E con Playwright (navegación, descargas, responsive en 360×780 y accesibilidad) y pytest para el backend y el agente. Todo corre en GitHub Actions antes de cada deploy.

## Inicio rápido

Requisitos: Node 20+, pnpm 12+ y [uv](https://docs.astral.sh/uv/) (solo para la HV y el agente).

```bash
git clone https://github.com/Harp-Andres/mi-portafolio.git
cd mi-portafolio
pnpm install
pnpm dev            # http://localhost:5173/mi-portafolio/
```

| Tarea | Comando |
| --- | --- |
| Type-check · tests unitarios · build | `pnpm lint` · `pnpm test` · `pnpm build` |
| Tests E2E | `pnpm test:e2e` |
| Tests del backend y del agente | `pnpm test:backend` · `pnpm test:agent` |
| Todo lo que corre CI | `pnpm release` |
| Estado de la HV · aplicar una solicitud | `pnpm cv:status` · `pnpm cv:apply` |

## Actualizar la hoja de vida

1. Copia `cv/input/request-template.md` a `cv/input/requests/<tema>.md` y deja solo las secciones que cambian (curso, experiencia, habilidades, dato personal…). También puedes pedírselo al agente con la herramienta MCP `cv-apply`.
2. `pnpm cv:apply` valida la solicitud, regenera Word/PDF + `cv-data.json` y archiva la solicitud en `cv/input/processed/`.
3. Revisa `git diff cv/`, corre `pnpm test` y abre un PR. El merge a `main` publica la web.

Formato completo: [docs/CV_MANAGEMENT/WORKFLOW.md](docs/CV_MANAGEMENT/WORKFLOW.md).

## Estructura

```
apps/web/        React + Vite (páginas, componentes, Vitest, Playwright)
apps/api/        Backend Python de la HV (dominio, casos de uso, render Word/PDF, CLI y API HTTP opcional)
packages/core/   Datos compartidos de la web: lee cv/output/cv-data.json y el catálogo de demos
cv/              input/ (solicitudes pendientes y aplicadas) y output/ (Word/PDF + cv-data.json)
agent/           Servidor MCP maestro: interfaz, orquestador y skills
scripts/         Scripts reutilizables (sincronía de descargas de la HV)
docs/            Setup, contribución, flujo de la HV y API
.github/         CI/CD, agentes, instrucciones, prompts y skills para IA
```

## CI/CD

`.github/workflows/deploy.yml` corre en cada push y PR: type-check, tests unitarios con cobertura, backend, agente y E2E en paralelo; después el build. En `main` publica en GitHub Pages. Nunca se hace push directo a `main`; todo entra por PR con checks en verde ([CONTRIBUTING](docs/CONTRIBUTING.md)).

## Documentación

[Setup](docs/SETUP.md) · [Contribuir](docs/CONTRIBUTING.md) · [Flujo de la HV](docs/CV_MANAGEMENT/WORKFLOW.md) · [API local](docs/API.md) · [Agente maestro](agent/README.md) · [E2E](apps/web/tests/e2e/README.md)

## Contacto

- **Portafolio:** https://harp-andres.github.io/mi-portafolio/
- **LinkedIn:** [Andrés Rodríguez Pisa](https://www.linkedin.com/in/andresrodriguezpisa-seniorqa/)
- **GitHub:** [@Harp-Andres](https://github.com/Harp-Andres)
- **Email:** andresrdrgzps05@gmail.com · Bogotá, Colombia

Licencia ISC.
