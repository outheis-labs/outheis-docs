#!/usr/bin/env python3
"""
Generate contents.md by traversing the docs/ file tree.

Structure is derived from:
- Directories = Sections (foundations, design, implementation, ...)
- Files = Items, ordered by filename (01-xxx.md, 02-xxx.md, ...)
- index.md in each directory = section overview (listed first)

No static STRUCTURE needed — file system is the source of truth.
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_ROOT = PROJECT_ROOT / 'docs'
DOCS_DE_ROOT = PROJECT_ROOT / 'docs-de'

# Section order and labels (only metadata, not file lists)
SECTIONS = {
    "foundations": {"label": "Foundations", "label_de": "Grundlagen", "order": 1},
    "design": {"label": "Design", "label_de": "Design", "order": 2},
    "implementation": {"label": "Implementation", "label_de": "Implementierung", "order": 3},
    "installation": {"label": "Installation", "label_de": "Installation", "order": 4},
    "workflows": {"label": "Workflows", "label_de": "Workflows", "order": 5},
}

MAX_DESC_LENGTH = 100


def extract_metadata(content: str) -> tuple[str, str]:
    """Extract title and description from markdown content."""
    lines = content.strip().split('\n')
    
    title = ''
    desc = ''
    
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title = line[2:].strip()
            
            for j in range(i + 1, min(i + 10, len(lines))):
                next_line = lines[j].strip()
                
                if not next_line:
                    continue
                if next_line.startswith('---'):
                    continue
                
                # Italic line = description
                if next_line.startswith('*') and next_line.endswith('*') and not next_line.startswith('**'):
                    desc = next_line.strip('*').strip()
                    break
                
                # First paragraph = fallback
                if not next_line.startswith('#') and not next_line.startswith('-') and not next_line.startswith('<'):
                    desc = next_line
                    break
            
            break
    
    if len(desc) > MAX_DESC_LENGTH:
        desc = desc[:MAX_DESC_LENGTH - 3].rsplit(' ', 1)[0] + '...'
    
    return title, desc


def get_section_files(docs_root: Path, section: str) -> list[Path]:
    """Get all markdown files in a section directory, sorted."""
    section_dir = docs_root / section
    if not section_dir.exists():
        return []
    
    files = []
    for f in section_dir.glob('*.md'):
        if f.name == 'contents.md':
            continue
        files.append(f)
    
    # Sort: index.md first, then by filename
    def sort_key(f):
        if f.name == 'index.md':
            return ('0', '')
        return ('1', f.name)
    
    return sorted(files, key=sort_key)


def generate_contents_md(docs_root: Path, lang: str = 'en') -> str:
    """Generate contents.md by traversing file system."""
    label_key = 'label_de' if lang == 'de' else 'label'
    
    lines = ['# Contents', '']
    
    # Get sections sorted by order
    sorted_sections = sorted(SECTIONS.items(), key=lambda x: x[1]['order'])
    
    for section_id, section_meta in sorted_sections:
        files = get_section_files(docs_root, section_id)
        
        if not files:
            continue
        
        section_label = section_meta.get(label_key, section_meta['label'])
        
        lines.append(f'## {section_label} {{#{section_id}}}')
        lines.append('')
        lines.append('<ul class="toc-list">')
        
        for file_path in files:
            content = file_path.read_text(encoding='utf-8')
            title, desc = extract_metadata(content)
            
            if not title:
                # Fallback title from filename
                title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
                title = re.sub(r'^\d+\s*', '', title)
            
            # Convert to HTML path
            rel_path = file_path.relative_to(docs_root)
            html_path = str(rel_path.with_suffix('.html'))
            
            desc_html = f'<div class="description">{desc}</div>' if desc else '<div class="description"></div>'
            lines.append(f'<li><a href="{html_path}"><div class="title">{title}</div>{desc_html}</a></li>')
        
        lines.append('</ul>')
        lines.append('')
    
    return '\n'.join(lines)


def main():
    print("Generating contents.md from file tree...")
    
    # EN
    if DOCS_ROOT.exists():
        contents_en = generate_contents_md(DOCS_ROOT, 'en')
        output_path = DOCS_ROOT / 'contents.md'
        output_path.write_text(contents_en, encoding='utf-8')
        print(f"  Generated {output_path.relative_to(PROJECT_ROOT)}")
    
    # DE
    if DOCS_DE_ROOT.exists():
        contents_de = generate_contents_md(DOCS_DE_ROOT, 'de')
        output_path = DOCS_DE_ROOT / 'contents.md'
        output_path.write_text(contents_de, encoding='utf-8')
        print(f"  Generated {output_path.relative_to(PROJECT_ROOT)}")
    
    print("Done.")


if __name__ == '__main__':
    main()
