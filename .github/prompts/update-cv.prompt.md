---
description: "Update the Hoja de Vida from chat: write a change request, apply it with the Python backend (Word/PDF + web data) and verify."
agent: portfolio-cv-manager
tools: [read, edit, execute, search, 'maestro/*']
argument-hint: "What changes (e.g. 'add course X — Udemy, 12h, DevOps & Cloud, certificate C:\\...\\cert.jpg')"
---

Update the CV with: ${input:change:What should change in the CV?}

1. Call `maestro-context`, then `cv-status`. Report if the documents were already out of sync or requests are pending.
2. Write the change as a request in the format of `cv/input/request-template.md` (only the needed sections; `certificado` = the path the user gave). If the user gave a `.md`/`.txt` path, use it as is.
3. Call `cv-apply` with `content` (or `request_path`). Fallback: save it in `cv/input/requests/` and run `pnpm cv:apply`. Fix any problem it lists and retry.
4. Run `pnpm -F @mportafolio/web test`.
5. Reply in Spanish with: what changed, the regenerated files in `cv/output/`, test results, and ask whether to open a branch + PR.
