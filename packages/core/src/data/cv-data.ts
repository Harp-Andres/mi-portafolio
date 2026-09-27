/**
 * @mportafolio/core - cv-data.ts
 * ⭐ SINGLE SOURCE OF TRUTH
 * 
 * This is the centralized source for all CV and portfolio data.
 * All applications (Web, DOCX, PDF, Excel) consume from this file.
 * 
 * CRITICAL: Keep this synchronized across all platforms
 */

import type { CV_Data, Project } from '../types';

// Root-level properties for backward compatibility with existing components
const profileData = {
  name: 'ANDRES RODRIGUEZ PISA',
  title: 'SDET | Senior QA Automation Engineer | API · Backend · Mobile · Web | Entornos DevOps | IA aplicada a QA',
  email: 'andresrdrgzps05@gmail.com',
  phone: '(+57) 320 324 5988',
  phone1: '(+57) 320 324 5988',
  phone2: '(+57) 301 211 9295',
  location: 'Bogotá, Colombia',
  birthDate: '1993-04-05',
  bio: 'Ingeniero de Sistemas especializado en aseguramiento de calidad de software, con expertise en arquitectura de frameworks de automatización multiplataforma (Web, API, Mobile) y prácticas DevOps de clase empresarial. Sólida experiencia en diseño e implementación de estrategias QA con patrones avanzados (Screenplay, POM), CI/CD (GitHub Actions, GitLab CI, Jenkins, Azure DevOps), ecosistema Azure (Pipelines YAML, ACR, Blob Storage, Docker) y validación de servicios REST/SOAP con trazabilidad de calidad.',
  github: 'https://github.com/Harp-Andres',
  linkedin: 'https://www.linkedin.com/in/andresrodriguezpisa-qa/',
  portfolio: 'https://harp-andres.github.io/mi-portafolio/',
};

export const CV_DATA: any = {
  // Root-level properties for backward compatibility
  ...profileData,
  profile: profileData,

  skills: [
    {
      category: 'Mobile Automation',
      skills: [
        { name: 'Appium', level: 'expert' },
        { name: 'Appium Server', level: 'expert' },
        { name: 'Appium Inspector', level: 'advanced' },
        { name: 'Android/iOS', level: 'advanced' },
        { name: 'ADB', level: 'advanced' },
      ],
    },
    {
      category: 'Web Automation',
      skills: [
        { name: 'Selenium WebDriver', level: 'expert' },
        { name: 'Playwright', level: 'expert' },
        { name: 'Cypress', level: 'advanced' },
        { name: 'Serenity BDD', level: 'advanced' },
        { name: 'HTML', level: 'advanced' },
        { name: 'CSS', level: 'advanced' },
      ],
    },
    {
      category: 'API / Backend Testing',
      skills: [
        { name: 'REST Assured', level: 'expert' },
        { name: 'Karate', level: 'expert' },
        { name: 'Postman', level: 'advanced' },
        { name: 'SoapUI', level: 'intermediate' },
        { name: 'Swagger', level: 'advanced' },
      ],
    },
    {
      category: 'Performance',
      skills: [
        { name: 'JMeter', level: 'advanced' },
        { name: 'Gatling', level: 'intermediate' },
      ],
    },
    {
      category: 'BDD / Frameworks',
      skills: [
        { name: 'Cucumber', level: 'expert' },
        { name: 'Reqnroll (.NET)', level: 'advanced' },
        { name: 'Serenity BDD', level: 'advanced' },
        { name: 'JUnit', level: 'advanced' },
        { name: 'TestNG', level: 'advanced' },
        { name: 'Katalon Studio', level: 'intermediate' },
      ],
    },
    {
      category: 'Arquitectura / Patrones',
      skills: [
        { name: 'Screenplay', level: 'expert' },
        { name: 'Page Object Model (POM)', level: 'expert' },
        { name: 'Programación Orientada a Objetos', level: 'expert' },
        { name: 'DTO / Entities', level: 'advanced' },
        { name: 'SOLID Principles', level: 'expert' },
      ],
    },
    {
      category: 'CI/CD & DevOps',
      skills: [
        { name: 'GitHub Actions', level: 'expert' },
        { name: 'GitLab CI/CD', level: 'expert' },
        { name: 'Jenkins', level: 'advanced' },
        { name: 'Azure DevOps', level: 'expert' },
        { name: 'Docker', level: 'advanced' },
        { name: 'Git', level: 'expert' },
        { name: 'SonarQube', level: 'intermediate' },
      ],
    },
    {
      category: 'Cloud & Plataformas',
      skills: [
        { name: 'BrowserStack', level: 'advanced' },
        { name: 'AWS Device Farm', level: 'intermediate' },
        { name: 'Sauce Labs', level: 'intermediate' },
      ],
    },
    {
      category: 'Azure (Contenedores & Kubernetes)',
      skills: [
        { name: 'Azure Storage', level: 'advanced' },
        { name: 'Azure Kubernetes Service (AKS)', level: 'intermediate' },
        { name: 'Azure Container Registry (ACR)', level: 'advanced' },
        { name: 'Docker', level: 'advanced' },
        { name: 'Kubernetes', level: 'intermediate' },
      ],
    },
    {
      category: 'Lenguajes',
      skills: [
        { name: 'Java', level: 'expert' },
        { name: 'JavaScript', level: 'expert' },
        { name: 'TypeScript', level: 'expert' },
        { name: 'C#', level: 'advanced' },
        { name: 'SQL', level: 'advanced' },
      ],
    },
    {
      category: 'Build Tools',
      skills: [
        { name: 'Gradle', level: 'advanced' },
        { name: 'Maven', level: 'advanced' },
        { name: 'Node.js', level: 'advanced' },
        { name: 'PNPM', level: 'advanced' },
      ],
    },
    {
      category: 'Reporting',
      skills: [
        { name: 'Allure Report', level: 'expert' },
        { name: 'Cucumber HTML', level: 'advanced' },
        { name: 'GitHub Pages', level: 'advanced' },
      ],
    },
    {
      category: 'Bases de Datos',
      skills: [
        { name: 'SQL Server', level: 'advanced' },
        { name: 'MySQL', level: 'advanced' },
        { name: 'Oracle', level: 'intermediate' },
        { name: 'PostgreSQL', level: 'advanced' },
        { name: 'MongoDB', level: 'intermediate' },
      ],
    },
    {
      category: 'Gestión / Colaboración',
      skills: [
        { name: 'Jira', level: 'advanced' },
        { name: 'Kanban', level: 'expert' },
        { name: 'Azure Boards', level: 'advanced' },
        { name: 'Liderazgo Técnico', level: 'advanced' },
      ],
    },
    {
      category: 'IA & Productividad',
      skills: [
        { name: 'GitHub Copilot', level: 'expert' },
        { name: 'MCP Playwright', level: 'expert' },
        { name: 'Claude (Anthropic)', level: 'expert' },
        { name: 'Prompting Avanzado', level: 'expert' },
      ],
    },
    {
      category: 'Scripting / Consola',
      skills: [
        { name: 'PowerShell', level: 'advanced' },
        { name: 'Bash', level: 'advanced' },
        { name: 'CMD', level: 'intermediate' },
      ],
    },
  ],

  experience: [
    {
      id: 'gft-2026',
      title: 'Test Automation Analyst III',
      company: 'GFT Technologies',
      period: 'Feb 2026 – Actualidad',
      description: 'Lidero la estrategia de automatización QA en entornos CI/CD para pruebas de servicios y front-end.',
      technologies: ['Playwright', 'Selenium', 'Karate', 'GitHub Actions', 'Azure DevOps', 'IA'],
      achievements: [
        'Lidero la estrategia de automatización QA en entornos CI/CD para pruebas de servicios y front-end.',
        'Diseño y ejecuto pruebas de performance para validar estabilidad y comportamiento bajo carga.',
        'Gestiono DoD, Test Plan y trazabilidad de calidad con cobertura de criterios de aceptación.',
        'Implemento pruebas de aceptación con Karate y automatización web con Serenity.',
        'Desarrollo automatizaciones inteligentes con IA integrada para auto-curación de tests.',
      ],
    },
    {
      id: 'bizagi-2025',
      title: 'Senior QA Engineer L1',
      company: 'Bizagi Latam SAS',
      period: 'Ago 2025 – Dic 2025',
      description: 'Diseñé e implementé arquitecturas de automatización para pruebas API, Web y Mobile.',
      technologies: ['Java', 'Selenium', 'Appium', 'REST Assured', 'Azure', 'Docker'],
      achievements: [
        'Diseñé e implementé arquitecturas de automatización para pruebas API, Web y Mobile.',
        'Implementé soluciones en Azure para optimizar tiempos de ejecución.',
        'Establecí estándares de calidad técnica y patrones de diseño (Screenplay, POM).',
        'Diseñé soluciones con IA para validación visual y auto-curación de tests.',
        'Lideré capacitación QA y revisión de código con enfoque en mantenibilidad.',
      ],
    },
    {
      id: 'tcs-2024',
      title: 'Domain Consultant – QA Automation',
      company: 'Tata Consultancy Services (TCS)',
      period: 'Dic 2024 – Ago 2025',
      description: 'Orquesté marcos de automatización QA alineados a pipelines CI/CD corporativos.',
      technologies: ['Azure DevOps', 'YAML', 'Selenium', 'Postman', 'Git'],
      achievements: [
        'Orquesté marcos de automatización QA alineados a pipelines CI/CD corporativos.',
        'Analicé y reestructuré soluciones de automatización de alta complejidad.',
        'Mejoré mantenibilidad mediante estandarización técnica y principios SOLID.',
        'Administré pipelines en YAML y Azure DevOps alineados a estándares corporativos.',
        'Brindé capacitación continua al equipo QA para elevar madurez técnica.',
      ],
    },
    {
      id: 'banco-occidente-2023',
      title: 'QA Automation Engineer',
      company: 'Banco de Occidente',
      period: 'Abr 2023 – Dic 2024',
      description: 'Diseñé estrategias de pruebas automatizadas multiplataforma en entornos bancarios.',
      technologies: ['Playwright', 'Selenium', 'GitHub Actions', 'GitLab CI', 'Azure DevOps'],
      achievements: [
        'Diseñé estrategias de pruebas automatizadas multiplataforma (Web, API, Mobile) en entornos bancarios.',
        'Implementé pipelines CI/CD con GitHub Actions, GitLab CI y Azure DevOps.',
        'Optimicé flujos de trabajo QA y fortalecí procesos de validación funcional.',
        'Capacité continuamente al equipo QA en herramientas y buenas prácticas.',
      ],
    },
  ],

  education: [
    {
      id: 'unad-2024',
      degree: 'Ingeniero de Sistemas',
      institution: 'Universidad Nacional Abierta y a Distancia (UNAD)',
      graduation: '2024',
      description: 'Formación en ingeniería de sistemas con énfasis en calidad de software',
    },
    {
      id: 'sena-2018',
      degree: 'Tecnólogo en Gestión de Redes de Datos',
      institution: 'SENA',
      graduation: '2018',
      description: 'Formación técnica en infraestructura y redes de datos',
    },
  ],

  certificates: {
    'DevOps & Cloud': [
      {
        id: 'azure-udemy',
        name: 'DevOps y Cloud con Azure DevOps, App Service Pipelines y Git',
        issuer: 'Udemy',
        date: '2024',
        hours: 21,
      },
      {
        id: 'docker-sysadmin-udemy',
        name: 'Maneja Docker en 5 días: SysAdmin Linux o DevOps',
        issuer: 'Udemy',
        date: '2026',
        hours: 7,
      },
      {
        id: 'docker-selenium',
        name: 'Docker Compose with Selenium',
        issuer: 'Udemy',
        date: '2024',
        hours: 3,
      },
      {
        id: 'jenkins-udemy',
        name: 'La Guía de Jenkins: De Cero a Experto',
        issuer: 'Udemy',
        date: '2024',
        hours: 32,
      },
    ],
    'Calidad & QA': [
      {
        id: 'istqb-udemy',
        name: 'ISTQB Certified Tester Foundation Level (CTFL 4.0)',
        issuer: 'Udemy',
        date: '2024',
        hours: 18,
      },
      {
        id: 'jmeter-udemy',
        name: 'Master: Pruebas de Rendimiento con Apache JMeter',
        issuer: 'Udemy',
        date: '2024',
        hours: 16,
      },
      {
        id: 'puppeteer-platzi',
        name: 'Introducción a Automatización de Pruebas con Puppeteer',
        issuer: 'Platzi',
        date: '2023',
        hours: 12,
      },
    ],
    'Automatización Web & Mobile': [
      {
        id: 'selenium-udemy',
        name: 'Selenium WebDriver y Grid',
        issuer: 'Udemy',
        date: '2023',
        hours: 21,
      },
      {
        id: 'selenium-linkedin',
        name: 'Selenium Essential Training',
        issuer: 'LinkedIn Learning',
        date: '2023',
        hours: 5,
      },
      {
        id: 'appium-udemy',
        name: 'Master Class de Appium 2 con Java',
        issuer: 'Udemy',
        date: '2024',
        hours: 22,
      },
      {
        id: 'appium-serenity',
        name: 'Configuración básica con Appium+Serenity',
        issuer: 'Udemy',
        date: '2023',
        hours: 8,
      },
      {
        id: 'cypress-udemy',
        name: 'Cypress: Master en Automatización Test QA',
        issuer: 'Udemy',
        date: '2023',
        hours: 23,
      },
      {
        id: 'katalon-udemy',
        name: 'Master: Katalon Studio Test QA Automation',
        issuer: 'Udemy',
        date: '2023',
        hours: 20,
      },
    ],
    'Playwright & API Testing': [
      {
        id: 'playwright-api-rest',
        name: 'Automatización de Pruebas API Rest con Playwright',
        issuer: 'Udemy',
        date: '2024',
        hours: 16,
      },
      {
        id: 'playwright-javascript',
        name: 'Curso de Playwright con JavaScript',
        issuer: 'Udemy',
        date: '2024',
        hours: 19,
      },
      {
        id: 'playwright-typescript',
        name: 'Dominando Playwright con TypeScript: E2E Testing moderno',
        issuer: 'Udemy',
        date: '2024',
        hours: 21,
      },
    ],
    'IA & Productividad': [
      {
        id: 'ai-fluency-anthropic',
        name: 'AI Fluency: Framework & Foundations',
        issuer: 'Anthropic',
        date: '2024',
        hours: 2,
      },
      {
        id: 'claude-cowork',
        name: 'Introduction to Claude Cowork',
        issuer: 'Anthropic',
        date: '2024',
        hours: 1,
      },
      {
        id: 'claude-101',
        name: 'Claude 101',
        issuer: 'Anthropic',
        date: '2024',
        hours: 1,
      },
      {
        id: 'prompting-microsoft',
        name: 'Escriba indicaciones eficaces para lograr resultados óptimos',
        issuer: 'Microsoft',
        date: '2024',
        hours: 3,
      },
      {
        id: 'copilot-studio',
        name: 'Introducción a Microsoft Copilot Studio',
        issuer: 'Microsoft',
        date: '2024',
        hours: 2,
      },
      {
        id: 'copilot-chat',
        name: 'Introducción a Microsoft 365 Copilot Chat (básico)',
        issuer: 'Microsoft',
        date: '2024',
        hours: 2,
      },
    ],
  },

  languages: ['Español (Nativo)', 'Inglés (B1 - en progreso)'],

  // Backward compatibility properties for existing components
  certificatesByCategory: {
    'DevOps & Cloud': [
      { title: 'DevOps y Cloud con Azure DevOps, App Service Pipelines y Git — Udemy', filePath: '/certificados/Azure/Udemy/certificado-azure.jpg', hours: 21 },
      { title: 'Maneja Docker en 5 días: SysAdmin Linux o DevOps — Udemy', filePath: '/certificados/Docker/certificado-docker.jpg', hours: 7 },
      { title: 'Docker Compose with Selenium — Udemy', filePath: null, hours: 3 },
      { title: 'La Guía de Jenkins: De Cero a Experto — Udemy', filePath: '/certificados/Jenkins/Udemy/certificado-jenkins.jpg', hours: 32 },
    ],
    'Calidad & QA': [
      { title: 'ISTQB Certified Tester Foundation Level (CTFL 4.0) — Udemy', filePath: '/certificados/ISTQB/Udemy/certificado-ISTQB.jpg', hours: 18 },
      { title: 'Master: Pruebas de Rendimiento con Apache JMeter — Udemy', filePath: '/certificados/Jmeter/Udemy/certificado-Jmeter.jpg', hours: 16 },
      { title: 'Introducción a Automatización de Pruebas con Puppeteer — Platzi', filePath: '/certificados/Puppeteer/diploma-puppeteer.pdf', hours: 12 },
    ],
    'Automatización Web & Mobile': [
      { title: 'Selenium WebDriver y Grid — Udemy', filePath: '/certificados/Selenium/Udemy/Certificado-Selenium.jpeg', hours: 21 },
      { title: 'Selenium Essential Training — LinkedIn Learning', filePath: '/certificados/Selenium/LinkedIn/certificado.png', hours: 5 },
      { title: 'Master Class de Appium 2 con Java — Udemy', filePath: '/certificados/Appium/Udemy/certificado-appium.jpg', hours: 22 },
      { title: 'Configuración básica con Appium+Serenity — Udemy', filePath: null, hours: 8 },
      { title: 'Cypress: Master en Automatización Test QA — Udemy', filePath: '/certificados/Cypress/Udemy/certificado-cypress.jpg', hours: 23 },
      { title: 'Master: Katalon Studio Test QA Automation — Udemy', filePath: '/certificados/Katalon/Udemy/certificado-katalon.jpg', hours: 20 },
    ],
    'Playwright & API Testing': [
      { title: 'Automatización de Pruebas API Rest con Playwright — Udemy', filePath: '/certificados/Playwright/Udemy/ApiRest.jpg', hours: 16 },
      { title: 'Curso de Playwright con JavaScript — Udemy', filePath: '/certificados/Playwright/Udemy/Playwright-JavaScript.jpg', hours: 19 },
      { title: 'Dominando Playwright con TypeScript: E2E Testing moderno — Udemy', filePath: '/certificados/Playwright/Udemy/Playwright-TypeScript.jpg', hours: 21 },
    ],
    'IA & Productividad': [
      { title: 'AI Fluency: Framework & Foundations — Anthropic', filePath: '/certificados/Claude/Anthropic/certificate-ajn9p5t7viwu-1785328726.pdf', hours: 2 },
      { title: 'Introduction to Claude Cowork — Anthropic', filePath: '/certificados/Claude/Anthropic/certificate-mhvrsy7hrbqy-1785539021.pdf', hours: 1 },
      { title: 'Claude 101 — Anthropic', filePath: '/certificados/Claude/Anthropic/certificate-va95o32xghxo-1785468260.pdf', hours: 1 },
      { title: 'Escriba indicaciones eficaces para lograr resultados óptimos — Microsoft', filePath: null, hours: 3 },
      { title: 'Introducción a Microsoft Copilot Studio — Microsoft', filePath: null, hours: 2 },
      { title: 'Introducción a Microsoft 365 Copilot Chat (básico) — Microsoft', filePath: null, hours: 2 },
    ],
  },

  learningPathsCertifications: [
    { title: 'JavaScript — Cymetria Group', filePath: '/certificados/JavaScript/Cymetria/certificado-Hardware-Andres-Rodriguez.pdf', hours: 40 },
    { title: 'Programa Oracle Next Education (7 formaciones) — Oracle + Alura', filePath: '/certificados/Alura/Hardware-Andres-Rodriguez-Programa.pdf', hours: 240 },
  ],

  officialCertifications: [
    { title: 'Linux Essentials', issuer: 'LPI', color: 'border-orange-500 bg-orange-50', icon: '🐧' },
    { title: 'Scrum Practitioner', issuer: 'CertMind', color: 'border-blue-500 bg-blue-50', icon: '⚡' },
  ],
};

// Portfolio Projects - demo/showcase repos (not production products)
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

// Export convenience function for getting certificate total hours
export function getTotalCertificationHours(): number {
  return Object.values(CV_DATA.certificates)
    .flat()
    .reduce((total: number, cert: any) => total + (cert.hours || 0), 0);
}

// Export convenience function to get all certificates flattened
export function getAllCertificates(): any[] {
  return Object.values(CV_DATA.certificates).flat();
}
