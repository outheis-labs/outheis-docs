#!/usr/bin/env python3
"""
Build the outheis website from docs/ and docs-de/.

Reads Markdown, converts to HTML, wraps in the layout template,
and outputs to html/ (EN) and html/de/ (DE).

Usage:
    python scripts/build-site.py
"""

import re
import shutil
from pathlib import Path
import markdown

ROOT = Path(__file__).parent.parent
DOCS_SOURCE = ROOT / "docs"
DOCS_DE = ROOT / "docs-de"
DOCS = ROOT / "html"
TEMPLATES = ROOT / "templates"

SITE_TITLE = "outheis"

# Navigation structure
NAV_STRUCTURE = [
    {
        "id": "foundations",
        "label": "Foundations",
        "label_de": "Grundlagen",
        "items": [
            {"label": "Why outheis", "label_de": "Warum outheis", "url": "foundations/index.html", "match": "foundations/index", "desc": "The case for cognitive sovereignty — why AI assistance needs a different model.", "desc_de": "Das Argument für kognitive Souveränität — warum KI-Assistenz ein anderes Modell braucht."},
            {"label": "Design Principles", "label_de": "Designprinzipien", "url": "foundations/01-design-principles.html", "match": "01-design-principles", "desc": "Local-first, transparent, separated — the core principles behind the architecture.", "desc_de": "Local-first, transparent, getrennt — die Kernprinzipien hinter der Architektur."},
            {"label": "Information and Semantics", "label_de": "Information und Semantik", "url": "foundations/02-semantic-foundations.html", "match": "02-semantic", "desc": "How meaning emerges from structure, and why formats matter.", "desc_de": "Wie Bedeutung aus Struktur entsteht, und warum Formate wichtig sind."},
            {"label": "Attention as Architecture", "label_de": "Aufmerksamkeit als Architekturprinzip", "url": "foundations/03-attention-as-architecture.html", "match": "03-attention", "desc": "Designing systems that respect and direct human attention.", "desc_de": "Systeme entwerfen, die menschliche Aufmerksamkeit respektieren und lenken."},
            {"label": "Annotation as Ground Truth", "label_de": "Annotation als Ground Truth", "url": "foundations/04-annotation-as-ground-truth.html", "match": "04-annotation", "desc": "Why explicit annotation beats implicit inference.", "desc_de": "Warum explizite Annotation implizite Inferenz schlägt."},
            {"label": "Tags as Scaffolding", "label_de": "Tags als Gerüst", "url": "foundations/05-tags-as-scaffolding.html", "match": "05-tags", "desc": "Lightweight structure that grows with your thinking.", "desc_de": "Leichtgewichtige Struktur, die mit deinem Denken wächst."},
        ],
    },
    {
        "id": "design",
        "label": "Design",
        "label_de": "Design",
        "items": [
            {"label": "Overview", "label_de": "Überblick", "url": "design/index.html", "match": "^design/index", "desc": "The big picture — how the pieces fit together.", "desc_de": "Das große Bild — wie die Teile zusammenpassen."},
            {"label": "OS Principles", "label_de": "OS-Prinzipien", "url": "design/01-why-os-principles.html", "match": "01-why-os", "desc": "What we learned from decades of operating system design.", "desc_de": "Was wir aus Jahrzehnten Betriebssystem-Design gelernt haben."},
            {"label": "Systems Survey", "label_de": "Systemvergleich", "url": "design/02-systems-survey.html", "match": "02-systems", "desc": "Existing approaches and why they fall short.", "desc_de": "Bestehende Ansätze und warum sie nicht ausreichen."},
            {"label": "Architecture", "label_de": "Architektur", "url": "design/03-architecture.html", "match": "03-architecture", "desc": "Five agents, message passing, explicit capabilities.", "desc_de": "Fünf Agenten, Nachrichtenübermittlung, explizite Fähigkeiten."},
            {"label": "Data Formats", "label_de": "Datenformate", "url": "design/04-data-formats.html", "match": "04-data", "desc": "Markdown, JSON, and the case for human-readable storage.", "desc_de": "Markdown, JSON und das Argument für menschenlesbare Speicherung."},
            {"label": "Related Work", "label_de": "Verwandte Ansätze", "url": "design/05-related-work.html", "match": "05-related", "desc": "Prior art and influences.", "desc_de": "Vorarbeiten und Einflüsse."},
            {"label": "Agent Prompts", "label_de": "Agenten-Prompts", "url": "design/06-agent-prompts.html", "match": "06-agent", "desc": "How agents are instructed and constrained.", "desc_de": "Wie Agenten instruiert und eingeschränkt werden."},
            {"label": "Hybrid Memory Stack", "label_de": "Hybrider Memory-Stack", "url": "design/07-hybrid-memory-stack.html", "match": "07-hybrid", "desc": "Combining retrieval methods for robust context.", "desc_de": "Kombination von Abrufmethoden für robusten Kontext."},
            {"label": "Quality Threshold", "label_de": "Qualitätsschwelle", "url": "design/08-quality-threshold.html", "match": "08-quality", "desc": "When to act, when to wait.", "desc_de": "Wann handeln, wann warten."},
        ],
    },
    {
        "id": "implementation",
        "label": "Implementation",
        "label_de": "Implementierung",
        "items": [
            {"label": "Current State", "label_de": "Aktueller Stand", "url": "implementation/01-architecture.html", "match": "01-architecture", "desc": "Where we are now.", "desc_de": "Wo wir jetzt stehen."},
            {"label": "Memory & Rules", "label_de": "Memory & Regeln", "url": "implementation/02-memory.html", "match": "02-memory", "desc": "How memory and rules work.", "desc_de": "Wie Memory und Regeln funktionieren."},
            {"label": "Agenda", "label_de": "Agenda", "url": "implementation/03-agenda.html", "match": "03-agenda", "desc": "Task management and scheduling.", "desc_de": "Aufgabenverwaltung und Planung."},
            {"label": "Skills", "label_de": "Skills", "url": "implementation/04-skills.html", "match": "04-skills", "desc": "Extending agent capabilities.", "desc_de": "Agentenfähigkeiten erweitern."},
            {"label": "Code Agent", "label_de": "Code-Agent", "url": "implementation/05-alan.html", "match": "05-alan", "desc": "The alan agent for code tasks.", "desc_de": "Der alan-Agent für Code-Aufgaben."},
            {"label": "Action Agent", "label_de": "Action-Agent", "url": "implementation/06-hiro.html", "match": "06-hiro", "desc": "The hiro agent for actions.", "desc_de": "Der hiro-Agent für Aktionen."},
            {"label": "Signal", "label_de": "Signal", "url": "implementation/07-signal.html", "match": "07-signal", "desc": "The signal mechanism.", "desc_de": "Der Signal-Mechanismus."},
            {"label": "Annotation Feedback", "label_de": "Annotations-Feedback", "url": "implementation/08-annotation-feedback.html", "match": "08-annotation-feedback", "desc": "Learning from corrections.", "desc_de": "Aus Korrekturen lernen."},
            {"label": "Vault", "label_de": "Vault", "url": "implementation/09-vault.html", "match": "09-vault", "desc": "Data storage structure.", "desc_de": "Datenspeicherstruktur."},
            {"label": "Configuration", "label_de": "Konfiguration", "url": "implementation/10-config.html", "match": "10-config", "desc": "Configuration options.", "desc_de": "Konfigurationsoptionen."},
            {"label": "Getting Started", "label_de": "Erste Schritte", "url": "implementation/11-guide.html", "match": "11-guide", "desc": "Setup and first steps.", "desc_de": "Einrichtung und erste Schritte."},
            {"label": "Migration", "label_de": "Migration", "url": "implementation/12-migration.html", "match": "12-migration", "desc": "Upgrading between versions.", "desc_de": "Zwischen Versionen wechseln."},
            {"label": "Web UI", "label_de": "Web UI", "url": "implementation/13-webui.html", "match": "13-webui", "desc": "The browser interface.", "desc_de": "Die Browser-Oberfläche."},
        ],
    },
    {
        "id": "installation",
        "label": "Installation",
        "label_de": "Installation",
        "items": [
            {"label": "Release Notes", "label_de": "Release Notes", "url": "installation/01-release-notes.html", "match": "01-release-notes", "desc": "What's new in each version.", "desc_de": "Was in jeder Version neu ist."},
            {"label": "Models", "label_de": "Modelle", "url": "installation/02-models.html", "match": "02-models", "desc": "Supported LLM providers.", "desc_de": "Unterstützte LLM-Anbieter."},
            {"label": "Communication", "label_de": "Kommunikation", "url": "installation/03-communication.html", "match": "03-communication", "desc": "How to talk to outheis.", "desc_de": "Wie man mit outheis spricht."},
        ],
    },
    {
        "id": "workflows",
        "label": "Workflows",
        "label_de": "Workflows",
        "items": [
            {"label": "Overview", "label_de": "Überblick", "url": "workflows/index.html", "match": "workflows/index", "desc": "Practical patterns for daily use.", "desc_de": "Praktische Muster für den täglichen Gebrauch."},
            {"label": "Tags", "label_de": "Tags", "url": "workflows/01-tags.html", "match": "01-tags", "desc": "Using tags for organization.", "desc_de": "Tags zur Organisation verwenden."},
        ],
    },
]


def get_flat_nav_list(lang: str) -> list:
    """Get a flat list of all pages in order for prev/next navigation."""
    flat = []
    label_key = 'label_de' if lang == 'de' else 'label'
    for section in NAV_STRUCTURE:
        for item in section['items']:
            flat.append({
                'label': item.get(label_key, item['label']),
                'url': item['url'],
                'match': item['match'],
                'section_id': section['id'],
                'section_label': section.get(label_key, section['label']),
            })
    return flat


def find_current_page(current_rel: str, flat_nav: list) -> tuple:
    """Find current page index and return (prev, current, next) info."""
    current_idx = None
    for i, item in enumerate(flat_nav):
        if re.search(item['match'], current_rel):
            current_idx = i
            break
    
    if current_idx is None:
        return None, None, None
    
    prev_item = flat_nav[current_idx - 1] if current_idx > 0 else None
    current_item = flat_nav[current_idx]
    next_item = flat_nav[current_idx + 1] if current_idx < len(flat_nav) - 1 else None
    
    return prev_item, current_item, next_item


def extract_title(content: str, filepath: Path) -> str:
    """Extract title from first H1 or derive from filename."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filepath.stem.replace('-', ' ').title()


def extract_subtitle(content: str) -> str:
    """
    Extract subtitle from markdown content.
    Subtitle is the first italic line after H1 and before ---.
    Returns empty string if no subtitle found.
    """
    lines = content.strip().split('\n')
    found_h1 = False
    
    for line in lines:
        line = line.strip()
        
        # Skip until we find H1
        if line.startswith('# '):
            found_h1 = True
            continue
        
        if not found_h1:
            continue
        
        # Stop at horizontal rule
        if line.startswith('---'):
            break
        
        # Skip empty lines
        if not line:
            continue
        
        # Italic line = subtitle
        if line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            return line.strip('*').strip()
    
    return ''


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter if present."""
    if content.startswith('---\n'):
        end = content.find('\n---\n', 4)
        if end != -1:
            return content[end + 5:]
    return content


def md_to_html(content: str) -> str:
    """Convert Markdown to HTML."""
    html = markdown.markdown(
        content,
        extensions=['tables', 'fenced_code', 'attr_list', 'toc'],
        extension_configs={'toc': {'permalink': False}}
    )
    # Wrap Greek text (οὐθείς) in span for Inter font
    html = re.sub(r'οὐθείς', '<span class="greek">οὐθείς</span>', html)
    return html


def wrap_content_in_sections(html: str) -> str:
    """
    Wrap content in section divs with the two-column layout.
    Each H2 starts a new section with the heading as the left label.
    H1 is removed (shown in page header).
    Subtitle (first italic paragraph before H2) is removed (shown in page header).
    All hr tags are removed (section borders are CSS-based).
    H2 is duplicated in section-text for mobile/desktop CSS switching.
    H2 IDs are transferred to the section element.
    """
    # Remove H1 (shown in page header)
    html = re.sub(r'<h1[^>]*>.*?</h1>\s*', '', html, count=1, flags=re.DOTALL)
    
    # Remove all hr tags (section borders are handled by CSS)
    html = re.sub(r'\s*<hr\s*/?>\s*', '\n', html)
    
    # Split by H2 headings
    parts = re.split(r'(<h2[^>]*>.*?</h2>)', html, flags=re.DOTALL)
    
    if len(parts) <= 1:
        # No H2 headings
        content = html.strip()
        # Remove subtitle (first <p><em>...</em></p>)
        content = re.sub(r'^(\s*<p><em>.*?</em></p>\s*)', '', content, count=1)
        if content:
            return f'<section class="section"><h2></h2><div class="section-text">{content}</div></section>'
        return ''
    
    sections = []
    current_heading = None
    current_content = []
    
    # First part before any H2 (intro/lead text)
    intro = parts[0].strip()
    # Remove subtitle (first <p><em>...</em></p>) - it's shown in page header
    intro = re.sub(r'^(\s*<p><em>.*?</em></p>\s*)', '', intro, count=1)
    intro = intro.strip()
    if intro:
        sections.append(f'<section class="section"><h2></h2><div class="section-text">{intro}</div></section>')
    
    for part in parts[1:]:
        if re.match(r'<h2[^>]*>', part):
            # Save previous section
            if current_heading is not None:
                content = ''.join(current_content).strip()
                # Extract ID from heading if present
                id_match = re.search(r'id="([^"]*)"', current_heading)
                section_id = f' id="{id_match.group(1)}"' if id_match else ''
                # Get heading text without tags and ID
                heading_text = re.sub(r'</?h2[^>]*>', '', current_heading).strip()
                sections.append(
                    f'<section class="section"{section_id}>\n'
                    f'      <h2>{heading_text}</h2>\n'
                    f'      <div class="section-text"><h2>{heading_text}</h2>\n'
                    f'        {content}\n'
                    f'      </div>\n'
                    f'    </section>'
                )
            current_heading = part
            current_content = []
        else:
            current_content.append(part)
    
    # Last section
    if current_heading is not None:
        content = ''.join(current_content).strip()
        # Extract ID from heading if present
        id_match = re.search(r'id="([^"]*)"', current_heading)
        section_id = f' id="{id_match.group(1)}"' if id_match else ''
        # Get heading text without tags and ID
        heading_text = re.sub(r'</?h2[^>]*>', '', current_heading).strip()
        sections.append(
            f'<section class="section"{section_id}>\n'
            f'      <h2>{heading_text}</h2>\n'
            f'      <div class="section-text"><h2>{heading_text}</h2>\n'
            f'        {content}\n'
            f'      </div>\n'
            f'    </section>'
        )
    
    return '\n\n    '.join(sections)


def build_breadcrumb(current_item: dict, root: str) -> str:
    """Build breadcrumb HTML."""
    if current_item is None:
        return ''
    
    return (
        f'<div class="breadcrumb">\n'
        f'        <span class="separator">/</span>\n'
        f'        <a href="{root}contents.html#{current_item["section_id"]}">{current_item["section_label"]}</a>\n'
        f'        <span class="separator">/</span>\n'
        f'        <span class="current">{current_item["label"]}</span>\n'
        f'      </div>'
    )


def build_book_nav(prev_item: dict, current_item: dict, next_item: dict, root: str, lang: str) -> str:
    """Build book-style navigation HTML."""
    section_id = current_item['section_id'] if current_item else ''
    section_label = current_item['section_label'] if current_item else ''
    
    prev_html = ''
    if prev_item:
        prev_label = "Zurück" if lang == "de" else "Previous"
        prev_html = (
            f'<a href="{root}{prev_item["url"]}">\n'
            f'          <span class="label">← {prev_label}</span>\n'
            f'          <span class="title">{prev_item["label"]}</span>\n'
            f'        </a>'
        )
    
    toc_label = "Inhalt" if lang == "de" else "Contents"
    toc_html = (
        f'<a href="{root}contents.html#{section_id}">\n'
        f'          <span class="label">{toc_label}</span>\n'
        f'          <span class="title">{section_label}</span>\n'
        f'        </a>'
    )
    
    next_html = ''
    if next_item:
        next_label = "Weiter" if lang == "de" else "Next"
        next_html = (
            f'<a href="{root}{next_item["url"]}">\n'
            f'          <span class="label">{next_label} →</span>\n'
            f'          <span class="title">{next_item["label"]}</span>\n'
            f'        </a>'
        )
    
    return (
        f'<nav class="book-nav">\n'
        f'      <div class="prev">{prev_html}</div>\n'
        f'      <div class="toc-center">{toc_html}</div>\n'
        f'      <div class="next">{next_html}</div>\n'
        f'    </nav>'
    )


def build_page(src: Path, src_root: Path, out_root: Path, template: str, lang: str):
    """Build one page: Markdown → HTML → wrapped in template."""
    raw = src.read_text(encoding='utf-8')
    content_md = strip_frontmatter(raw)
    title = extract_title(content_md, src)
    subtitle = extract_subtitle(content_md)
    content_html = md_to_html(content_md)
    
    # Wrap content in sections
    content_wrapped = wrap_content_in_sections(content_html)
    
    rel_local = str(src.relative_to(src_root).with_suffix('.html'))
    dst = out_root / rel_local
    rel_from_html = str(dst.relative_to(DOCS))
    
    depth = len(rel_from_html.split('/')) - 1
    root = '../' * depth if depth > 0 else ''
    
    # Navigation
    flat_nav = get_flat_nav_list(lang)
    prev_item, current_item, next_item = find_current_page(rel_local, flat_nav)
    
    breadcrumb_html = build_breadcrumb(current_item, root)
    book_nav_html = build_book_nav(prev_item, current_item, next_item, root, lang)
    section_anchor = f'#{current_item["section_id"]}' if current_item else ''
    
    # Language switcher — DE hidden until translation is ready for publication
    lang_switch_html = ''
    
    # Subtitle HTML
    subtitle_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ''
    
    page = (template
            .replace('<!-- ROOT -->', root)
            .replace('<!-- TITLE -->', f'{title} · {SITE_TITLE}')
            .replace('<!-- PAGE_TITLE -->', title)
            .replace('<!-- SUBTITLE -->', subtitle_html)
            .replace('<!-- BREADCRUMB -->', breadcrumb_html)
            .replace('<!-- SECTION_ANCHOR -->', section_anchor)
            .replace('<!-- LANG_SWITCH -->', lang_switch_html)
            .replace('<!-- CONTENT -->', content_wrapped)
            .replace('<!-- BOOK_NAV -->', book_nav_html))
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding='utf-8')
    print(f"  {src.relative_to(src_root)} → {dst.relative_to(DOCS)}")


def build_index_page(src: Path, src_root: Path, out_root: Path, hero_template: str, lang: str):
    """Build the index/landing page with hero template."""
    raw = src.read_text(encoding='utf-8')
    content_md = strip_frontmatter(raw)
    title = extract_title(content_md, src)
    
    # Split content at first --- to separate lead from rest
    parts = re.split(r'\n---\n', content_md, maxsplit=1)
    
    # Extract lead (everything after H1, before ---)
    lead_md = parts[0]
    lead_md = re.sub(r'^#\s+.+\n+', '', lead_md)  # Remove H1
    lead_html = md_to_html(lead_md)
    
    # Convert <p>...</p><p>...</p> to inline format with <br><br>
    # Strip <p> tags and join with <br><br>
    lead_html = re.sub(r'<p>(.*?)</p>\s*', r'\1<br><br>', lead_html, flags=re.DOTALL)
    lead_html = re.sub(r'(<br><br>)+$', '', lead_html)  # Remove trailing br
    lead_html = lead_html.strip()
    
    # Rest of content (after ---)
    rest_md = parts[1] if len(parts) > 1 else ''
    rest_html = md_to_html(rest_md)
    content_wrapped = wrap_content_in_sections(rest_html)
    
    rel_local = str(src.relative_to(src_root).with_suffix('.html'))
    dst = out_root / rel_local
    rel_from_html = str(dst.relative_to(DOCS))
    
    depth = len(rel_from_html.split('/')) - 1
    root = '../' * depth if depth > 0 else ''
    
    # Language switcher — DE hidden until translation is ready for publication
    lang_switch_html = ''
    
    page = (hero_template
            .replace('<!-- ROOT -->', root)
            .replace('<!-- TITLE -->', f'{title} · {SITE_TITLE}')
            .replace('<!-- PAGE_TITLE -->', title)
            .replace('<!-- HERO_LEAD -->', lead_html)
            .replace('<!-- LANG_SWITCH -->', lang_switch_html)
            .replace('<!-- CONTENT -->', content_wrapped))
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page, encoding='utf-8')
    print(f"  {src.relative_to(src_root)} → {dst.relative_to(DOCS)} (hero)")


def copy_assets():
    """Copy assets from docs/assets/ to html/."""
    assets_src = DOCS_SOURCE / "assets"
    if not assets_src.exists():
        return
    
    assets_dst = DOCS / "assets"
    assets_dst.mkdir(parents=True, exist_ok=True)
    
    for f in assets_src.iterdir():
        if f.is_dir():
            dst_dir = assets_dst / f.name
            if dst_dir.exists():
                shutil.rmtree(dst_dir)
            shutil.copytree(f, dst_dir)
            print(f"  assets/{f.name}/ → assets/{f.name}/")
        else:
            shutil.copy(f, assets_dst / f.name)
            # Copy favicon files to root
            if f.name.startswith('favicon') or f.name.startswith('apple-touch') or f.name.startswith('web-app') or f.name == 'site.webmanifest':
                shutil.copy(f, DOCS / f.name)
                print(f"  assets/{f.name} → {f.name}")
            else:
                print(f"  assets/{f.name} → assets/{f.name}")


def main():
    template = (TEMPLATES / "default.html").read_text(encoding='utf-8')
    hero_template = (TEMPLATES / "hero.html").read_text(encoding='utf-8')
    
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(exist_ok=True)
    
    print(f"Building EN: {DOCS_SOURCE.name}/ → {DOCS.name}/")
    for md_file in sorted(DOCS_SOURCE.rglob("*.md")):
        if any(part.startswith('_') for part in md_file.parts):
            continue
        if md_file.name == 'index.md' and md_file.parent == DOCS_SOURCE:
            build_index_page(md_file, DOCS_SOURCE, DOCS, hero_template, 'en')
        else:
            build_page(md_file, DOCS_SOURCE, DOCS, template, 'en')
    
    print(f"\nBuilding DE: {DOCS_DE.name}/ → {DOCS.name}/de/")
    for md_file in sorted(DOCS_DE.rglob("*.md")):
        if any(part.startswith('_') for part in md_file.parts):
            continue
        if md_file.name == 'index.md' and md_file.parent == DOCS_DE:
            build_index_page(md_file, DOCS_DE, DOCS / 'de', hero_template, 'de')
        else:
            build_page(md_file, DOCS_DE, DOCS / 'de', template, 'de')
    
    print("\nCopying assets...")
    copy_assets()
    print("\nDone.")


if __name__ == "__main__":
    main()
