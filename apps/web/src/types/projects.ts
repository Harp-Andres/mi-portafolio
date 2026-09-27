export interface Project {
  id: string
  name: string
  description: string
  longDescription: string
  technologies: string[]
  github: string
  link?: string
  highlights: string[]
  type: 'featured' | 'secondary' | 'supporting'
  image?: string
  stats?: {
    stars?: number
    watchers?: number
    forks?: number
  }
}

/** Kept in sync with packages/core PROJECTS (Portfolio page reads from @mportafolio/core). */
export const PROJECTS: Project[] = [
  {
    id: 'qa-playwright-ai-framework',
    name: 'QA Playwright AI Framework',
    description:
      'Framework reutilizable: Playwright + TypeScript (web & API), env Zod, logging pino, helpers AI-ready',
    longDescription:
      'Framework base (no producto productivo) para automatización web y API con Playwright + TypeScript estricto. POM, clientes API con mocks para CI, Docker/K8s, y capa AI-ready (healing/fallos). Unit tests con Vitest; E2E aparte.',
    technologies: [
      'Playwright',
      'TypeScript',
      'Vitest',
      'GitHub Actions',
      'Docker',
      'Kubernetes',
      'API Testing',
    ],
    github: 'https://github.com/Harp-Andres/qa-playwright-ai-framework',
    highlights: [
      'Framework reutilizable web + API',
      'Unit tests (Vitest) + E2E Playwright',
      'Logging estructurado (pino) sin console.log',
      'CI/CD, Docker y Kubernetes Job de ejemplo',
    ],
    type: 'featured',
  },
  {
    id: 'appium-mobile-cloud-automation-framework',
    name: 'Appium Mobile Cloud Framework',
    description:
      'Especializado en device farms (BrowserStack): Appium + Cucumber + Allure en la nube',
    longDescription:
      'Demo enfocada en ejecución cloud (BrowserStack App Automate). Appium, Cucumber/BDD, JUnit 5, Allure y GitHub Actions. Local solo como fallback. Complementa el framework Appium local hermano.',
    technologies: [
      'Appium',
      'Java',
      'Cucumber',
      'JUnit 5',
      'Allure',
      'BrowserStack',
      'GitHub Actions',
      'SLF4J',
    ],
    github: 'https://github.com/Harp-Andres/appium-mobile-cloud-automation-framework',
    highlights: [
      'Especialización cloud / BrowserStack',
      'Unit tests Gradle sin Appium',
      'Logging SLF4J/Logback (sin System.out)',
      'BDD + Allure en CI',
    ],
    type: 'featured',
  },
  {
    id: 'literalura',
    name: 'Literalura - Spring Boot',
    description:
      'Backend demo: Spring Boot, cliente Gutendex, JPA/PostgreSQL, consola separada del dominio',
    longDescription:
      'Demo Spring Boot con servicios de dominio, importación desde API externa, JPA y adaptador de consola desacoplado. Logging SLF4J; tests con H2/Mockito. Enfoque backend, no QA.',
    technologies: ['Java', 'Spring Boot', 'Spring Data JPA', 'PostgreSQL', 'REST APIs', 'Maven', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/Literalura',
    highlights: [
      'SOLID: servicios vs consola',
      'JPA + H2 en tests',
      'Cliente HTTP / mapeo DTO→entity',
      'Sin System.out en el dominio',
    ],
    type: 'featured',
  },
  {
    id: 'demo-playwright-datadriven-e2e',
    name: 'Playwright Data-Driven E2E Demo',
    description:
      'Demo de dominio: E2E data-driven (Excel) con Playwright + TypeScript — no es un framework rival',
    longDescription:
      'Sample de dominio (búsqueda de cruceros) que demuestra data-driven testing, mappers y POM por capas. Complementa qa-playwright-ai-framework (framework) en lugar de competir con él. Unit tests Vitest + logger estructurado.',
    technologies: ['Playwright', 'TypeScript', 'Vitest', 'Excel/XLSX', 'Data-Driven Testing', 'POM'],
    github: 'https://github.com/Harp-Andres/demo-playwright-datadriven-e2e',
    highlights: [
      'Especialización data-driven / dominio',
      'Unit tests Vitest (URL, env, mappers)',
      'Logger JSON (sin console.log)',
      'Complementa el framework Playwright',
    ],
    type: 'featured',
  },
  {
    id: 'portfolio-site',
    name: 'Mi Portafolio (This Site)',
    description: 'Demo portfolio site: React, TypeScript, monorepo, tests and GitHub Pages',
    longDescription:
      'This portfolio is itself a showcase: React + TypeScript monorepo, Vitest/Playwright tests, CV document generation, and GitHub Actions deploy to GitHub Pages.',
    technologies: [
      'React',
      'TypeScript',
      'Vite',
      'Tailwind CSS',
      'Vitest',
      'Playwright',
      'GitHub Actions',
      'GitHub Pages',
    ],
    github: 'https://github.com/Harp-Andres/mi-portafolio',
    link: 'https://harp-andres.github.io/mi-portafolio/',
    highlights: [
      'Monorepo with shared core data',
      'Unit + E2E test suites',
      'CI/CD to GitHub Pages',
      'Downloadable CV (PDF/DOCX)',
    ],
    type: 'featured',
  },
  {
    id: 'demo-serenity-screenplay-mobile',
    name: 'Serenity Screenplay Mobile',
    description: 'Demo didáctico: Serenity BDD Screenplay + Appium (patrón Screenplay)',
    longDescription:
      'Enseña el patrón Screenplay con Serenity BDD y Appium (Android/iOS). Paquetes com.harp.demo.screenplay, unit tests Gradle, E2E opcional con dispositivo. No compite con los frameworks Appium “raw”.',
    technologies: ['Java', 'Serenity BDD', 'Screenplay', 'Appium', 'Gradle', 'Cucumber', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/demo-serenity-screenplay-mobile',
    highlights: [
      'Especialización patrón Screenplay',
      'Unit tests sin dispositivo',
      'Logging SLF4J/Log4j2',
      'E2E opcional (./gradlew e2e)',
    ],
    type: 'secondary',
  },
  {
    id: 'appium-mobile-automation-framework',
    name: 'Appium Mobile Framework (Local)',
    description: 'Especializado en emulador/dispositivo local: Appium + Cucumber + JUnit 5',
    longDescription:
      'Demo Appium local (Maven). CI unitario sin Appium; BDD con perfil -Pbdd. Cloud queda en el repo hermano BrowserStack. Logging SLF4J/Logback.',
    technologies: ['Appium', 'Java', 'Cucumber', 'JUnit 5', 'Allure', 'Maven', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/appium-mobile-automation-framework',
    highlights: [
      'Especialización local/emulator',
      'mvn test = unitarios sin Appium',
      'Sin System.out; SLF4J/Logback',
      'Hermano cloud separado',
    ],
    type: 'secondary',
  },
  {
    id: 'automation-test-reports-hub',
    name: 'Automation Test Reports Hub',
    description: 'Demo hub: publicar reportes CI (Allure/Cucumber/Serenity) vía GitHub Pages',
    longDescription:
      'Scaffold público para centralizar enlaces/reportes CI de varios demos. Complemento DevOps/reporting, no un framework de tests.',
    technologies: ['GitHub Actions', 'GitHub Pages', 'Allure', 'Cucumber', 'Serenity'],
    github: 'https://github.com/Harp-Andres/automation-test-reports-hub',
    highlights: [
      'Hub de reportes multi-proyecto',
      'GitHub Pages',
      'Complemento DevOps a los frameworks',
    ],
    type: 'secondary',
  },
];
