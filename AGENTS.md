# Agents

Constellation-wide rules: `~/work/capp/spine/AGENTS.md`. Read it once, then this. The map is
`docs/ARCHITECTURE.md`.

## Stack

Vanilla HTML, CSS and JS in one fragment, `index.html`. Python 3.10+ standard library for
`build.py`, `dev.py`, the tests and `check_sources.py`. No package manager, no dependencies.

## Commands

```bash
python3 -m unittest  # the proof — content parses, every tool cited, page builds (12 tests)
./dev.py             # 127.0.0.1:5656, rebuilds public/ on every page load
./build.py           # → public/index.html + public/fonts/
./build.py --check   # parse and validate the markdown only
./check_sources.py   # DOI citations against Crossref; run when a citation changes
```

The page's behaviour (the run, the fence, the ledger) has no JS test harness. Verify it in a
browser: start a run, reach Close, log it, mark it done on the ledger.

## Do not touch

`public/`. It's generated and gitignored. `fonts/` are copied from `~/personal/site/fonts`, so
keep them identical so the page can move onto paramv.com unchanged.

## Invariants

- **`index.html` is an artifact fragment**, the same format as paramv.com. `<title>` goes on
  line 1, and there's no doctype, html, head or body tag. The `/*DATA*/` placeholder inside
  `<script id="data">` is where `build.py` inlines the toolbox. Tests check all three.
- **No network requests from the page.** No CDN, no analytics, no fonts from anywhere but
  `fonts/`. The only outbound links are doi.org citations, followed on click.
- **No sounds.** The fence ends in words and a filled line, never audio.
- **The page never writes or suggests an intervention.** The sparring brief tells a model the
  same. Don't add "suggested interventions", ranking or scoring against a norm.
- **Every tool cites something.** The build fails otherwise. If you add a DOI, run
  `check_sources.py` before committing.
- **Storage key `cognitive-scaffolding.v1` and the run shape** (see ARCHITECTURE) are how
  the ledger is read back. A shape change needs a version bump and a migration in `load()`, or
  every existing ledger is orphaned.
- No colours in JS. State is CSS classes; tokens live in `:root`.

## Traps

- **A formatter hook rewrites `.md` and `.html` on Write/Edit.** It adds blank lines and can
  quote frontmatter values. `build.py` tolerates both. Don't start a frontmatter value with
  a quote mark when there are quotes inside it too: the unwrapping would mangle it.
- **`pagehide` saves the in-memory store.** Editing `localStorage` in devtools and then
  reloading gets overwritten by the old state. Two open tabs: the last writer wins.
- **Reveal-on-scroll:** blocks already in the viewport get `.in` synchronously after a layout
  read. Don't move that to `requestAnimationFrame`, because a background tab never runs it and
  the view stays blank.
- The clipboard API is refused in some embedded browsers. `copyBrief` falls back to a visible
  textarea plus `execCommand("copy")`.
