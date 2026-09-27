/**
 * CV data rendered by the web. It is the JSON the Python backend (apps/api) writes next to the
 * Word/PDF it renders, so the page always shows exactly what the downloadable CV says.
 * Change the CV with a request in cv/input/requests and `pnpm cv:apply`; never edit it here.
 */

import type { CertificateLink, CourseCertificate, CVData, CVDocument, CVDocumentFormat, CVDocumentVariant } from '../types';
import backendOutput from '../../../../cv/output/cv-data.json';

const { _meta: meta, ...data } = backendOutput;

export const CV_DATA: CVData = data;

export const CV_DOCUMENTS: CVDocument[] = meta.documents.map((doc) => ({
  variant: doc.variant as CVDocumentVariant,
  format: doc.format as CVDocumentFormat,
  file: doc.file,
}));

export const CV_FINGERPRINT: string = meta.fingerprint;

export function getCvDocument(variant: CVDocumentVariant, format: CVDocumentFormat = 'pdf'): CVDocument {
  const document = CV_DOCUMENTS.find((doc) => doc.variant === variant && doc.format === format);
  if (!document) throw new Error(`The backend did not publish a ${variant} ${format} CV`);
  return document;
}

export function getAllCertificates(): CourseCertificate[] {
  return [...CV_DATA.learningPathsCertifications, ...Object.values(CV_DATA.certificatesByCategory).flat()];
}

/** Official certifications, learning paths and courses, in the order the carousel shows them. */
export function getCertificateLinks(): CertificateLink[] {
  return [
    ...CV_DATA.officialCertifications.map((cert) => ({ title: `${cert.title} — ${cert.issuer}`, filePath: cert.filePath })),
    ...getAllCertificates().map((course) => ({ title: course.title, filePath: course.filePath })),
  ];
}

export function getTotalCertificationHours(): number {
  return getAllCertificates().reduce((total, cert) => total + (cert.hours ?? 0), 0);
}
