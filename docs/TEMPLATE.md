# Running your own

## What is Param's

| Thing                                            | Where                                | Replace with                       |
| ------------------------------------------------ | ------------------------------------ | ---------------------------------- |
| The first-person framing                         | `about.md`                           | your own reason for the scaffold   |
| Which tools exist and how they're worded         | `tools/*.md`                         | the tools your loops actually need |
| The six lenses                                   | `lenses/*.md`                        | the frames you overthink through   |
| Body states (includes "wired", "overstimulated") | `STATES` in `index.html`             | the states your body actually has  |
| Placeholder examples (dinners, essays)           | the `input(…)` calls in `index.html` | your own                           |
| Fence lengths 10/15/25                           | `FENCES` in `index.html`             | whatever you'll actually hold to   |

## What is the scaffold

The run's structure: fence, body, why → how, tools, lens, intervene, close. Also the rule that
an intervention has a cue and a direction. The ledger and its pending/done/dropped states. The
sparring brief's rules. The build that turns markdown into one offline page.

## Running it against your own life

1. Clone, then `python3 -m unittest`.
2. Rewrite `about.md`. Delete the tools you'd never reach for, and add yours with sources.
3. `./dev.py` and open http://127.0.0.1:5656.
4. Do one run on a real loop before changing anything else.

## What will not work yet

- `STATES`, `FENCES`, `TOWARD` and the placeholders are constants in `index.html`, not
  content files.
- The ledger lives in one browser. There's no sync, and no reading it from another tool.
