# Portfolio — Bryan Debnam

Source for the GitHub Pages portfolio site.

- **`portfolio.md`** — the content. Edit this.
- **`index.html`** — build output, committed because GitHub Pages serves it directly. Do not edit by hand.
- **`build_site.py`** — regenerates `index.html` from `portfolio.md`.
- **`resume/`** — resume PDFs and DOCXs, linked from the top of the page. Build output; don't
  edit here. These are the **public** copies: identical to the private ones except the phone
  number is stripped, since this directory is served on the open web. Regenerate with
  `Enterprise-Sandbox/documents/build_public_resumes.sh` after editing the Markdown sources.

## Rebuild

    /home/bigperms/Enterprise-Sandbox/documents/.md2pdf-venv/bin/python build_site.py
    git commit -am "portfolio: update" && git push

Any Python with the `markdown` package works; that venv just already has it.

## GitHub Pages

Settings → Pages → Build and deployment → Deploy from a branch → `main` / `/(root)` → Save.
The site then serves at `https://<username>.github.io/Portfolio-GitHub/`.

`.nojekyll` is present so Pages serves the files as-is instead of running Jekyll.
