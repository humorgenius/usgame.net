# Stance briefs — read the one your task names, and only that one

Five siblings, one page each, five genuinely different visual and rhetorical stances. Adjacent
variants deliberately share no axis: A is brand-immersive, B is content-dense editorial, C is
utilitarian terminal, D is image-first magazine, E is layout-first product portal.

---

## STANCE A — Neon Vice（霓虹罪恶城）

**One line:** the homepage as the game's own poster — a full-bleed cinematic sunset, the loudest
headline on the site, and everything else arranged underneath it like a film's end credits.

### Reference vocabulary
Rockstar's own GTA VI promotional website · GTA Vice City's in-game art direction · late-80s Miami
tourist posters · neon signage photography. Think *heat haze and hotel neon*, not *cyberpunk*.

### Art direction
- Ground: near-black plum `#0B0710` (never pure black), with a subtle noise grain and a horizon glow
  behind the hero.
- Accent pair: hot magenta `#FF2D95` (primary) + sunset orange `#FF8A3D` (secondary). Held tightly —
  magenta for interactive/emphasis, orange only for the horizon glow and one or two dividers.
- Hero: full-bleed `hero-sunset.webp` with a multi-stop dark scrim (dark at the bottom, saturated at
  the top), a fine horizontal scanline wash at very low opacity, headline sitting at the lower-left of
  the wrap. Headline: very heavy condensed grotesque, caps, `clamp(2.6rem, 7vw, 5.6rem)`, slightly
  negative tracking.
- Display font: **Anton** (fallback `Impact, "Arial Black", Bahnschrift, sans-serif`). Body: **Inter**
  (fallback `"Segoe UI", system-ui, sans-serif`).
- Cards: dark plum panels, 14px radius, 1px magenta-tinted border at ~14% opacity, image bleeding to
  the card's top edge, category as a small uppercase magenta label, date right-aligned in the meta
  row. Hover: card lifts 2px, image scales 1.04, border brightens — 180ms ease.

### Page order (the stance — the brand leads, the utility follows)
1. Header: wordmark `USGAME` + `GTA VI` badge, nav, search icon, ZH/EN toggle, hamburger.
2. Ad placeholder below nav.
3. **Full-bleed hero** — eyebrow, huge headline (two lines), lede, two CTAs, launch meta row.
4. **Trailer theatre** — the embed as a wide cinematic band on a darker ground, with the official
   caption and the privacy note. It must feel like act two of the hero, not a widget.
5. **Latest news** — section heading + `All news` link; wide 2-column grid on desktop (the first card
   spans both columns as the lead story); each card has image, category, date, title, excerpt, read
   time. In-feed ad after the 4th card. Category filter tabs (`All / News / Guides / Map /
   Characters`) that actually filter.
6. **Guides you need on day one** — 3-up grid; each card carries the tier label and read time.
7. **Quick entries** — 8 compact tiles with tiny art thumbnails; they read as a menu, not as cards.
8. **Videos** — one larger embed plus two smaller thumbnail links. Use the real YouTube IDs.
9. **Closing CTA band** — newsletter block (pure front-end, dashed "not wired up yet" note) plus the
   independence disclaimer from the content pack.
10. Footer: 3 columns + legal line + repeated language switch. Ad placeholder at end of content.

### Deliberately NOT
A SaaS dashboard · white panels · pastel gradients · a sidebar · a four-number stats band (those
belong to variant E) · glassmorphism.

---

## STANCE B — Newsroom Editorial（新闻编辑部）

**One line:** the homepage as the front page of a serious desk — a lead story, a dateline, a rail of
secondary stories, and hairline rules instead of decoration.

### Reference vocabulary
IGN · Polygon · Eurogamer · VGC · a printed broadsheet front page · wire-copy discipline.

### Art direction
- Ground: deep charcoal `#12100E`, text warm off-white `#EDE7DE` (not `#FFF` — the point is newsprint
  warmth under a dark theme). Panels are a barely-lifted `#1A1714`.
- Accent: one saturated ink red `#E63946`, used **only** for category eyebrows, the active tab
  underline, and hovered links. No glow, no gradient.
- Headlines: **Playfair Display** (fallback `Georgia, Constantia, "Times New Roman", serif`), tight
  leading, roman with a single italic word for emphasis. Body and UI: **Inter**
  (fallback `"Segoe UI", system-ui`).
- Separation comes from **1px hairline rules** (`rgba(237,231,222,.14)`) and whitespace, not from card
  shadows or radius. Radius 2–4px maximum; images get 2px.
- Density is deliberately higher than the other variants: 12-column grid on desktop, tightly packed,
  small metadata type (11–12px, letterspaced uppercase), generous line-height only inside prose.
- Every item carries its provenance: category eyebrow · date · `Updated` stamp. This is the variant
  that most obviously answers "why should AdSense trust this site".

### Page order (the stance — credibility leads)
1. **Masthead**: wordmark, current date + "Leonida, USA" dateline, nav row beneath it separated by a
   rule, then a thin second row with section links + search field + ZH/EN toggle. Sticky on scroll;
   collapses to wordmark + hamburger + toggle on mobile.
2. Ad placeholder below the masthead.
3. **Lead story**: one large story — image beside text on desktop, serif headline up to
   `clamp(2rem, 4.4vw, 3.2rem)`, deck, byline row, `Read the full story`. This is the `<h1>`.
4. **The rail**: 3-column news grid of the remaining 5 stories with small thumbnails and hairline
   separators, plus a category filter row that filters. In-feed ad after the 4th item.
5. **Official video** — the trailer as a newsroom video card with caption and attribution note; 16:9,
   full content width on mobile, about two-thirds width on desktop with the "most read" rail beside it.
6. **Sidebar / secondary column** (sticky on desktop, stacked below on mobile): `Most read` as an
   ordered list with 01–05 numerals and hairline separators; `Latest updates` log with timestamps; the
   sidebar ad placeholder (300×250); a compact subscribe block.
7. **Guide index** — presented as an **index, not cards**: numbered rows
   (`01  First three hours: a spoiler-free starting route   Walkthrough · 12 min`); hover reveals a
   red left rule.
8. **FAQ teaser** — 4 question rows; the expandable one is your open/close interaction.
9. Footer: dense multi-column link list, legal + independence disclaimer, repeated language switch.
   Ad placeholder at end of content.

### Deliberately NOT
Neon · large rounded cards · drop shadows · glassmorphism · full-bleed cinematic hero · big decorative
numbers · a bento grid · any accent colour other than the single red.

---

## STANCE C — Heist Dossier（行动档案 / 终端）

**One line:** the site as an operative's terminal — everything indexed, labelled, timestamped and
sourced, because you are casing Leonida, not browsing a magazine.

### Reference vocabulary
GTA's own mission-briefing UI and in-game browser · a case-file/dossier binder · Bloomberg terminal
density · brutalist HUD design · court-exhibit labelling.

### Art direction
- Ground: `#07090A` (near-black, slightly blue) with one visible hairline grid drawn with
  `repeating-linear-gradient` at ~4% opacity. No photographic hero.
- Accent: phosphor amber `#FFB000` as the single accent — the active index item, the cursor block, key
  numerals, the one alert line. A muted cyan `#4FD1C5` may appear **only** inside status readouts.
- Type: **IBM Plex Mono** for UI, labels, tables and headings (fallback
  `Consolas, "Cascadia Mono", monospace`); one sans (**Inter** / `Segoe UI`) for long-form prose only,
  so guide descriptions stay readable. Radius 0 everywhere. No shadows — depth comes from hairlines
  and inverted blocks.
- Everything is labelled like evidence: an ID (`FILE 0142`), a source (`SRC: ROCKSTAR NEWSWIRE`), a
  timestamp (`2026-09-24T09:00Z`), a status (`VERIFIED / RUMOUR / OFFICIAL`). A legend in the footer
  explains the status tags.
- Layout is **split-pane**: a sticky left rail (~260px on desktop) holding the section index
  `01 NEWS 02 GUIDES 03 MAP …` with the active item in amber and a small fill bar; the right pane
  carries the content. On mobile the rail collapses into a horizontal scroll strip of the same
  numbered index under the sticky header — it must not become a hamburger drawer.
- Content is **tabulated** rather than carded: a dated log table for news (columns DATE / FILE /
  SUBJECT / STATUS) and a numbered procedure list for guides (NO. / PROCEDURE / TIER / DURATION).
  Rows highlight on hover with an amber 2px left rule.

### Page order (the stance — the index leads)
1. **Status bar** across the very top: `LEONIDA // ONLINE`, a static timestamp, `RELEASE T-<n> DAYS`,
   and the ZH/EN toggle styled as `[EN] [中文]`.
2. **Terminal header**: wordmark `USGAME` in mono with a blinking block cursor, nav as a numbered
   inline index, search as a mono input with a `/` hint, hamburger below 900px.
3. Ad placeholder below the header, drawn as a labelled `[ AD ]` slot in the same hairlines.
4. **Terminal index / quick entries** — the 8 quick entries as an indexed two-column list with `→`
   affordances; this is the hero of the page, opening with a one-line typed-out mission statement
   using the hero lede from the content pack. `<h1>` lives here.
5. **Evidence reel** — the trailer labelled `EVIDENCE 002 / OFFICIAL` in a 16:9 frame with a mono
   caption block: source, date, runtime, privacy note.
6. **News log** — the dated table described above, with a status filter (`ALL / OFFICIAL / RUMOUR /
   PATCH`) that actually filters. In-feed ad slotted as a table-derived block after row 4.
7. **Procedures (guides)** — numbered rows with tier + duration and a 2–3 line summary each.
8. **Videos** — 3 rows, each with the YouTube ID, title and runtime.
9. **Footer** — index of every section as a numbered list, the status-tag legend, the independence
   disclaimer, and an "end of file" terminal line. Ad placeholder at end of content.

### Deliberately NOT
Photography-led · a big cinematic hero · rounded corners · friendly marketing copy · parallax or soft
fades · emoji · any gradient other than the hairline grid.

---

## STANCE D — Poster Magazine（杂志封面）

**One line:** the homepage as a magazine — a cover you have to look at, cover lines you have to read,
and features laid out like spreads rather than cards.

### Reference vocabulary
A printed film magazine (Little White Lies, Sight & Sound) · Apple TV+ and A24 title pages · Criterion
cover design · oversized editorial cover typography.

### Art direction
- Ground: true black `#000` for the cover, then a clean `#0F0F10` for features. Cover type is warm
  cream `#F5EADB`; one electric accent — cyan `#35E1D0` — for rules, the active tab and the "in this
  issue" numerals. Nothing else gets colour.
- **Cover**: `hero-keyart` (1280×412, the wide official key art) as a full-bleed letterbox band across
  the top of the viewport, with the oversized display headline **overlapping** it — the type bleeds up
  past the image's bottom edge using `margin-top: -0.35em` on the headline block (use negative margin,
  not `transform`, which a `to{transform:none}` entry animation would cancel). Cover lines stack
  vertically at the right on desktop (`Inside: 142 collectibles mapped` / `The six-star problem` /
  `Why November 19 survived twice`), becoming a plain list under the headline on mobile.
- Display type: **Archivo Black** (fallback `Impact, "Arial Black", Bahnschrift`) for the cover, caps,
  tight negative tracking, `clamp(3rem, 11vw, 9rem)` — the size is the statement. Feature titles use a
  serif deck: **Playfair Display** (fallback `Georgia, Constantia`). Body: Inter.
- Sections are **spreads**, not grids: each feature is a full-width band with an asymmetric 2-column
  interior alternating side to side (`image 7fr / text 5fr`, then `text 5fr / image 7fr`). The wrap may
  be `max-width: 84rem`, but header, every spread and every footer row still share it exactly.
- A numbered **contents** list (01–08) does the work other variants give to cards: hairline rules, a
  big cyan numeral, the title, a one-line standfirst. Hover: the numeral slides, the row lifts 3%.
- No cards. No shadows. No radius above 4px. Rules and whitespace only.

### Page order (the stance — the cover leads)
1. Minimal top bar: wordmark left, nav inline, search icon, ZH/EN toggle, hamburger — deliberately
   thin so the cover owns the first screen.
2. **Cover** — `<h1>` is the cover headline (two lines, EN and ZH from the content pack), the deck
   (lede), one primary CTA (`Latest news`), the issue line (`ISSUE 01 · LEONIDA · 2026`), and the
   cover lines. The ad placeholder sits *below* the cover fold as a thin labelled strip so it reads as
   page furniture — never above the fold.
3. **In this issue** — the numbered contents list (quick entries + the 6 guides merged into one
   editorial list of 8 rows).
4. **Feature 01 — Official video**: the trailer as a full-width cinematic band with a serif caption
   and the attribution note. The centrepiece spread.
5. **Feature 02 — Latest news**: a 3-story editorial selection (not a 6-card grid) — one large story
   with a big image, two smaller with modest thumbnails — plus category filter tabs that filter.
   In-feed ad after the 3rd item.
6. **Feature 03 — Videos**: 3 items as a film strip: one landscape embed and two thumbnails in a row
   that scrolls horizontally on mobile.
7. **Subscribe page**: a full-width closing band styled as a magazine subscription card — cream type
   on black, one cyan CTA, dashed "front-end only" note.
8. Footer: thin, 4 columns, legal + independence disclaimer. Ad placeholder at end of content.

### Deliberately NOT
A card grid · a sidebar · utility chrome or badges/pills · a stats band · monospace · glow · anything
that reads as a dashboard.

---

## STANCE E — Bento Portal（工具门户）

**One line:** the homepage as a precision tool — a sticky search-first header, a bento grid of real
art tiles, and every answer one click away.

### Reference vocabulary
Linear · Vercel · Raycast · Arc · Apple product pages · the "bento grid" pattern as used by good game
wikis, not by marketing sites.

### Art direction
- Ground: neutral dark greys, cooled slightly — page `#0C0D10`, surface `#14161A`, raised `#1B1E24`.
  Text `#E7E9EE`, muted `#9AA0AC`.
- Accent: one acid lime `#C7F53B` for the primary button, the active tab, focus rings and the live
  dot. A second accent is **not** allowed.
- Surfaces use real art: every bento tile has a GTA VI image behind a dark scrim, with
  `object-fit: cover` + `filter: saturate(1.05)` and the label on top in solid contrast. Tiles are
  16px radius, 1px `rgba(255,255,255,.06)` border, soft layered shadow
  (`0 1px 2px rgba(0,0,0,.4), 0 12px 32px rgba(0,0,0,.28)`). **No glow.**
- Type: **Space Grotesk** for headings and numerals (fallback `Bahnschrift, "Segoe UI", sans-serif`),
  **Inter** for body/UI. Tight heading leading, `clamp(1.9rem, 4vw, 3rem)` — this variant is compact,
  not cinematic.
- The header is **sticky and functionally dense**: wordmark, inline nav, a search input styled as a
  command palette (with a keyboard hint on desktop), ZH/EN toggle, hamburger below 900px. On scroll it
  shrinks to a ~56px bar with a bottom hairline.
- The bento grid must tile exactly: plan the spans so the last row is full — no hole in the
  bottom-right. Suggested 4-column desktop layout for the 8 quick entries: a 2×2 hero tile
  (Interactive map), four 1×1 tiles, one 2×1 wide tile, two 1×1 tiles. Tablet 2 columns; mobile
  1 column, or two small squares on one row.
- Hover on a tile: image scales 1.05, scrim deepens, an arrow slides in — 200ms,
  `cubic-bezier(.22,.61,.36,1)`.

### Page order (the stance — the tools lead)
1. Sticky header with search.
2. Ad placeholder under the header, as a slim labelled slot that does not push the grid far down.
3. **Compact hero strip**: one line of positioning copy (`<h1>`, 2 lines max) over
   `hero-neon-night.webp` at low opacity, or beside a small art panel — but do **not** build a
   full-viewport cinematic hero; this variant's job is to reach the grid fast. Below the copy, a
   **stats band** with the 4 stats from the content pack (value big in Space Grotesk, label muted,
   hairline dividers between).
4. **Bento grid** — the 8 quick entries as described, plus the trailer as one wide tile so the video
   is part of the grid rather than a separate section. The centrepiece.
5. **Latest news** — a two-column split: left = a compact filterable list of the 6 news items (small
   thumb, title, category, date), right = a sticky rail with the trailer embed and the sidebar ad.
   The news category filter tabs must actually work. In-feed ad after the 4th news row.
6. **Guides** — 3-up cards with tier label, duration and a thin lime rule; hover lifts the card 2px.
7. **FAQ** — a 2-column accordion of 6 questions (your open/close interaction; keyboard operable with
   `aria-expanded`).
8. **Closing band + footer** — subscribe input with the dashed "front-end only, not wired" note, then
   a 4-column footer with the independence disclaimer and the language switch repeated. Ad placeholder
   at end of content.

### Deliberately NOT
Retro / synthwave / 80s Miami · grunge or grain · serif display type · full-bleed cinematic hero · a
split-pane terminal · print-magazine spreads · more than one accent colour.
