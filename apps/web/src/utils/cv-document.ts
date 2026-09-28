import { getCvDocument } from '@mportafolio/core'
import type { CVDocumentVariant } from '@mportafolio/core'

/** Public URL of a CV PDF rendered by the backend (cv/output, served under /cv/). */
export const cvDocumentUrl = (variant: CVDocumentVariant): { href: string; filename: string } => {
  const { file } = getCvDocument(variant, 'pdf')
  return { href: `${import.meta.env.BASE_URL}cv/${file}`, filename: file }
}
