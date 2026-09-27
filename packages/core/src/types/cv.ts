/**
 * CV data contract: the shape of cv/output/cv-data.json, written by the Python backend
 * (apps/api/app/infrastructure/persistence/json_codec.py) together with the Word/PDF.
 */

export interface SkillCategory {
  category: string;
  items: string;
}

export interface Experience {
  company: string;
  role: string;
  period: string;
  technologies: string[];
  bullets: string[];
}

export interface Education {
  degree: string;
  institution: string;
  year: string;
}

export interface CourseCertificate {
  title: string;
  filePath: string | null;
  hours?: number;
}

export interface OfficialCertification {
  title: string;
  issuer: string;
  color: string;
  icon: string;
  filePath: string | null;
}

export interface CertificateLink {
  title: string;
  filePath: string | null;
}

export interface Language {
  lang: string;
  level: string;
}

export interface CVData {
  name: string;
  title: string;
  email: string;
  phone1: string;
  phone2: string;
  location: string;
  linkedin: string;
  github: string;
  portfolio: string;
  birthDate: string;
  profile: string;
  skills: SkillCategory[];
  experience: Experience[];
  education: Education[];
  officialCertifications: OfficialCertification[];
  certificatesByCategory: Record<string, CourseCertificate[]>;
  learningPathsCertifications: CourseCertificate[];
  languages: Language[];
}

export type CVDocumentVariant = 'ats' | 'visual';
export type CVDocumentFormat = 'pdf' | 'docx';

/** A CV file rendered by the backend into cv/output and served by the web under /cv/. */
export interface CVDocument {
  variant: CVDocumentVariant;
  format: CVDocumentFormat;
  file: string;
}
