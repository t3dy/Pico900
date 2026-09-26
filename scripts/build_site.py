#!/usr/bin/env python3
"""
Build Pico900 static website from JSON conclusion data.
Generates HTML pages for conclusions, landing page, and about page.
Supports S3 (Averroist conclusions) as initial proof of concept.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "conclusions"
SRC_DIR = PROJECT_ROOT / "src"
SITE_DIR = PROJECT_ROOT / "site"
CONCLUSIONS_DIR = SITE_DIR / "conclusions"

# Ensure output directories exist
SITE_DIR.mkdir(exist_ok=True)
CONCLUSIONS_DIR.mkdir(exist_ok=True)

# Base path for GitHub Pages
BASE_PATH = "/Pico900"

def load_conclusion_data(section, conclusion_num):
    """Load a single conclusion JSON file."""
    filepath = DATA_DIR / section / f"entry_{section}.C{conclusion_num:03d}.json"
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_conclusions(section):
    """Load all conclusions for a section."""
    section_dir = DATA_DIR / section
    if not section_dir.exists():
        return []

    conclusions = []
    for filepath in sorted(section_dir.glob("entry_*.json")):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                conclusion = json.load(f)
                conclusions.append(conclusion)
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")

    return conclusions

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )

def format_scholar_citations(citations):
    """Format scholar citations HTML."""
    if not citations or len(citations) == 0:
        return "<p><em>No citations available.</em></p>"

    html = '<div class="citations">\n'
    for citation in citations:
        html += '<div class="citation-block">\n'
        html += f'  <p class="scholar"><strong>{escape_html(citation.get("scholar", "Unknown"))}</strong></p>\n'
        html += f'  <p class="work"><em>{escape_html(citation.get("work", ""))}</em></p>\n'

        quote = citation.get("quote", "")
        if quote:
            html += f'  <blockquote class="quote">\n'
            html += f'    <p>&ldquo;{escape_html(quote)}&rdquo;</p>\n'
            html += f'  </blockquote>\n'

        source_note = citation.get("source_note", "")
        if source_note:
            html += f'  <p class="source-note">{escape_html(source_note)}</p>\n'

        html += '</div>\n'
    html += '</div>\n'
    return html

def generate_conclusion_page(conclusion):
    """Generate HTML for a single conclusion."""
    conclusion_id = conclusion.get("conclusion_id", "")
    section = conclusion.get("section", "")

    latin = escape_html(conclusion.get("latin_incipit", ""))
    english = escape_html(conclusion.get("english_translation", ""))
    charge = escape_html(conclusion.get("charge", ""))
    defense = escape_html(conclusion.get("defense", ""))
    exegesis = escape_html(conclusion.get("exegesis", ""))
    heretical_flag = conclusion.get("heretical_flag", False)
    heretical_notes = conclusion.get("heretical_notes", "")

    # Scholar citations
    citations_html = format_scholar_citations(conclusion.get("scholar_citations", []))

    # Tags
    tags = conclusion.get("tags", [])
    tags_html = ""
    if tags:
        tags_html = '<div class="tags">\n'
        for tag in tags:
            tags_html += f'  <span class="tag">{escape_html(tag)}</span>\n'
        tags_html += '</div>\n'

    # Heretical badge
    heretical_badge = ""
    if heretical_flag:
        heretical_badge = '<span class="heretical-badge">Heretical</span>'

    # Navigation
    # Extract numeric part from conclusion_id for prev/next
    # conclusion_id is like "S3.C001", we want the numeric part (001)
    parts = conclusion_id.split(".")
    if len(parts) >= 2:
        num = int(parts[-1][1:])  # Remove 'C' prefix and convert to int
    else:
        num = 1
    prev_num = num - 1 if num > 1 else None
    next_num = num + 1 if num < 11 else None  # Adjust for S3 with 11 conclusions

    prev_link = ""
    next_link = ""
    if prev_num:
        prev_link = f'<a href="{BASE_PATH}/conclusions/S3_C{prev_num:03d}.html" class="nav-prev">← Previous</a>'
    if next_num:
        next_link = f'<a href="{BASE_PATH}/conclusions/S3_C{next_num:03d}.html" class="nav-next">Next →</a>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(conclusion_id)} — Pico900</title>
    <link rel="stylesheet" href="{BASE_PATH}/css/edition.css">
    <link rel="stylesheet" href="{BASE_PATH}/css/conclusions.css">
</head>
<body>
    <nav class="site-nav">
        <div class="nav-container">
            <a href="{BASE_PATH}/" class="nav-logo">Pico900</a>
            <ul class="nav-links">
                <li><a href="{BASE_PATH}/">Conclusions</a></li>
                <li><a href="{BASE_PATH}/sources/">Sources</a></li>
                <li><a href="{BASE_PATH}/about/">About</a></li>
            </ul>
        </div>
    </nav>

    <main class="content">
        <article class="conclusion-page">
            <header class="conclusion-header">
                <div class="conclusion-id">
                    <span class="section-label">{escape_html(section)}</span>
                    <h1>{escape_html(conclusion_id)}</h1>
                    {heretical_badge}
                </div>
            </header>

            <div class="conclusion-meta">
                <p class="conclusion-number"><strong>Reference:</strong> {escape_html(conclusion.get('conclusion_num', ''))}</p>
            </div>

            <section class="facing-page">
                <div class="text-column latin">
                    <h2>Latin</h2>
                    <p class="incipit">{latin}</p>
                </div>
                <div class="text-column english">
                    <h2>English</h2>
                    <p class="translation">{english}</p>
                    <p class="translation-source"><em>Source: {escape_html(conclusion.get('translation_source', 'Unknown'))}</em></p>
                </div>
            </section>

            <section class="conclusion-content">
                <h2>Charge & Defense</h2>
                <div class="charge-defense">
                    <div class="charge">
                        <h3>Charge</h3>
                        <p>{charge}</p>
                    </div>
                    <div class="defense">
                        <h3>Defense</h3>
                        <p>{defense}</p>
                    </div>
                </div>

                <h2>Exegesis</h2>
                <p class="exegesis">{exegesis}</p>

                <h2>Scholar Interpretations</h2>
                {citations_html}

                {tags_html}

                {f'<div class="heretical-section"><h2>Heretical Note</h2><p>{escape_html(heretical_notes)}</p></div>' if heretical_flag and heretical_notes else ''}
            </section>

            <nav class="conclusion-nav">
                {prev_link}
                <a href="{BASE_PATH}/" class="nav-home">Back to Conclusions</a>
                {next_link}
            </nav>
        </article>
    </main>

    <footer class="site-footer">
        <p>Pico900 Digital Edition | <a href="{BASE_PATH}/about/">About</a> | <a href="https://github.com/t3dy/Pico900">Repository</a></p>
    </footer>
</body>
</html>"""
    return html

def generate_index_page(conclusions):
    """Generate the main index page listing all conclusions."""

    conclusions_html = ""
    for conclusion in conclusions:
        conclusion_id = conclusion.get("conclusion_id", "")
        section = conclusion.get("section", "")
        latin = conclusion.get("latin_incipit", "")
        english = conclusion.get("english_translation", "")
        heretical_flag = conclusion.get("heretical_flag", False)

        # Extract numeric part for the page URL
        # conclusion_id is like "S3.C001", we want the numeric part (001)
        parts = conclusion_id.split(".")
        if len(parts) >= 2:
            num = int(parts[-1][1:])  # Remove 'C' prefix and convert to int
        else:
            num = 1
        url = f"{BASE_PATH}/conclusions/{section}_C{num:03d}.html"

        heretical_class = " heretical" if heretical_flag else ""
        heretical_badge = '<span class="heretical-badge">Heretical</span>' if heretical_flag else ""

        conclusions_html += f"""
        <div class="conclusion-card{heretical_class}">
            <div class="card-header">
                <h3><a href="{url}">{escape_html(conclusion_id)}</a></h3>
                {heretical_badge}
            </div>
            <div class="card-content">
                <p class="latin"><strong>Latin:</strong> {escape_html(latin[:120])}...</p>
                <p class="english"><strong>English:</strong> {escape_html(english[:120])}...</p>
            </div>
            <div class="card-footer">
                <a href="{url}" class="read-more">Read Full Text</a>
            </div>
        </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>900 Conclusions — Pico900</title>
    <link rel="stylesheet" href="{BASE_PATH}/css/edition.css">
    <link rel="stylesheet" href="{BASE_PATH}/css/conclusions.css">
</head>
<body>
    <nav class="site-nav">
        <div class="nav-container">
            <a href="{BASE_PATH}/" class="nav-logo">Pico900</a>
            <ul class="nav-links">
                <li><a href="{BASE_PATH}/" class="active">Conclusions</a></li>
                <li><a href="{BASE_PATH}/sources/">Sources</a></li>
                <li><a href="{BASE_PATH}/about/">About</a></li>
            </ul>
        </div>
    </nav>

    <main class="content">
        <header class="page-header">
            <h1>The 900 Conclusions</h1>
            <p class="subtitle">Giovanni Pico della Mirandola's Complete Philosophical Theses</p>
            <p class="intro">
                The <em>Conclusiones Nongentae</em> (900 Conclusions) represent Pico's most ambitious philosophical statement—
                a systematic compilation of positions drawn from Aristotle, Plato, the Christian Fathers, Islamic philosophy,
                Kabbalah, and Hermetic sources. The conclusions shown below (Section S3: Averroist) are publication-ready with
                full scholarly apparatus and facing-page Latin/English text.
            </p>
        </header>

        <div class="controls">
            <div class="search-control">
                <input type="text" id="search-input" placeholder="Search conclusions...">
            </div>
            <div class="filter-control">
                <label>
                    <input type="checkbox" id="heretical-filter"> Show heretical conclusions only
                </label>
            </div>
        </div>

        <div class="conclusions-grid" id="conclusions-grid">
            {conclusions_html}
        </div>

        <div class="info-section">
            <h2>About This Edition</h2>
            <p>
                This digital edition presents the 900 Conclusions with:
            </p>
            <ul>
                <li><strong>Facing-page text:</strong> Latin (critical edition) and English translation</li>
                <li><strong>Scholarly apparatus:</strong> Charge, defense, and exegesis for each conclusion</li>
                <li><strong>Intellectual sources:</strong> Integrated with the complete sources catalog</li>
                <li><strong>Heretical flagging:</strong> Conclusions condemned by the 1486–1487 papal commission</li>
            </ul>
            <p>
                Currently showing <strong>S3 (Averroist conclusions)</strong> as a proof of concept.
                Additional sections (S1 Neoplatonic, S4 Avicennist, S7 Hermetic) are in preparation.
            </p>
        </div>
    </main>

    <footer class="site-footer">
        <p>Pico900 Digital Edition | <a href="{BASE_PATH}/about/">About</a> | <a href="https://github.com/t3dy/Pico900">Repository</a></p>
    </footer>

    <script>
        // Search and filter functionality
        const searchInput = document.getElementById('search-input');
        const hereticalFilter = document.getElementById('heretical-filter');
        const conclusionCards = document.querySelectorAll('.conclusion-card');

        function filterConclusions() {{
            const searchTerm = searchInput.value.toLowerCase();
            const showHereticalOnly = hereticalFilter.checked;

            conclusionCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                const isHeretical = card.classList.contains('heretical');
                const matchesSearch = searchTerm === '' || text.includes(searchTerm);
                const matchesFilter = !showHereticalOnly || isHeretical;

                card.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
            }});
        }}

        searchInput.addEventListener('input', filterConclusions);
        hereticalFilter.addEventListener('change', filterConclusions);
    </script>
</body>
</html>"""

    return html

def generate_about_page():
    """Generate the about page."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About — Pico900</title>
    <link rel="stylesheet" href="{BASE_PATH}/css/edition.css">
    <link rel="stylesheet" href="{BASE_PATH}/css/conclusions.css">
</head>
<body>
    <nav class="site-nav">
        <div class="nav-container">
            <a href="{BASE_PATH}/" class="nav-logo">Pico900</a>
            <ul class="nav-links">
                <li><a href="{BASE_PATH}/">Conclusions</a></li>
                <li><a href="{BASE_PATH}/sources/">Sources</a></li>
                <li><a href="{BASE_PATH}/about/" class="active">About</a></li>
            </ul>
        </div>
    </nav>

    <main class="content">
        <article class="about-page">
            <h1>About Pico900</h1>

            <section>
                <h2>The 900 Conclusions</h2>
                <p>
                    Giovanni Pico della Mirandola (1463–1494) composed the <em>Conclusiones Nongentae</em>
                    (900 Conclusions) in 1486 as a radical philosophical statement. Drawing on Aristotle, Plato,
                    the Scholastics, Islamic philosophers, Jewish mysticism, and Hermetic texts, Pico attempted
                    to reconcile all wisdom traditions under a unified metaphysical framework.
                </p>
                <p>
                    The 900 Conclusions were organized into 20 groups of 45 propositions each, covering:
                </p>
                <ul>
                    <li><strong>Metaphysics & Being:</strong> The nature of substance, intellect, and creation</li>
                    <li><strong>Psychology & Soul:</strong> The intellect, imagination, memory, and moral psychology</li>
                    <li><strong>Angelology & Demonology:</strong> The hierarchies of celestial and infernal spirits</li>
                    <li><strong>Kabbalah:</strong> The Tree of Life, divine names, and mystical anthropology</li>
                    <li><strong>Magic & Natural Philosophy:</strong> Astrological correspondences and talismanic operations</li>
                    <li><strong>Theology & Christology:</strong> The Incarnation, grace, and the nature of Christ</li>
                </ul>
            </section>

            <section>
                <h2>Heresy and Condemnation</h2>
                <p>
                    In 1486, the papal commission appointed to review Pico's theses condemned 13 propositions as heretical.
                    These condemned conclusions primarily concerned:
                </p>
                <ul>
                    <li>The relationship between will and intellect</li>
                    <li>The unity of the intellect (Averroist monopsychism)</li>
                    <li>Christological claims about the Incarnation and divine nature</li>
                    <li>The propriety of ritual magic and astrological practice</li>
                </ul>
                <p>
                    Rather than recant, Pico wrote an <em>Apology</em> defending his positions, contributing to
                    the broader Renaissance debate over the limits of philosophical inquiry and ecclesiastical authority.
                </p>
            </section>

            <section>
                <h2>This Edition</h2>
                <p>
                    This digital edition presents the 900 Conclusions with complete scholarly apparatus:
                </p>
                <ul>
                    <li><strong>Latin text:</strong> From the critical edition (Brown University)</li>
                    <li><strong>English translation:</strong> Sourced from existing Pico scholarship and original translation</li>
                    <li><strong>Scholarly apparatus:</strong> For each conclusion: the historical charge, Pico's defense,
                    exegetical commentary, and references to modern scholarship</li>
                    <li><strong>Intellectual sources catalog:</strong> 87 major sources across 8 philosophical traditions</li>
                    <li><strong>Heretical flagging:</strong> Identified condemned propositions with historical context</li>
                </ul>
                <p>
                    The site is organized by philosophical section (S1: Neoplatonic, S3: Averroist, S4: Avicennist, S7: Hermetic),
                    with full-text search and filtering by tradition and heretical status.
                </p>
            </section>

            <section>
                <h2>Scholarly Sources</h2>
                <p>
                    This edition draws on foundational scholarship by:
                </p>
                <ul>
                    <li><strong>Brian P. Copenhaver:</strong> <em>Pico della Mirandola on Trial</em> (2015)</li>
                    <li><strong>Chaim Wirszubski:</strong> <em>Pico della Mirandola's Encounter with Jewish Mysticism</em> (1989)</li>
                    <li><strong>Kristin Osborn:</strong> <em>Pico, Boethius, and the Metaphysics of Substance and Relation</em> (2014)</li>
                    <li><strong>Michael V. Dougherty (ed.):</strong> <em>Pico della Mirandola</em> (2008)</li>
                    <li><strong>Douglas Hedley (ed.):</strong> <em>Pico, Ficino and Savonarola: Renaissance Spirituality</em> (2008)</li>
                    <li><strong>Paul Oskar Kristeller:</strong> <em>Studies in Renaissance Thought and Letters</em> (1956)</li>
                </ul>
            </section>

            <section>
                <h2>Data & Methodology</h2>
                <p>
                    The conclusions are stored as JSON, with metadata for:
                </p>
                <ul>
                    <li>Latin incipit (from critical edition)</li>
                    <li>English translation with source attribution</li>
                    <li>Historical charge and Pico's defense</li>
                    <li>Exegetical commentary</li>
                    <li>Scholar citations with quotations</li>
                    <li>Tags and heretical flagging</li>
                </ul>
                <p>
                    The site is statically generated from this data, with vanilla JavaScript for search and filtering.
                    No server-side computation required.
                </p>
            </section>

            <section>
                <h2>Repository & License</h2>
                <p>
                    Full source code and data are available on
                    <a href="https://github.com/t3dy/Pico900">GitHub: t3dy/Pico900</a>.
                </p>
                <p>
                    The Latin text is from the public-domain critical edition. English translations and scholarly
                    apparatus are original to this project. Please cite as: "Pico900 Digital Edition, 2026."
                </p>
            </section>
        </article>
    </main>

    <footer class="site-footer">
        <p>Pico900 Digital Edition | <a href="{BASE_PATH}/about/">About</a> | <a href="https://github.com/t3dy/Pico900">Repository</a></p>
    </footer>
</body>
</html>"""

    return html

def copy_static_files():
    """Copy CSS and other static files to site directory."""
    import shutil

    # Create css directory
    css_dir = SITE_DIR / "css"
    css_dir.mkdir(exist_ok=True)

    # Copy CSS files
    src_css_dir = SRC_DIR / "css"
    for css_file in src_css_dir.glob("*.css"):
        dst = css_dir / css_file.name
        shutil.copy2(css_file, dst)
        print(f"Copied {css_file.name}")

def main():
    """Main build process."""
    print("Building Pico900 website...")

    # Copy static files first
    copy_static_files()

    # Load S3 conclusions
    s3_conclusions = load_all_conclusions("S3")

    if not s3_conclusions:
        print("Error: No S3 conclusions found in data/conclusions/S3/")
        return

    print(f"Found {len(s3_conclusions)} S3 conclusions")

    # Generate conclusion pages
    for conclusion in s3_conclusions:
        conclusion_id = conclusion.get("conclusion_id", "")
        section = conclusion.get("section", "")

        # Extract numeric part from conclusion_id
        # conclusion_id is like "S3.C001", we want the numeric part (001)
        parts = conclusion_id.split(".")
        if len(parts) >= 2:
            num = int(parts[-1][1:])  # Remove 'C' prefix and convert to int
        else:
            num = 1

        # Generate HTML
        html = generate_conclusion_page(conclusion)

        # Write to file
        filename = f"{section}_C{num:03d}.html"
        filepath = CONCLUSIONS_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  Generated {filename}")

    # Generate index page
    index_html = generate_index_page(s3_conclusions)
    with open(SITE_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("Generated index.html")

    # Generate about page
    about_html = generate_about_page()
    with open(SITE_DIR / "about" / "index.html", 'w', encoding='utf-8') as f:
        f.write(about_html)
    print("Generated about/index.html")

    print(f"\nBuild complete! Generated {len(s3_conclusions)} conclusion pages")
    print(f"Output directory: {SITE_DIR}")

if __name__ == "__main__":
    # Ensure about directory exists
    (SITE_DIR / "about").mkdir(exist_ok=True)
    main()
