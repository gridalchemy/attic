# Attic

**A salvaged UX reading list.** → **[gridalchemy.github.io/attic](https://gridalchemy.github.io/attic/)**

In 2021–2022 I saved 286 links of supplementary reading from a UX design
program. The program and its platform have since shut down. In 2026 I went
back through every link, kept what still worked, read it, and wrote it up.
The one link left out, the old course sign-in page, is the reason the rest
exists.

286 saved links → 118 entries, plus 15 recorded as lost.
143 links were absorbed into clusters where several pieces made the same
argument, and 25 were cut. The About page and "What didn't survive" page show
the full accounting.

Most of what gets published online does not last. This is a small attempt to
make sure the thinking outlives the pages.

## What it is

One self-contained HTML file, [`index.html`](index.html). No dependencies, no
external requests, no tracking, no cookies, no login. The typefaces are
base64-embedded rather than loaded from a font service, so nothing about a
visit leaves the browser. The only outbound links are the ones you click.

Also mirrored as a Claude artifact:
[claude.ai/artifact/J4MMwCUqUFWGsQAMLmMd8x](https://claude.ai/artifact/J4MMwCUqUFWGsQAMLmMd8x)

## Source of truth

[`kb.json`](kb.json) holds every record: title, author, source, topic, summary,
key points, URLs, and why a link was cut. Everything else is generated from it
or assembles around it.

| File | Role |
| --- | --- |
| `kb.json` | The archive. Edit this. |
| `principles.json` | 27 principles in 6 groups |
| `master.json` | Original inventory of all 286 links, used to check nothing was missed |
| `build.py` | `kb.json` → `data.json`, with link-accounting and deep-link assertions |
| `page3.py` | Fonts + CSS + JS + data → `index.html` |
| `css3.txt`, `js3.txt` | Stylesheet and app logic |
| `fonts.css` | Embedded woff2 typefaces. Required: the build fails without it |
| `data.json` | Generated, kept so the repo is clone-and-open |

## Rebuild

Needs Python 3, nothing else.

```bash
python3 build.py && python3 page3.py
```

(On Windows, `python` instead of `python3`.) `build.py` refuses to build if the
link counts stop adding up to 286 or if any deep-link key collides. See
[`REBUILD.md`](REBUILD.md) for the fonts step and pre-publish checks, and
[`DEPLOY.md`](DEPLOY.md) for the publishing checklist.

## Credits

Links saved 2021–2022. Read, written and assembled with Claude, 2026.
Every entry paraphrases and links out to its source, which belongs to whoever
wrote it.

Made by [Iulia](https://icvc.framer.website/).
