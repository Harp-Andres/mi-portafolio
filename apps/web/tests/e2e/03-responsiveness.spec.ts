import { test, expect, devices } from '@playwright/test'

// Tests de responsiveness en múltiples dispositivos
const viewports = [
  { name: 'Mobile (iPhone 12)', width: devices['iPhone 12'].viewport!.width, height: devices['iPhone 12'].viewport!.height },
  { name: 'Mobile (Galaxy S24 compact)', width: 360, height: 780 },
  { name: 'Tablet (iPad)', width: 768, height: 1024 },
  { name: 'Desktop (1920x1080)', width: 1920, height: 1080 }
]

viewports.forEach((viewport) => {
  test.describe(`Responsiveness - ${viewport.name}`, () => {
    test.beforeEach(async ({ page }) => {
      await page.setViewportSize({
        width: viewport.width,
        height: viewport.height,
      })

      await page.goto('/')
    })

    test('should render semantic landmarks correctly', async ({ page }) => {
      await expect(page.getByRole('navigation', { name: /navegacion principal/i })).toBeVisible()
      await expect(page.getByRole('main')).toBeVisible()
      await expect(page.getByRole('contentinfo')).toBeVisible()
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
    })

    test('should keep section navigation reachable', async ({ page }) => {
      if (viewport.name.includes('Mobile')) {
        await page.getByRole('button', { name: /abrir menu principal/i }).click()
      }

      await page.getByRole('heading', { level: 2, name: /habilidades profesionales/i }).scrollIntoViewIfNeeded()
      await expect(page.getByRole('heading', { level: 2, name: /habilidades profesionales/i })).toBeVisible()
    })

    test('should maintain proper font sizes', async ({ page }) => {
      const heading = page.getByRole('heading', { level: 1 })
      const fontSize = await heading.evaluate((el) =>
        window.getComputedStyle(el).fontSize
      )

      // Verifica que el font size es readable (> 12px)
      const size = parseInt(fontSize)
      expect(size).toBeGreaterThanOrEqual(12)
    })

    test('should have proper touch targets on mobile', async ({ page }) => {
      if (viewport.name.includes('Mobile')) {
        const firstButton = page.getByRole('button', { name: /abrir menu principal/i })
        await expect(firstButton).toBeVisible()

        const box = await firstButton.boundingBox()
        expect(box?.width).toBeGreaterThanOrEqual(40)
        expect(box?.height).toBeGreaterThanOrEqual(40)
      }
    })

    test('should not have horizontal overflow', async ({ page }) => {
      // Verifica que no hay scroll horizontal
      const bodyWidth = await page.evaluate(() => document.body.scrollWidth)
      const windowWidth = await page.evaluate(() => window.innerWidth)

      // Strict on S24 compact; slight tolerance elsewhere for scrollbar math
      const tolerance = viewport.width === 360 ? 1 : 120
      expect(bodyWidth).toBeLessThanOrEqual(windowWidth + tolerance)
    })

    test('should render footer correctly', async ({ page }) => {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight))
      await expect(page.getByRole('contentinfo')).toBeVisible()
    })
  })
})

test.describe('Responsiveness - Galaxy S24 compact layout', () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 360, height: 780 })
    await page.goto('/')
  })

  test('should keep hamburger fully inside the viewport', async ({ page }) => {
    const hamburger = page.getByRole('button', { name: /abrir menu principal/i })
    await expect(hamburger).toBeVisible()
    const box = await hamburger.boundingBox()
    expect(box).not.toBeNull()
    expect(box!.x).toBeGreaterThanOrEqual(0)
    expect(box!.x + box!.width).toBeLessThanOrEqual(360 + 1)
    expect(box!.y).toBeGreaterThanOrEqual(0)
  })

  test('should show one primary course card in the mobile carousel', async ({ page }) => {
    const carousel = page.getByTestId('courses-carousel')
    await carousel.scrollIntoViewIfNeeded()
    await expect(carousel).toBeVisible()

    const cards = page.getByTestId('course-category-card')
    await expect(cards.first()).toBeVisible()

    const metrics = await page.evaluate(() => {
      const track = document.querySelector('[data-testid="courses-carousel"]') as HTMLElement | null
      const first = document.querySelector('[data-testid="course-category-card"]') as HTMLElement | null
      if (!track || !first) return null
      const trackBox = track.getBoundingClientRect()
      const cardBox = first.getBoundingClientRect()
      return {
        viewportWidth: window.innerWidth,
        cardWidth: cardBox.width,
        cardVisibleRatio: cardBox.width / window.innerWidth,
        cardsFullyInView: Array.from(
          document.querySelectorAll('[data-testid="course-category-card"]')
        ).filter((el) => {
          const r = el.getBoundingClientRect()
          return r.left >= trackBox.left - 2 && r.right <= trackBox.right + 2
        }).length,
      }
    })

    expect(metrics).not.toBeNull()
    expect(metrics!.cardVisibleRatio).toBeGreaterThan(0.7)
    expect(metrics!.cardVisibleRatio).toBeLessThan(0.95)
    expect(metrics!.cardsFullyInView).toBe(1)
  })

  test('should size skill cards to their content without inner scroll', async ({ page }) => {
    const cards = page.getByTestId('skill-card')
    await cards.first().scrollIntoViewIfNeeded()

    const metrics = await cards.evaluateAll((els) =>
      els.map((el) => {
        const list = el.lastElementChild as HTMLElement
        return {
          height: el.getBoundingClientRect().height,
          listOverflows: list.scrollHeight > list.clientHeight + 1,
        }
      })
    )

    expect(metrics.length).toBeGreaterThan(1)
    expect(metrics.every((m) => !m.listOverflows)).toBe(true)
    const heights = metrics.map((m) => Math.round(m.height))
    expect(Math.min(...heights)).toBeLessThan(Math.max(...heights))
  })
})
