# The public site

Builds `../../bigfoot200-training/` from this repo:

| Output | Built from |
|---|---|
| `index.html` | `template.html` + `../plan/schedule.json` |
| `log.html` | `../tracker/template.html` + `../tracker/weeks.json` |
| `blocks.html` | `../plan/block-targets.md` |
| `plan.html` | `../plan/sub100-plan.md` |

    make dashboard

`bigfoot200-training` is a **view**. Never edit its HTML — it is overwritten every
build. Then:

    cd ../bigfoot200-training && git add -A && git commit -m "Regenerate" && git push

## Not published

`plan/runner-manual-2026.md` — Destination Trail's copyrighted manual. `build.py`
hard-refuses to finish if a file matching `runner-manual` appears in the public repo.

## No dependencies, on purpose

The build uses only the Python standard library. `md.py` is a small Markdown
renderer written for this repo precisely so `make` behaves identically on the
Mac mini, the MacBook and any sandbox with no `pip install` on any of them.
Do not reintroduce a third-party import here — it will work on whichever machine
you were sitting at and break on the other two.

## Files here

- `template.html` — the Today page. Data-driven via `/*__DATA__*/`.
- `doc_shell.py` — page shell for the markdown-rendered pages.
- `nav.py` — the shared nav bar, injected after `<body>` on every page.
- `md.py` — stdlib-only Markdown renderer (headings, GFM tables, blockquotes, lists, inline).
- `build.py` — the build.

Still hardcoded in `template.html`: a few dated Block-1 Saturday prescriptions
(Angels Rest, Three Sisters). One-off workout notes, not schedule data.
