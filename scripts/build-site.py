#!/usr/bin/env python3
"""
Build the outheis website from docs/.

Reads Markdown from docs/, converts to HTML, wraps in the layout template,
and outputs to html/. Run locally or via GitHub Actions.

Usage:
    python scripts/build-site.py
"""

import re
import shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
HTML = ROOT / "html"
TEMPLATES = ROOT / "templates"

SITE_TITLE = "outheis"

# Navigation definition — order matters
# URLs are defined as absolute but converted to relative during build
NAV_ITEMS = [
    {"label": "Home",          "url": "index.html",                              "match": "^index\\.html$"},
    {"section": "Philosophy"},
    {"label": "Why outheis",   "url": "philosophy/index.html",                   "match": "philosophy"},
    {"section": "Design"},
    {"label": "Overview",      "url": "design/index.html",                       "match": "^design/index\\.html$"},
    {"label": "OS Principles", "url": "design/01-why-os-principles.html",        "match": "01-why-os"},
    {"label": "Systems Survey","url": "design/02-systems-survey.html",           "match": "02-systems"},
    {"label": "Architecture",  "url": "design/03-architecture.html",             "match": "03-architecture"},
    {"label": "Data Formats",  "url": "design/04-data-formats.html",             "match": "04-data"},
    {"label": "Related Work",  "url": "design/05-related-work.html",             "match": "05-related"},
    {"label": "Agent Prompts", "url": "design/06-agent-prompts.html",            "match": "06-agent"},
    {"section": "Implementation"},
    {"label": "Current State", "url": "implementation/architecture.html",        "match": "implementation/architecture"},
    {"label": "Memory & Rules","url": "implementation/memory.html",              "match": "implementation/memory"},
    {"label": "Agenda",        "url": "implementation/agenda.html",              "match": "implementation/agenda"},
    {"label": "Skills",        "url": "implementation/skills.html",              "match": "implementation/skills"},
    {"label": "Migration",     "url": "implementation/migration.html",           "match": "implementation/migration"},
    {"label": "Config",        "url": "implementation/config.html",              "match": "implementation/config"},
    {"label": "CLI Guide",     "url": "implementation/guide.html",               "match": "implementation/guide"},
    {"label": "Web UI",        "url": "implementation/webui.html",               "match": "implementation/webui"},
    {"label": "Code Agent",    "url": "implementation/alan.html",                "match": "implementation/alan"},
    {"section": ""},
    {"label": "GitHub ↗",      "url": "https://github.com/outheis-labs/outheis-minimal", "external": True},
]


def relative_url(from_path: str, to_path: str) -> str:
    """Calculate relative URL from one page to another."""
    from_parts = from_path.split('/')
    to_parts = to_path.split('/')
    
    # From root (index.html) — no prefix needed
    if len(from_parts) == 1:
        return to_path
    
    # From subdir (design/foo.html) — need ../ prefix
    depth = len(from_parts) - 1
    return '../' * depth + to_path


def build_nav(current_rel: str) -> str:
    """Build sidebar nav HTML with active class for current page."""
    items = []
    for item in NAV_ITEMS:
        if "section" in item:
            items.append(f'<li class="nav-section">{item["section"]}</li>')
        elif item.get("external"):
            items.append(
                f'<li><a href="{item["url"]}" class="nav-external">{item["label"]}</a></li>'
            )
        else:
            match = item.get("match", "")
            is_active = bool(re.search(match, current_rel)) if match else False
            active = ' class="active"' if is_active else ''
            url = relative_url(current_rel, item["url"])
            items.append(f'<li><a href="{url}"{active}>{item["label"]}</a></li>')
    return "\n          ".join(items)


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
    """Determine output path: docs/foo/bar.md -> html/foo/bar.html"""
    rel = src.relative_to(DOCS)
    return HTML / rel.with_suffix('.html')


def build_page(src: Path, template: str):
    """Build one page: Markdown → HTML → wrapped in template."""
    raw = src.read_text(encoding='utf-8')
    content_md = strip_frontmatter(raw)
    title = extract_title(content_md, src)
    content_html = md_to_html(content_md)

    dst = output_path(src)
    rel = str(dst.relative_to(HTML))
    
    # Calculate path to root (e.g., "" for index.html, "../" for design/foo.html)
    depth = len(rel.split('/')) - 1
    root = '../' * depth if depth > 0 else ''

    nav_html = build_nav(rel)
    page = (template
            .replace('<!-- ROOT -->', root)
            .replace('<!-- TITLE -->', f'{title} · {SITE_TITLE}' if title != SITE_TITLE else SITE_TITLE)
            .replace('<!-- NAV -->', nav_html)
            .replace('<!-- CONTENT -->', content_html))

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding='utf-8')
    print(f"  {src.relative_to(DOCS)} → {dst.relative_to(HTML)}")


def copy_assets():
    """Copy assets from docs/assets/ to html/."""
    assets_src = DOCS / "assets"
    if not assets_src.exists():
        return

    # Logo goes into html/assets/
    logo_dst = HTML / "assets" / "logo.svg"
    logo_dst.parent.mkdir(parents=True, exist_ok=True)
    logo_src = assets_src / "logo.svg"
    if logo_src.exists():
        shutil.copy(logo_src, logo_dst)
        print("  assets/logo.svg → assets/logo.svg")
    
    # PNG logo as fallback
    logo_png = assets_src / "logo.png"
    if logo_png.exists():
        shutil.copy(logo_png, HTML / "assets" / "logo.png")
        print("  assets/logo.png → assets/logo.png")

    # Other assets go to root (favicon, manifest, etc.)
    for f in assets_src.iterdir():
        if f.name in ("logo.svg", "logo.png"):
            continue
        shutil.copy(f, HTML / f.name)
        print(f"  assets/{f.name} → {f.name}")


def main():
    template = (TEMPLATES / "default.html").read_text(encoding='utf-8')

    HTML.mkdir(exist_ok=True)

    print("Building docs/ → html/")
    for md_file in sorted(DOCS.rglob("*.md")):
        if any(part.startswith('_') for part in md_file.parts):
            continue
        build_page(md_file, template)

    print("\nCopying assets...")
    copy_assets()
    print("\nDone.")


if __name__ == "__main__":
    main()
