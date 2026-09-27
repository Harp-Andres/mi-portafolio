/**
 * Resolve a path under `public/` against Vite's base URL.
 * GitHub Pages deploys this app under `/mi-portafolio/`, so root-absolute
 * paths like `/certificados/...` 404 unless prefixed with BASE_URL.
 */
export function resolvePublicAssetUrl(filePath: string): string {
  const base = import.meta.env.BASE_URL || '/'
  const normalizedBase = base.endsWith('/') ? base : `${base}/`
  const relative = filePath.replace(/^\/+/, '')
  const encoded = relative
    .split('/')
    .map((segment) => encodeURIComponent(segment))
    .join('/')
  return `${normalizedBase}${encoded}`
}

export function publicAssetFilename(filePath: string): string {
  const name = filePath.split('/').filter(Boolean).pop() || 'certificado'
  try {
    return decodeURIComponent(name)
  } catch {
    return name
  }
}
