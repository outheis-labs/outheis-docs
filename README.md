# outheis-docs

Documentation for [outheis](https://github.com/outheis-labs/outheis-beta) — a privacy-first multi-agent personal AI assistant.

**📖 [Read the documentation](https://outheis.com)**

## Structure

```
outheis-docs/
├── docs/              # Source (Markdown, English)
├── docs-de/           # Source (Markdown, German)
├── html/              # Built site (HTML) — served via GitHub Pages
├── templates/         # Page template
└── scripts/
    ├── build-site.py           # Build script (EN + DE)
    └── generate-contents.py   # Auto-generate contents.md for each language
```

## Building locally

```bash
pip install markdown
python scripts/generate-contents.py
python scripts/build-site.py
```

Generates `html/` from `docs/` (English) and `html/de/` from `docs-de/` (German).

## Deployment

GitHub Actions builds and commits `html/` on every push to `main` that touches `docs/`, `docs-de/`, `templates/`, or `scripts/`. GitHub Pages serves `html/`.
