/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          dark: "#0b132b",
          navy: "#1c2541",
          blue: "#1e3a8a",
          teal: "#0d9488",
          gold: "#d97706",
          emerald: "#059669",
          slate: "#f1f5f9"
        }
      }
    },
  },
  plugins: [],
}
