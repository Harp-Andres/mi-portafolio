import { test, expect } from '@playwright/test'
import { promises as fs, readFileSync } from 'node:fs'

type CvVariant = 'ats' | 'visual'

interface CvOutput {
  name: string
  _meta: { documents: { variant: CvVariant; format: string; file: string }[] }
}

const cvOutput: CvOutput = JSON.parse(
  readFileSync(new URL('../../../../cv/output/cv-data.json', import.meta.url), 'utf-8'),
)

const cvPdfFile = (variant: CvVariant): string => {
  const doc = cvOutput._meta.documents.find((d) => d.variant === variant && d.format === 'pdf')
  if (!doc) throw new Error(`cv-data.json lists no ${variant} PDF`)
  return doc.file
}

const PDF_VARIANTS = [
  { variant: 'ats', link: /formato ats pdf/i, title: `${cvOutput.name} - CV ATS` },
  { variant: 'visual', link: /formato visual pdf/i, title: `${cvOutput.name} - CV Visual` },
] as const

test.describe('CV Download E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should expose semantic download trigger and dialog', async ({ page }) => {
    const trigger = page.getByRole('button', { name: /hoja de vida descargable/i }).first()
    await expect(trigger).toBeVisible()
    await expect(trigger).toBeEnabled()

    await trigger.click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog).toBeVisible()
    await expect(dialog.getByText(/selecciona el formato/i)).toBeVisible()
  })

  for (const { variant, link, title } of PDF_VARIANTS) {
    test(`should download the ${variant} PDF CV from its own option`, async ({ page }) => {
      const expectedFile = cvPdfFile(variant)
      await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

      const option = page.getByRole('link', { name: link })
      await expect(option).toHaveAttribute('download', expectedFile)
      await expect(option).toHaveAttribute('href', new RegExp(`/cv/${expectedFile}$`))

      const [download] = await Promise.all([page.waitForEvent('download'), option.click()])

      await expect(download.failure()).resolves.toBeNull()
      expect(download.suggestedFilename()).toBe(expectedFile)

      const downloadedPath = await download.path()
      expect(downloadedPath).toBeTruthy()

      const body = await fs.readFile(downloadedPath!, 'latin1')
      expect(body.startsWith('%PDF')).toBe(true)
      expect(body).toContain(`/Title (${title})`)
    })
  }

  test('should expose both semantic format options in dialog', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog.getByRole('link', { name: /formato ats pdf/i })).toBeVisible()
    await expect(dialog.getByRole('link', { name: /formato visual pdf/i })).toBeVisible()
  })

  test('should close download dialog with close semantic button', async ({ page }) => {
    await page.getByRole('button', { name: /hoja de vida descargable/i }).first().click()

    const dialog = page.getByRole('dialog', { name: /descargar hoja de vida/i })
    await expect(dialog).toBeVisible()

    await page.getByRole('button', { name: /cerrar dialogo de descarga/i }).click()
    await expect(dialog).toBeHidden()
  })
})
