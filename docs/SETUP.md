# Setup & Installation Guide

## Prerequisites

- **Node.js**: v18+ (v24 recommended)
- **pnpm**: v12+
- **Git**: Latest version

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Harp-Andres/MiPortafolio.git
cd MiPortafolio
```

### 2. Install Dependencies
```bash
pnpm install
```

### 3. Python (only to change the CV)
Install [uv](https://docs.astral.sh/uv/). The CV backend (`apps/api`) installs its own dependencies on first run.

## Development Environment Setup

### Frontend Development
```bash
# Start development server
pnpm -C apps/web dev

# Run tests
pnpm -C apps/web test

# Build for production
pnpm -C apps/web build
```

### CV backend (from the repo root)
```bash
pnpm cv:status      # Word/PDF/JSON in sync? pending requests?
pnpm cv:apply       # apply cv/input/requests/*.md|txt and regenerate the CV
pnpm test:backend   # pytest
pnpm dev:backend    # optional local HTTP API (docs/API.md)
```

### Agent Development (Python)
```bash
cd agent
python -m venv venv
source venv/bin/activate
pip install -e .

# Run agent CLI
python -m agent.cli
```

## Environment Configuration

The web and the CV backend need no environment variables.

### Agent (.env in agent/)
```
LOG_LEVEL=INFO
STORAGE_PATH=./data
```

## Monorepo Structure

```
MiPortafolio/
├── apps/
│   ├── web/                 # React frontend (Vite): displays cv/output
│   └── api/                 # Python CV backend: request → Word/PDF + cv-data.json
├── packages/
│   ├── ui/                  # React UI components
│   ├── core/                # Shared utilities
│   ├── api-client/          # API client library
│   ├── backend/             # Backend utilities
│   └── config/              # Shared configuration
├── agent/                   # Python agent with 7-layer architecture
├── docs/                    # Documentation
└── scripts/                 # Automation scripts
```

## Troubleshooting

### Dependencies Not Installing
```bash
# Clear pnpm cache and reinstall
pnpm install --force
```

### Port Already in Use
```bash
# Change default ports in respective apps
# Frontend: vite.config.ts - server.port
# Backend: main.py - port parameter
# Agent: .env - AGENT_PORT
```

### Node Modules Issues
```bash
# Prune and reinstall
pnpm store prune
pnpm install
```

## Documentation Links

- [Architecture Overview](./MONOREPO_ARCHITECTURE.md)
- [Contributing Guide](./CONTRIBUTING.md)
- [API Documentation](./API.md)
- [Agent Documentation](../agent/README.md)

## Support

For issues and questions:
1. Check [existing issues](https://github.com/Harp-Andres/MiPortafolio/issues)
2. Review development documentation in `.dev-docs/`
3. Contact the development team

## License

See LICENSE file in root directory
