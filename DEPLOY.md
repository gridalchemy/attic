# Attic — publishing to GitHub Pages

Hand this whole file to Claude Code. The source zip from the chat has everything
needed; unzip it into the repo root first.

---

## 1. Repo setup

- [ ] Create a public repo. Suggested name: `attic`.
- [ ] Unzip the Attic source into the repo root so these files sit at top level:
      `kb.json` `principles.json` `master.json` `data.json`
      `build.py` `page3.py` `css3.txt` `js3.txt` `fonts.css`
      `REBUILD.md` `DEPLOY.md`
- [ ] Do **not** add a `.gitignore` that excludes `fonts.css` or `data.json`.
      `fonts.css` is 450KB of base64 typefaces and is load-bearing: without it the
      build fails and the privacy claim breaks. `data.json` is generated but cheap
      to keep and makes the repo clone-and-open.

## 2. Build the output

- [ ] Confirm `page3.py` writes `index.html` to the repo root and `build.py`
      writes `data.json` to the working directory.
- [ ] Rebuild and confirm `index.html` appears in the repo root:
      `python3 build.py && python3 page3.py`

## 3. Verify the build before committing

Run these against the freshly built `index.html`. All must pass.

- [ ] **Zero external resource loads.** No `src="http`, no `<link href="http`,
      no `url(http` in CSS, no iframes. One external `<a href>` is expected and
      correct: Peri's link to the portfolio.
- [ ] **18 `@font-face` rules, 18 base64 woff2 data URIs.** If these numbers drop,
      `fonts.css` did not load and the page is silently using fallback fonts.
- [ ] **Embedded JSON parses**, and contains 118 live entries, 15 dead, 27 principles
      in 6 groups, 10 topics.
- [ ] **The link accounting adds up.** `build.py` asserts this itself and prints
      `links 286 = 68 solo + 193 clustered + 25 killed`. If that assertion fails,
      `kb.json` was edited and a record is missing a `url`, `extra_urls`, `unlisted_urls` or `kill_cat`.
      The About page and the "What didn't survive" page both render from these numbers,
      so they can never drift from the data.
- [ ] **Deep links resolve.** `build.py` asserts the 131 keys (118 entry ids, 10 topic
      slugs, 3 page ids) are unique and hash-safe. Open the page and check that
      `#ui-vs-ux-2018`, `#foundations` and `#about` each land correctly, that the
      browser Back button moves between entries instead of leaving the site, and
      that typing in the search box does not fill the history.
- [ ] **These selectors all still exist** (a careless CSS splice deleted them once):
      `.srcs a` `.tagrow` `.tag` `.navback` `.chart` `.bar .fill` `.cardgrid`
      `.cardblock` `.hero h2` `.legend` `.pgroup`
- [ ] **Every font-size lands on an even pixel value.** All sizes are in rem at a
      16px root: valid values are .75 / .875 / 1 / 1.125 / 1.875rem.
- [ ] **Both palettes, both modes pass WCAG AA** (4.5:1) on every rendered text pair,
      including the blended selected-row backgrounds.
- [ ] **No second-person address to a specific reader.** Grep for `your career`,
      `your job hunt`, `your B2B`, `relevant to you`, `given you're`. Generic
      instructional "you" is fine; assuming who the reader is, is not.

## 4. GitHub Pages

- [ ] Settings → Pages → Source: Deploy from branch, `main`, `/ (root)`.
- [ ] Wait for the first deploy, then open the URL and check:
      - fonts render as Newsreader / Literata / Spline (not system fallbacks)
      - light/dark toggle works and persists across reload
      - the accent switch toggles Madder / Plum and persists
      - Peri opens the portfolio in a new tab
      - no console errors
- [ ] Note the live URL. You will need it for step 6.

## 5. README

- [ ] Write a short `README.md`: what Attic is, that it is one self-contained HTML
      file with no external requests, how to rebuild (`python3 build.py && python3 page3.py`),
      and that `kb.json` is the source of truth. Link the live Pages URL and the
      Claude artifact.

## 6. Add the source link to the About page (do this last)

Once the Pages URL exists, add one line to the colophon at the bottom of the About
page in `js3.txt`, after the existing "One HTML file. No dependencies." block:

> Source and data: <github URL>

Then rebuild, re-run the step 3 checks, and commit.

## 7. Keep both homes in sync

- [ ] Re-publish the updated `index.html` to the Claude artifact so the two match.
      Open the existing artifact and publish an update to it — **do not** use
      Unpublish. Unpublishing is permanent: that artifact can never be published
      again, and the URL dies for everyone who has it.
- [ ] From here on: edit the source, rebuild once, deploy to both. `kb.json` and the
      build scripts are the source of truth; the two URLs are just outputs.
