# Common brief — GTA VI homepage design sketches (usgame.net)

You are producing **ONE throwaway design sketch**: the homepage of a GTA VI news & guides site
(`usgame.net`), delivered as a **single self-contained HTML file**. It is a design artefact for the
owner to compare against four sibling variants; it is not production code.

## 1. Read these first

| File | Why |
|---|---|
| `D:/【建立网站】/GTA6/usgame.net/design/content-pack.json` | **All copy comes from here.** Nav labels, hero lines, 6 news items, 6 guide items, 8 quick entries, stats, videos, footer, UI strings — with EN and ZH for every field. Use the text verbatim. Do **not** invent article titles. |
| `D:/【建立网站】/GTA6/usgame.net/design/assets/img/` | Local images (WebP). Slugs below. |
| Your own stance file, named in your task | The visual direction you must execute. |

Image slugs available:
`hero-keyart` `hero-sunset` `hero-neon-night` `scene-airboat` `scene-plane` `scene-beach`
`scene-pool` `scene-car-night` `scene-keys` `scene-street-night` `scene-dance` `scene-panther`
`scene-turtle` `scene-weapons` `scene-festival` `scene-boxart` `scene-tropical` `scene-moody`
`card-lucia` `card-jason` `card-ambrosia` `card-grassrivers`

Reference them with a **relative** path from your HTML file, e.g. `../assets/img/hero-sunset.webp`.
Your file lives at `D:/【建立网站】/GTA6/usgame.net/design/<your-folder>/index.html`.

## 2. Hard constraints

1. **One file.** One inline `<style>`, one inline `<script>`. No build step.
2. **No external JS.** No Tailwind CDN, no icon font, no jQuery. Icons = inline SVG (hand-written,
   `stroke="currentColor"`, 1.5–1.75 stroke width) or CSS shapes.
3. **Exactly one external resource is allowed**: a Google Fonts `<link>` (max 2 families) — always
   followed by a real local fallback stack so the page still looks intentional offline.
   Windows system fonts you may fall back to: `Bahnschrift`, `Impact`, `Franklin Gothic Medium`,
   `Georgia`, `Constantia`, `Palatino Linotype`, `Consolas`, `Cascadia Mono`, `Segoe UI`.
4. **Responsive**: must render correctly and attractively at **1440px and at 390px**. Fluid layout,
   `clamp()` for type, no fixed page widths. Test both.
5. **The language toggle must actually work.** One inline JS dictionary drives EN ⇄ ZH for all nav
   labels, section headings, buttons, UI strings, and the 6 news titles/excerpts + 6 guide titles.
   Default state = **EN**. Put the toggle in the header on desktop and inside the mobile menu too.
6. **Real interactivity**, all three:
   - one filter/tab that visibly filters a list (e.g. news by category, or quick entries by type);
   - one open/close (mobile hamburger menu, accordion, or expandable panel);
   - hover/focus states on every card, button and link.
7. **Images**: every `<img>` needs `alt`, intrinsic `width`/`height` (or CSS `aspect-ratio`), and
   `loading="lazy"` — except the hero image, which is `loading="eager"` + `fetchpriority="high"`.
   Never stretch a 1280×412 key art into a square; crop with `object-fit: cover`.
8. **AdSense**: include the loader exactly once in `<head>`
   ```html
   <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9680789453651246" crossorigin="anonymous"></script>
   ```
   and **4 clearly-labelled ad placeholder containers**: below the nav, in-feed after the 4th news
   card, in the sidebar (or equivalent secondary column), and at the end of the content. Each shows
   the visible word **Advertisement / 广告** plus its intended size from `content-pack.json → ads`.
   Placeholders are dashed/hairlined boxes with a muted label — never hidden, never disguised as
   content, never more prominent than the content around them.
9. **Trailer embed** in a prominent position, responsive 16:9 via `aspect-ratio`, using exactly:
   `https://www.youtube-nocookie.com/embed/VQRLujxTm3c?si=BV4Rlx2bLlOjeuQU&start=3`
   with `loading="lazy"`, a `title` attribute, `allowfullscreen`.
10. **Accessibility**: semantic `header/nav/main/section/article/footer`, exactly one `<h1>`,
    visible `:focus-visible` rings, a skip link, `aria-label` on icon-only buttons,
    `aria-expanded` on the hamburger, `aria-current="page"` on the active nav item.
11. **Motion**: only CSS transitions / keyframe animations. Every entry animation must be wrapped in
    `@media (prefers-reduced-motion: no-preference)` **or** cancelled by
    `@media (prefers-reduced-motion: reduce){*{animation:none!important;transition:none!important}}`.
    One `animation` shorthand per element — two on the same element silently override each other.

## 3. Layout rules (measured — the owner is sensitive to misalignment)

- **Exactly one text axis.** Every section's container is `.wrap{max-width:<72–80rem>;margin:0 auto;
  padding-inline:24px}` (pick one value and reuse it for header, main sections and footer).
- **Never** give a heading block its own `max-width` + `margin:0 auto` — that creates a second
  centre, and it is the #1 defect the owner has caught before. Measured drift was 136px.
- If you use cards, **one** horizontal padding value site-wide (22, 24 or 28 — not a mix).
- Header container, all section containers and the footer container share the same max-width and the
  same `padding-inline`.
- A section eyebrow/badge goes **above** its heading, not to the left of it (left-side badges indent
  the heading text off the axis by the badge width).
- Chinese body copy: `text-align: justify`, headings left; CJK paragraph `line-height >= 1.75`.
  No drop caps for Chinese.
- **Zero horizontal overflow** at any width — nothing may extend past the wrap's right edge.

## 4. Design quality bar — this is the part that decides whether the variant survives

- It must **not** look like generic AI output. Banned: purple→blue gradient on white; three
  identical rounded cards with a generic line icon each; emoji used as icons; "Lorem ipsum"; a
  hero that is just centred text on a gradient; the same card repeated six times.
- **Restraint.** One accent colour (or one tight pair). One radius scale. One shadow scale.
  If everything has a glow, nothing does.
- **Tone of voice**: GTA VI swagger — confident, concrete, slightly lurid. Short sentences.
  Real numbers. No "Welcome to our website, your one-stop destination".
- Type and colour choices must be **defensible**. At the top of the file write an HTML comment
  (≤ 14 lines) stating: the stance in one sentence, the reference sites/artefacts you are stealing
  from, the type + colour decisions and why, and what this variant deliberately is **not**.
- Ship a page the owner can scroll end to end. No half-finished section, no stray `TODO`.

## 5. Self-check before you return

Run these in the file (a browser, or by reading your own CSS carefully) and fix what fails:

- [ ] At 1440px and at 390px: no horizontal scrollbar; nothing clipped; no overlap.
- [ ] `document.querySelectorAll('h1').length === 1`.
- [ ] Grep your file: no `<script src` other than the AdSense loader; no `tailwind`; no `cdn.`.
- [ ] Every structural left edge (brand, h1, section headings, lede, footer) measures the same value
      ±1px at 1440px. Measure with:
      `el.getBoundingClientRect().left + parseFloat(getComputedStyle(el).paddingLeft)`.
- [ ] All 4 ad placeholders are visually labelled and none is hidden.
- [ ] The ZH toggle changes at least 20 visible strings.

## 6. Return

Report back: the absolute file path · file size in KB · a 3-sentence description of the visual
stance · the one deliberate trade-off you made · anything you could not verify.
