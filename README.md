# Portfolio — Bryan Debnam

Source for the GitHub Pages portfolio site.

- **`portfolio.md`** — the content. Edit this.
- **`index.html`** — build output, committed because GitHub Pages serves it directly. Do not edit by hand.
- **`build_site.py`** — regenerates `index.html` from `portfolio.md`.
- **`resume/`** — resume PDFs and DOCXs, linked from the top of the page. Built from the
  Markdown sources in `Enterprise-Sandbox/documents/`; copy new builds in, don't edit here.

## Rebuild

    /home/bigperms/Enterprise-Sandbox/documents/.md2pdf-venv/bin/python build_site.py
    git commit -am "portfolio: update" && git push

Any Python with the `markdown` package works; that venv just already has it.

## GitHub Pages

Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/(root)` → Save.
The site then serves at `https://<username>.github.io/Portfolio-GitHub/`.

`.nojekyll` is present so Pages serves the files as-is instead of running Jekyll.
