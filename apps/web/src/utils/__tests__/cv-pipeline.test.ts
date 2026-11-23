/// <reference types="vitest/globals" />
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { CV_DOWNLOAD_PROFILES, CV_FINGERPRINT, getCertificateLinks } from '@mportafolio/core'

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', '..', '..')
const outputDirs = {
  qa: join(repoRoot, 'cv', 'qa', 'output'),
  'devops-qa': join(repoRoot, 'cv', 'devops-qa', 'output'),
}
const publicDir = join(repoRoot, 'apps', 'web', 'public')

describe('CV pipeline (request -> Python backend -> Word/PDF + JSON -> web)', () => {
  it('every document listed by each backend profile exists in its output directory', () => {
    const missing = CV_DOWNLOAD_PROFILES.flatMap((profile) =>
      profile.documents.filter((doc) => !existsSync(join(outputDirs[profile.id], doc.file))),
    )
    expect(missing).toEqual([])
  })

  it('the PDFs were rendered from the same CV data exported for each profile', () => {
    for (const profile of CV_DOWNLOAD_PROFILES) {
      const metadata = JSON.parse(readFileSync(join(outputDirs[profile.id], 'cv-data.json'), 'utf-8'))
      for (const doc of profile.documents.filter((item) => item.format === 'pdf')) {
        const pdf = readFileSync(join(outputDirs[profile.id], doc.file), 'latin1')
        expect(pdf, doc.file).toContain(`cv-fingerprint:${metadata._meta.fingerprint}`)
      }
    }
    expect(CV_DOWNLOAD_PROFILES[0].documents).not.toHaveLength(0)
    expect(CV_FINGERPRINT).toBeTruthy()
  })

  it('every certificate filePath exists in apps/web/public', () => {
    const missing = getCertificateLinks()
      .map((cert) => cert.filePath)
      .filter((filePath): filePath is string => Boolean(filePath))
      .filter((filePath) => !existsSync(join(publicDir, filePath)))
    expect(missing).toEqual([])
  })
})
