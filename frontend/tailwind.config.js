module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#3D7BA4',
        'secondary-orange': '#E78D45',
        'accent-blue': '#1E4E6C',
        'background': '#F5F7FA',
        'text': '#333333',
        'success': '#4CAF50',
        'warning': '#FFC107',
        'error': '#F44336',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'mono': ['Roboto Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
