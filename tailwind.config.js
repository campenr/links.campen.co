module.exports = {
  theme: {
    fontFamily: {
      'sans': ['Roboto Condensed', 'sans-serif'],
      'base': ['Roboto', 'sans-serif'],
    },
    colors: {
      'white': '#fff',
      'black': '#000',
      'purple': '#6366F1',
      'green': '#10B981',
    },
    extend: {
      screens: {
        xs: '480px',
      }
    }
  },
  purge: {
    enabled: false,
    content: ['./app/app/**/*.html'],
  },
}