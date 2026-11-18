#!/bin/bash
# Run once per session, from the folder that holds snap.js:  bash setup_fonts.sh
set -e
mkdir -p fonts && cd fonts && npm init -y >/dev/null && npm i @fontsource/playfair-display @fontsource/plus-jakarta-sans >/dev/null 2>&1 && cd ..
F=$PWD/fonts/node_modules/@fontsource
python3 - "$F" <<'PY'
import sys
F=sys.argv[1]; css=''
for st in ['normal','italic']:
  for w in [400,500]:
    css+=f"@font-face{{font-family:'Playfair Display';font-style:{st};font-weight:{w};src:url(file://{F}/playfair-display/files/playfair-display-latin-{w}-{st}.woff2) format('woff2');}}\n"
for w in [300,400,500,600,700,800]:
  css+=f"@font-face{{font-family:'Plus Jakarta Sans';font-style:normal;font-weight:{w};src:url(file://{F}/plus-jakarta-sans/files/plus-jakarta-sans-latin-{w}-normal.woff2) format('woff2');}}\n"
open('fonts.css','w').write(css)
PY
echo "fonts.css ready. Usage: node snap.js /abs/path/page.html out.jpg 1440 900 <selector|-> <fullpage 0|1>"
