import { useState } from 'react'
import { Download, X } from 'lucide-react'
import { CV_DOWNLOAD_PROFILES } from '@mportafolio/core'
import type { CVDownloadProfile, CVDocumentFormat, CVDocumentVariant } from '@mportafolio/core'
import { cvDocumentUrl } from '../utils/cv-document'

const FORMAT_LABELS: Record<CVDocumentFormat, string> = { pdf: 'PDF', docx: 'Word' }
const VARIANT_LABELS: Record<CVDocumentVariant, string> = { ats: 'ATS', visual: 'Visual' }

const ProfileDownloads = ({ profile, onDownload }: { profile: CVDownloadProfile; onDownload: () => void }) => (
  <section aria-labelledby={`cv-profile-${profile.id}`} className="rounded-xl border border-gray-200 p-4">
    <div className="mb-4">
      <h4 id={`cv-profile-${profile.id}`} className="text-lg font-bold text-gray-900">{profile.label}</h4>
      <p className="mt-1 text-sm text-gray-600">{profile.description}</p>
    </div>
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
      {profile.documents.map((document) => {
        const target = cvDocumentUrl(document.variant, document.format, profile.id)
        const label = `${VARIANT_LABELS[document.variant]} ${FORMAT_LABELS[document.format]}`
        return (
          <a
            key={`${profile.id}-${document.variant}-${document.format}`}
            href={target.href}
            download={target.filename}
            onClick={onDownload}
            aria-label={`Descargar hoja de vida ${profile.label} formato ${label}`}
            className="flex min-h-11 items-center justify-between gap-3 rounded-lg border-2 border-blue-600 p-3 text-gray-900 transition-colors hover:bg-blue-50"
          >
            <span className="font-semibold">{label}</span>
            <Download className="shrink-0 text-blue-600" size={20} aria-hidden="true" />
          </a>
        )
      })}
    </div>
  </section>
)

export const CVDownloads = () => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        aria-haspopup="dialog"
        aria-expanded={isOpen}
        aria-controls="cv-download-dialog"
        className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
      >
        <Download size={18} aria-hidden="true" />
        Hojas de Vida Descargables
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div
            id="cv-download-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="cv-download-title"
            aria-describedby="cv-download-description"
            className="max-h-[calc(100vh-2rem)] w-full max-w-4xl overflow-y-auto rounded-lg bg-white p-5 sm:p-8"
          >
            <div className="mb-4 flex items-center justify-between gap-4">
              <h3 id="cv-download-title" className="text-2xl font-bold text-gray-900">Descargar hojas de vida</h3>
              <button
                onClick={() => setIsOpen(false)}
                aria-label="Cerrar dialogo de descarga"
                className="flex min-h-11 min-w-11 shrink-0 items-center justify-center text-gray-500 hover:text-gray-900"
              >
                <X size={24} aria-hidden="true" />
              </button>
            </div>

            <p id="cv-download-description" className="mb-6 text-gray-600">
              Elige el perfil y el formato que necesitas. Cada hoja está disponible en versión ATS y Visual.
            </p>

            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              {CV_DOWNLOAD_PROFILES.map((profile) => (
                <ProfileDownloads key={profile.id} profile={profile} onDownload={() => setIsOpen(false)} />
              ))}
            </div>

            <p className="mt-6 text-center text-xs text-gray-500">
              Formatos disponibles: PDF y Word, según el documento publicado por el backend.
            </p>
          </div>
        </div>
      )}
    </>
  )
}
