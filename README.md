# RDS Independent PU College website

This is a static HTML website. Tailwind CSS is compiled locally into the CSS files served from `assets/css`; the pages do not load Tailwind from a CDN.

## Build styles

Install Node.js LTS, then run these commands from the project folder:

```powershell
npm.cmd install
npm.cmd run build
```

The build creates `assets/css/site.css` for the gold-theme pages and `assets/css/site-green.css` for Downloads, Events, Facilities, and Gallery. Commit the generated CSS files with any HTML or Tailwind theme changes so static hosting can serve the updated styles.

Do not edit the generated CSS directly. Update the page markup, `tailwind.themes.json`, or `tailwind.config.js`, then rebuild.
