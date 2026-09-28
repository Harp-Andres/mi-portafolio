import { describe, it, expect } from 'vitest'
import { PROJECTS } from '@mportafolio/core'

const featuredIds = PROJECTS.filter(p => p.type === 'featured').map(p => p.id)

describe('PROJECTS', () => {
  it('features the mobile demos alongside the web frameworks', () => {
    expect(featuredIds).toEqual(
      expect.arrayContaining([
        'qa-playwright-ai-framework',
        'appium-mobile-cloud-automation-framework',
        'appium-mobile-automation-framework',
        'demo-serenity-screenplay-mobile',
      ]),
    )
  })

  it('keeps project ids unique', () => {
    expect(new Set(PROJECTS.map(p => p.id)).size).toBe(PROJECTS.length)
  })

  it.each(PROJECTS.map(p => [p.id, p] as const))('%s copy does not undersell the demo', (_id, project) => {
    const copy = [project.description, project.longDescription, ...project.highlights].join(' ').toLowerCase()
    for (const phrase of ['productivo', 'didáctico', 'no compite', 'rival', 'competir', 'scaffold', 'fallback']) {
      expect(copy).not.toContain(phrase)
    }
  })
})
