---
title: The run, the toolbox and the ledger
status: shipped
created: 2026-09-30
---

# 001 — The run, the toolbox and the ledger

## Why

Param's pattern is intellectualised rumination that ends in withdrawal: a problem gets run
through philosophy, realpolitik, critical theory and the science, and the result is
understanding plus isolation. He wanted "cognitive scaffolding", a reasoning toolbox that
turns the overthinking into interventions that change his lived experience and, through them,
the kind of person he takes himself to be.

The tool must not decide for him. It demands an intervention and structures it (cue, direction,
deadline, obstacle), but it never proposes one. The sparring brief carries the same rule to any
model he uses.

## What changes

- Before: nothing. `/systems` on paramv.com named "Cognitive Scaffolding" with nothing behind it.
- After: a local page. **Run** takes a loop through a fenced, six-step procedure that ends in a
  logged if-then. **Toolbox** has 17 cited tools in 6 families and 6 lenses with guards.
  **Ledger** tracks every run as pending, done or dropped.

## Where

| File                                                   | Change                         |
| ------------------------------------------------------ | ------------------------------ |
| `index.html`                                           | new — the page fragment        |
| `about.md`, `families.md`, `tools/*.md`, `lenses/*.md` | new — the content              |
| `build.py`, `dev.py`                                   | new — build and dev server     |
| `test_build.py`, `check_sources.py`                    | new — tests and citation check |

## Out of scope

Linking from paramv.com (002). Syncing the ledger across devices. Reminders or notifications
for pending interventions, since there are no sounds and no nagging. Suggesting interventions.
Scoring runs.

## Acceptance checks

```bash
python3 -m unittest   # Ran 12 tests … OK
./build.py            # 17 tools in 6 families, 6 lenses / wrote …/public/index.html
./check_sources.py    # all DOI citations match Crossref  (28 ok, 10 nodoi)
```

- [x] A run started from the Run view reaches Close, logs, and appears on the ledger as pending
- [x] Intervene's Next stays disabled until when, "I will" and one direction are filled
- [x] The fence shows `fence up`, fills the header line and puts a banner on steps 1–4
- [x] Done on the ledger moves the tally. The entry shows every field of the run
- [x] Toolbox deep links (`#toolbox/<id>`) open the right card
- [x] No horizontal scroll at 375px, and the light and dark schemes both render

## Notes

The clipboard API was refused in the in-app browser used to verify this, and the textarea
fallback worked. On localhost in a normal browser, the clipboard path is the one that runs.
