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
