/// <reference types="vitest/globals" />
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { CV_DOCUMENTS, CV_FINGERPRINT, getCertificateLinks } from '@mportafolio/core'

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', '..', '..')
const outputDir = join(repoRoot, 'cv', 'output')
const publicDir = join(repoRoot, 'apps', 'web', 'public')

describe('CV pipeline (request -> Python backend -> Word/PDF + JSON -> web)', () => {
  it('every document listed by the backend exists in cv/output', () => {
    const missing = CV_DOCUMENTS.map((doc) => doc.file).filter((file) => !existsSync(join(outputDir, file)))
    expect(missing).toEqual([])
  })

  it('the PDFs were rendered from the same CV data the web shows (run `pnpm cv:generate`)', () => {
    for (const doc of CV_DOCUMENTS.filter((d) => d.format === 'pdf')) {
      const pdf = readFileSync(join(outputDir, doc.file), 'latin1')
      expect(pdf, doc.file).toContain(`cv-fingerprint:${CV_FINGERPRINT}`)
    }
  })

  it('every certificate filePath exists in apps/web/public', () => {
    const missing = getCertificateLinks()
      .map((cert) => cert.filePath)
      .filter((filePath): filePath is string => Boolean(filePath))
      .filter((filePath) => !existsSync(join(publicDir, filePath)))
    expect(missing).toEqual([])
  })
})
