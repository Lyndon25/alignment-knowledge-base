#!/usr/bin/env python3
"""
Regenerate all domain wikis from the updated template.
Extracts data from existing wikis and injects into the new template.
"""
import re, os, sys
from pathlib import Path

KB_DIR = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\knowledge_base")
TEMPLATE = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\resources\templates\wiki_template.html")

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ Written: {path.name}")

def extract_array(text, start_marker, start_pos=0):
    """
    Extract a JS array from text starting after start_marker.
    Returns (full_array_text_including_brackets, end_pos_after_closing_semicolon).

    Example: for `const PAPERS = [{...}];`, extracts `[{...}]` as the array text.
    """
    s = text.find(start_marker, start_pos)
    if s == -1:
        return None, -1
    s = text.find('[', s + len(start_marker))
    if s == -1:
        return None, -1

    # Bracket count from the opening [
    depth = 1
    pos = s + 1
    in_string = False
    while pos < len(text) and depth > 0:
        ch = text[pos]
        if ch == '"' and (pos == 0 or text[pos-1] != '\\'):
            in_string = not in_string
        if not in_string:
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
        pos += 1

    if depth != 0:
        return None, -1

    # text[s:pos] is the full array including [ ... ]
    array_text = text[s:pos]

    # Find ]; or ; after the array
    end_pos = text.find('];', pos)
    if end_pos == -1:
        end_pos = text.find(';', pos)
    if end_pos == -1:
        end_pos = pos
    else:
        end_pos += 2  # include ];

    return array_text, end_pos

def extract_wiki_data(filepath):
    """Extract all data from an existing wiki file."""
    content = read_file(filepath)
    dirname = filepath.parent.name

    # Domain name = directory name
    domain_name = dirname

    # Domain title
    m = re.search(r'<div class="header-title">(.+?)</div>', content)
    domain_title = m.group(1) if m else dirname

    # Domain subtitle - flexible regex for various inline styles
    m = re.search(r'margin-top:0\.\d+rem"[^>]*>(.+?)</div>', content)
    domain_subtitle = m.group(1) if m else ""

    # Domain ID
    m = re.search(r"const DOMAIN_ID\s*=\s*'([^']+)'", content)
    domain_id = m.group(1) if m else dirname

    # PAPERS array (full text including [])
    papers_data, end_pos = extract_array(content, 'const PAPERS = ')
    if papers_data is None:
        print(f"  ⚠ Could not extract PAPERS from {filepath.name}")
        papers_data = ""

    # NOTES array (full text including brackets). Search from start to avoid off-by-one after PAPERS extraction.
    notes_data, _ = extract_array(content, 'const NOTES = ', 0)
    if notes_data is None:
        notes_data = ""

    return {
        'domain_name': domain_name,
        'domain_title': domain_title,
        'domain_subtitle': domain_subtitle,
        'domain_id': domain_id,
        'papers_data': papers_data,
        'notes_data': notes_data,
    }

def generate_wiki(data, template_path):
    """Generate wiki HTML from template and data."""
    template = read_file(template_path)

    result = template.replace('__DOMAIN_NAME__', data['domain_name'])
    result = result.replace('__DOMAIN_TITLE__', data['domain_title'])
    result = result.replace('__DOMAIN_SUBTITLE__', data['domain_subtitle'])
    result = result.replace('__DOMAIN_ID__', data['domain_id'])
    result = result.replace('__PAPERS_DATA__', data['papers_data'])
    result = result.replace('__NOTES_DATA__', data['notes_data'])

    return result

def main():
    # All domain directories sorted (avoid duplicates)
    seen = set()
    all_domains = []
    for d in sorted(KB_DIR.iterdir()):
        if d.is_dir() and re.match(r'^\d{2}_', d.name) and d.name not in seen:
            seen.add(d.name)
            all_domains.append(d)

    print(f"Found {len(all_domains)} domain wikis to process")
    print()

    for domain in all_domains:
        wiki_path = domain / "wiki.html"
        if not wiki_path.exists():
            print(f"  ⚠ No wiki.html in {domain.name}, skipping")
            continue

        print(f"Processing: {domain.name}")
        data = extract_wiki_data(wiki_path)
        print(f"  Title: {data['domain_title']}")
        print(f"  Papers: {len(data['papers_data'])} chars, Notes: {len(data['notes_data'])} chars")

        new_html = generate_wiki(data, TEMPLATE)
        write_file(wiki_path, new_html)
        print()

if __name__ == '__main__':
    main()
