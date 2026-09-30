# Cognitive Scaffolding

Tools for structured overthinking, so the thinking ends in something done.

A local page with three views. **Run** takes one loop you're going round on through six steps inside a fixed time limit, the fence. It ends by asking for an intervention: a when-then you'll do, aimed at a person, the body or the world off the screen. **Toolbox** holds seventeen reasoning tools in six families, plus six lenses. Each tool has a move, the question you answer in a run, and its sources. **Ledger** keeps every run and whether its intervention happened.

Every run ends in an intervention, not a conclusion.

## What it reads, what it writes, what never leaves the machine

| Path                                                   | Direction         | What                                              |
| ------------------------------------------------------ | ----------------- | ------------------------------------------------- |
| `about.md`, `families.md`, `tools/*.md`, `lenses/*.md` | read at build     | the toolbox, written by hand                      |
| `public/index.html`                                    | written by build  | the page: one file with the toolbox inlined       |
| browser `localStorage`, key `cognitive-scaffolding.v1` | read + write      | the open run and the ledger, in that browser only |
| `cognitive-scaffolding-YYYY-MM-DD.json`                | written on Export | a copy of the ledger, wherever the browser saves  |

The page makes no network requests. Fonts are self-hosted. The DOI links in the toolbox go to doi.org, and only when you click one. `check_sources.py` calls api.crossref.org, and only when you run it.

## Prerequisites

Python 3.10 or later, standard library only. A browser.

## Run

```bash
./dev.py             # http://127.0.0.1:5656 — rebuilds on every page load
./build.py           # → public/index.html, which also opens straight from disk
python3 -m unittest  # the proof: content parses, every tool is cited, the page builds
./check_sources.py   # every DOI citation against Crossref (network)
./build.py --site ~/personal/site   # also regenerate the paramv.com page (then build + deploy the site)
```

## How it works

A run opens when you name the loop and pick a fence of 10, 15 or 25 minutes. The steps are **Body** (one physical move, the body's state, the belief under the loop, how sure you are), **Why → how** (rewrite the abstract question as a concrete one), **Tools** (up to three, one line each), **Lens** (optional: one of philosophy, realpolitik, critical theory, state of the world, science or social science, each with a guard), **Intervene** and **Close** (re-rate the belief, log it). The fence runs in the header. When it's up, the page says so in words and points you to the intervention. There's no sound, ever.

The intervention step won't go on until you've written the when and the "I will", and ticked at least one direction: another person, the body, or the world off the screen. Withdrawal is the loop's default direction, and this is the one hard rule. The page never proposes an intervention.

The lens step can copy a sparring brief for a model. The brief carries the run so far and a set of rules. The model asks one question at a time, gives no reassurance and no verdict, points out skipped steps and attacks on the source rather than the claim, and after five questions at most it has to ask for your intervention without suggesting one.

A logged run sits in the ledger as pending until you mark it done or dropped. The ledger counts runs, done, pending, dropped, done toward a person, and the median certainty before and after. A done intervention is a vote for the type of person who does interventions.

## Editing the toolbox

One markdown file per tool in `tools/`. Refresh `./dev.py` to see a change.

```markdown
---
name: Schelling fence
family: exit # an id from families.md
order: 1 # position inside the family
when: The loop has no natural end, so it doesn't end.
move: The operation, in a sentence or two.
ask: The question answered in one line during a run.
---

A paragraph or two. _Italics_ work. Nothing else is markdown.

## Grounding

- Author, A. (Year). Title. _Journal_, 1(2), 3–4. https://doi.org/…
```

The build fails if a tool has no grounding or names a family that doesn't exist. Lenses in `lenses/` take `name`, `order`, `question` and `guard`. The framing at the top of the toolbox is `about.md`.

## Part of the constellation

A personal tool, built because it's useful. It's not the Center's output. It's hosted publicly at [paramv.com/systems/cognitive-scaffolding](https://paramv.com/systems/cognitive-scaffolding), linked from `/systems`. Every visitor's ledger stays in their own browser. It keeps the constellation rules: local by default, flat files, no dependencies, and the tool never decides. The run demands an intervention but never writes one, and the sparring brief forbids a model from writing it too. `docs/TEMPLATE.md` says what is Param's and what is the scaffold.
