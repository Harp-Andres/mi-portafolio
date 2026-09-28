import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useScrollPosition, useSectionNavigation } from '../hooks'
import { CVDownloads } from './CVDownloads'

export const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false)
  const isScrolled = useScrollPosition()
  const { goToSection } = useSectionNavigation()

  const toggleMenu = () => setIsOpen(!isOpen)

  const navLinks: (
    | { label: string; sectionId: string; isRoute: false }
    | { label: string; href: string; isRoute: true }
  )[] = [
    { label: 'Sobre Mi', sectionId: 'about', isRoute: false },
    { label: 'Habilidades', sectionId: 'skills', isRoute: false },
    { label: 'Experiencia', sectionId: 'experience', isRoute: false },
    { label: 'Educacion', sectionId: 'education', isRoute: false },
    { label: 'Demos Técnicas', href: '/demos', isRoute: true },
  ]

  return (
    <nav
      aria-label="Navegacion principal"
      className={`fixed w-full z-50 transition-all duration-300 ${
      isScrolled ? 'bg-black shadow-lg' : 'bg-black'
    }`}
    >
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 gap-2">
          
          {/* Logo */}
          <div className="flex-shrink-0 min-w-0">
            <Link
              to="/"
              aria-label="Ir al inicio"
              className="text-white font-bold text-lg sm:text-xl"
              onClick={() => window.scrollTo({ top: 0, behavior: 'auto' })}
            >
              INICIO
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6 lg:gap-8">
            {navLinks.map(link => (
              link.isRoute ? (
                <Link
                  key={link.href}
                  to={link.href}
                  className="whitespace-nowrap text-gray-300 hover:text-white transition-colors font-semibold"
                >
                  {link.label}
                </Link>
              ) : (
                <button
                  key={link.sectionId}
                  type="button"
                  onClick={goToSection(link.sectionId)}
                  className="whitespace-nowrap text-gray-300 hover:text-white transition-colors"
                >
                  {link.label}
                </button>
              )
            ))}
          </div>

          {/* Download Button Desktop */}
          <div className="hidden lg:flex items-center">
            <CVDownloads />
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex-shrink-0">
            <button
              onClick={toggleMenu}
              aria-label={isOpen ? 'Cerrar menu principal' : 'Abrir menu principal'}
              aria-expanded={isOpen}
              aria-controls="menu-principal-movil"
              className="min-h-11 min-w-11 flex-shrink-0 inline-flex items-center justify-center p-2 text-gray-300 hover:text-white"
            >
              {isOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div id="menu-principal-movil" className="md:hidden pb-4">
            <div className="space-y-2">
              {navLinks.map(link => (
                link.isRoute ? (
                  <Link
                    key={link.href}
                    to={link.href}
                    className="block px-3 py-2 text-gray-300 hover:text-white transition-colors font-semibold"
                    onClick={() => setIsOpen(false)}
                  >
                    {link.label}
                  </Link>
                ) : (
                  <button
                    key={link.sectionId}
                    type="button"
                    onClick={(event) => {
                      goToSection(link.sectionId)(event)
                      setIsOpen(false)
                    }}
                    className="block w-full text-left px-3 py-2 text-gray-300 hover:text-white transition-colors"
                  >
                    {link.label}
                  </button>
                )
              ))}
              <div className="pt-4 px-3">
                <CVDownloads />
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
