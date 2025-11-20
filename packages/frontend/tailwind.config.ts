import type { Config } from 'tailwindcss'

export default <Config>{
  content: [
    './components/**/*.{vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.ts',
    './app.vue',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
