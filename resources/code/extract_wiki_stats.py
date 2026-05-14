#!/usr/bin/env python3
"""Extract per-domain stats from all wiki.html files for index page generation."""
import re, json
from pathlib import Path

KB_DIR = Path(r"C:\Users\Lyndon\Desktop\SW\一年级：2025-2026\Project：alignment\knowledge_base")

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_array(text, start_marker):
    """Extract a JS array from text starting after start_marker."""
    s = text.find(start_marker)
    if s == -1:
        return None
    s = text.find('[', s + len(start_marker))
    if s == -1:
        return None
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
        return None
    # Try to evaluate the JS array as JSON-like
    try:
        import json
        return json.loads(text[s:pos])
    except:
        return None

def extract_domain_stats(content):
    """Extract stats from wiki content."""
    # Domain title
    m = re.search(r'<div class="header-title">(.+?)</div>', content)
    title = m.group(1) if m else "Unknown"

    # Domain subtitle
    m = re.search(r'margin-top:0\.\d+rem[^>]*>(.+?)</div>', content)
    subtitle = m.group(1) if m else ""

    # Domain ID
    m = re.search(r"const DOMAIN_ID\s*=\s*'([^']+)'", content)
    domain_id = m.group(1) if m else ""

    # Extract PAPERS as raw text, then manually parse to count
    papers_text = ""
    paper_count = 0; must_count = 0; important_count = 0; ref_count = 0
    papers_start = content.find('const PAPERS = ')
    if papers_start != -1:
        s = content.find('[', papers_start + 14)
        if s != -1:
            depth = 1
            pos = s + 1
            in_string = False
            while pos < len(content) and depth > 0:
                ch = content[pos]
                if ch == '"' and (pos == 0 or content[pos-1] != '\\'):
                    in_string = not in_string
                if not in_string:
                    if ch == '[':
                        depth += 1
                    elif ch == ']':
                        depth -= 1
                pos += 1
            if depth == 0:
                papers_text = content[s:pos]
                # Count from extracted text
                paper_count = papers_text.count('id: "')
                must_count = papers_text.count('priority: "must"')
                important_count = papers_text.count('priority: "important"')
                ref_count = papers_text.count('priority: "ref"')

    # Extract NOTES
    notes_start = content.find('const NOTES = ')
    note_count = 0
    if notes_start != -1:
        s = content.find('[', notes_start + 14)
        if s != -1:
            depth = 1
            pos = s + 1
            in_string = False
            while pos < len(content) and depth > 0:
                ch = content[pos]
                if ch == '"' and (pos == 0 or content[pos-1] != '\\'):
                    in_string = not in_string
                if not in_string:
                    if ch == '[':
                        depth += 1
                    elif ch == ']':
                        depth -= 1
                pos += 1
            if depth == 0:
                note_count = content[s:pos].count('paper_id: "')

    # Extract tags
    tags = set()
    if paper_count > 0:
        # Find all "tags": [...] patterns
        tag_pattern = re.finditer(r'tags:\s*\[(.*?)\]', papers_text)
        for m in tag_pattern:
            tag_text = m.group(1)
            tag_items = re.findall(r'"([^"]*)"', tag_text)
            tags.update(tag_items)

    return {
        'title': title,
        'subtitle': subtitle,
        'domain_id': domain_id,
        'paper_count': paper_count,
        'must_count': must_count,
        'important_count': important_count,
        'ref_count': ref_count,
        'note_count': note_count,
        'tags': sorted(tags)[:10],
    }

def main():
    seen = set()
    all_domains = []
    for d in sorted(KB_DIR.iterdir()):
        if d.is_dir() and re.match(r'^\d{2}_', d.name) and d.name not in seen:
            seen.add(d.name)
            all_domains.append(d)

    results = {}
    for domain in all_domains:
        wiki_path = domain / "wiki.html"
        if not wiki_path.exists():
            print(f"⚠ No wiki.html in {domain.name}")
            continue
        content = read_file(wiki_path)
        stats = extract_domain_stats(content)
        results[domain.name] = stats
        print(f"{domain.name}:")
        print(f"  Title: {stats['title']}")
        print(f"  Papers: {stats['paper_count']} (must: {stats['must_count']}, important: {stats['important_count']}, ref: {stats['ref_count']})")
        print(f"  Notes: {stats['note_count']}")
        print(f"  Tags: {', '.join(stats['tags'][:8])}")
        print()

    print("=" * 50)
    total_papers = sum(s['paper_count'] for s in results.values())
    total_notes = sum(s['note_count'] for s in results.values())
    total_must = sum(s['must_count'] for s in results.values())
    total_important = sum(s['important_count'] for s in results.values())
    total_ref = sum(s['ref_count'] for s in results.values())
    print(f"TOTAL: {total_papers} papers, {total_notes} notes")
    print(f"  Must: {total_must}, Important: {total_important}, Ref: {total_ref}")

    # Save as JSON for the index generator
    output = {
        'domains': results,
        'totals': {
            'papers': total_papers,
            'notes': total_notes,
            'must': total_must,
            'important': total_important,
            'ref': total_ref,
            'domains': len(results)
        }
    }

    out_path = Path(__file__).parent.parent.parent / 'knowledge_base' / '_stats.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved stats to {out_path}")

if __name__ == '__main__':
    main()
