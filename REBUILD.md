# Attic — rebuild instructions

Upload this whole folder at the start of a new chat. The container resets
between sessions, so nothing here survives otherwise.

## Files
- `kb.json`      — THE SOURCE OF TRUTH. 133 records (118 live, 15 killed).
                   Every entry: id, title, author, source, year, module,
                   submodule, cat (topics), tier (A/B/C), summary (markdown),
                   key_points, still_relevant, url, extra_urls, kill_reason.
                   Optional unlisted_urls: saved links that count toward
                   the 286 but are not shown (e.g. the course sign-in page).
                   This is deliberate, not drift: 286 is how many unique URLs
                   were saved in 2021-22, and that fact does not change because
                   one of them leads nowhere. 260 render as sources, 25 sit on
                   the dead page, 1 is unlisted. Do not move the sign-in URL
                   back to extra_urls, and do not change any 286 to 285.
- `principles.json` — 27 principles in 6 themed groups
                   (was 38 flat; merged Oct 2026). Shape: [{g, d, items[]}].
- `master.json`  — original Pearltrees inventory, 286 unique links, with
                   module/submodule paths. Used to verify nothing is missed.
- `build.py`     — kb.json -> data.json (markdown converted to HTML).
- `css3.txt`     — stylesheet.
- `js3.txt`      — app logic (nav, views, copy for About/home).
- `page3.py`     — assembles fonts + css + js + data into the final HTML.
- `fonts.css`    — base64-embedded woff2 faces. INCLUDED NOW, so the npm
                   step below is only needed if a typeface changes.
- `data.json`    — generated; rebuild it rather than editing it.
- `peri-favicon.svg` — the tab icon: filled Peri in the Madder palette, with
                   its own light/dark media query, because a tab icon cannot
                   inherit page CSS (light: body #1D2816, antenna #862721;
                   dark: body #DCE1B9, antenna #F98F82). page3.py embeds it as
                   a base64 data URI. Never link it as a file: that would be an
                   external request. The filled variant is deliberate; the
                   outline Peri from the footer disappears at 16px.
- `og.png`       — the social preview card, 1200x630. Only link crawlers fetch
                   it, never a visitor's browser. Its URL is hard-coded in the
                   og:/twitter: tags in page3.py, so it must stay at the root.
- `brand/`       — sources, not used by the build. `og-card.html` renders
                   og.png (fonts inlined; 1200x630 at device scale factor 1);
                   `favicon-preview.png` shows the favicon at 16-128px.

## Rebuild
```bash
cd <folder>
# fonts.css is already in this folder — skip straight to the two python steps.
python3 build.py && python3 page3.py
```

### Only if a typeface changes
```bash
npm install @fontsource/literata @fontsource/newsreader @fontsource/gloock \
  @fontsource/instrument-sans @fontsource/schibsted-grotesk @fontsource/heebo \
  @fontsource/spline-sans-mono @fontsource/martian-mono @fontsource/courier-prime
# regenerate fonts.css: base64-embed the latin woff2 subsets (see fonts step below)
python3 build.py      # kb.json -> data.json
python3 page3.py      # -> index.html
```

## Fonts step
Embed as base64 data URIs, never link to Google Fonts. A Munich court ruled
in 2022 that embedding Google Fonts without consent breaches GDPR, and the
site's privacy claim depends on zero external requests. Latin subsets only.
Faces in use: Literata 400/400i/600/700, Newsreader 400/400i/600,
Gloock 400, Instrument Sans 400/600, Schibsted Grotesk 400/600, Heebo 400/500/700,
Spline Sans Mono 400, Martian Mono 400, Courier Prime 400.

## Verify before publishing
- zero matches for `(src|href)="https?://` outside the entry source links
- the embedded JSON parses
- these selectors all still exist: .srcs a, .tagrow, .tag, .navback, .chart,
  .bar .fill, .cardgrid, .cardblock, .hero h2, .legend
  (a careless CSS splice deleted all of them once)
- every font-size lands on an even pixel value
- no second-person address to a specific reader. Generic instructional
  'you' is fine; assuming who the reader is, is not. The archive is public.
