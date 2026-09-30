# Contributing

## Before you start

Read `AGENTS.md`, then `docs/ARCHITECTURE.md`. That's the map.

## The unit of work

One feature is one file in `docs/features/`, numbered in creation order and never
renumbered. A spec ends with acceptance checks that are commands with expected output.

Adding or rewording a tool isn't a feature. Edit `tools/<id>.md`, keep it cited, and run the
checks below.

## Check by hand

```bash
python3 -m unittest   # Ran 13 tests … OK
./check_sources.py    # all DOI citations match Crossref (only if a citation changed)
```

There's no CI. The page's behaviour is checked in a browser: start a run, reach Close, log it,
mark it done on the ledger.

## What a change must respect

Local by default: the page makes no requests. Flat files: markdown for the toolbox, JSON for
the ledger export. The tool never decides: nothing proposes an intervention, ranks the tools or
scores a run. No sounds. No new dependency without a dated entry in `docs/DECISIONS.md`.

## Style

Plain declarative prose, no emoji. Code matches its neighbours. Commit subjects say what
changed and why it mattered.
