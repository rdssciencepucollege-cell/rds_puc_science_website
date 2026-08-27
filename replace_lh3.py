import pathlib
import re

images = [
    'images/college-from-ground.jpg',
    'images/rds-rightwing-building.png',
    'images/rds-corridor.png',
    'images/rds-chem-lab.png',
    'images/rds-bio-lab.png',
    'images/rds-sports.png',
    'images/vid-teach-collage-hori.png',
    'images/vid-teaching-bio-vert.png',
    'images/vid-teaching-bio.png',
    'images/vid-teaching-hori.png',
]
pattern = re.compile(r'https://lh3\.googleusercontent\.com[^\)"\'\s]+')
idx = [0]
replaced = [0]
for path in sorted(pathlib.Path('.').glob('*.html')):
    text = path.read_text(encoding='utf-8')
    def repl(match):
        replacement = images[idx[0] % len(images)]
        idx[0] += 1
        replaced[0] += 1
        return replacement
    new_text = pattern.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding='utf-8')
        print(f'Updated {path} with {new_text.count("images/")} local references')
print(f'Total replaced remote URLs: {replaced[0]}')
