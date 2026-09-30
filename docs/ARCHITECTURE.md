# Architecture

## In one paragraph

A static page built from markdown. `build.py` reads the toolbox (`about.md`, `families.md`,
`tools/*.md`, `lenses/*.md`), turns it into JSON, inlines that into the `index.html` fragment,
wraps the fragment in a real document and writes `public/index.html` with the fonts beside it.
In the browser, one IIFE renders three views from the URL hash (`#run`, `#toolbox`,
`#ledger`) and keeps all state in `localStorage`. No server is needed. `dev.py` is only a
rebuild-on-refresh convenience.

## The tree

```
cognitive-scaffolding/
  index.html        the fragment: <title>, <style>, header, <main id="app">, data slot, app JS
  about.md          the framing at the top of the toolbox (first person, Param's)
  families.md       "## id · Name" + one line, in display order
  tools/*.md        one tool per file: frontmatter + paragraphs + "## Grounding" list
  lenses/*.md       one lens per file: name, order, question, guard
  build.py          markdown → JSON → public/index.html; --check validates only
  dev.py            127.0.0.1:5656, rebuilds on every page load
  test_build.py     python3 -m unittest
  check_sources.py  DOI citations vs Crossref (network, by hand)
  fonts/            Newsreader + IBM Plex Mono woff2, same files as paramv.com
  public/           generated, gitignored
```

## Data flow

```
tools/*.md ─┐
lenses/*.md ├─ build.load() ─ inline() escapes + <em> + doi links ─ JSON ─┐
about.md ───┤                                                              ├─ wrap() ─ public/index.html
families.md ┘                                        index.html fragment ─┘

browser: #data JSON ─▶ D ─▶ render() by hash ─▶ viewRun / viewToolbox / viewLedger
         input/change/click delegated on #app ─▶ store.current (the open run) ─▶ save() ─▶ localStorage
         Log the run ─▶ store.runs.unshift(run) ─▶ ledger (pending → done | dropped)
```

The toolbox strings in `D` are already HTML-safe (escaped at build). Everything the person
types goes through `esc()` before it touches `innerHTML`.

## What it reads and writes

| Path                                       | Direction    | What                                          |
| ------------------------------------------ | ------------ | --------------------------------------------- |
| `localStorage["cognitive-scaffolding.v1"]` | read + write | `{ v: 1, runs: Run[], current: Run \| null }` |
| Export → `cognitive-scaffolding-DATE.json` | write        | `{ v: 1, exported, runs }`                    |
| Import ← any export                        | read         | merged by run `id`, existing runs kept        |

`SCAFFOLD_PORT` changes the dev port (default 5656).

A run:

```
{ id, started, fence (min), loop, step (open runs only), fenceHit,
  body: { moved, states[], belief, sure 0–100 },
  why, how, tools: [{ id, answer }] (≤3), lens: { id, answer } | null, spar,
  act: { when, will, toward[] ⊂ person|body|world, by today|tomorrow|week, obstacle, ifObstacle },
  sureAfter, note, ended, status pending|done|dropped, resolved }
```

## Invariants

- The Intervene step's Next and Close's "Log the run" stay disabled until `when`, `will` and
  one `toward` are filled (`actReady`). This is the scaffold's one hard rule.
- The fence is set before the run starts and can't be changed from inside it.
- Tool ids are file stems. Renaming a tool file orphans its answers in old runs. The ledger
  shows the raw id instead of crashing, but prefer not to rename.

## Known sharp edges

- `render()` replaces `#app` wholesale. It animates only when the view/step key changes
  (`ui.lastKey`), so in-place re-renders like picking a tool or marking done don't replay
  the reveal.
- Open ledger entries survive re-renders through `ui.open`, fed by a capturing `toggle`
  listener, because `toggle` doesn't bubble.
- A run's fence counts from `started`, wall-clock. A run left open overnight shows "fence up"
  the next morning, which is correct.
