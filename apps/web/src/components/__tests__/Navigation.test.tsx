/// <reference types="vitest/globals" />
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { HashRouter } from 'react-router-dom'
import { Navigation } from '../Navigation'

vi.mock('../../hooks', () => ({
  useScrollPosition: () => false,
  useSectionNavigation: () => ({
    goToSection: () => () => undefined,
  }),
}))

const renderNavigation = () => render(<HashRouter><Navigation /></HashRouter>)

describe('Navigation Component', () => {
  it('should render navigation with logo', () => {
    renderNavigation()
    expect(screen.getByText('INICIO')).toBeInTheDocument()
  })

  it('should render all navigation links', () => {
    renderNavigation()
    expect(screen.getByText('Sobre Mi')).toBeInTheDocument()
    expect(screen.getByText('Habilidades')).toBeInTheDocument()
    expect(screen.getByText('Experiencia')).toBeInTheDocument()
    expect(screen.getByText('Educacion')).toBeInTheDocument()
  })

  it('should render section links as buttons', () => {
    renderNavigation()
    expect(screen.getByRole('button', { name: /sobre mi/i })).toBeInTheDocument()
  })

  it('should toggle mobile menu on button click', () => {
    renderNavigation()

    fireEvent.click(screen.getByRole('button', { name: /abrir menu principal/i }))

    expect(screen.getAllByText('Sobre Mi').length).toBeGreaterThan(1)
  })

  it('should expose a 44px touch target on the hamburger button', () => {
    renderNavigation()
    const menuButton = screen.getByRole('button', { name: /abrir menu principal/i })
    expect(menuButton).toHaveClass('min-h-11')
    expect(menuButton).toHaveClass('min-w-11')
    expect(menuButton).toHaveClass('flex-shrink-0')
  })

  it('should be fixed position', () => {
    const { container } = renderNavigation()
    const nav = container.querySelector('nav')
    expect(nav).toHaveClass('fixed')
    expect(nav).toHaveClass('w-full')
    expect(nav).toHaveClass('z-50')
  })
})
