#!/usr/bin/env python3
"""build_corpus_registry.py: write data/corpus/registry.json, the list of text files the harvester and the
dossier builder read, one entry per *work* (duplicate conversions collapsed), with the locator file for each.

Sources: E:\pdf\renaissance magic\Pico\Markdown\*.md (canonical locators: audits cite these line numbers) and
E:\pdf\renaissance magic\Pico\plain_text_drafts\*.txt (audiobookmaker text; used only for works that have no
Markdown twin). Major works carry hand-entered bibliographic labels and a `role` the harvester keys on;
the rest are labelled from their file names and should be corrected by hand as they are used.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = r"E:\pdf\renaissance magic\Pico"
MD, TXT = os.path.join(BASE, "Markdown"), os.path.join(BASE, "plain_text_drafts")

# substring of Markdown file name -> (key, author, title, year, kind, role)
HAND = [
    ("Stephen_A_Farmer", ("farmer1998", "Stephen A. Farmer", "Syncretism in the West: Pico's 900 Theses (1486)", 1998, "edition", "edition_farmer")),
    ("Pico_della_Mirandola_on_Trial", ("copenhaver2022", "Brian P. Copenhaver", "Pico della Mirandola on Trial: Heresy, Freedom, and Philosophy", 2022, "monograph", "trial_copenhaver")),
    ("Magic_and_the_Dignity", ("copenhaver2019", "Brian P. Copenhaver", "Magic and the Dignity of Man: Pico della Mirandola and His Oration in Modern Memory", 2019, "monograph", None)),
    ("Wirszubski_Paul_Oskar_Kristeller_Pico_della_Mirandola_s_Encounter_with_Jewish_Mysticism_Ha", ("wirszubski1989", "Chaim Wirszubski", "Pico della Mirandola's Encounter with Jewish Mysticism", 1989, "monograph", "kabbalah_wirszubski")),
    ("A_Philosopher_at_the_Crossroads", ("edelheit2022", "Amos Edelheit", "A Philosopher at the Crossroads: Giovanni Pico della Mirandola's Encounter with Scholastic Philosophy", 2022, "monograph", "scholastic_edelheit")),
    ("Ficino_Pico_and_Savonarola", ("edelheit2008", "Amos Edelheit", "Ficino, Pico and Savonarola: The Evolution of Humanist Theology 1461/2-1498", 2008, "monograph", None)),
    ("Scholastic_Florence", ("edelheit2014", "Amos Edelheit", "Scholastic Florence: Moral Psychology in the Quattrocento", 2014, "monograph", None)),
    ("Sophia_Howlett", ("howlett2021", "Sophia Howlett", "Re-evaluating Pico: Aristotelianism, Kabbalism, and Platonism in the Philosophy of Giovanni Pico della Mirandola", 2021, "monograph", None)),
    ("M_V_Dougherty_Pico_della_Mirandola__New_Essays_pdf", ("dougherty2008", "M. V. Dougherty (ed.)", "Pico della Mirandola: New Essays", 2008, "collection", None)),
    ("Black_Crofton", ("black2006", "Crofton Black", "Pico's Heptaplus and Biblical Hermeneutics", 2006, "monograph", None)),
    ("Allen_MichaelJ_B_Studies_in_the_Platonism", ("allen2017", "Michael J. B. Allen", "Studies in the Platonism of Marsilio Ficino and Giovanni Pico", 2017, "collection", None)),
    ("Brill_s_Studies_in_Intellectual_History_325_Ovanes_Akopyan", ("akopyan2021", "Ovanes Akopyan", "Debating the Stars in the Italian Renaissance: Giovanni Pico della Mirandola's Disputationes adversus astrologiam divinatricem and Its Reception", 2021, "monograph", None)),
    ("I_Tatti_Studies", ("akopyan2018", "Ovanes Akopyan", "Giovanni Pico della Mirandola and Astrology (1486-1493): From Scientia Naturalis to the Disputationes", 2018, "article", None)),
    ("Renaissance_Studies_2017", ("akopyan2017", "Ovanes Akopyan", "Princeps aliorum and his followers: Giovanni Pico della Mirandola on the astrological tradition", 2017, "article", None)),
    ("Giulio_Busi_Raphael_Ebgi", ("busi2014", "Giulio Busi and Raphael Ebgi", "Giovanni Pico della Mirandola: Mito, magia, Qabbalah", 2014, "edition_it", None)),
    ("Entdeckung_der_j", ("busi_german", "Giulio Busi", "Giovanni Pico della Mirandola und die Entdeckung der juedischen Mystik im italienischen Quattrocento", None, "article", None)),
    ("ERSTER_TEIL_Erkenntnistheorie", ("kabbalah_paradigma", "(author to be confirmed from front matter)", "Erkenntnistheorie und christliche Kabbalah: Das Paradigma des Pico della Mirandola", None, "monograph", None)),
    ("Corazzol", ("corazzol2019", "Giacomo Corazzol", "From Sinai to Athens: Giovanni Pico della Mirandola's philological quest for the transmission of theological truth", 2019, "article", None)),
    ("Abravanel_Isaac_Allemanno", ("ogren2009", "Brian Ogren", "The Beginning of the World in Renaissance Jewish Thought: Ma'aseh Bereshit in Italian Jewish Philosophy and Kabbalah, 1492-1535", 2009, "monograph", None)),
    ("Apologia_conclusionum_suarum", ("fornaciari2010", "Paolo Edoardo Fornaciari (ed.)", "Apologia conclusionum suarum (front matter and contents only in the corpus)", 2010, "edition", None)),
    ("Conclusioni_ermetiche_magiche_e_orfiche", ("conclusioni_ermetiche", "(Italian edition; editor to be confirmed)", "Conclusioni ermetiche, magiche e orfiche", None, "edition_it", None)),
    ("Heptaplus_Pico_della_Mirandola_On_the_Dignity", ("wallis1965", "Wallis, Miller, Carmichael (tr.)", "On the Dignity of Man; On Being and the One; Heptaplus", 1965, "translation", None)),
    ("Borghesi_Francesco", ("borghesi2012", "Borghesi, Papio, Riva (eds.)", "Oration on the Dignity of Man: A New Translation and Commentary", 2012, "edition", None)),
    ("Lettere_libgen", ("lettere", "Francesco Borghesi (ed.)", "Lettere", 2018, "edition", None)),
    ("Truglia", ("truglia2010", "Craig Truglia", "Al-Ghazali and Giovanni Pico della Mirandola on the Question of Human Freedom and the Chain of Being", 2010, "article", None)),
    ("Girdner", ("girdner2018", "Scott Michael Girdner", "Giovanni Pico della Mirandola, Johanan Alemanno and The Book of Love by Al-Ghazali", 2018, "article", None)),
    ("Novak", ("novak1982", "B. C. Novak", "Giovanni Pico della Mirandola and Jochanan Alemanno", 1982, "article", None)),
    ("Ernst_Cassirer", ("cassirer1942", "Ernst Cassirer", "Giovanni Pico della Mirandola: A Study in the History of Renaissance Ideas", 1942, "article", None)),
    ("Steiris", ("steiris2014", "Georgios Steiris", "Giovanni Pico della Mirandola on Anaxagoras", 2014, "article", None)),
    ("Salas_Victor", ("salas2014", "Victor M. Salas", "Giovanni Pico della Mirandola on Being and Unity: A Thomistic Solution to an Ancient Quarrel", 2014, "article", None)),
    ("Mandosio", ("mandosio2012", "Jean-Marc Mandosio", "Beyond Pico della Mirandola: John Dee's formal numbers and real cabala", 2012, "article", None)),
    ("An_Anatomy_of_Influence", ("walden2012", "Justine Walden", "An Anatomy of Influence: Savonarola and Pico (RSA 2012 paper)", 2012, "paper", None)),
    ("Self-Knowledge_Illumination", ("selfknowledge_notes", "(unidentified)", "Self-Knowledge, Illumination and Natural: notes on Pico sources", None, "notes", None)),
    ("Knots_and_Spirals", ("knots_spirals", "(unidentified)", "Knots and Spirals I: Pico della Mirandola", None, "article", None)),
    ("Kibre_Princeps", ("kibre1941", "Pearl Kibre (review of Dulles, Princeps Concordiae)", "Isis review", 1941, "review", None)),
    ("The_Library_of_Pico", ("kibre1937", "Pearl Kibre", "The Library of Pico della Mirandola (review)", 1937, "review", None)),
    ("Kristeller_Paul_Oskar_Giovanni_Pico_della_Mirandola_and_His_La", ("kristeller1976", "Paul Oskar Kristeller", "Giovanni Pico della Mirandola and His Latin Poems: A New Manuscript", 1976, "article", None)),
    ("Pflaum", ("pflaum1928", "Heinz Pflaum", "Leone Ebreo und Pico della Mirandola", 1928, "article", None)),
    ("Toscano", ("toscano_zambelli", "Anna Toscano (review of Zambelli, L'apprendista stregone)", "Nuncius review", None, "review", None)),
    ("Albrecht", ("albrecht2014", "R. Albrecht", "Pico della Mirandola and Raymond Llull", 2014, "note", None)),
    ("Breen_Giovanni_Pico", ("breen1952a", "Quirinus Breen", "Giovanni Pico della Mirandola on the Conflict of Philosophy and Rhetoric", 1952, "article", None)),
    ("Breen_Melancthon", ("breen1952b", "Quirinus Breen", "Melanchthon's Reply to G. Pico della Mirandola", 1952, "article", None)),
    ("Forbes", ("forbes1942", "Elizabeth Livermore Forbes (tr.)", "Of the Dignity of Man: Oration of Giovanni Pico della Mirandola", 1942, "translation", None)),
    ("Rijser", ("rijser2009", "David Rijser", "How like an Angel: Self-Fashioning in Pico della Mirandola and Raphael", 2009, "article", None)),
    ("Lamanna", ("lamanna", "Francesco Lamanna", "Il concetto di Dio nel pensiero di Pico della Mirandola", None, "monograph", None)),
    ("Filosofia_e_cabbala", ("filosofia_cabbala", "(unidentified)", "Filosofia e cabbala nel Commento al Cantico", None, "article", None)),
    ("Del_Soldato", ("delsoldato2021", "Eva Del Soldato", "Review of Copenhaver, Magic and the Dignity of Man (Speculum)", 2021, "review", None)),
    ("Lesley", ("lesley2008", "Arthur M. Lesley", "Review of Dougherty (ed.), Pico della Mirandola: New Essays (The Thomist)", 2008, "review", None)),
    ("Kuntz", ("kuntz2008", "Marion Leathers Kuntz", "Review of Dougherty (ed.), Pico della Mirandola: New Essays (RQ)", 2008, "review", None)),
    ("Celenza", ("celenza2000", "Christopher Celenza", "Review of Allen, Synoptic Art (RQ)", 2000, "review", None)),
    ("Marsh_David", ("marsh2020", "David Marsh", "Review of Borghesi (ed.), Lettere (RQ)", 2020, "review", None)),
    ("Roush", ("roush2002", "Sherry Roush", "Dante as Piagnone Prophet: Girolamo Benivieni's Cantico in laude di Dante", 2002, "article", None)),
    ("Pugliese", ("pugliese2003", "Olga Zorzi Pugliese", "Girolamo Benivieni amico e collaboratore di Giovanni Pico della Mirandola", 2003, "article", None)),
    ("Motta", ("motta2005", "Uberto Motta", "Review of Garfagnini (ed.), Trattato in difesa di Girolamo Savonarola (Aevum)", 2005, "review", None)),
    ("Thompson", ("thompson1970", "David Thompson", "Pico della Mirandola's praise of Lorenzo", 1970, "article", None)),
    ("Sheehan", ("sheehan_hamm", "Daniel F. Sheehan and Victor Michael Hamm", "Pico della Mirandola, Of Being and Unity (Classical Weekly)", None, "review", None)),
    ("Dorothy_H_Brown", ("brown_review", "Dorothy H. Brown", "Review of McGaw (tr.), Heptaplus", None, "review", None)),
    ("Philosophical_Studies_vol_3", ("philstudies1953", "(reviewer)", "Pico della Mirandola: Of Being and Unity (Philosophical Studies)", 1953, "review", None)),
    ("Gallello", ("gallello2018", "Gianni Gallello et al.", "Poisoning histories in the Italian Renaissance: The case of Pico della Mirandola and Angelo Poliziano", 2018, "article", None)),
    ("CHANCE_1992", ("chance1992", "(CHANCE 1992)", "Pico della Mirandola: A Philosophical Forefather of Applied Statistics?", 1992, "article", None)),
    ("Benivieni_Girolamo_Two_Poems", ("benivieni_poems", "Girolamo Benivieni", "Two Poems on Spiritual Renewal", None, "edition", None)),
    ("Heptaplus_libgen", ("heptaplus_it", "(Italian edition)", "Heptaplus", None, "edition_it", None)),
    ("pico_being_pdf", ("pico_being", "(edition)", "Pico: On Being and the One", None, "edition", None)),
]
SKIP_SUBSTR = ["Medieval_Renaissance_Texts_Studies_167",      # duplicate of Farmer
               "Encounter_with_Jewish_Mysticism_li_pdf",      # duplicate of Wirszubski
               "New_Essays_libgen_li",                        # duplicate of Dougherty
               "Ovanes_Akopyan_Debating_the_Stars_in_the_Italian_Renaissance__Giovanni_Pico_della_Mirandola_s__D",  # duplicate hash
               "Supplements_to_the_journal_of_Jewish_thought",  # duplicate of Ogren
               "Variorum_Collected_Studies_1063",              # duplicates of Allen
               "pico_being_epub",                              # duplicate
               "Omnibus_Medici",                                # a novel
               ]


def slugify(s):
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").lower()
    return s[:40]


def name_key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())[:60]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cat = json.load(io.open(os.path.join(BASE, "data", "corpus_catalog.json"), encoding="utf-8"))["documents"]
    src_by_md = {d["id"] + ".md": d for d in cat}
    works, used_keys = {}, set()
    md_files = sorted(f for f in os.listdir(MD) if f.endswith(".md"))
    txt_files = sorted(f for f in os.listdir(TXT) if f.endswith(".txt"))
    txt_by_key = {name_key(os.path.splitext(f)[0]): f for f in txt_files}
    matched_txt = set()
    for f in md_files:
        if any(s in f for s in SKIP_SUBSTR):
            continue
        meta = next((h for sub, h in HAND if sub in f), None)
        d = src_by_md.get(f, {})
        src = os.path.splitext(d.get("source_file", f))[0]
        twin = txt_by_key.get(name_key(src))
        if twin:
            matched_txt.add(twin)
        if meta:
            key, author, title, year, kind, role = meta
        else:
            key, author, title, year, kind, role = slugify(f)[:30], "(from file name)", src[:120], None, d.get("document_type", "unknown"), None
        if key in used_keys:
            key = key + "_" + f[-11:-3]
        used_keys.add(key)
        works[key] = {"author": author, "title": title, "year": year, "kind": kind, "role": role,
                      "path": os.path.join(MD, f), "locator_unit": "markdown line",
                      "plain_text_twin": os.path.join(TXT, twin) if twin else None,
                      "word_count": d.get("word_count"), "source_file": d.get("source_file")}
    # plain-text-only works
    for f in txt_files:
        if f in matched_txt:
            continue
        if any(name_key(s) and name_key(s) in name_key(f) for s in ["Omnibus Medici", "Medieval Renaissance Texts Studies 167", "Variorum Collected Studies 1063", "libgen li pico being", "Supplements to the journal", "Ovanes Akopyan Debating the Stars", "_footnote_conversion_report", "Philosophical Transactions", "Shofar An Interdisciplinary"]):
            continue
        # crude twin check against already-registered Markdown by first 25 alnum chars
        k25 = name_key(f)[:25]
        if any(name_key(w.get("source_file") or "")[:25] == k25 for w in works.values()):
            continue
        key = "txt_" + slugify(os.path.splitext(f)[0])[:34]
        if key in used_keys:
            continue
        used_keys.add(key)
        works[key] = {"author": "(from file name)", "title": os.path.splitext(f)[0][:140], "year": None, "kind": "unknown",
                      "role": None, "path": os.path.join(TXT, f), "locator_unit": "plain-text line", "plain_text_twin": None,
                      "word_count": None, "source_file": f, "note": "plain-text only (no Markdown conversion)"}
    out = os.path.join(ROOT, "data", "corpus", "registry.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8") as fh:
        json.dump({"_note": "One entry per work. `path` is the locator file (cite as key:line). Hand-labelled entries carry a role "
                   "the harvester keys on; '(from file name)' entries need bibliographic confirmation before citation.",
                   "works": works}, fh, indent=1, ensure_ascii=False)
    n_md = sum(1 for w in works.values() if w["locator_unit"] == "markdown line")
    print(f"registry: {len(works)} works ({n_md} markdown, {len(works) - n_md} plain-text only); hand-labelled {sum(1 for w in works.values() if w['author'] != '(from file name)')}")


if __name__ == "__main__":
    main()
