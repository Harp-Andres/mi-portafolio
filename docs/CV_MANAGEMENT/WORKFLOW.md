# Flujo de actualización de la Hoja de Vida

Tres responsabilidades separadas, en una sola dirección:

```text
 1. ENTRADA (tú)                      2. BACKEND Python (apps/api)                    3. WEB (apps/web)
 ─────────────────                    ───────────────────────────                     ─────────────────
 chat Copilot/Cursor ─► solicitud .md ┐
 archivo .md/.txt tuyo ──────────────┼─► aplica cambios ─► valida ─► renderiza ─┬─► cv/output/HV_*_ATS|Visual.pdf|docx ─► descargas
 cv/input/requests/*.md|txt ─────────┘                                        └─► cv/output/cv-data.json ─────────────► secciones
```

1. **Entrada**: una *solicitud de cambio* en `.md` o `.txt` que dice qué incorporar a la HV. Puede ser un archivo tuyo en cualquier ruta, un archivo en `cv/input/requests/`, o instrucciones en el chat que el agente escribe como solicitud.
2. **Backend** (`apps/api`, Python, POO + SOLID): interpreta la solicitud, aplica los cambios al CV, valida las reglas, copia certificados y genera la HV en **Word y PDF** (ATS y Visual). Junto a ellos escribe `cv/output/cv-data.json`, el gemelo estructurado de esos documentos.
3. **Web**: solo muestra. Lee `cv/output/cv-data.json` (vía `@mportafolio/core`) y sirve los PDF de `cv/output/` como descargas. Nunca edita ni genera datos del CV.

Word, PDF y JSON llevan la misma **huella** (`fingerprint`, SHA-256 del contenido): en los metadatos del PDF (`Keywords`), del DOCX (`identifier`) y en `_meta.fingerprint`. Así `cv:status` y los tests comprueban que la web muestra exactamente lo que dicen los documentos. La web usa el JSON y no parsea el PDF, porque extraer datos de un PDF pierde estructura.

## Rutas

| Qué | Ruta | ¿Se edita? |
|-----|------|-----------|
| Solicitudes pendientes | `cv/input/requests/*.md\|txt` | **Sí** (tú o el agente) |
| Plantilla de solicitud | `cv/input/request-template.md` | Referencia |
| Solicitudes aplicadas (historial) | `cv/input/processed/` | No, las archiva el backend |
| Backend | `apps/api/app/` | Solo para cambiar reglas o diseño |
| HV (Word/PDF ATS y Visual) + datos web | `cv/output/` | No, las escribe el backend |
| Descargas servidas por la web | `apps/web/public/cv/` | No, copia automática (gitignored) |
| Certificados | `apps/web/public/certificados/<Proveedor>/` | No, los copia el backend desde la ruta de la solicitud |

## Formato de la solicitud

Secciones `##` (en `.txt` también `[Curso]`) con líneas `- campo: valor`. Se ignoran el título `#`, el texto fuera de secciones y los comentarios `<!-- -->`. Los campos no distinguen mayúsculas ni tildes.

```md
## Curso
- titulo: Docker Mastery — Udemy
- categoria: DevOps & Cloud
- horas: 14
- certificado: C:\Users\me\Downloads\docker.pdf

## Experiencia
- empresa: ACME
- cargo: QA Lead
- periodo: 2026 – Actualidad
- tecnologias: Playwright, k6
- logros:
  - Diseñé el framework de automatización
  - Reduje la regresión un 40%
```

| Sección | Campos (`*` obligatorio) |
|---------|--------------------------|
| `Curso` | `titulo*`, `categoria*`, `horas`, `certificado`, `carpeta` |
| `Ruta de aprendizaje` | `titulo*`, `horas`, `certificado`, `carpeta` |
| `Certificación oficial` | `titulo*`, `emisor*`, `icono`, `color`, `certificado`, `carpeta` |
| `Experiencia` | `empresa*`, `cargo*`, `periodo*`, `logros*` (lista), `tecnologias` |
| `Educación` | `titulo*`, `institucion*`, `año*` |
| `Habilidades` | `categoria*`, `agregar*` (lista separada por comas) |
| `Idioma` | `idioma*`, `nivel*` (crea o actualiza) |
| `Perfil` | `texto*` (reemplaza el perfil) |
| `Dato personal` | `campo*` (nombre, titulo, email, telefono 1/2, ubicacion, linkedin, github, portafolio), `valor*` |
| `Eliminar` | `titulo*` (curso, ruta o certificación) |

`certificado` acepta una ruta absoluta o relativa a la solicitud. El backend la copia a `apps/web/public/certificados/<carpeta>/`; por defecto `<carpeta>` es el proveedor que va después de `—` en el título.

## Casos de uso

### CU-1 · Actualizar la HV desde el chat (recomendado)

1. En Copilot Chat o Cursor escribe, por ejemplo: *"Agrega el curso X de Udemy, 12 horas, categoría DevOps & Cloud; el certificado está en `C:\...\cert.jpg`"*. También puedes usar el prompt `/update-cv`.
2. El agente (MCP-first) llama a `maestro-context`, luego a `maestro-agent portfolio-cv-manager`, y escribe tus instrucciones como solicitud `.md`.
3. El agente llama a la herramienta MCP `cv-apply` con ese contenido. El backend aplica, valida, copia el certificado, genera Word/PDF + JSON y archiva la solicitud en `cv/input/processed/`.
4. El agente ejecuta `pnpm -F @mportafolio/web test` y te muestra el `git diff`. Revisas los PDF de `cv/output/` y, si te gustan, se crea la rama y el PR.

### CU-2 · Actualizar la HV con un archivo tuyo

1. Escribe la solicitud (parte de `cv/input/request-template.md`) y guárdala en `cv/input/requests/` o en cualquier ruta.
2. Ejecuta `pnpm cv:apply` (aplica todo lo pendiente en `cv/input/requests/`) o `pnpm cv:apply -- C:\ruta\mi-solicitud.txt`.
3. Si algo no cumple las reglas (título duplicado, campo desconocido, certificado inexistente...), el backend lista el problema y **no cambia nada**: ni documentos, ni JSON, ni certificados. La solicitud queda pendiente para corregirla.

### CU-3 · Ver la HV en la web local

`pnpm dev` sincroniza `cv/output` a las descargas y abre `http://localhost:5173/mi-portafolio/`.

### CU-4 · Publicar

Al hacer merge del PR a `main`, GitHub Actions ejecuta `pnpm -F @mportafolio/web build` y despliega a GitHub Pages. CI no necesita Python porque `cv/output/` está versionado.

### CU-5 · Cambiar el diseño del Word/PDF (no los datos)

Edita `apps/api/app/infrastructure/documents/` (`pdf_renderer.py`, `docx_renderer.py`, `theme.py`) y regenera con `pnpm cv:generate`.

## Arquitectura del backend (`apps/api/app`)

| Capa | Módulos | Responsabilidad |
|------|---------|-----------------|
| Dominio | `domain/models.py`, `changes.py`, `validation.py` | Agregado `CurriculumVitae`, un comando por tipo de cambio (`AddCourse`, `AddExperience`, ...), reglas de negocio. Sin I/O. |
| Aplicación | `application/ports.py`, `apply_change_request.py`, `generate_documents.py`, `curriculum_status.py` | Casos de uso que dependen solo de puertos (interfaces). |
| Infraestructura | `infrastructure/requests`, `persistence`, `documents`, `assets` | Parser `.md`/`.txt`, repositorio JSON, renderers PDF/DOCX, almacén de certificados. |
| Interfaces | `interfaces/cli.py`, `http.py` | CLI (`python -m app`) y API HTTP local sobre los mismos casos de uso. |
| Composición | `composition.py` | Único lugar que conecta cada puerto con su implementación. |

Un tipo de solicitud nuevo se agrega con una clase en `domain/changes.py` y un `SectionBuilder` en `infrastructure/requests/sections.py`. El resto del código no cambia.

## Verificación

| Comprobación | Comando |
|--------------|---------|
| ¿Word/PDF/JSON sincronizados? ¿Solicitudes pendientes? | `pnpm cv:status` o MCP `cv-status` |
| Tests del backend | `pnpm test:backend` |
| Tests de la web (incluye huella PDF ↔ JSON) | `pnpm -F @mportafolio/web test` |
| Descargas reales | `pnpm -F @mportafolio/web test:e2e` (`02-cv-download.spec.ts`) |

Requisitos: [uv](https://docs.astral.sh/uv/). En redes con proxy corporativo añade `--system-certs` a `uv run`.
