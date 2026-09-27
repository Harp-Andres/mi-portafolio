import { test, expect } from '@playwright/test'
import { promises as fs } from 'fs'

test.describe('Certificate download E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should download a course certificate using the Vite base path', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /certificaciones & formación/i }).scrollIntoViewIfNeeded()

    const azureButton = page.getByRole('button', {
      name: /DevOps y Cloud con Azure DevOps, App Service Pipelines y Git — Udemy/i,
    })
    await expect(azureButton).toBeVisible()

    const [download] = await Promise.all([
      page.waitForEvent('download'),
      azureButton.click(),
    ])

    await expect(download.failure()).resolves.toBeNull()
    expect(download.suggestedFilename()).toMatch(/certificado-azure\.jpg$/i)

    const downloadedPath = await download.path()
    expect(downloadedPath).toBeTruthy()
    const body = await fs.readFile(downloadedPath!)
    expect(body.byteLength).toBeGreaterThan(1000)
  })

  test('should request certificate assets under /mi-portafolio/ base', async ({ page }) => {
    await page.getByRole('heading', { level: 2, name: /certificaciones & formación/i }).scrollIntoViewIfNeeded()

    const responsePromise = page.waitForResponse(
      (response) =>
        response.url().includes('/mi-portafolio/certificados/') &&
        response.status() === 200
    )

    await page
      .getByRole('button', {
        name: /DevOps y Cloud con Azure DevOps, App Service Pipelines y Git — Udemy/i,
      })
      .click()

    const response = await responsePromise
    expect(response.url()).toContain('/mi-portafolio/certificados/Azure/Udemy/certificado-azure.jpg')
  })
})
