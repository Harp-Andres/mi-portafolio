/**
 * CV data rendered by the web. It is the JSON the Python backend (apps/api) writes next to the
 * Word/PDF it renders, so the page always shows exactly what the downloadable CV says.
 * Change the CV with a request in cv/qa/input/requests and `pnpm cv:apply`; never edit it here.
 */

import type { CertificateLink, CourseCertificate, CVData, CVDocument, CVDocumentFormat, CVDocumentVariant, CVDownloadProfile, CVProfile } from '../types';
import backendOutput from '../../../../cv/qa/output/cv-data.json';
import devopsBackendOutput from '../../../../cv/devops-qa/output/cv-data.json';

const { _meta: meta, ...data } = backendOutput;
const { _meta: devopsMeta } = devopsBackendOutput;

const toDocuments = (documents: typeof meta.documents): CVDocument[] => documents.map((doc) => ({
  variant: doc.variant as CVDocumentVariant,
  format: doc.format as CVDocumentFormat,
  file: doc.file,
}));

export const CV_DATA: CVData = data;

export const CV_DOCUMENTS: CVDocument[] = toDocuments(meta.documents);

export const CV_DOWNLOAD_PROFILES: CVDownloadProfile[] = [
  {
    id: 'qa',
    label: 'QA Automation',
    description: 'Automatización Web, API y Mobile con enfoque en calidad continua.',
    documents: CV_DOCUMENTS,
  },
  {
    id: 'devops-qa',
    label: 'DevOps',
    description: 'Experiencia QA orientada a CI/CD, contenedores y automatización de entregas.',
    documents: toDocuments(devopsMeta.documents),
  },
];

export const CV_FINGERPRINT: string = meta.fingerprint;

export function getCvDocument(variant: CVDocumentVariant, format: CVDocumentFormat = 'pdf'): CVDocument {
  return getProfileCvDocument('qa', variant, format);
}

export function getProfileCvDocuments(profile: CVProfile): CVDocument[] {
  const documents = CV_DOWNLOAD_PROFILES.find((item) => item.id === profile)?.documents;
  if (!documents) throw new Error(`The backend did not publish the ${profile} CV profile`);
  return documents;
}

export function getProfileCvDocument(
  profile: CVProfile,
  variant: CVDocumentVariant,
  format: CVDocumentFormat = 'pdf',
): CVDocument {
  const document = getProfileCvDocuments(profile).find((doc) => doc.variant === variant && doc.format === format);
  if (!document) throw new Error(`The backend did not publish a ${variant} ${format} CV for ${profile}`);
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
