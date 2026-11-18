# Funnel tools (not published: GitHub Pages ignores folders starting with "_")

- `setup_fonts.sh` + `snap.js`: font-accurate Playwright screenshots of local pages (prints horizontal overflow, must be 0).
- `make_music_432.py <seconds> <name>`: the approved 432 Hz music bed (v6). Then `ffmpeg -i name.wav -b:a 256k name.mp3`.
- `checkout_product_card.html`: Raw HTML product card for a Systeme checkout (swap image, title, bullets).
- `checkout_header_code.css`: the full header-code CSS that makes the Systeme checkout two-column on desktop and clean on phones. Swap the element IDs for the new checkout's IDs.
- Page templates: `../index.html` (opt-in/sales), `../thank-you/index.html` (upsell), `../access/index.html` (delivery). Copy, then change copy and images.
