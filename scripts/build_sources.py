#!/usr/bin/env python3
"""
Build Pico900 Sources pages from JSON data.

Generates:
1. sources/index.html - Landing page with filterable source cards
2. sources/{source-id}/index.html - Detail page for each source

Usage:
    python scripts/build_sources.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_sources():
    """Load sources.json from data directory."""
    sources_path = Path('data/sources.json')
    if not sources_path.exists():
        print(f"ERROR: {sources_path} not found")
        sys.exit(1)

    with open(sources_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_sources_index(sources_data):
    """Build the main sources landing page."""
    template_path = Path('src/templates/sources.html')
    if not template_path.exists():
        print(f"ERROR: {template_path} not found")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace placeholder with actual JSON
    sources_json = json.dumps(sources_data)
    html = html.replace('{SOURCES_JSON_PLACEHOLDER}', sources_json)

    # Ensure output directory exists
    output_dir = Path('site/sources')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write index.html
    output_file = output_dir / 'index.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] Built {output_file}")

def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

def build_source_details(sources_data):
    """Build individual detail pages for each source."""
    template_path = Path('src/templates/source_detail.html')
    if not template_path.exists():
        print(f"ERROR: {template_path} not found")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    output_base = Path('site/sources')

    # Build mapping of source IDs to their tradition
    source_to_tradition = {}
    for tradition in sources_data['traditions']:
        for source in tradition['sources']:
            source_to_tradition[source['id']] = tradition

    # Generate detail page for each source
    total = 0
    for tradition in sources_data['traditions']:
        for source in tradition['sources']:
            html = template

            # Basic info
            html = html.replace('{SOURCE_NAME}', escape_html(source['name']))
            html = html.replace('{WORK_TITLE}', escape_html(source['work']))
            html = html.replace('{DATES}', escape_html(source['dates']))
            html = html.replace('{BLURB}', escape_html(source['blurb']))
            html = html.replace('{TRADITION_LABEL}', escape_html(tradition['label']))
            html = html.replace('{TRADITION_COLOR}', tradition['color'])
            html = html.replace('{PRIORITY}', escape_html(source['priority']))
            html = html.replace('{CONCLUSIONS_LINKED}', str(source['conclusions_linked']))
            html = html.replace('{SCHOLARS_COUNT}', str(len(source['scholars'])))

            # Relevance items
            relevance_html = ''
            for item in source['relevance'].split(', '):
                relevance_html += f'<li>{escape_html(item.strip())}</li>\n                '
            html = html.replace('{RELEVANCE_ITEMS}', relevance_html.rstrip())

            # Scholars badges
            scholars_html = ''
            for scholar in source['scholars']:
                scholars_html += f'<span class="scholar-badge">{escape_html(scholar)}</span>\n                '
            html = html.replace('{SCHOLARS_BADGES}', scholars_html.rstrip())

            # Conclusion links - placeholder for now (would need conclusions data to populate)
            html = html.replace('{CONCLUSION_LINKS}',
                f'<span style="font-size: 0.9rem; color: #999;">{source["conclusions_linked"]} conclusions linked</span>')

            # Related sources from same tradition
            related_html = ''
            for other_source in tradition['sources']:
                if other_source['id'] != source['id']:
                    priority_class = f"priority-{other_source['priority']}"
                    related_html += f'''<div class="related-card" onclick="window.location.href='/Pico900/sources/{escape_html(other_source['id'])}/'; return false;">
                        <div class="related-card-name">{escape_html(other_source['name'])}</div>
                        <div class="related-card-work">{escape_html(other_source['work'])}</div>
                        <span class="priority-badge {priority_class}">{escape_html(other_source['priority'])}</span>
                    </div>
                    '''
            if not related_html:
                related_html = '<p style="color: #999; font-size: 0.9rem;">No other sources in this tradition.</p>'
            html = html.replace('{RELATED_SOURCES}', related_html)

            # Create output directory for this source
            source_dir = output_base / source['id']
            source_dir.mkdir(parents=True, exist_ok=True)

            # Write detail page
            output_file = source_dir / 'index.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)

            total += 1

    print(f"[OK] Built {total} source detail pages")

def main():
    """Main build process."""
    print("Building Pico900 Sources pages...")

    sources_data = load_sources()

    build_sources_index(sources_data)
    build_source_details(sources_data)

    print("\n[OK] Sources pages built successfully!")
    print(f"  - Landing page: site/sources/index.html")
    print(f"  - Detail pages: site/sources/{{source-id}}/index.html")

if __name__ == '__main__':
    main()
