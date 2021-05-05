module.exports = {
  theme: {
    fontFamily: {
      'sans': ['Roboto Condensed', 'sans-serif'],
      'base': ['Roboto', 'sans-serif'],
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