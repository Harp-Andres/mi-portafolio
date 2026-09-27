/// <reference types="vitest/globals" />
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { Certificates } from '../Certificates'

const mockByCategory = {
  'DevOps & Cloud': [
    {
      title: 'Azure DevOps — Udemy',
      filePath: '/certificados/Azure/Udemy/certificado-azure.jpg',
      hours: 21,
    },
  ],
  'Calidad & QA': [
    { title: 'ISTQB Foundation', filePath: null, hours: 24 },
  ],
  'IA & Productividad': [
    { title: 'GitHub Copilot', filePath: null, hours: 5 },
  ],
}

describe('Certificates Component', () => {
  it('should render courses carousel with snap classes on mobile layout', () => {
    render(<Certificates byCategory={mockByCategory} />)

    const carousel = screen.getByTestId('courses-carousel')
    expect(carousel).toHaveClass('overflow-x-auto')
    expect(carousel).toHaveClass('snap-x')
    expect(carousel).toHaveClass('snap-mandatory')
    expect(carousel).toHaveClass('md:grid')
    expect(carousel).toHaveClass('md:grid-cols-2')
    expect(carousel).toHaveClass('lg:grid-cols-3')
  })

  it('should render course category cards at ~85% width with snap-center', () => {
    render(<Certificates byCategory={mockByCategory} />)

    const cards = screen.getAllByTestId('course-category-card')
    expect(cards.length).toBe(3)
    cards.forEach((card) => {
      expect(card).toHaveClass('w-[85%]')
      expect(card).toHaveClass('snap-center')
      expect(card).toHaveClass('md:w-auto')
    })
  })

  it('should show mobile swipe hint for course categories', () => {
    render(<Certificates byCategory={mockByCategory} />)
    expect(
      screen.getByText(/Desliza horizontalmente para ver cada categoría/i)
    ).toBeInTheDocument()
  })

  it('should use single-column then two-column grid for official certifications', () => {
    const { container } = render(
      <Certificates
        byCategory={mockByCategory}
        officialCertifications={[
          {
            title: 'ISTQB',
            issuer: 'ISTQB',
            color: 'border-blue-500 bg-blue-50',
            icon: '✅',
          },
          {
            title: 'Azure',
            issuer: 'Microsoft',
            color: 'border-sky-500 bg-sky-50',
            icon: '☁️',
          },
        ]}
      />
    )

    const officialGrid = container.querySelector('.grid.grid-cols-1.sm\\:grid-cols-2')
    expect(officialGrid).toBeInTheDocument()
  })

  describe('certificate downloads', () => {
    beforeEach(() => {
      ;(import.meta.env as { BASE_URL: string }).BASE_URL = '/mi-portafolio/'
      vi.stubGlobal('URL', {
        ...URL,
        createObjectURL: vi.fn(() => 'blob:mock-cert'),
        revokeObjectURL: vi.fn(),
      })
      vi.stubGlobal(
        'fetch',
        vi.fn(async () => ({
          ok: true,
          status: 200,
          blob: async () => new Blob(['fake-cert']),
        }))
      )
    })

    afterEach(() => {
      vi.unstubAllGlobals()
      vi.restoreAllMocks()
    })

    it('should fetch certificates under BASE_URL when clicked', async () => {
      render(<Certificates byCategory={mockByCategory} />)
      fireEvent.click(screen.getByRole('button', { name: /Azure DevOps — Udemy/i }))

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          '/mi-portafolio/certificados/Azure/Udemy/certificado-azure.jpg'
        )
      })
      await waitFor(() => {
        expect(URL.createObjectURL).toHaveBeenCalled()
      })
    })
  })
})
