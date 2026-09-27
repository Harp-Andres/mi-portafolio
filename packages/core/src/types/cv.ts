/**
 * CV data contract. The editable source is cv/input/cv-data.json; Python validates it and
 * writes packages/core/src/data/cv-data.generated.json with this shape.
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
  /** Derived by Python: official + learning paths + courses, used by the certificates carousel. */
  certificates: CertificateLink[];
  languages: Language[];
}
