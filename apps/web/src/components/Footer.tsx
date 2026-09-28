export const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="bg-black text-white py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <p className="text-center text-gray-400">
          © {currentYear} Andrés Rodríguez Pisa. Todos los derechos reservados.
        </p>
      </div>
    </footer>
  )
}
