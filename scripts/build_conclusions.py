#!/usr/bin/env python3
"""
T-SITE-06: Generate thesis explorer and detail pages from thesis_cards_data.json.

Generates:
- site/conclusions/index.html (thesis explorer with filtering, search, relevance bars)
- site/conclusions/{thesis_id}/index.html (detail pages for each thesis, 900 pages)

Reads from:
- data/thesis_cards_data.json (all 900 theses with person relevance)
- data/inventory/theses.json (full thesis metadata for detail pages)
- entries/*.json (verified thesis content, if available)

Usage:
    python scripts/build_conclusions.py
"""

import json
import os
from pathlib import Path
from urllib.parse import quote

BASE = os.environ.get("PICO_BASE_PATH", "/Pico900").rstrip("/")

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

def load_json(path):
    """Load JSON file safely."""
    if not os.path.exists(path):
        return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def build_explorer():
    """Build site/conclusions/index.html with interactive explorer."""
    data = load_json('data/thesis_cards_data.json')
    if not data:
        print("ERROR: data/thesis_cards_data.json not found")
        return

    theses = data['theses']
    persons = list(set(p['person_id'] for t in theses for p in t.get('person_relevance', [])))
    sections = list(set(t['section_name'] for t in theses if t.get('section_name')))

    # Build relevance bar legend
    legend_html = '<div class="relevance-legend">'
    for person_id in sorted(persons)[:10]:
        color = data['person_colors'].get(person_id, '#999999')
        legend_html += f'<div class="legend-item"><div class="color-box" style="background-color: {color};"></div>{person_id}</div>'
    legend_html += '</div>'

    # Build explorer HTML
    explorer_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Conclusions Explorer - Pico900</title>
    <link rel="stylesheet" href="{BASE}/css/style.css">
    <style>
        .explorer-controls {{
            display: flex;
            gap: 1em;
            margin-bottom: 2em;
            flex-wrap: wrap;
        }}
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5em;
        }}
        .filter-group label {{
            font-weight: bold;
            font-size: 0.9em;
        }}
        .filter-group input, .filter-group select {{
            padding: 0.5em;
            border: 1px solid #ccc;
            border-radius: 4px;
        }}
        .thesis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 1.5em;
        }}
        .thesis-card {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1em;
            background: #f9f9f9;
        }}
        .thesis-card:hover {{
            border-color: #8B4513;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .thesis-id {{
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5em;
        }}
        .thesis-latin {{
            font-size: 0.9em;
            color: #555;
            font-style: italic;
            margin-bottom: 1em;
        }}
        .thesis-link {{
            display: inline-block;
            margin-top: 0.5em;
            padding: 0.5em 1em;
            background: #8B4513;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }}
        .thesis-link:hover {{
            background: #A0522D;
        }}
        .relevance-bars {{
            margin-top: 1em;
            border-top: 1px solid #ddd;
            padding-top: 1em;
        }}
        .relevance-bar {{
            display: grid;
            grid-template-columns: 120px 1fr 50px;
            gap: 0.5em;
            align-items: center;
            margin-bottom: 0.5em;
            font-size: 0.85em;
        }}
        .bar-container {{
            height: 12px;
            background: #e0e0e0;
            border-radius: 2px;
            overflow: hidden;
        }}
        .bar {{
            height: 100%;
            transition: width 0.2s;
        }}
        .relevance-legend {{
            display: flex;
            gap: 1em;
            flex-wrap: wrap;
            margin-bottom: 2em;
            font-size: 0.85em;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.3em;
        }}
        .color-box {{
            width: 16px;
            height: 16px;
            border-radius: 2px;
        }}
    </style>
</head>
<body>
    <header class="top">
        <a class="brand" href="{BASE}/">Pico della Mirandola, <em>Conclusiones</em> (1486)</a>
        <a href="{BASE}/sections/">Sections</a>
        <a href="{BASE}/condemned/">The thirteen condemned</a>
        <a href="{BASE}/sources/">Sources</a>
        <a href="{BASE}/conclusions/">Conclusions</a>
        <a href="{BASE}/scholarship/">Scholarship</a>
        <a href="{BASE}/about/">Method</a>
    </header>
    <main>
        <h1>Thesis Explorer</h1>
        <p>Browse all 900 conclusions with person relevance from scholarly mentions and verified claims.</p>

        <div class="explorer-controls">
            <div class="filter-group">
                <label for="section-filter">Section</label>
                <select id="section-filter">
                    <option value="">All sections</option>
'''

    for section in sorted(sections):
        explorer_html += f'                    <option value="{escape_html(section)}">{escape_html(section)}</option>\n'

    explorer_html += f'''                </select>
            </div>
            <div class="filter-group">
                <label for="search-input">Search</label>
                <input type="text" id="search-input" placeholder="Thesis ID or Latin text">
            </div>
        </div>

        <h3>Person Relevance</h3>
        {legend_html}

        <div class="thesis-grid" id="thesis-grid">
            <!-- Cards generated by JavaScript -->
        </div>
    </main>
    <footer>
        A digital edition in preparation. <span class="badge">explorer prototype</span>
    </footer>

    <script>
        const theses = {json.dumps(theses, ensure_ascii=False)};
        const colors = {json.dumps(data['person_colors'], ensure_ascii=False)};

        function renderCards(filtered) {{
            const grid = document.getElementById('thesis-grid');
            grid.innerHTML = '';

            for (const thesis of filtered) {{
                const card = document.createElement('div');
                card.className = 'thesis-card';

                let barsHtml = '';
                if (thesis.person_relevance && thesis.person_relevance.length > 0) {{
                    barsHtml = '<div class="relevance-bars">';
                    for (const person of thesis.person_relevance.slice(0, 5)) {{
                        const color = colors[person.person_id] || '#999999';
                        const width = Math.min(person.score * 10, 100);
                        barsHtml += `
                            <div class="relevance-bar">
                                <div class="person-label">${{escapeHtml(person.name)}}</div>
                                <div class="bar-container">
                                    <div class="bar" style="width: ${{width}}%; background-color: ${{color}};"></div>
                                </div>
                                <div class="bar-score">${{person.score.toFixed(1)}}</div>
                            </div>
                        `;
                    }}
                    barsHtml += '</div>';
                }}

                card.innerHTML = `
                    <div class="thesis-id">${{escapeHtml(thesis.thesis_id)}}</div>
                    <div class="thesis-latin">${{escapeHtml(thesis.latin.substring(0, 150))}}...</div>
                    ${{barsHtml}}
                    <a href="{BASE}/conclusions/${{encodeURIComponent(thesis.thesis_id)}}/" class="thesis-link">Read full thesis</a>
                `;
                grid.appendChild(card);
            }}
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        function filter() {{
            const section = document.getElementById('section-filter').value;
            const search = document.getElementById('search-input').value.toLowerCase();

            const filtered = theses.filter(t => {{
                if (section && t.section_name !== section) return false;
                if (search && !t.thesis_id.toLowerCase().includes(search) && !t.latin.toLowerCase().includes(search)) return false;
                return true;
            }});

            renderCards(filtered);
        }}

        document.getElementById('section-filter').addEventListener('change', filter);
        document.getElementById('search-input').addEventListener('input', filter);

        // Initial render
        renderCards(theses);
    </script>
</body>
</html>
'''

    # Write explorer page
    out_dir = Path('site/conclusions')
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(explorer_html)

    print(f"[OK] Generated site/conclusions/index.html (explorer with {len(theses)} theses)")

    return len(theses)

def build_detail_pages():
    """Generate detail pages for each thesis."""
    cards_data = load_json('data/thesis_cards_data.json')
    theses_data = load_json('data/inventory/theses.json')

    if not cards_data or not theses_data:
        print("ERROR: Missing thesis data")
        return 0

    theses_by_id = {t['thesis_id']: t for t in theses_data['theses']}
    out_dir = Path('site/conclusions')
    out_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for thesis in cards_data['theses']:
        thesis_id = thesis['thesis_id']
        full_thesis = theses_by_id.get(thesis_id, {})

        # Build relevance bars
        bars_html = ''
        if thesis.get('person_relevance'):
            bars_html = '<div class="relevance-section"><h3>Person Relevance</h3>'
            for person in thesis['person_relevance'][:5]:
                color = cards_data['person_colors'].get(person['person_id'], '#999999')
                width = min(person['score'] * 10, 100)
                bars_html += f'''
                <div class="relevance-bar">
                    <div class="person-label">{escape_html(person["name"])}</div>
                    <div class="bar-container">
                        <div class="bar" style="width: {width}%; background-color: {color};"></div>
                    </div>
                    <div class="bar-score">{person["score"]:.1f}</div>
                </div>
                '''
            bars_html += '</div>'

        # Build detail page
        detail_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Thesis {escape_html(thesis_id)} - Pico900</title>
    <link rel="stylesheet" href="{BASE}/css/style.css">
    <style>
        .thesis-detail {{
            max-width: 900px;
            margin: 0 auto;
        }}
        .thesis-header {{
            border-bottom: 2px solid #8B4513;
            padding-bottom: 1em;
            margin-bottom: 2em;
        }}
        .thesis-id {{
            font-size: 1.2em;
            font-weight: bold;
            color: #8B4513;
            margin-bottom: 0.5em;
        }}
        .thesis-section {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 1em;
        }}
        .thesis-latin {{
            font-size: 1.1em;
            font-style: italic;
            background: #f9f9f9;
            padding: 1em;
            border-left: 4px solid #8B4513;
            margin: 1em 0;
            line-height: 1.6;
        }}
        .relevance-section {{
            background: #f5f5f5;
            padding: 1em;
            border-radius: 8px;
            margin: 2em 0;
        }}
        .relevance-section h3 {{
            margin-top: 0;
        }}
        .relevance-bar {{
            display: grid;
            grid-template-columns: 150px 1fr 60px;
            gap: 0.5em;
            align-items: center;
            margin-bottom: 0.8em;
        }}
        .bar-container {{
            height: 16px;
            background: #e0e0e0;
            border-radius: 2px;
            overflow: hidden;
        }}
        .bar {{
            height: 100%;
        }}
        .nav-links {{
            display: flex;
            gap: 1em;
            margin-top: 2em;
            justify-content: space-between;
        }}
        .nav-links a {{
            padding: 0.5em 1em;
            background: #8B4513;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }}
        .nav-links a:hover {{
            background: #A0522D;
        }}
    </style>
</head>
<body>
    <header class="top">
        <a class="brand" href="{BASE}/">Pico della Mirandola, <em>Conclusiones</em> (1486)</a>
        <a href="{BASE}/sections/">Sections</a>
        <a href="{BASE}/condemned/">The thirteen condemned</a>
        <a href="{BASE}/sources/">Sources</a>
        <a href="{BASE}/conclusions/">Conclusions</a>
        <a href="{BASE}/scholarship/">Scholarship</a>
        <a href="{BASE}/about/">Method</a>
    </header>
    <main class="thesis-detail">
        <div class="thesis-header">
            <div class="thesis-id">{escape_html(thesis_id)}</div>
            <div class="thesis-section">{escape_html(thesis.get("section_name", ""))}</div>
        </div>

        <h2>Latin Text</h2>
        <div class="thesis-latin">
            {escape_html(full_thesis.get("latin", thesis.get("latin", "")))}
        </div>

        {bars_html}

        <div class="nav-links">
            <a href="{BASE}/conclusions/">← Back to explorer</a>
            <a href="{BASE}/sections/">Browse sections →</a>
        </div>
    </main>
    <footer>
        A digital edition in preparation.
    </footer>
</body>
</html>
'''

        # Create thesis detail directory
        thesis_dir = out_dir / quote(thesis_id.replace('/', '_'), safe='')
        thesis_dir.mkdir(parents=True, exist_ok=True)

        with open(thesis_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(detail_html)

        count += 1

    print(f"[OK] Generated {count} thesis detail pages in site/conclusions/*/")
    return count

def main():
    print("T-SITE-06: Building thesis explorer and detail pages...")

    explorer_count = build_explorer()
    detail_count = build_detail_pages()

    print(f"\n[OK] Thesis cards site built!")
    print(f"  - Explorer: site/conclusions/index.html")
    print(f"  - Detail pages: {detail_count} thesis pages")
    print(f"  - Total: {explorer_count} theses with interactive filtering")

if __name__ == '__main__':
    main()
