#!/usr/bin/env node
/**
 * Generates docs/github-profile/README.md aligned with packages/core/src/data/cv-data.ts
 * and apps/web portfolio content (single source of truth for the GitHub welcome repo).
 *
 * Usage: node scripts/generate-github-profile-readme.mjs
 */

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');
const cvPath = join(root, 'packages/core/src/data/cv-data.ts');
const outDir = join(root, 'docs/github-profile');
const outFile = join(outDir, 'README.md');

const cvSource = readFileSync(cvPath, 'utf8');

function extractString(field) {
  const re = new RegExp(`${field}:\\s*'([^']+)'`);
  const m = cvSource.match(re);
  if (!m) throw new Error(`Missing field in cv-data.ts: ${field}`);
  return m[1];
}

function extractBio() {
  const m = cvSource.match(/bio:\s*'([^']+)'/);
  if (!m) throw new Error('Missing bio in cv-data.ts');
  return m[1];
}

const profile = {
  name: extractString('name'),
  title: extractString('title'),
  email: extractString('email'),
  location: extractString('location'),
  github: extractString('github'),
  linkedin: extractString('linkedin'),
  portfolio: extractString('portfolio').replace(/Harp-Andres\.github\.io/i, 'harp-andres.github.io'),
  bio: extractBio(),
};

const displayName = 'Andrés Rodríguez Pisa';

// Experience block from cv-data (kept in sync manually with roles; validated by field checks above)
const experience = [
  {
    role: 'Test Automation Analyst III',
    company: 'GFT Technologies',
    period: 'Feb 2026 – Actualidad',
    stack: 'Playwright · Selenium · Karate · GitHub Actions · Azure DevOps · IA',
  },
  {
    role: 'Senior QA Engineer L1',
    company: 'Bizagi Latam SAS',
    period: 'Ago 2025 – Dic 2025',
    stack: 'Java · Selenium · Appium · REST Assured · Azure · Docker',
  },
  {
    role: 'Domain Consultant – QA Automation',
    company: 'Tata Consultancy Services (TCS)',
    period: 'Dic 2024 – Ago 2025',
    stack: 'Azure DevOps · YAML · Selenium · Postman · Git',
  },
  {
    role: 'QA Automation Engineer',
    company: 'Banco de Occidente',
    period: 'Abr 2023 – Dic 2024',
    stack: 'Playwright · Selenium · GitHub Actions · GitLab CI · Azure DevOps',
  },
];

const projects = [
  {
    name: 'qa-playwright-ai-framework',
    url: 'https://github.com/Harp-Andres/qa-playwright-ai-framework',
    description: 'Framework Playwright + TypeScript con helpers AI-ready, Zod y logging',
  },
  {
    name: 'appium-mobile-automation-framework',
    url: 'https://github.com/Harp-Andres/appium-mobile-automation-framework',
    description: 'Demo Appium local (Maven) con Cucumber BDD y JUnit 5',
  },
  {
    name: 'appium-mobile-cloud-automation-framework',
    url: 'https://github.com/Harp-Andres/appium-mobile-cloud-automation-framework',
    description: 'Appium + BrowserStack (Screenplay + Cucumber)',
  },
  {
    name: 'automation-test-reports-hub',
    url: 'https://github.com/Harp-Andres/automation-test-reports-hub',
    description: 'Hub público de reportes CI/CD (Allure, Cucumber, Serenity)',
  },
  {
    name: 'mi-portafolio',
    url: 'https://github.com/Harp-Andres/mi-portafolio',
    description: 'Portafolio profesional con generación de CV (DOCX / PDF / Excel)',
  },
];

const shortBio = profile.bio.split('. ').slice(0, 2).join('. ') + '.';

const experienceMd = experience
  .map(
    (e) =>
      `| **${e.role}** | ${e.company} | ${e.period} | \`${e.stack}\` |`,
  )
  .join('\n');

const projectsMd = projects
  .map((p) => `| [${p.name}](${p.url}) | ${p.description} |`)
  .join('\n');

const readme = `<div align="center">

# ¡Hola! Soy ${displayName} 👋

### ${profile.title}

${shortBio}

📍 ${profile.location} · 🎓 Ingeniero de Sistemas (UNAD) · 🐧 LPI Linux Essentials · ⚡ Scrum Practitioner

[![Portfolio](https://img.shields.io/badge/Portfolio-Visitar-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white)](${profile.portfolio})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](${profile.linkedin})
[![Email](https://img.shields.io/badge/Email-Contacto-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:${profile.email})
[![GitHub](https://img.shields.io/badge/GitHub-Harp--Andres-181717?style=for-the-badge&logo=github&logoColor=white)](${profile.github})
[![mi-portafolio](https://img.shields.io/badge/Repo-mi--portafolio-111827?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Harp-Andres/mi-portafolio)

</div>

---

## 🧰 Stack tecnológico

> Alineado con la hoja de vida y el portafolio en [\`mi-portafolio\`](https://github.com/Harp-Andres/mi-portafolio)  
> (\`packages/core/src/data/cv-data.ts\` — single source of truth).

### Lenguajes
<p align="center">
  <img src="https://skillicons.dev/icons?i=java,javascript,typescript,cs,html,css&perline=6" alt="Lenguajes" />
</p>

### Automatización Web · Mobile · API
<p align="center">
  <img src="https://skillicons.dev/icons?i=selenium,cypress,postman,gherkin,vitest&perline=5" alt="Testing icons" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge" alt="Playwright" />
  <img src="https://img.shields.io/badge/Appium-EE376D?style=for-the-badge&logo=appium&logoColor=white" alt="Appium" />
  <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium" />
  <img src="https://img.shields.io/badge/Cypress-17202C?style=for-the-badge&logo=cypress&logoColor=white" alt="Cypress" />
  <img src="https://img.shields.io/badge/Cucumber-23D96C?style=for-the-badge&logo=cucumber&logoColor=white" alt="Cucumber" />
  <img src="https://img.shields.io/badge/Serenity%20BDD-124C7F?style=for-the-badge" alt="Serenity BDD" />
  <img src="https://img.shields.io/badge/Katalon%20Studio-01B9EF?style=for-the-badge" alt="Katalon" />
  <img src="https://img.shields.io/badge/REST%20Assured-5B9BD5?style=for-the-badge&logo=swagger&logoColor=white" alt="REST Assured" />
  <img src="https://img.shields.io/badge/Karate-000000?style=for-the-badge" alt="Karate" />
  <img src="https://img.shields.io/badge/JUnit-25A162?style=for-the-badge&logo=junit5&logoColor=white" alt="JUnit" />
  <img src="https://img.shields.io/badge/TestNG-FF6A00?style=for-the-badge" alt="TestNG" />
  <img src="https://img.shields.io/badge/Reqnroll-.NET-512BD4?style=for-the-badge&logo=dotnet&logoColor=white" alt="Reqnroll" />
  <img src="https://img.shields.io/badge/JMeter-D22128?style=for-the-badge&logo=apachejmeter&logoColor=white" alt="JMeter" />
  <img src="https://img.shields.io/badge/Allure%20Report-FD5A3E?style=for-the-badge" alt="Allure" />
</p>

### CI/CD · DevOps · Cloud · Azure
<p align="center">
  <img src="https://skillicons.dev/icons?i=git,github,githubactions,gitlab,jenkins,docker,kubernetes,linux,aws,azure,gcp&perline=11" alt="CI/CD DevOps Cloud" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Azure%20DevOps-0078D7?style=for-the-badge" alt="Azure DevOps" />
  <img src="https://img.shields.io/badge/BrowserStack-E76F00?style=for-the-badge" alt="BrowserStack" />
  <img src="https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonar&logoColor=white" alt="SonarQube" />
  <img src="https://img.shields.io/badge/Sauce%20Labs-E2231A?style=for-the-badge&logo=saucelabs&logoColor=white" alt="Sauce Labs" />
  <img src="https://img.shields.io/badge/AWS%20Device%20Farm-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS Device Farm" />
</p>

### Frontend · Build · Bases de datos
<p align="center">
  <img src="https://skillicons.dev/icons?i=react,vue,flutter,nodejs,vite,pnpm,gradle,maven,mysql,postgres,mongodb&perline=11" alt="Frontend Build DB" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SQL%20Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white" alt="SQL Server" />
  <img src="https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle" />
</p>

### IDEs · Consola · Virtualización
<p align="center">
  <img src="https://skillicons.dev/icons?i=vscode,idea,eclipse,visualstudio,powershell,bash&perline=6" alt="IDEs and Shell" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VirtualBox-183A61?style=for-the-badge&logo=virtualbox&logoColor=white" alt="VirtualBox" />
  <img src="https://img.shields.io/badge/VMware-607078?style=for-the-badge&logo=vmware&logoColor=white" alt="VMware" />
</p>

### IA & Productividad
<p align="center">
  <img src="https://img.shields.io/badge/GitHub%20Copilot-000000?style=for-the-badge&logo=githubcopilot&logoColor=white" alt="GitHub Copilot" />
  <img src="https://img.shields.io/badge/Claude-D97757?style=for-the-badge&logo=claude&logoColor=white" alt="Claude" />
  <img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" alt="Cursor" />
  <img src="https://img.shields.io/badge/MCP%20Playwright-2EAD33?style=for-the-badge" alt="MCP Playwright" />
  <img src="https://img.shields.io/badge/Prompting%20Avanzado-7C3AED?style=for-the-badge" alt="Prompting" />
</p>

### Gestión & Colaboración
<p align="center">
  <img src="https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=jira&logoColor=white" alt="Jira" />
  <img src="https://img.shields.io/badge/Azure%20Boards-0078D7?style=for-the-badge" alt="Azure Boards" />
  <img src="https://img.shields.io/badge/Kanban-0052CC?style=for-the-badge&logo=trello&logoColor=white" alt="Kanban" />
  <img src="https://img.shields.io/badge/Screenplay%20%2B%20POM-111827?style=for-the-badge" alt="Patterns" />
</p>

---

## 💼 Experiencia

| Rol | Empresa | Periodo | Stack |
| :--- | :--- | :--- | :--- |
${experienceMd}

---

## 🚀 Portafolio & proyectos

👉 **[Visitar Mi Portafolio Web](${profile.portfolio})** — misma fuente de datos que este perfil.

| Proyecto | Descripción |
| :--- | :--- |
${projectsMd}

---

## 🎓 Formación & certificaciones

| Tipo | Detalle |
| :--- | :--- |
| Educación | Ingeniero de Sistemas — UNAD (2024) |
| Educación | Tecnólogo en Gestión de Redes de Datos — SENA (2018) |
| Oficial | **LPI Linux Essentials** |
| Oficial | **Scrum Practitioner (CertMind)** |
| Destacadas | Azure DevOps, Jenkins, Appium, Playwright, Cypress, Katalon, ISTQB CTFL, Claude / Copilot (Anthropic & Microsoft) |

---

## 📊 GitHub Stats

<div align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=Harp-Andres&show_icons=true&theme=transparent&hide_border=true&count_private=true" alt="GitHub Stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=Harp-Andres&layout=compact&theme=transparent&hide_border=true" alt="Top Languages" />
</div>

---

## 📫 Conecta conmigo

- **LinkedIn:** [${displayName}](${profile.linkedin})
- **Email:** [${profile.email}](mailto:${profile.email})
- **Portafolio:** [${profile.portfolio.replace(/^https?:\/\//, '')}](${profile.portfolio})
- **Ubicación:** ${profile.location}

---

<div align="center">

⭐ *Datos sincronizados con [\`mi-portafolio\`](https://github.com/Harp-Andres/mi-portafolio) · abierto a colaborar en calidad de software, automatización e IA aplicada a QA.*

<sub>Regenerar: <code>pnpm sync:github-profile</code></sub>

</div>
`;

mkdirSync(outDir, { recursive: true });
writeFileSync(outFile, readme, 'utf8');

// Sanity: no known-invalid skillicons IDs
const forbidden = [
  'serenity',
  'appium',
  'katalon',
  'cucumber',
  'junit',
  'testng',
  'azuredevops',
  'virtualbox',
  'veamware',
  'vmware',
  'githubcopilot',
  'intellij',
  'playwright',
];
const skillIconBlocks = [...readme.matchAll(/skillicons\.dev\/icons\?i=([^"&]+)/g)].map((m) => m[1]);
for (const block of skillIconBlocks) {
  for (const id of block.split(',')) {
    if (forbidden.includes(id)) {
      throw new Error(`Invalid skillicons id in generated README: ${id}`);
    }
  }
}

console.log(`✓ Generated ${outFile}`);
console.log(`  name: ${displayName}`);
console.log(`  title: ${profile.title}`);
console.log(`  portfolio: ${profile.portfolio}`);
