# Monorepo Map

Top-level:
- agent: maestro MCP server (interface, orchestrator and skills layers)
- apps/web: React + Vite + Playwright
- apps/api: Python CV backend (request -> Word/PDF + cv-data.json) + pytest
- packages: shared modules

Core workflows:
- CI: lint -> types -> tests -> build
- Deploy: build -> validate -> release

Critical paths:
- agent/1_interface: MCP server, agent registry, CV backend adapter
- agent/2_orchestrator: workflow catalog and maestro runner
- agent/4_skills: command skills (pnpm/uv/git/gh)
- .github/agents/*.agent.md: hierarchy and responsibilities
- .mcp.json: MCP server registration
