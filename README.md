# outheis-docs

Documentation for [outheis](https://github.com/outheis-labs/outheis-minimal) — a multi-agent personal AI assistant.

## Structure

```
outheis-docs/
├── docs/           # Source markdown files
├── html/           # Generated Jekyll site (ready for GitHub Pages)
└── scripts/
    └── build-site.py
```

## Building

```bash
python scripts/build-site.py
```

This reads from `docs/` and generates `html/`.

## Deployment

The `html/` directory is ready for GitHub Pages or any static hosting.

## Live Site

https://outheis-labs.github.io/outheis-minimal/
