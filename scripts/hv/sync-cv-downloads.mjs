#!/usr/bin/env node
/**
 * Copies each CV profile into its own public directory so files with matching names do not overwrite.
 * Runs before `pnpm dev` and `pnpm build` of @mportafolio/web.
 */
import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const repoRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const publicRoot = join(repoRoot, 'apps', 'web', 'public', 'cv')
const profiles = [
  { id: 'qa', source: join(repoRoot, 'cv', 'qa', 'output'), target: join(publicRoot, 'qa') },
  { id: 'devops-qa', source: join(repoRoot, 'cv', 'devops-qa', 'output'), target: join(publicRoot, 'devops-qa') },
]

rmSync(publicRoot, { recursive: true, force: true })

for (const profile of profiles) {
  if (!existsSync(profile.source)) {
    console.error(`[sync-cv] Missing ${profile.source}. Run the ${profile.id} CV generator first.`)
    process.exit(1)
  }

  const files = readdirSync(profile.source).filter((name) => /\.(pdf|docx)$/i.test(name))
  if (files.length === 0) {
    console.error(`[sync-cv] ${profile.id} has no PDF/DOCX files. Run the CV generator first.`)
    process.exit(1)
  }

  mkdirSync(profile.target, { recursive: true })
  for (const name of files) copyFileSync(join(profile.source, name), join(profile.target, name))
  console.log(`[sync-cv] ${files.length} ${profile.id} CV files copied`)
}
