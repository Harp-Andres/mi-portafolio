/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { publicAssetFilename, resolvePublicAssetUrl } from '../public-asset'

describe('public-asset helpers', () => {
  const originalBase = import.meta.env.BASE_URL

  beforeEach(() => {
    vi.stubEnv('BASE_URL', '/mi-portafolio/')
  })

  afterEach(() => {
    vi.unstubAllEnvs()
    // restore in case stubEnv does not cover import.meta.env.BASE_URL in this setup
    ;(import.meta.env as { BASE_URL: string }).BASE_URL = originalBase
  })

  it('prefixes asset paths with Vite BASE_URL', () => {
    ;(import.meta.env as { BASE_URL: string }).BASE_URL = '/mi-portafolio/'
    expect(resolvePublicAssetUrl('/certificados/Azure/Udemy/certificado-azure.jpg')).toBe(
      '/mi-portafolio/certificados/Azure/Udemy/certificado-azure.jpg'
    )
  })

  it('encodes spaces in path segments', () => {
    ;(import.meta.env as { BASE_URL: string }).BASE_URL = '/mi-portafolio/'
    expect(
      resolvePublicAssetUrl(
        '/certificados/Scrum/Certmind/certificate_Scrum Practitioner_hardware andres_rodriguez.pdf'
      )
    ).toBe(
      '/mi-portafolio/certificados/Scrum/Certmind/certificate_Scrum%20Practitioner_hardware%20andres_rodriguez.pdf'
    )
  })

  it('extracts a human filename from the path', () => {
    expect(publicAssetFilename('/certificados/Docker/certificado-docker.jpg')).toBe(
      'certificado-docker.jpg'
    )
  })
})
