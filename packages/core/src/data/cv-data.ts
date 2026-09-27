/**
 * CV data rendered by the web. Do not edit here: change cv/input/cv-data.json and run
 * `pnpm generate:cv`, which validates the input and rewrites cv-data.generated.json.
 */

import type { CourseCertificate, CVData } from '../types';
import generated from './cv-data.generated.json';

export const CV_DATA: CVData = generated;

export function getAllCertificates(): CourseCertificate[] {
  return [...CV_DATA.learningPathsCertifications, ...Object.values(CV_DATA.certificatesByCategory).flat()];
}

export function getTotalCertificationHours(): number {
  return getAllCertificates().reduce((total, cert) => total + (cert.hours ?? 0), 0);
}
