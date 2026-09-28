import type { Project } from '../types';

export const PROJECTS: Project[] = [
  {
    id: 'qa-playwright-ai-framework',
    name: 'QA Playwright AI Framework',
    description:
      'Framework de automatización Web y API con Playwright y TypeScript, listo para integrarse en pipelines CI/CD',
    longDescription:
      'Arquitectura de referencia para automatización Web y API con Playwright y TypeScript estricto: Page Object Model, clientes API con mocks para CI, configuración validada con Zod, logging estructurado con pino y una capa AI-ready para análisis de fallos y auto-curación de pruebas. Incluye pruebas unitarias con Vitest y ejecución contenedorizada con Docker y Kubernetes.',
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
      'Automatización Web y API en un mismo framework',
      'Capa AI-ready para análisis de fallos y auto-curación',
      'Logging estructurado con pino y configuración validada con Zod',
      'Pipeline CI/CD con Docker y Job de Kubernetes',
    ],
    type: 'featured',
  },
  {
    id: 'demo-playwright-datadriven-e2e',
    name: 'Playwright Data-Driven E2E',
    description: 'Pruebas E2E data-driven con Playwright y TypeScript alimentadas desde Excel',
    longDescription:
      'Suite E2E sobre un flujo de negocio real (búsqueda de cruceros) que aplica data-driven testing desde Excel, mappers de datos tipados y Page Object Model por capas. Cuenta con pruebas unitarias en Vitest y logger estructurado en JSON para una trazabilidad clara de cada ejecución.',
    technologies: ['Playwright', 'TypeScript', 'Vitest', 'Excel/XLSX', 'Data-Driven Testing', 'POM'],
    github: 'https://github.com/Harp-Andres/demo-playwright-datadriven-e2e',
    highlights: [
      'Escenarios parametrizados desde Excel/XLSX',
      'Page Object Model por capas y mappers tipados',
      'Pruebas unitarias con Vitest',
      'Logger estructurado en JSON',
    ],
    type: 'featured',
  },
  {
    id: 'appium-mobile-cloud-automation-framework',
    name: 'Appium Mobile Cloud Framework',
    description: 'Automatización mobile en la nube con Appium, Cucumber y Allure sobre BrowserStack',
    longDescription:
      'Framework de automatización mobile orientado a device farms: ejecuta escenarios BDD con Appium en BrowserStack App Automate, publica reportes Allure y se integra con GitHub Actions. Separa la lógica de negocio de la infraestructura de ejecución para escalar la cobertura en múltiples dispositivos.',
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
      'Ejecución en la nube con BrowserStack App Automate',
      'Escenarios BDD con Cucumber y reportes Allure en CI',
      'Pruebas unitarias con Gradle sin depender de Appium',
      'Logging con SLF4J/Logback',
    ],
    type: 'featured',
  },
  {
    id: 'appium-mobile-automation-framework',
    name: 'Appium Mobile Framework (Local)',
    description: 'Automatización mobile en emulador y dispositivo real con Appium, Cucumber y JUnit 5',
    longDescription:
      'Framework Appium con Maven para ejecución en emulador o dispositivo físico: escenarios BDD con Cucumber mediante el perfil -Pbdd, pruebas unitarias en CI sin dependencia de Appium, reportes Allure y logging con SLF4J/Logback. Comparte enfoque y buenas prácticas con su versión cloud para BrowserStack.',
    technologies: ['Appium', 'Java', 'Cucumber', 'JUnit 5', 'Allure', 'Maven', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/appium-mobile-automation-framework',
    highlights: [
      'Ejecución en emulador o dispositivo real',
      'Pruebas unitarias en CI sin Appium (mvn test)',
      'Escenarios BDD con Cucumber y reportes Allure',
      'Versión cloud complementaria para BrowserStack',
    ],
    type: 'featured',
  },
  {
    id: 'demo-serenity-screenplay-mobile',
    name: 'Serenity Screenplay Mobile',
    description: 'Automatización mobile con el patrón Screenplay sobre Serenity BDD y Appium',
    longDescription:
      'Implementación del patrón Screenplay con Serenity BDD y Appium para Android e iOS: actores, tareas y preguntas reutilizables, escenarios Cucumber y reportes de Serenity. Incluye pruebas unitarias con Gradle sin dispositivo y una suite E2E ejecutable con ./gradlew e2e.',
    technologies: ['Java', 'Serenity BDD', 'Screenplay', 'Appium', 'Gradle', 'Cucumber', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/demo-serenity-screenplay-mobile',
    highlights: [
      'Patrón Screenplay: actores, tareas y preguntas',
      'Reportes de Serenity BDD',
      'Pruebas unitarias sin dispositivo',
      'Suite E2E con ./gradlew e2e',
    ],
    type: 'featured',
  },
  {
    id: 'literalura',
    name: 'Literalura - Spring Boot',
    description: 'Backend Spring Boot con consumo de API externa, JPA/PostgreSQL y arquitectura por capas',
    longDescription:
      'Aplicación Spring Boot con servicios de dominio desacoplados, integración con la API de Gutendex, persistencia con JPA/PostgreSQL y un adaptador de consola independiente del dominio. Pruebas con H2 y Mockito y logging con SLF4J.',
    technologies: ['Java', 'Spring Boot', 'Spring Data JPA', 'PostgreSQL', 'REST APIs', 'Maven', 'SLF4J'],
    github: 'https://github.com/Harp-Andres/Literalura',
    highlights: [
      'Principios SOLID: dominio separado de la consola',
      'Persistencia JPA con pruebas sobre H2',
      'Cliente HTTP y mapeo DTO a entidad',
      'Logging con SLF4J',
    ],
    type: 'featured',
  },
  {
    id: 'portfolio-site',
    name: 'Mi Portafolio',
    description:
      'Portafolio en monorepo React + TypeScript con backend Python que genera la hoja de vida en Word y PDF',
    longDescription:
      'Monorepo React + TypeScript con un backend Python de arquitectura limpia que genera la hoja de vida en Word y PDF a partir de solicitudes en texto. Incluye pruebas con Vitest y Playwright, un servidor MCP de agentes y despliegue continuo en GitHub Pages con GitHub Actions.',
    technologies: [
      'React',
      'TypeScript',
      'Vite',
      'Tailwind CSS',
      'Python',
      'Vitest',
      'Playwright',
      'GitHub Actions',
    ],
    github: 'https://github.com/Harp-Andres/mi-portafolio',
    link: 'https://harp-andres.github.io/mi-portafolio/',
    highlights: [
      'Hoja de vida generada por backend (Word y PDF)',
      'Pruebas unitarias y E2E en CI',
      'Despliegue continuo en GitHub Pages',
      'Servidor MCP que orquesta agentes de desarrollo',
    ],
    type: 'featured',
  },
  {
    id: 'automation-test-reports-hub',
    name: 'Automation Test Reports Hub',
    description: 'Portal de reportes de pruebas (Allure, Cucumber, Serenity) publicado desde CI en GitHub Pages',
    longDescription:
      'Centraliza los reportes de ejecución de los frameworks de automatización y los publica automáticamente en GitHub Pages desde GitHub Actions, dando visibilidad continua de la calidad.',
    technologies: ['GitHub Actions', 'GitHub Pages', 'Allure', 'Cucumber', 'Serenity'],
    github: 'https://github.com/Harp-Andres/automation-test-reports-hub',
    highlights: [
      'Reportes de múltiples proyectos en un solo portal',
      'Publicación automática en GitHub Pages',
      'Visibilidad continua de la calidad',
    ],
    type: 'secondary',
  },
];
