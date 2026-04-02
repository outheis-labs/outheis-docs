# outheis-docs

Documentation for [outheis](https://github.com/outheis-labs/outheis-minimal) — a privacy-first multi-agent personal AI assistant.

**📖 [Read the documentation](https://outheis-labs.github.io/outheis-docs/)**

## Structure

```
outheis-docs/
├── docs/              # Source (Markdown)
├── html/              # Built site (HTML)
├── templates/         # Page template
└── scripts/
    └── build-site.py  # Build script
```

## Building locally

```bash
pip install markdown
python scripts/build-site.py
```

Generates `html/` from `docs/`.

## Deployment

GitHub Pages serves from `html/` on push to `main`.
