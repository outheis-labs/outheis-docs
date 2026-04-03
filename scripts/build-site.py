#!/usr/bin/env python3
"""
Build the outheis website from docs_source/.

Reads Markdown from docs_source/, converts to HTML, wraps in the layout template,
and outputs to docs/. Run locally or via GitHub Actions.

Usage:
    python scripts/build-site.py
"""

import re
import shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent.parent
DOCS_SOURCE = ROOT / "docs"
DOCS = ROOT / "html"  # Output (served by GitHub Pages)
TEMPLATES = ROOT / "templates"

SITE_TITLE = "outheis"

# Navigation: four top-level sections, each with sub-pages.
# 'match' is a regex tested against the current page's relative path.
NAV_SECTIONS = [
    {
        "label": "Foundations",
        "url": "foundations/index.html",
        "match": "foundations",
        "items": [
            {"label": "Why outheis",               "url": "foundations/index.html",                       "match": "foundations/index"},
            {"label": "Information and Semantics", "url": "foundations/02-semantic-foundations.html",      "match": "02-semantic"},
            {"label": "Attention as Architecture", "url": "foundations/03-attention-as-architecture.html", "match": "03-attention"},
        ],
    },
    {
        "label": "Design",
        "url": "design/index.html",
        "match": "^design/",
        "items": [
            {"label": "Overview",              "url": "design/index.html",                        "match": "^design/index"},
            {"label": "OS Principles",         "url": "design/01-why-os-principles.html",         "match": "01-why-os"},
            {"label": "Systems Survey",        "url": "design/02-systems-survey.html",            "match": "02-systems"},
            {"label": "Architecture",          "url": "design/03-architecture.html",              "match": "03-architecture"},
            {"label": "Data Formats",          "url": "design/04-data-formats.html",              "match": "04-data"},
            {"label": "Related Work",          "url": "design/05-related-work.html",              "match": "05-related"},
            {"label": "Agent Prompts",         "url": "design/06-agent-prompts.html",             "match": "06-agent"},
            {"label": "Hybrid Memory Stack",   "url": "design/07-hybrid-memory-stack.html",       "match": "07-hybrid"},
        ],
    },
    {
        "label": "Implementation",
        "url": "implementation/architecture.html",
        "match": "implementation/(architecture|memory|agenda|skills|alan)",
        "items": [
            {"label": "Current State",  "url": "implementation/architecture.html", "match": "implementation/architecture"},
            {"label": "Memory & Rules", "url": "implementation/memory.html",       "match": "implementation/memory"},
            {"label": "Agenda",         "url": "implementation/agenda.html",       "match": "implementation/agenda"},
            {"label": "Skills",         "url": "implementation/skills.html",       "match": "implementation/skills"},
            {"label": "Code Agent",     "url": "implementation/alan.html",         "match": "implementation/alan"},
        ],
    },
    {
        "label": "Workflows",
        "url": "workflows/index.html",
        "match": "^workflows/",
        "items": [
            {"label": "Overview", "url": "workflows/index.html", "match": "workflows/index"},
        ],
    },
    {
        "label": "Installation",
        "url": "installation/index.html",
        "match": "installation|guide|config|migration|webui|signal",
        "items": [
            {"label": "Installation",    "url": "installation/index.html",          "match": "installation/index"},
            {"label": "Release Notes",   "url": "installation/release-notes.html",  "match": "release-notes"},
            {"label": "Getting Started", "url": "implementation/guide.html",        "match": "implementation/guide"},
            {"label": "Configuration",   "url": "implementation/config.html",       "match": "implementation/config"},
            {"label": "Signal",          "url": "implementation/signal.html",       "match": "implementation/signal"},
            {"label": "Migration",       "url": "implementation/migration.html",    "match": "implementation/migration"},
            {"label": "Web UI",          "url": "implementation/webui.html",        "match": "implementation/webui"},
        ],
    },
]


def relative_url(from_path: str, to_path: str) -> str:
    """Calculate relative URL from one page to another."""
    from_parts = from_path.split('/')
    # From root (index.html) — no prefix needed
    if len(from_parts) == 1:
        return to_path
    # From subdir (design/foo.html) — need ../ prefix
    depth = len(from_parts) - 1
    return '../' * depth + to_path


def build_nav(current_rel: str) -> tuple[str, str]:
    """
    Build top nav and sub-nav HTML for the current page.

    Returns (topnav_html, subnav_html).
    topnav_html: the four section links + GitHub
    subnav_html: the sub-pages of the active section (empty string if none)
    """
    # Determine active section
    active_section = None
    for section in NAV_SECTIONS:
        if re.search(section["match"], current_rel):
            active_section = section
            break

    # Top nav
    top_items = []
    for section in NAV_SECTIONS:
        is_active = section is active_section
        active_cls = ' class="active"' if is_active else ''
        url = relative_url(current_rel, section["url"])
        top_items.append(f'<a href="{url}"{active_cls}>{section["label"]}</a>')
    # GitHub link (hidden on mobile via CSS)
    top_items.append('<a href="https://github.com/outheis-labs/outheis-minimal" class="external">GitHub ↗</a>')
    topnav_html = "\n        ".join(top_items)

    # Sub nav (only for the active section)
    subnav_html = ""
    if active_section:
        sub_items = []
        for item in active_section.get("items", []):
            match = item.get("match", "")
            is_active = bool(re.search(match, current_rel)) if match else False
            active_cls = ' class="active"' if is_active else ''
            url = relative_url(current_rel, item["url"])
            sub_items.append(f'<a href="{url}"{active_cls}>{item["label"]}</a>')
        subnav_html = "\n      ".join(sub_items)

    return topnav_html, subnav_html


def extract_title(content: str, filepath: Path) -> str:
    """Extract title from first H1 or derive from filename."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filepath.stem.replace('-', ' ').title()


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter if present."""
    if content.startswith('---\n'):
        end = content.find('\n---\n', 4)
        if end != -1:
            return content[end + 5:]
    return content


def md_to_html(content: str) -> str:
    """Convert Markdown to HTML."""
    return markdown.markdown(
        content,
        extensions=['tables', 'fenced_code', 'attr_list', 'toc'],
        extension_configs={
            'toc': {'permalink': False}
        }
    )


def output_path(src: Path) -> Path:
    """Determine output path: docs_source/foo/bar.md -> docs/foo/bar.html"""
    rel = src.relative_to(DOCS_SOURCE)
    return DOCS / rel.with_suffix('.html')


def build_page(src: Path, template: str):
    """Build one page: Markdown → HTML → wrapped in template."""
    raw = src.read_text(encoding='utf-8')
    content_md = strip_frontmatter(raw)
    title = extract_title(content_md, src)
    content_html = md_to_html(content_md)

    dst = output_path(src)
    rel = str(dst.relative_to(DOCS))

    # Calculate path to root (e.g., "" for index.html, "../" for design/foo.html)
    depth = len(rel.split('/')) - 1
    root = '../' * depth if depth > 0 else ''

    topnav_html, subnav_html = build_nav(rel)

    if subnav_html:
        subnavbar_html = (
            '<div class="subnav-bar">\n'
            '    <div class="subnav-inner">\n'
            f'      {subnav_html}\n'
            '    </div>\n'
            '  </div>'
        )
    else:
        subnavbar_html = ''

    page = (template
            .replace('<!-- ROOT -->', root)
            .replace('<!-- TITLE -->', f'{title} · {SITE_TITLE}' if title != SITE_TITLE else SITE_TITLE)
            .replace('<!-- TOPNAV -->', topnav_html)
            .replace('<!-- SUBNAVBAR -->', subnavbar_html)
            .replace('<!-- CONTENT -->', content_html))

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding='utf-8')
    print(f"  {src.relative_to(DOCS_SOURCE)} → {dst.relative_to(DOCS)}")


def copy_assets():
    """Copy assets from docs_source/assets/ to docs/."""
    assets_src = DOCS_SOURCE / "assets"
    if not assets_src.exists():
        return

    assets_dst = DOCS / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)

    logo_src = assets_src / "logo.svg"
    if logo_src.exists():
        shutil.copy(logo_src, assets_dst / "logo.svg")
        print("  assets/logo.svg → assets/logo.svg")

    logo_png = assets_src / "logo.png"
    if logo_png.exists():
        shutil.copy(logo_png, assets_dst / "logo.png")
        print("  assets/logo.png → assets/logo.png")

    for f in assets_src.iterdir():
        if f.name in ("logo.svg", "logo.png"):
            continue
        if f.is_dir():
            dst_dir = assets_dst / f.name
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(f, dst_dir)
            print(f"  assets/{f.name}/ → assets/{f.name}/")
        else:
            shutil.copy(f, DOCS / f.name)
            print(f"  assets/{f.name} → {f.name}")


def main():
    template = (TEMPLATES / "default.html").read_text(encoding='utf-8')

    # Clean and recreate output
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(exist_ok=True)

    print(f"Building {DOCS_SOURCE.name}/ → {DOCS.name}/")
    for md_file in sorted(DOCS_SOURCE.rglob("*.md")):
        if any(part.startswith('_') for part in md_file.parts):
            continue
        build_page(md_file, template)

    print("\nCopying assets...")
    copy_assets()
    print("\nDone.")


if __name__ == "__main__":
    main()
