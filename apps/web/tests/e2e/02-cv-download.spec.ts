import { test, expect } from '@playwright/test'
import { promises as fs, readFileSync } from 'node:fs'

type CvProfile = 'qa' | 'devops-qa'
type CvVariant = 'ats' | 'visual'
type CvFormat = 'pdf' | 'docx'

interface CvOutput {
  name: string
  _meta: { documents: { variant: CvVariant; format: CvFormat; file: string }[] }
}

const outputs: Record<CvProfile, CvOutput> = {
  qa: JSON.parse(readFileSync(new URL('../../../../cv/qa/output/cv-data.json', import.meta.url), 'utf-8')),
  'devops-qa': JSON.parse(
    readFileSync(new URL('../../../../cv/devops-qa/output/cv-data.json', import.meta.url), 'utf-8'),
  ),
}

const PROFILE_LABELS: Record<CvProfile, string> = { qa: 'QA Automation', 'devops-qa': 'DevOps' }
const VARIANT_LABELS: Record<CvVariant, string> = { ats: 'ATS', visual: 'Visual' }

const cvFile = (profile: CvProfile, variant: CvVariant, format: CvFormat): string => {
  const doc = outputs[profile]._meta.documents.find((item) => item.variant === variant && item.format === format)
  if (!doc) throw new Error(`${profile} lists no ${variant} ${format}`)
  return doc.file
}

test.describe('CV Download E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should expose semantic trigger and both CV profile sections', async ({ page }) => {
    await page.getByRole('button', { name: /hojas de vida descargables/i }).first().click()

    const dialog = page.getByRole('dialog', { name: /descargar hojas de vida/i })
    await expect(dialog).toBeVisible()
    await expect(dialog.getByRole('heading', { name: 'QA Automation' })).toBeVisible()
    await expect(dialog.getByRole('heading', { name: 'DevOps' })).toBeVisible()
    await expect(dialog.getByRole('link')).toHaveCount(8)
  })

  for (const profile of ['qa', 'devops-qa'] as const) {
    for (const variant of ['ats', 'visual'] as const) {
      for (const format of ['pdf', 'docx'] as const) {
        test(`should download ${profile} ${variant} ${format} from its own option`, async ({ page }) => {
          const expectedFile = cvFile(profile, variant, format)
          await page.getByRole('button', { name: /hojas de vida descargables/i }).first().click()

          const option = page.getByRole('link', {
            name: `Descargar hoja de vida ${PROFILE_LABELS[profile]} formato ${VARIANT_LABELS[variant]} ${format === 'pdf' ? 'PDF' : 'Word'}`,
          })
          const profilePath = `${profile}/`
          await expect(option).toHaveAttribute('download', expectedFile)
          await expect(option).toHaveAttribute('href', new RegExp(`/cv/${profilePath}${expectedFile}$`))

          const [download] = await Promise.all([page.waitForEvent('download'), option.click()])
          await expect(download.failure()).resolves.toBeNull()
          expect(download.suggestedFilename()).toBe(expectedFile)

          const downloadedPath = await download.path()
          expect(downloadedPath).toBeTruthy()
          const body = await fs.readFile(downloadedPath!)
          expect(body.byteLength).toBeGreaterThan(0)
          if (format === 'pdf') {
            const text = body.toString('latin1')
            expect(text.startsWith('%PDF')).toBe(true)
            expect(text).toContain(`/Title (${outputs[profile].name} - CV ${VARIANT_LABELS[variant]})`)
          } else {
            expect(body.subarray(0, 2).toString()).toBe('PK')
          }
        })
      }
    }
  }

  test('should close download dialog with close semantic button', async ({ page }) => {
    await page.getByRole('button', { name: /hojas de vida descargables/i }).first().click()
    const dialog = page.getByRole('dialog', { name: /descargar hojas de vida/i })
    await expect(dialog).toBeVisible()
    await page.getByRole('button', { name: /cerrar dialogo de descarga/i }).click()
    await expect(dialog).toBeHidden()
  })
})
