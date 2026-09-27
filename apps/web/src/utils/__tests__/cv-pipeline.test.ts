/// <reference types="vitest/globals" />
import { createHash } from 'node:crypto'
import { existsSync, readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { CV_DATA } from '@mportafolio/core'
import generated from '../../../../../packages/core/src/data/cv-data.generated.json'

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..', '..', '..')
const inputPath = join(repoRoot, 'cv', 'input', 'cv-data.json')
const publicDir = join(repoRoot, 'apps', 'web', 'public')

describe('CV pipeline (cv/input -> Python -> web)', () => {
  it('generated web data is up to date with cv/input/cv-data.json (run `pnpm generate:cv`)', () => {
    const input = readFileSync(inputPath, 'utf8').replace(/\r\n/g, '\n')
    const digest = createHash('sha256').update(input, 'utf8').digest('hex')
    expect(generated._meta.sourceSha256).toBe(digest)
  })

  it('every certificate filePath exists in apps/web/public', () => {
    const missing = CV_DATA.certificates
      .map((cert) => cert.filePath)
      .filter((filePath): filePath is string => Boolean(filePath))
      .filter((filePath) => !existsSync(join(publicDir, filePath)))
    expect(missing).toEqual([])
  })

  it('cv/output contains the ATS and Visual CV in PDF and DOCX', () => {
    const files = readdirSync(join(repoRoot, 'cv', 'output'))
    for (const variant of ['ATS', 'Visual']) {
      for (const ext of ['pdf', 'docx']) {
        expect(files).toContain(`HV_2026_2_${variant}_AndresRodriguez.${ext}`)
      }
    }
  })
})
