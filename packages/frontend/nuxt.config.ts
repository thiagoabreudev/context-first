// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],

  devtools: { enabled: true },

  typescript: {
    strict: true,
    typeCheck: false, // Desabilitado para MVP - habilitar em produção
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
    },
  },

  compatibilityDate: '2024-11-20',
})
