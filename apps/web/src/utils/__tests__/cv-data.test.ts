/// <reference types="vitest/globals" />
import { describe, it, expect } from 'vitest'
import { CV_DATA, CV_DOCUMENTS, getCertificateLinks, getCvDocument } from '@mportafolio/core'

describe('CV Data Constants', () => {
  it('should have required personal information', () => {
    expect(CV_DATA.name).toBeTruthy()
    expect(CV_DATA.title).toBeTruthy()
    expect(CV_DATA.email).toBeTruthy()
    expect(CV_DATA.phone1).toBeTruthy()
    expect(CV_DATA.location).toBeTruthy()
  })

  it('should have valid email format', () => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    expect(CV_DATA.email).toMatch(emailRegex)
  })

  it('should have valid contact links', () => {
    expect(CV_DATA.linkedin).toBeTruthy()
    expect(CV_DATA.github).toBeTruthy()
  })

  it('should use the renamed GitHub Pages portfolio URL', () => {
    expect(CV_DATA.portfolio).toBe('https://harp-andres.github.io/mi-portafolio/')
  })

  it('should have non-empty profile description', () => {
    expect(CV_DATA.profile.length).toBeGreaterThan(50)
  })

  it('should have skills array with categories', () => {
    expect(Array.isArray(CV_DATA.skills)).toBe(true)
    expect(CV_DATA.skills.length).toBeGreaterThan(0)
  })

  it('should have experience array with required fields', () => {
    expect(Array.isArray(CV_DATA.experience)).toBe(true)
    expect(CV_DATA.experience.length).toBeGreaterThan(0)
  })

  it('should have education array', () => {
    expect(Array.isArray(CV_DATA.education)).toBe(true)
    expect(CV_DATA.education.length).toBeGreaterThan(0)
  })

  it('should derive the flat certificate list from every category, learning path and official cert', () => {
    const courses = Object.values(CV_DATA.certificatesByCategory).flat()
    const expected =
      CV_DATA.officialCertifications.length + CV_DATA.learningPathsCertifications.length + courses.length
    expect(getCertificateLinks()).toHaveLength(expected)
    expect(getCertificateLinks()[0].title).toContain(CV_DATA.officialCertifications[0].issuer)
  })

  it('should expose the ATS and Visual documents published by the backend', () => {
    expect(CV_DOCUMENTS).toHaveLength(4)
    expect(getCvDocument('ats').file).toMatch(/_ATS_.*\.pdf$/)
    expect(getCvDocument('visual', 'docx').file).toMatch(/_Visual_.*\.docx$/)
  })

  it('should have languages', () => {
    expect(Array.isArray(CV_DATA.languages)).toBe(true)
    expect(CV_DATA.languages.length).toBeGreaterThan(0)
  })

  it('should have valid birth date format', () => {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/
    expect(CV_DATA.birthDate).toMatch(dateRegex)
  })
})
