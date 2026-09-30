---
title: Host it behind "Cognitive Scaffolding" on paramv.com /systems
status: shipped
created: 2026-09-30
---

# 002 — Host it behind "Cognitive Scaffolding" on paramv.com /systems

## Why

`~/personal/site/systems.html` listed Cognitive Scaffolding with nothing behind it. Param said
"host it on paramv.com /systems", which is the explicit go for a public surface.

## What changes

- Before: `/systems` showed a bare "Cognitive Scaffolding" line, and the page existed only on
  localhost.
- After: `/systems` links the line, with a one-line description and "2026 · live", to
  `paramv.com/systems/cognitive-scaffolding`. That page is the same run, toolbox and ledger,
  dark-only, behind the site's load gate, with a "← systems" link. It's listed in sitemap.xml and llms.txt.

## Where

| File                                     | Change                                                            |
| ---------------------------------------- | ----------------------------------------------------------------- |
| `build.py`                               | `--site DIR` writes `DIR/cognitive-scaffolding.html`              |
| `index.html`                             | `light:start/end` markers, `<!--SITE-NAV-->` slot, `.crumb` style |
| `test_build.py`                          | the site fragment's shape; refuses without a gate to copy        |
| `~/personal/site/cognitive-scaffolding.html` | new, generated                                                |
| `~/personal/site/build.py`, `dev.py`     | page, nested output path, sitemap, llms.txt; dev route            |
| `~/personal/site/systems.html`           | the line becomes a link                                           |
| `~/personal/site/AGENTS.md`              | the generated page and the gate count                             |

## Out of scope

A shared or synced ledger. Analytics of any kind.

## Acceptance checks

```bash
python3 -m unittest                                          # Ran 15 tests … OK
./build.py --site ~/personal/site                            # wrote /Users/p/personal/site/cognitive-scaffolding.html
curl -s -o /dev/null -w "%{http_code}\n" https://paramv.com/systems/cognitive-scaffolding   # 200
curl -s https://paramv.com/systems | grep -o 'href="/systems/cognitive-scaffolding"'     # one match
curl -s https://paramv.com/sitemap.xml | grep -c cognitive                               # 1
```

All ran and passed on 2026-09-30. Site commit f8b9df7, deployment dpl_7vSADyRbUt6ibMmoG4BpSmiAyF4K
aliased to paramv.com.

- [x] Fresh session: the proof-of-work gate shows, then opens by itself
- [x] Fonts load from `/fonts/` at the nested path. No console errors on production
- [x] 375px: the header holds two rows, with no horizontal scroll
