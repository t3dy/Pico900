# Interface verification record

## T-SITE-09 pass — 2026-10-10

Driven against https://t3dy.github.io/Pico900/cards/ (production, base path `/Pico900/`).

### Checklist (from SITE_DESIGN.md s10)

| item | result | note |
|---|---|---|
| Load cards page at real base path | PASS | 1886 cards, all JS loads (no console errors) |
| Apply two facets, confirm counts against JSON | PASS | trad=scholastic → 184; + tier=primary → 20; verified against `P.byId` count |
| Sort by importance | PASS | sort control sets `P.S.sort="imp"`, render works |
| Search phrase, confirm count | PASS | "Ficino" → 380 claims |
| Open card, follow relation / trail | PASS | trail shows after 2nd card opened; text matches card ID and content |
| Collect a card and reload (state persists) | PASS | `localStorage["pico900.collection.v1"]` persists; tray shows "1 collected" after reload |
| Narrow-screen layout | PASS | 375 px mobile: sidebar stacks above grid, nav wraps, tray docks at bottom |
| Note area in drawer | PASS | `.wb-note` textarea injected after card open |
| Matrix view | PASS | matrix table renders with brown shading, close button works |
| Save lens button | PASS | button present in toolbar; lens section present in sidebar |

### What was NOT driven

- Keyboard tab navigation (not drivable from the browser automation in this session)
- Greyscale colour-channel check (needs OS-level filter)
- Compare overlay on live (tested locally; confirmed CSS present)
- Export Markdown / Export JSON buttons (present, not clicked)
- Sources and People tabs (T-SITE-05 pages exist at /scholarship/ and /sections/)

### Known issues

None found in the driven items.
