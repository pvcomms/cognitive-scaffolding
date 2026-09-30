# Decisions

Append-only. One entry per real decision, dated, with the why.

## 2026-09-30 — A run ends in an intervention, not a conclusion

The brief was "tools for structured overthinking" to break intellectualised rumination and
withdrawal. A reference list of biases would feed the loop it's meant to break: more material
to think about. So the core is a procedure with a stopping rule (the fence) and a required
output (an if-then aimed at a person, the body or the world). The toolbox is what the
procedure draws on. Grounding: rumination research (Watkins 2008), implementation intentions
(Gollwitzer & Sheeran 2006), self-perception (Bem 1972).

## 2026-09-30 — Static fragment + build.py, not Next.js

paramv.com's `/systems` already lists "Cognitive Scaffolding", and paramv.com is built from
artifact fragments by `build.py`. Writing this in the same format with the same fonts means it
can move onto the site later without a rewrite. It also opens from disk, offline, with no
install.

## 2026-09-30 — localStorage + Export/Import, not a local server

A server would put the ledger on disk as JSON, but then the page wouldn't work from `file://`
or from a static host. Per-browser storage with an export button is enough for one person on
one machine. Revisit if shosai should read the ledger, since that's the point where a
`~/…/ledger.json` earns a server.

## 2026-09-30 — One markdown file per tool

So the toolbox can be edited without touching code, per the standing preference. Frontmatter
for the structured fields, paragraphs for the argument, a Grounding list for sources. The
build enforces that every tool cites something.

## 2026-09-30 — DOIs on citations, checked against Crossref

28 of the 38 citations have DOIs, and each one's title and year match Crossref
(`check_sources.py`). The other 10 are books, a LessWrong post, an SRI report, and Schelling's
1984 AER lecture, which Crossref doesn't index. Its title was confirmed through the 2007
reprint.

## 2026-09-30 — No dependencies

Nothing here needs one. The stdlib covers the build, the dev server, the tests and the
Crossref check.
