# Flujo de actualización de la Hoja de Vida

La hoja de vida tiene **una sola entrada** y **una sola dirección**:

```text
            (tú editas)                     (Python genera)                         (la web muestra)
chat Copilot/Cursor ─┐
                     ├─► cv/input/cv-data.json ─► scripts/hv/generate-cv-pdf.py ─┬─► cv/output/HV_2026_2_*.pdf|docx  ─► descargas de la web
otro JSON ───────────┘                                                          └─► packages/core/src/data/cv-data.generated.json ─► secciones de la web
```

- La **web nunca se edita a mano** para cambiar datos del CV: renderiza lo que Python generó.
- Los archivos de `cv/output/` son **tus HV locales** y son exactamente los que la web ofrece para descargar (`scripts/hv/sync-cv-downloads.mjs` los copia a `apps/web/public/cv/` antes de cada `pnpm dev` / `pnpm build`).

## Rutas

| Qué | Ruta | ¿Se edita? |
|-----|------|-----------|
| Entrada única de datos | `cv/input/cv-data.json` | **Sí** (chat o archivo) |
| Generador + validación | `scripts/hv/generate-cv-pdf.py` | Solo para cambiar el diseño del PDF/DOCX |
| HV locales (PDF/DOCX ATS y Visual) | `cv/output/` | No, las escribe Python |
| Datos que usa la web | `packages/core/src/data/cv-data.generated.json` | No, lo escribe Python |
| Descargas servidas por la web | `apps/web/public/cv/` | No, copia automática (gitignored) |
| Imágenes/PDF de certificados | `apps/web/public/certificados/<Tema>/` | Sí, al agregar un certificado |

## Casos de uso

### CU-1 · Actualizar la HV desde el chat (recomendado)

1. En Copilot Chat o Cursor escribe, por ejemplo: *"Agrega el curso X de Udemy, 12 horas, categoría DevOps & Cloud; el certificado está en `C:\...\cert.jpg`"*. También puedes usar el prompt `/update-cv`.
2. El agente (MCP-first) llama `maestro-context` → `maestro-agent portfolio-cv-manager`, copia el certificado a `apps/web/public/certificados/<Tema>/` y edita **solo** `cv/input/cv-data.json`.
3. El agente llama la herramienta MCP `cv-generate` (o `pnpm generate:cv`). Python valida y regenera `cv/output/` + el JSON de la web.
4. El agente ejecuta `pnpm -F @mportafolio/web test` (incluye `cv-pipeline.test.ts`) y te muestra el `git diff`.
5. Revisas los PDF en `cv/output/`, y si te gustan, se crea la rama + PR.

### CU-2 · Actualizar la HV con otro archivo de entrada

1. Prepara un JSON con la misma forma que `cv/input/cv-data.json` (puedes partir de una copia).
2. Ejecuta `uv run scripts/hv/generate-cv-pdf.py ruta/a/mi-cv.json` (o `cv-generate` con `input_path`).
3. Si es válido, Python lo copia como nuevo `cv/input/cv-data.json` y regenera todo. Si no, lista los errores y **no escribe nada**.

### CU-3 · Ver la HV en la web local

`pnpm dev` → sincroniza `cv/output` a las descargas y abre `http://localhost:5173/mi-portafolio/`. Los datos visibles salen de `cv-data.generated.json`.

### CU-4 · Publicar

Merge del PR a `main` → GitHub Actions ejecuta `pnpm -F @mportafolio/web build` (que sincroniza `cv/output`) y despliega a GitHub Pages. No se necesita Python en CI: `cv/output/` y el JSON generado están versionados.

### CU-5 · Cambiar el diseño del PDF/DOCX (no los datos)

Edita las funciones de layout de `scripts/hv/generate-cv-pdf.py` (`build_ats_pdf`, `build_visual_pdf`, `build_docx`) y regenera con `pnpm generate:cv`.

## Reglas de la entrada (`cv/input/cv-data.json`)

- Cada curso aparece **una sola vez**, dentro de `certificatesByCategory.<Categoría>` (o `learningPathsCertifications` / `officialCertifications`). La lista plana `certificates` del carrusel la **deriva Python**; no la escribas.
- `filePath` es la ruta pública del certificado (`/certificados/...`) o `null` si no hay archivo. Python falla si el archivo no existe en `apps/web/public`.
- `hours` es entero ≥ 0. Títulos duplicados → error.
- Las URLs (`linkedin`, `github`) van completas; en el PDF se muestran sin `https://`.

## Verificación

| Comprobación | Comando |
|--------------|---------|
| ¿La web está al día con la entrada? | `pnpm sync:verify` o MCP `cv-status` |
| Tests unitarios (incluye pipeline) | `pnpm -F @mportafolio/web test` |
| Descargas reales | `pnpm -F @mportafolio/web test:e2e` (`02-cv-download.spec.ts`) |

Requisitos: [uv](https://docs.astral.sh/uv/) (instala `python-docx` y `reportlab` automáticamente desde la cabecera del script). En redes con proxy corporativo añade `--system-certs` a `uv run`.
