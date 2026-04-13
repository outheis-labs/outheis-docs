#!/usr/bin/env python3
"""
Validate documentation structure.

This script:
1. Finds all markdown files in docs/
2. Checks they are listed in generate-contents.py STRUCTURE
3. Checks all links in contents.md are valid
4. Reports missing files and broken links

Run after any content changes to ensure consistency.
"""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_ROOT = PROJECT_ROOT / 'docs'
DOCS_DE_ROOT = PROJECT_ROOT / 'docs-de'
HTML_ROOT = PROJECT_ROOT / 'html'

# Import STRUCTURE from generate-contents.py
sys.path.insert(0, str(SCRIPT_DIR))
from importlib import import_module

def get_structure():
    """Import STRUCTURE from generate-contents.py"""
    spec = import_module('generate-contents')
    return spec.STRUCTURE

def find_all_md_files(docs_root: Path) -> set:
    """Find all markdown files in docs directory."""
    files = set()
    for f in docs_root.rglob('*.md'):
        rel = str(f.relative_to(docs_root))
        # Skip contents.md (generated)
        if rel == 'contents.md':
            continue
        files.add(rel)
    return files

def get_structure_files() -> set:
    """Get all files listed in STRUCTURE."""
    try:
        # Can't import directly due to hyphen, read and parse
        contents_py = SCRIPT_DIR / 'generate-contents.py'
        content = contents_py.read_text()
        
        # Extract file paths from STRUCTURE
        files = set()
        for match in re.finditer(r'"([^"]+\.md)"', content):
            files.add(match.group(1))
        return files
    except Exception as e:
        print(f"Error reading STRUCTURE: {e}")
        return set()

def check_html_exists(docs_root: Path, html_root: Path) -> list:
    """Check that HTML files exist for all md files."""
    errors = []
    for md_file in docs_root.rglob('*.md'):
        if md_file.name == 'contents.md':
            continue
        rel = md_file.relative_to(docs_root)
        html_file = html_root / rel.with_suffix('.html')
        if not html_file.exists():
            errors.append(f"Missing HTML: {html_file.relative_to(PROJECT_ROOT)}")
    return errors

def check_contents_links(docs_root: Path) -> list:
    """Check all links in contents.md are valid."""
    errors = []
    contents_file = docs_root / 'contents.md'
    if not contents_file.exists():
        return [f"Missing: {contents_file.relative_to(PROJECT_ROOT)}"]
    
    content = contents_file.read_text()
    
    # Find all href links
    for match in re.finditer(r'href="([^"]+)"', content):
        href = match.group(1)
        # Skip external links
        if href.startswith('http'):
            continue
        # Skip anchor-only links
        if href.startswith('#'):
            continue
        
        # Convert .html to .md for checking
        md_path = href.replace('.html', '.md')
        # Remove anchor
        md_path = md_path.split('#')[0]
        
        full_path = docs_root / md_path
        if not full_path.exists():
            errors.append(f"Broken link in contents.md: {href}")
    
    return errors

def main():
    print("Validating documentation structure...\n")
    
    errors = []
    warnings = []
    
    # Get files from STRUCTURE
    structure_files = get_structure_files()
    
    # Check EN docs
    print("Checking docs/ ...")
    md_files = find_all_md_files(DOCS_ROOT)
    
    # Files in docs but not in STRUCTURE
    missing_from_structure = md_files - structure_files
    for f in sorted(missing_from_structure):
        warnings.append(f"Not in STRUCTURE: docs/{f}")
    
    # Files in STRUCTURE but not in docs
    missing_from_docs = structure_files - md_files
    for f in sorted(missing_from_docs):
        if not f.startswith('docs-de/'):  # Skip DE files
            errors.append(f"In STRUCTURE but missing: docs/{f}")
    
    # Check HTML exists
    html_errors = check_html_exists(DOCS_ROOT, HTML_ROOT)
    errors.extend(html_errors)
    
    # Check contents.md links
    link_errors = check_contents_links(DOCS_ROOT)
    errors.extend(link_errors)
    
    # Check DE docs
    print("Checking docs-de/ ...")
    if DOCS_DE_ROOT.exists():
        de_md_files = find_all_md_files(DOCS_DE_ROOT)
        de_html_root = HTML_ROOT / 'de'
        
        html_errors = check_html_exists(DOCS_DE_ROOT, de_html_root)
        errors.extend(html_errors)
        
        link_errors = check_contents_links(DOCS_DE_ROOT)
        errors.extend(link_errors)
    
    # Report
    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")
        print()
    
    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        print()
        print(f"Found {len(errors)} error(s) and {len(warnings)} warning(s)")
        sys.exit(1)
    else:
        print(f"✓ All checks passed ({len(warnings)} warning(s))")
        sys.exit(0)

if __name__ == '__main__':
    main()
