import type { CourseCertificate, OfficialCertification } from '@mportafolio/core'
import { downloadPublicAsset } from '../utils/public-asset'

interface CertificatesProps {
  byCategory?: Record<string, CourseCertificate[]>
  learningPaths?: CourseCertificate[]
  officialCertifications?: OfficialCertification[]
}

const CATEGORY_STYLES: Record<string, { color: string; icon: string }> = {
  'DevOps & Cloud': { color: 'border-orange-500 bg-orange-50', icon: '☁️' },
  'Calidad & QA': { color: 'border-blue-500 bg-blue-50', icon: '✅' },
  'Automatización Web & Mobile': { color: 'border-green-500 bg-green-50', icon: '🔧' },
  'Playwright & API Testing': { color: 'border-purple-500 bg-purple-50', icon: '🎭' },
  'Otros Frameworks & Herramientas': { color: 'border-pink-500 bg-pink-50', icon: '⚙️' },
  'IA & Productividad': { color: 'border-red-500 bg-red-50', icon: '🤖' },
  'Programación & Desarrollo': { color: 'border-indigo-500 bg-indigo-50', icon: '💻' },
}

const DEFAULT_CATEGORY_STYLE = { color: 'border-gray-300 bg-gray-50', icon: '📌' }

interface DownloadButtonProps {
  title: string
  filePath: string
  className: string
  iconClassName: string
}

const DownloadButton = ({ title, filePath, className, iconClassName }: DownloadButtonProps) => (
  <button
    type="button"
    onClick={() => void downloadPublicAsset(filePath)}
    className={`text-left text-blue-600 hover:text-blue-800 hover:underline transition-colors cursor-pointer ${className}`}
    title="Clic para descargar"
  >
    {title}
    <span className={iconClassName}>📥</span>
  </button>
)

const OfficialCertifications = ({ items }: { items: OfficialCertification[] }) => (
  <div className="mb-16">
    <h3 className="text-2xl font-bold mb-8 text-gray-900">Certificaciones Oficiales</h3>
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
      {items.map((cert, index) => (
        <div key={index} className={`border-l-4 rounded-lg p-6 flex flex-col items-start ${cert.color}`}>
          <div className="flex items-center gap-3 mb-3">
            <span className="text-3xl">{cert.icon}</span>
            <div>
              <h4 className="text-lg font-bold text-gray-900">{cert.title}</h4>
              <p className="text-sm text-gray-600">Emisor: {cert.issuer}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
)

const LearningPaths = ({ items }: { items: CourseCertificate[] }) => (
  <div className="mb-16">
    <h3 className="text-2xl font-bold mb-8 text-gray-900">Rutas de Aprendizaje</h3>
    <p className="text-gray-600 mb-6 text-sm italic">Programas formales y de mayor duración</p>
    <div className="grid grid-cols-1 gap-6">
      {items.map((cert, index) => (
        <div
          key={index}
          className="border-l-4 border-indigo-500 bg-indigo-50 rounded-lg p-6 flex flex-col sm:flex-row sm:items-center sm:justify-between"
        >
          <div className="flex-1">
            {cert.filePath ? (
              <DownloadButton
                title={cert.title}
                filePath={cert.filePath}
                className="text-lg font-semibold"
                iconClassName="ml-2 text-sm"
              />
            ) : (
              <h4 className="text-lg font-semibold text-gray-900">{cert.title}</h4>
            )}
          </div>
          {cert.hours ? (
            <div className="mt-3 sm:mt-0 sm:ml-4 flex items-center gap-2 bg-white rounded-full px-4 py-2 text-sm font-semibold text-indigo-700">
              <span>⏱️</span>
              <span>{cert.hours} horas</span>
            </div>
          ) : null}
        </div>
      ))}
    </div>
  </div>
)

const CourseCategoryCard = ({ category, courses }: { category: string; courses: CourseCertificate[] }) => {
  const style = CATEGORY_STYLES[category] ?? DEFAULT_CATEGORY_STYLE

  return (
    <div
      data-testid="course-category-card"
      className={`border-l-4 rounded-lg p-6 min-h-56 flex flex-col shrink-0 w-[85%] snap-center md:w-auto md:min-w-0 md:shrink ${style.color}`}
    >
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">{style.icon}</span>
        <h4 className="text-lg font-bold text-gray-900">{category}</h4>
      </div>
      <ul className="space-y-3">
        {courses.map((course, index) => (
          <li key={index} className="flex flex-col gap-1">
            <div className="flex items-start gap-2">
              <span className="text-blue-600 font-bold mt-1">•</span>
              {course.filePath ? (
                <DownloadButton
                  title={course.title}
                  filePath={course.filePath}
                  className="text-sm"
                  iconClassName="ml-1 text-xs"
                />
              ) : (
                <span className="text-gray-700 text-sm">{course.title}</span>
              )}
            </div>
            {course.hours ? <span className="text-xs text-gray-500 ml-5">⏱️ {course.hours} horas</span> : null}
          </li>
        ))}
      </ul>
    </div>
  )
}

const CourseCategories = ({ byCategory }: { byCategory: Record<string, CourseCertificate[]> }) => (
  <div>
    <h3 className="text-2xl font-bold mb-4 text-gray-900">Cursos de Formación</h3>
    <p className="md:hidden text-sm text-gray-500 mb-4 italic">Desliza horizontalmente para ver cada categoría</p>
    <div
      data-testid="courses-carousel"
      className="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-2 -mx-4 px-4 md:mx-0 md:px-0 md:grid md:grid-cols-2 lg:grid-cols-3 md:overflow-visible md:snap-none md:pb-0"
    >
      {Object.entries(byCategory).map(([category, courses]) => (
        <CourseCategoryCard key={category} category={category} courses={courses} />
      ))}
    </div>
  </div>
)

export const Certificates = ({ byCategory = {}, learningPaths = [], officialCertifications = [] }: CertificatesProps) => (
  <section id="certificates" aria-labelledby="certificates-title" className="py-16 bg-white">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 id="certificates-title" className="text-3xl font-bold mb-12 text-gray-900">Certificaciones & Formación</h2>
      {officialCertifications.length > 0 && <OfficialCertifications items={officialCertifications} />}
      {learningPaths.length > 0 && <LearningPaths items={learningPaths} />}
      <CourseCategories byCategory={byCategory} />
    </div>
  </section>
)
