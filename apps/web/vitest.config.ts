import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    pool: 'forks',
    server: {
      deps: {
        inline: ['react-router-dom'],
      },
    },
    setupFiles: ['./vitest.setup.ts'],
    exclude: [
      'node_modules/',
      'dist/',
      'tests/e2e/',
      '**/*.spec.ts'
    ],
    reporters: ['default', 'html'],
    outputFile: {
      html: '.vitest/index.html'
    },
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'dist/',
        'tests/',
        '**/*.spec.ts',
        '**/*.test.ts'
      ]
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@mportafolio/core': path.resolve(__dirname, '../../packages/core/src'),
    }
  }
})
