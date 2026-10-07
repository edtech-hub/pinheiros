# Starter kit

Copy this folder into a new client repo (`~/projects/<slug>/`), then follow `../CLAUDE.md`.

- `assets/css/wp-blocks.css`: official WordPress block styles (subset of @wordpress/block-library 11.2.0). Do not edit.
- `assets/css/site.css`: theme layer. Change the color tokens at the top to the client's brand; the rest usually stays.
- `assets/js/site.js`: open/closed status, sticky header, overlay menu, mega menu, lightbox, fade-ins, Gravity-style forms, mobile action bar.
- `tools/build_site.py`: page generator. Reference content is I&M Services. Replace the CONFIG block and every line of copy, then `python3 tools/build_site.py .`
- `tools/images.js`: WebP sizes, transparent logo, favicon, OG image. `cd tools && npm install`, then `node tools/images.js images.json`.
- `tools/qa/phone.html`: 390px iframe for phone screenshots (headless Chrome won't go below 500px wide).
