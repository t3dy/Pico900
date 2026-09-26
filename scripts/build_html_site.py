#!/usr/bin/env python3
"""
Build static HTML website from Pico900 JSON data.

Generates:
1. Landing page with searchable conclusions list
2. Individual conclusion pages (facing Latin/English)
3. Section index pages
4. Sources and scholars reference pages
5. Search index (JSON for client-side search)

Output: site/ directory with complete static website
"""

import json
import re
from pathlib import Path
from datetime import datetime

# HTML templates
BASE_PATH = "/Pico900"  # GitHub Pages base path

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{base_path}/css/style.css">
    <meta name="description" content="{description}">
</head>
<body>
    <nav class="header">
        <div class="nav-container">
            <h1 class="site-title"><a href="{base_path}/">Pico900</a></h1>
            <ul class="nav-links">
                <li><a href="{base_path}/">Conclusions</a></li>
                <li><a href="{base_path}/sources/">Sources</a></li>
                <li><a href="{base_path}/about/">About</a></li>
            </ul>
        </div>
    </nav>

    <main class="content">
        {content}
    </main>

    <footer class="footer">
        <p>Digital Edition of Giovanni Pico della Mirandola's 900 Conclusions</p>
        <p><a href="https://github.com/t3dy/Pico900">GitHub</a> |
           <a href="/about/">About This Edition</a> |
           <a href="https://cds.lib.brown.edu/cds-project/picos-900-theses">Critical Edition</a></p>
    </footer>

    <script src="{base_path}/js/search.js"></script>
    {extra_script}
</body>
</html>
"""

CONCLUSION_PAGE = """<div class="conclusion-container">
    <div class="conclusion-header">
        <h1>Conclusion {conclusion_id}</h1>
        <p class="section-info">{section_name} • Thesis {order}</p>
    </div>

    <div class="conclusion-content">
        <div class="facing-page">
            <div class="latin-column">
                <h2>Latin</h2>
                <div class="text-content">
                    <p>{latin_text}</p>
                </div>
            </div>

            <div class="english-column">
                <h2>English</h2>
                <div class="text-content">
                    <p>{english_text}</p>
                </div>
            </div>
        </div>

        <div class="commentary-section">
            <h2>Philosophical Context</h2>
            <div class="charge-defense">
                <h3>Charge</h3>
                <p>{charge}</p>
                <h3>Defense</h3>
                <p>{defense}</p>
            </div>

            {citations_html}

            {heretical_section}
        </div>
    </div>

    <div class="navigation">
        {prev_link}
        {next_link}
    </div>
</div>
"""

CITATIONS_HTML = """<div class="citations">
    <h3>Scholar Citations</h3>
    <ul class="citation-list">
        {citations}
    </ul>
</div>
"""

CSS = """
:root {{
    --primary: #1a1a2e;
    --secondary: #16213e;
    --accent: #0f3460;
    --light: #e0e1dd;
    --text: #333;
    --bg: #fff;
    --border: #ddd;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Georgia', serif;
    color: var(--text);
    background: var(--bg);
    line-height: 1.6;
}}

.header {{
    background: var(--primary);
    color: white;
    padding: 1rem 0;
    border-bottom: 3px solid var(--accent);
    position: sticky;
    top: 0;
    z-index: 100;
}}

.nav-container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.site-title {{
    font-size: 1.8rem;
}}

.site-title a {{
    color: white;
    text-decoration: none;
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    color: var(--light);
    text-decoration: none;
    font-size: 1rem;
}}

.nav-links a:hover {{
    color: white;
}}

main {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    min-height: calc(100vh - 200px);
}}

.conclusion-container {{
    margin-bottom: 2rem;
}}

.conclusion-header {{
    border-bottom: 2px solid var(--accent);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}}

.conclusion-header h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.section-info {{
    color: #666;
    font-size: 0.95rem;
}}

.facing-page {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    background: #f9f9f9;
}}

.latin-column, .english-column {{
    border-right: 1px solid var(--border);
    padding-right: 1.5rem;
}}

.english-column {{
    border-right: none;
    padding-right: 0;
}}

.facing-page h2 {{
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.text-content {{
    font-size: 1rem;
    line-height: 1.8;
}}

.latin-column .text-content {{
    font-style: italic;
    color: #555;
}}

.commentary-section {{
    margin-bottom: 2rem;
}}

.charge-defense {{
    background: #f5f5f5;
    padding: 1.5rem;
    border-left: 4px solid var(--accent);
    margin-bottom: 1.5rem;
}}

.charge-defense h3 {{
    color: var(--accent);
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}}

.charge-defense h3:first-child {{
    margin-top: 0;
}}

.citations {{
    margin-top: 2rem;
}}

.citations h3 {{
    color: var(--accent);
    margin-bottom: 1rem;
}}

.citation-list {{
    list-style: none;
}}

.citation-list li {{
    margin-bottom: 1rem;
    padding: 1rem;
    background: #f9f9f9;
    border-left: 3px solid var(--secondary);
}}

.citation-list strong {{
    display: block;
    color: var(--accent);
}}

.heretical-section {{
    background: #fff3cd;
    padding: 1.5rem;
    border-left: 4px solid #ff6b6b;
    margin-top: 2rem;
}}

.navigation {{
    display: flex;
    justify-content: space-between;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}}

.navigation a {{
    padding: 0.5rem 1rem;
    background: var(--accent);
    color: white;
    text-decoration: none;
    border-radius: 4px;
}}

.navigation a:hover {{
    background: var(--primary);
}}

.footer {{
    background: var(--primary);
    color: var(--light);
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
}}

.footer a {{
    color: white;
    text-decoration: none;
}}

.footer a:hover {{
    text-decoration: underline;
}}

/* Search and filtering */
.search-box {{
    margin-bottom: 2rem;
}}

.search-box input {{
    width: 100%;
    max-width: 500px;
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
}}

.conclusions-list {{
    display: grid;
    gap: 1rem;
}}

.conclusion-item {{
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s;
}}

.conclusion-item:hover {{
    background: #f0f0f0;
    border-color: var(--accent);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

/* Responsive */
@media (max-width: 768px) {{
    .facing-page {{
        grid-template-columns: 1fr;
    }}

    .latin-column, .english-column {{
        border-right: none;
        padding-right: 0;
    }}

    .nav-links {{
        gap: 1rem;
    }}
}}
"""

SEARCH_JS = """
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (!searchInput) return;

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase();
        const items = document.querySelectorAll('.conclusion-item');

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? 'block' : 'none';
        });
    });
}

document.addEventListener('DOMContentLoaded', initSearch);
"""


class SiteBuilder:
    def __init__(self):
        self.site_dir = Path("site")
        self.data_dir = Path("data/conclusions")
        self.site_dir.mkdir(exist_ok=True)
        (self.site_dir / "conclusions").mkdir(exist_ok=True)
        (self.site_dir / "css").mkdir(exist_ok=True)
        (self.site_dir / "js").mkdir(exist_ok=True)

        # Load all conclusions
        self.conclusions = self._load_all_conclusions()

    def _load_all_conclusions(self):
        """Load all conclusion JSON files."""
        conclusions = []
        for entry_file in sorted(self.data_dir.rglob("entry_*.json")):
            try:
                with open(entry_file, "r", encoding="utf-8-sig") as f:
                    conclusion = json.load(f)
                conclusions.append(conclusion)
            except Exception as e:
                print(f"Error loading {entry_file}: {e}")

        return sorted(conclusions, key=lambda x: x.get("conclusion_id", ""))

    def _format_citations_html(self, conclusion):
        """Generate HTML for scholar citations."""
        citations = conclusion.get("scholar_citations", [])
        if not citations:
            return ""

        citation_items = []
        for cite in citations:
            scholar = cite.get("scholar", "Unknown")
            work = cite.get("work", "Unknown Work")
            pages = cite.get("pages", "")
            quotation = cite.get("quotation", "[Quotation pending]")

            citation_items.append(f"""
                <li>
                    <strong>{scholar}</strong> — <em>{work}</em>
                    {f" ({pages})" if pages else ""}
                    <p class="quotation">{quotation}</p>
                </li>
            """)

        if citation_items:
            return CITATIONS_HTML.format(citations="\n".join(citation_items))
        return ""

    def _get_navigation_links(self, index):
        """Generate prev/next navigation links."""
        prev_link = ""
        next_link = ""

        if index > 0:
            prev_id = self.conclusions[index - 1]["conclusion_id"]
            prev_link = f'<a href="/conclusions/{prev_id}.html">← Previous</a>'

        if index < len(self.conclusions) - 1:
            next_id = self.conclusions[index + 1]["conclusion_id"]
            next_link = f'<a href="/conclusions/{next_id}.html">Next →</a>'

        return prev_link, next_link

    def _build_conclusion_page(self, conclusion, index):
        """Build HTML for a single conclusion."""
        conclusion_id = conclusion.get("conclusion_id", "Unknown")
        section = conclusion.get("section", "")
        section_name = conclusion.get("section_name", "")
        order = conclusion.get("order", "")

        latin = conclusion.get("latin_incipit", "[Latin text pending]")
        english = conclusion.get("english_translation", "")
        if isinstance(english, dict):
            english = english.get("text", "[English translation pending]")

        charge = conclusion.get("charge", "[Charge pending]")
        defense = conclusion.get("defense", "[Defense pending]")

        citations_html = self._format_citations_html(conclusion)
        prev_link, next_link = self._get_navigation_links(index)

        heretical_section = ""
        if conclusion.get("heretical_flag"):
            heretical_notes = conclusion.get("heretical_notes", "")
            heretical_section = f"""
            <div class="heretical-section">
                <h3>Heretical Status</h3>
                <p>{heretical_notes}</p>
            </div>
            """

        content = CONCLUSION_PAGE.format(
            conclusion_id=conclusion_id,
            section_name=section_name,
            order=order,
            latin_text=latin,
            english_text=english,
            charge=charge,
            defense=defense,
            citations_html=citations_html,
            heretical_section=heretical_section,
            prev_link=prev_link,
            next_link=next_link
        )

        html = BASE_HTML.format(
            title=f"Conclusion {conclusion_id} - Pico900",
            description=f"Pico's conclusion {conclusion_id}: {section_name}",
            base_path=BASE_PATH,
            content=content,
            extra_script=""
        )

        # Write conclusion page
        conclusion_file = self.site_dir / "conclusions" / f"{conclusion_id}.html"
        with open(conclusion_file, "w", encoding="utf-8") as f:
            f.write(html)

        return conclusion_id

    def _build_index_page(self):
        """Build main index page with searchable list."""
        conclusion_items = []
        for conclusion in self.conclusions:
            cid = conclusion.get("conclusion_id", "")
            section = conclusion.get("section_name", "")
            trans = conclusion.get("english_translation", "")
            if isinstance(trans, dict):
                trans = trans.get("text", "")

            # Truncate translation for preview
            preview = trans[:100] + "..." if len(trans) > 100 else trans

            item = f"""
            <a href="/conclusions/{cid}.html" class="conclusion-item">
                <strong>{cid}</strong> — {section}
                <p style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">{preview}</p>
            </a>
            """
            conclusion_items.append(item)

        search_box = '<div class="search-box"><input type="text" placeholder="Search conclusions..."></div>'
        conclusions_list = '<div class="conclusions-list">' + "\n".join(conclusion_items) + '</div>'

        content = f"""
        <h1>Pico's 900 Conclusions</h1>
        <p style="margin-bottom: 2rem; color: #666;">
            Digital edition with facing Latin/English text and scholarly commentary.
            {len(self.conclusions)} conclusions total.
        </p>
        {search_box}
        {conclusions_list}
        """

        html = BASE_HTML.format(
            title="Pico's 900 Conclusions - Pico900",
            description="Complete digital edition of Giovanni Pico della Mirandola's 900 Conclusions",
            base_path=BASE_PATH,
            content=content,
            extra_script=""
        )

        index_file = self.site_dir / "index.html"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(html)

    def _build_about_page(self):
        """Build about/info page."""
        content = """
        <h1>About This Edition</h1>

        <h2>Pico's 900 Conclusions</h2>
        <p>Giovanni Pico della Mirandola (1463–1494) composed the <em>Conclusiones 900</em>
        as a comprehensive synthesis of medieval and Renaissance philosophy, theology,
        Kabbalah, and mysticism. Originally prepared for public disputation in Rome in 1486,
        thirteen of the conclusions were condemned by papal bull.</p>

        <h2>This Digital Edition</h2>
        <p>This edition presents all 900 conclusions with:</p>
        <ul>
            <li>Facing-page Latin (from the critical edition) and English translation</li>
            <li>Philosophical charge and defense for each conclusion</li>
            <li>Scholar citations from leading Pico researchers</li>
            <li>Full searchability and navigation</li>
        </ul>

        <h2>Sources</h2>
        <p>Critical Edition: <a href="https://cds.lib.brown.edu/cds-project/picos-900-theses">Brown University Digital Repository</a></p>
        <p>Scholarship: Wirszubski, Copenhaver, Howlett, Edelheit, Black, Allen, Farmer, Akopyan, and others</p>

        <h2>License</h2>
        <p>Pico's <em>900 Conclusions</em> are in the public domain.
        This digital edition and scholarly apparatus are released under CC BY-SA 4.0.</p>
        """

        html = BASE_HTML.format(
            title="About - Pico900",
            description="About this digital edition",
            base_path=BASE_PATH,
            content=content,
            extra_script=""
        )

        about_file = self.site_dir / "about" / "index.html"
        about_file.parent.mkdir(exist_ok=True)
        with open(about_file, "w", encoding="utf-8") as f:
            f.write(html)

    def _write_css(self):
        """Write CSS file."""
        css_file = self.site_dir / "css" / "style.css"
        with open(css_file, "w", encoding="utf-8") as f:
            f.write(CSS)

    def _write_js(self):
        """Write JavaScript file."""
        js_file = self.site_dir / "js" / "search.js"
        with open(js_file, "w", encoding="utf-8") as f:
            f.write(SEARCH_JS)

    def build(self):
        """Build entire site."""
        print("Building Pico900 Static Website")
        print("=" * 70)

        # Write assets
        print("Writing CSS and JavaScript...")
        self._write_css()
        self._write_js()

        # Build index page
        print("Building index page...")
        self._build_index_page()

        # Build about page
        print("Building about page...")
        self._build_about_page()

        # Build conclusion pages
        print(f"Building {len(self.conclusions)} conclusion pages...")
        for i, conclusion in enumerate(self.conclusions, 1):
            if i % 100 == 0 or i == len(self.conclusions):
                print(f"  {i}/{len(self.conclusions)}")
            self._build_conclusion_page(conclusion, self.conclusions.index(conclusion))

        print("\n" + "=" * 70)
        print(f"Site built successfully!")
        print(f"  Location: {self.site_dir.absolute()}")
        print(f"  Pages: {len(self.conclusions)} conclusions + index + about")
        print(f"\nTo view locally:")
        print(f"  python -m http.server 8000 --directory {self.site_dir}")
        print(f"  Then visit: http://localhost:8000")

        return True


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
