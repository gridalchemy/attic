# Social preview card — repo task

Two things to add to the repo. Hand this file to Claude Code.

---

## 1. Put `og.png` at the repo root

Next to `index.html`, so that `https://gridalchemy.github.io/attic/og.png` resolves.
The meta tags below point at that exact URL.

`og-card.html` is the source the image was rendered from (1200×630, Newsreader and
Spline inlined). Keep it in the repo so the card can be regenerated later. It was
rendered headless at a device scale factor of 1.

Verify by opening the og.png URL directly in a browser before posting anywhere.

---

## 2. Add these tags to `page3.py`

Insert immediately **after** the existing `<meta name="description" ...>` line in the
`H = f"""..."""` block, and **before** `<style>{fonts}</style>`.

```html
<link rel="canonical" href="https://gridalchemy.github.io/attic/">
<!-- Social preview. Read only by link crawlers, never fetched by a visitor's
     browser, so the page still makes zero external requests. -->
<meta property="og:type" content="website">
<meta property="og:url" content="https://gridalchemy.github.io/attic/">
<meta property="og:site_name" content="Attic">
<meta property="og:title" content="Attic — a salvaged UX reading list">
<meta property="og:description" content="286 links of supplementary reading from a UX design curriculum that no longer exists, read again and written up as 118 entries.">
<meta property="og:image" content="https://gridalchemy.github.io/attic/og.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Attic — a salvaged reading list. 286 links, read again and written up as 118 entries.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Attic — a salvaged UX reading list">
<meta name="twitter:description" content="286 links of supplementary reading from a UX design curriculum that no longer exists, read again and written up as 118 entries.">
<meta name="twitter:image" content="https://gridalchemy.github.io/attic/og.png">
```

It goes in `page3.py`, not into `index.html` by hand, so it survives every rebuild.

Then `python3 build.py && python3 page3.py` and commit.

### Why this does not break the privacy claim

These tags are metadata. A visitor's browser never requests `og.png`; only a link
crawler does, server-side, when someone pastes the URL. The page itself still makes
zero external requests, the fonts are still embedded, and the About page copy stays
true.

Verify after rebuilding — all three must still return nothing:

```bash
grep -o 'src="https\?://' index.html
grep -o '<link[^>]*rel="stylesheet"[^>]*href="https\?://' index.html
grep -oE 'url\(\s*"?https?:' index.html
```

---

## 3. Before posting: flush the LinkedIn cache

LinkedIn caches link previews hard and will keep serving an imageless card if it
saw the URL before the tags existed. Run the URL through the **LinkedIn Post
Inspector** once the commit is live, then post.

---

## 4. The 286 accounting — already correct, do not "fix" it

Checked against the live page: `links_total` is 286, 260 links render as clickable
sources, 25 are on the dead page, and exactly **1** is counted but deliberately
unlisted. That one is the CareerFoundry sign-in URL, held by `unlisted_urls`.

That is the intended behaviour, not drift. The number 286 is how many unique URLs
were saved in 2021-22, which is a fact that should not move because one of them
leads nowhere. Leave the field, the counts and the copy exactly as they are.

**Do not** re-add the sign-in URL to `extra_urls`, and do not change any 286 to 285.

---

## 5. Favicon — currently missing

The page has no `rel="icon"`, so the browser tab shows a blank default document icon.
`peri-favicon.svg` in this handover is the filled Peri, recoloured to Attic's Madder
palette, with its own light/dark media query inside the SVG (a tab icon cannot
inherit page CSS, so the colours are baked in).

- light: body `#1D2816`, antenna `#862721`
- dark:  body `#DCE1B9`, antenna `#F98F82`

Checked at 16, 32, 64 and 128px in both schemes. The silhouette and the antenna dot
both still read at 16px. The filled variant is deliberate: the outline Peri used in
the footer disappears at tab size.

**Embed it, do not link it.** A linked icon file would be an external request and
would break the privacy claim. Inline it as a data URI, using the same pattern
`page3.py` already uses for the fonts.

Add `peri-favicon.svg` to the repo root, then in `page3.py`:

```python
import base64
fav = base64.b64encode(open('peri-favicon.svg','rb').read()).decode()
```

and in the `H = f"""..."""` head, next to the other tags:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{fav}">
```

Keeping the SVG as a file means the icon stays editable; the build inlines it.

### Optional, same place

Tints the browser chrome on mobile to match the page. No request, two lines:

```html
<meta name="theme-color" content="#F4F5EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#21261A" media="(prefers-color-scheme: dark)">
```

---

## Order of operations before posting

1. Commit the tags, `og.png`, `og-card.html` and `peri-favicon.svg`; rebuild; push.
2. Open `https://gridalchemy.github.io/attic/og.png` directly and confirm it loads.
3. Run the site URL through the LinkedIn Post Inspector to flush the cached preview.
4. Then post.

Doing 4 before 2 is the one ordering that bites: LinkedIn will cache an imageless
card and keep serving it. Share the GitHub Pages URL, not the artifact URL, since
that is the one these tags describe.

