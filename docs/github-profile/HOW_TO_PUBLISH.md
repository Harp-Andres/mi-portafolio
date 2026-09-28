# Publicar el README de bienvenida (perfil GitHub)

Este contenido está **alineado con `mi-portafolio`** (misma bio, título, LinkedIn, portafolio y stack de la HV en `packages/core/src/data/cv-data.ts`).

El perfil de GitHub solo se muestra si el README vive en:

**https://github.com/Harp-Andres/Harp-Andres**

## Regenerar desde el monorepo

```bash
pnpm sync:github-profile
```

Esto actualiza `docs/github-profile/README.md` leyendo campos clave de `cv-data.ts`.

## Publicar en el repo de bienvenida (2 minutos)

1. Abre: https://github.com/Harp-Andres/Harp-Andres/edit/main/README.md  
2. Reemplaza **todo** el contenido con el de [`README.md`](./README.md).  
3. Commit en `main`.  
4. Recarga: https://github.com/Harp-Andres  

## Por qué se rompían los iconos

`skillicons.dev` deja **cuadrados vacíos** si el ID no existe. El README anterior usaba IDs inválidos (`serenity`, `appium`, `katalon`, `cucumber`, `junit`, `testng`, `azuredevops`, `virtualbox`, `veamware`, `githubcopilot`, `intellij`).

El generador solo usa IDs válidos de skillicons y completa el resto (Playwright, Copilot, Claude, Cursor, etc.) con badges de shields.io.
