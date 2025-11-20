<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full bg-white rounded-lg shadow-lg p-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">
        Context-First Platform
      </h1>
      <p class="text-lg text-gray-600 mb-6">
        Monorepo Setup Complete ✅
      </p>

      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
        <h2 class="text-sm font-semibold text-green-800 mb-2">
          Status: Ready for Development
        </h2>
        <ul class="text-sm text-green-700 space-y-1">
          <li>✓ Turborepo configured</li>
          <li>✓ PNPM workspaces working</li>
          <li>✓ Frontend (Nuxt 3) running</li>
          <li>✓ Backend (FastAPI) ready</li>
          <li>✓ Shared schemas available</li>
        </ul>
      </div>

      <div class="mt-6 text-sm text-gray-500">
        <p>Frontend: http://localhost:3000</p>
        <p>Backend: http://localhost:8000</p>
        <p>API Docs: http://localhost:8000/docs</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Test import from shared package
import type { Demand, Project, Metaspec } from 'shared'

// TODO: Use types in actual components (IAD-9)
// This validates that workspace dependency is working
</script>
