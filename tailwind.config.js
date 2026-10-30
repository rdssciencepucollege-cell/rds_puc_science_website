const path = require('path');
const themes = require('./tailwind.themes.json');

const greenPages = [
  'downloads.html',
  'events.html',
  'facilities.html',
  'gallery.html'
];
const goldPages = [
  'about.html',
  'academics.html',
  'admissions.html',
  'alumni.html',
  'calendar.html',
  'contact.html',
  'cookies.html',
  'faculty.html',
  'index.html',
  'map.html',
  'news.html',
  'privacy.html',
  'student-portal.html',
  'terms.html',
  'vidvat-coaching.html'
];
const themeName = process.env.SITE_THEME || 'gold';

if (!Object.hasOwn(themes, themeName)) {
  throw new Error(`Unknown Tailwind theme: ${themeName}`);
}

module.exports = {
  darkMode: 'class',
  content: (themeName === 'green' ? greenPages : goldPages).map(file =>
    path.join(__dirname, file)
  ),
  theme: {
    extend: themes[themeName]
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries')
  ]
};
