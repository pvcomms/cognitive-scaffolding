#!/usr/bin/env python3
"""Check every citation that carries a DOI against Crossref: title and year must match.

Covers tools/*.md and the two Watkins references in index.html. Citations without a DOI
(books, a LessWrong post, an SRI report, the 1984 AER lecture) are listed, not failed.
Network: api.crossref.org only. Run by hand when a citation changes; not part of the build.
Exit 1 if any DOI citation disagrees with Crossref.
"""
import json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).parent
DOI_RE = r"https://doi\.org/(\S+)"


def refs():
    for p in sorted((ROOT / "tools").glob("*.md")):
        _, _, g = p.read_text().partition("## Grounding")
        for line in g.splitlines():
            if line.strip().startswith("- "):
                yield p.stem, re.sub(r"[*_]", "", line.strip()[2:])
    page = (ROOT / "index.html").read_text()
    for m in re.finditer(r'"(Watkins, E\. R\..*?)";', page, flags=re.S):
        text = re.sub(r"<[^>]+>", "", m.group(1)).replace("&amp;", "&")
        yield "run", re.sub(r"doi:\S+", "", text).strip() + " " + " ".join(
            f"https://doi.org/{d}" for d in re.findall(r"href=['\"]https://doi\.org/([^'\"]+)", m.group(1))
        )


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def year_of(msg: dict) -> set[str]:
    years = set()
    for k in ("published-print", "published-online", "issued"):
        parts = (msg.get(k) or {}).get("date-parts") or [[None]]
        if parts[0][0]:
            years.add(str(parts[0][0]))
    return years


def check(ref: str) -> tuple[str, str]:
    m = re.search(DOI_RE, ref)
    if not m:
        return "nodoi", ""
    doi = m.group(1)
    cited_year = re.search(r"\((\d{4})\)", ref).group(1)
    req = urllib.request.Request(
        f"https://api.crossref.org/works/{doi}", headers={"User-Agent": "cognitive-scaffolding/1"}
    )
    try:
        msg = json.load(urllib.request.urlopen(req, timeout=30))["message"]
    except Exception as e:  # noqa: BLE001 — a lookup failure is a finding, not a crash
        return "FAIL", f"{doi}: {e}"
    title = norm((msg.get("title") or [""])[0])
    if title[:40] not in norm(ref):
        return "FAIL", f"{doi}: Crossref title is {msg.get('title')}"
    if cited_year not in year_of(msg):
        return "FAIL", f"{doi}: cited {cited_year}, Crossref has {sorted(year_of(msg))}"
    return "ok", doi


bad = 0
for where, ref in refs():
    status, note = check(ref)
    bad += status == "FAIL"
    print(f"{status:5}  {where:19} {ref[:64]}…  {note}")
    time.sleep(0.2)
print("all DOI citations match Crossref" if not bad else f"{bad} citation(s) disagree with Crossref")
sys.exit(1 if bad else 0)
