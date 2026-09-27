#!/usr/bin/env node

/**
 * Wrapper: regenerates CV DOCX + PDF via Python (reportlab + python-docx).
 * Keep scripts/hv/generate-cv-pdf.py DATA in sync with apps/web/src/utils/cv-data.ts
 *
 * Uso: node scripts/hv/generate-cv-sdet.mjs
 *   o: pnpm generate:cv
 */

import { spawnSync } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const script = join(__dirname, "generate-cv-pdf.py");

const result = spawnSync("python3", [script], {
  encoding: "utf8",
  stdio: "inherit",
});

process.exit(result.status ?? 1);
