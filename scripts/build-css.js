const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const cli = path.join(root, 'node_modules', 'tailwindcss', 'lib', 'cli.js');
const input = path.join(root, 'src', 'tailwind.css');
const outputDirectory = path.join(root, 'assets', 'css');

fs.mkdirSync(outputDirectory, { recursive: true });

for (const theme of ['gold', 'green']) {
  const output = path.join(outputDirectory, theme === 'green' ? 'site-green.css' : 'site.css');
  execFileSync(process.execPath, [
    cli,
    '-i', input,
    '-o', output,
    '--config', path.join(root, 'tailwind.config.js'),
    '--minify'
  ], {
    cwd: root,
    env: { ...process.env, SITE_THEME: theme },
    stdio: 'inherit'
  });
  console.log(`Built ${path.relative(root, output)}`);
}
