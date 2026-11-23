# DevOps-focused CV variant

This folder is an isolated CV variant for DevOps-oriented applications. It is not imported by `packages/core`, not copied to `apps/web/public/cv/`, and not used by the production website or its backend state in `cv/qa/output/`.

Structure:

- `input/requests/`: variant change requests.
- `input/processed/`: requests already applied to the isolated variant.
- `output/`: isolated ATS and Visual Word/PDF documents plus `cv-data.json`.

The documents in this folder are generated through the Python CV backend with `--variant devops-qa`. Certificates remain global in `apps/web/public/certificados/`; do not create a variant-local certificate store. Keep changes here separate from the web-facing CV in `cv/qa/output/`.
