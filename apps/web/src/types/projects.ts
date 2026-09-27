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
    description: 'Demo framework: Playwright + TypeScript for web & API, with AI-ready helpers',
    longDescription:
      'Showcase automation framework using Playwright and TypeScript (strict). Includes Page Object Model, API clients with local mocks for CI, Docker/K8s job examples, and an AI-ready layer for locator fallbacks and failure analysis. Built to demonstrate tooling and architecture—not a production product.',
    technologies: [
      'Playwright',
      'TypeScript',
      'GitHub Actions',
      'Docker',
      'Kubernetes',
      'API Testing',
    ],
    github: 'https://github.com/Harp-Andres/qa-playwright-ai-framework',
    highlights: [
      'Web + API test suites with stable CI mocks',
      'POM with selectors separated from actions',
      'CI/CD with GitHub Actions + Azure Pipelines examples',
      'Docker Compose and Kubernetes Job packaging',
    ],
    type: 'featured',
  },
  {
    id: 'appium-mobile-cloud-automation-framework',
    name: 'Appium Mobile Cloud Framework',
    description: 'Demo mobile automation on cloud devices (BrowserStack) with Appium + Cucumber',
    longDescription:
      'Showcase mobile test framework designed for cloud device farms (BrowserStack and similar). Uses Appium, Cucumber/BDD, JUnit 5, Allure, and GitHub Actions to demonstrate Android/iOS automation patterns and reporting.',
    technologies: [
      'Appium',
      'Java',
      'Cucumber',
      'JUnit 5',
      'Allure',
      'BrowserStack',
      'GitHub Actions',
    ],
    github: 'https://github.com/Harp-Andres/appium-mobile-cloud-automation-framework',
    highlights: [
      'Cloud device execution (Android & iOS)',
      'BDD with Cucumber + Allure reports',
      'CI workflows for BrowserStack runs',
      'Local emulator config as fallback',
    ],
    type: 'featured',
  },
  {
    id: 'literalura',
    name: 'Literalura - Spring Boot',
    description: 'Demo backend: Spring Boot console app with API consumption, JPA and PostgreSQL',
    longDescription:
      'Java Spring Boot demo that consumes a literature API, maps DTOs to entities, and persists authors/books with Spring Data JPA and PostgreSQL. Shows backend skills: HTTP clients, deserialization, repositories, and layered structure—training/demo scope, not a production service.',
    technologies: ['Java', 'Spring Boot', 'Spring Data JPA', 'PostgreSQL', 'REST APIs', 'Maven'],
    github: 'https://github.com/Harp-Andres/Literalura',
    highlights: [
      'Spring Boot + JPA persistence',
      'External REST API integration',
      'DTO/entity mapping and repositories',
      'Console-driven domain flows',
    ],
    type: 'featured',
  },
  {
    id: 'typescript-playwright-cruise-search-e2e',
    name: 'Cruise Search E2E (Playwright + TS)',
    description: 'Demo E2E: data-driven cruise search with Playwright, TypeScript and layered POM',
    longDescription:
      'End-to-end demo that searches cruises across browsers using Playwright and TypeScript. Uses a layered Page Object structure and data-driven scenarios to show practical UI automation patterns.',
    technologies: ['Playwright', 'TypeScript', 'E2E Testing', 'POM', 'Data-Driven Testing'],
    github: 'https://github.com/Harp-Andres/typescript-playwright-cruise-search-e2e',
    highlights: [
      'Multi-browser Playwright runs',
      'Layered POM architecture',
      'Data-driven search scenarios',
      'TypeScript-first test design',
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
    id: 'java-serenity-screenplay-mobile',
    name: 'Serenity Screenplay Mobile',
    description: 'Demo: Java + Serenity Screenplay + Appium for Android/iOS',
    longDescription:
      'Mobile automation demo using Serenity BDD Screenplay with Appium and Gradle. Illustrates tasks, interactions, UI mappings, and multiplatform mobile flows.',
    technologies: ['Java', 'Serenity BDD', 'Screenplay', 'Appium', 'Gradle', 'Cucumber'],
    github:
      'https://github.com/Harp-Andres/java-serenity-screenplay-automatizacion-movile-multiplataforma',
    highlights: [
      'Screenplay pattern on mobile',
      'Appium Android/iOS setup',
      'Serenity reporting',
      'Gradle-based build',
    ],
    type: 'secondary',
  },
  {
    id: 'appium-mobile-automation-framework',
    name: 'Appium Mobile Framework (Local)',
    description: 'Demo: Appium + Cucumber + JUnit 5 for local emulator automation',
    longDescription:
      'Companion mobile framework focused on local Appium execution (emulator/device), POM + BDD, Allure reports, and GitHub Actions—showcase of day-to-day mobile QA tooling.',
    technologies: ['Appium', 'Java', 'Cucumber', 'JUnit 5', 'Allure', 'Maven'],
    github: 'https://github.com/Harp-Andres/appium-mobile-automation-framework',
    highlights: [
      'Local Appium + emulator flows',
      'Cucumber BDD + Allure',
      'CI-ready GitHub Actions',
      'POM structure for mobile screens',
    ],
    type: 'secondary',
  },
  {
    id: 'automation-test-reports-hub',
    name: 'Automation Test Reports Hub',
    description: 'Demo hub concept: publish CI test reports (Allure/Cucumber/Serenity) via GitHub Pages',
    longDescription:
      'Public hub idea for centralizing CI/CD test reports from multiple automation projects. Currently a lightweight scaffold; useful as a DevOps/reporting showcase pointer.',
    technologies: ['GitHub Actions', 'GitHub Pages', 'Allure', 'Cucumber', 'Serenity'],
    github: 'https://github.com/Harp-Andres/automation-test-reports-hub',
    highlights: [
      'Central place for CI report links',
      'Multi-framework reporting concept',
      'GitHub Pages hosting',
    ],
    type: 'secondary',
  },
]
