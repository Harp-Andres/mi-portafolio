import { getProfileCvDocument } from '@mportafolio/core'
import type { CVDocumentFormat, CVDocumentVariant, CVProfile } from '@mportafolio/core'

/** Public URL of a generated CV rendered by the backend and served under /cv/. */
export const cvDocumentUrl = (
  variant: CVDocumentVariant,
  format: CVDocumentFormat = 'pdf',
  profile: CVProfile = 'qa',
): { href: string; filename: string } => {
  const { file } = getProfileCvDocument(profile, variant, format)
  return { href: `${import.meta.env.BASE_URL}cv/${profile}/${file}`, filename: file }
}
