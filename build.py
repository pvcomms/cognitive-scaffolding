#!/usr/bin/env python3
"""
Build public/index.html from the fragment and the markdown.

index.html is an artifact fragment, the same format as paramv.com: <title> on line 1,
then <style>, markup, <script>, and no doctype/html/head/body. This wraps it in a real
document, inlines the toolbox (about.md, families.md, tools/*.md, lenses/*.md) as JSON,
and copies the fonts. public/ is generated. Never edit it by hand.

    ./build.py                      build public/
    ./build.py --check              parse and validate the content, write nothing
    ./build.py --site ~/personal/site
                                    also write the paramv.com fragment there, as
                                    cognitive-scaffolding.html (served at /systems/cognitive-scaffolding)
"""
import html, json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).parent
PUB = ROOT / "public"
PLACEHOLDER = "/*DATA*/"

TOOL_FIELDS = ("name", "family", "order", "when", "move", "ask")
LENS_FIELDS = ("name", "order", "question", "guard")


def split_frontmatter(text: str, path: pathlib.Path) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, flags=re.S)
    if not m:
        raise ValueError(f"{path.name}: no frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"{path.name}: bad frontmatter line {line!r}")
        value = value.strip()
        # prettier may quote a value; unwrap only a single cleanly-wrapped string
        if len(value) > 1 and value[0] == value[-1] and value[0] in "'\"" and value[0] not in value[1:-1]:
            value = value[1:-1]
        meta[key.strip()] = value
    return meta, m.group(2)


def inline(text: str) -> str:
    """Escape, then *em* or _em_ → <em>, and a bare https://doi.org/ link → <a>. Nothing else."""
    out = html.escape(text, quote=False)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"(?<![\w])_(?!\s)(.+?)(?<!\s)_(?![\w])", r"<em>\1</em>", out)
    out = re.sub(r"https://doi\.org/(\S+)", r'<a href="https://doi.org/\1" rel="noopener">doi:\1</a>', out)
    return out


def parse_body(body: str) -> tuple[list[str], list[str]]:
    """Paragraphs before '## Grounding', and the '- ' items under it."""
    main, _, grounding = body.partition("## Grounding")
    paras = [inline(" ".join(p.split())) for p in re.split(r"\n\s*\n", main.strip()) if p.strip()]
    sources = [inline(line.strip()[2:].strip()) for line in grounding.splitlines() if line.strip().startswith("- ")]
    return paras, sources


def load_families() -> list[dict]:
    text = (ROOT / "families.md").read_text()
    fams = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, rest = block.partition("\n")
        fid, sep, name = head.partition("·")
        if not sep:
            raise ValueError(f"families.md: heading needs 'id · Name', got {head!r}")
        fams.append({"id": fid.strip(), "name": name.strip(), "line": inline(" ".join(rest.split()))})
    return fams


def load_dir(sub: str, fields: tuple[str, ...]) -> list[dict]:
    items = []
    for path in sorted((ROOT / sub).glob("*.md")):
        meta, body = split_frontmatter(path.read_text(), path)
        missing = [f for f in fields if not meta.get(f)]
        if missing:
            raise ValueError(f"{sub}/{path.name}: missing {', '.join(missing)}")
        paras, sources = parse_body(body)
        item = {"id": path.stem, **{k: inline(v) for k, v in meta.items() if k != "order"}}
        item["order"] = int(meta["order"])
        item["body"], item["grounding"] = paras, sources
        items.append(item)
    return items


def load() -> dict:
    meta, body = split_frontmatter((ROOT / "about.md").read_text(), ROOT / "about.md")
    families = load_families()
    fam_ids = [f["id"] for f in families]
    tools = load_dir("tools", TOOL_FIELDS)
    for t in tools:
        if t["family"] not in fam_ids:
            raise ValueError(f"tools/{t['id']}.md: family {t['family']!r} not in families.md")
        if not t["grounding"]:
            raise ValueError(f"tools/{t['id']}.md: no grounding — every tool cites something")
    tools.sort(key=lambda t: (fam_ids.index(t["family"]), t["order"]))
    lenses = sorted(load_dir("lenses", LENS_FIELDS), key=lambda l: l["order"])
    about = {k: inline(v) for k, v in meta.items()}
    about["body"] = parse_body(body)[0]
    return {"about": about, "families": families, "tools": tools, "lenses": lenses}


def payload(data: dict) -> str:
    # </ inside JSON would close the script tag early
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def wrap(fragment: str, data: dict) -> str:
    m = re.match(r"^<title>(.*?)</title>\s*", fragment, flags=re.S)
    if not m:
        raise ValueError("index.html: line 1 must be the <title>")
    if PLACEHOLDER not in fragment:
        raise ValueError(f"index.html: no {PLACEHOLDER} placeholder for the data")
    body = fragment[m.end():]
    styles = "\n".join(re.findall(r"<style>.*?</style>", body, flags=re.S))
    body = re.sub(r"<style>.*?</style>\s*", "", body, flags=re.S)
    body = body.replace(PLACEHOLDER, payload(data))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="dark light">
<title>{m.group(1)}</title>
<link rel="preload" href="fonts/newsreader-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' fill='%230b0c0e'/%3E%3Cpath d='M4 3v10M12 3v10M4 6h8M4 10h8' stroke='%23e3c567' stroke-width='1.4'/%3E%3C/svg%3E">
{styles}
</head>
<body>
{body}</body>
</html>
"""


SITE_PAGE = "cognitive-scaffolding.html"
SITE_NOTE = """<!--
  paramv.com/systems/cognitive-scaffolding. GENERATED, do not edit here.
  source: ~/personal/tools/apps/cognitive-scaffolding (github.com/pvcomms/cognitive-scaffolding)
  rebuild: cd there && ./build.py --site ~/personal/site
  the load-gate block is copied from systems.html at build time, so it stays identical.
-->
"""
GATE_TOP = re.compile(
    r'<style>\s*/\* gate .*?</style>\s*<script>\s*try \{ if \(!sessionStorage\.getItem\("pv-gate"\)\).*?</script>'
    r'\s*<div class="gate" id="gate".*?</altcha-widget>.*?</div>\s*</div>',
    flags=re.S,
)
GATE_BOTTOM = re.compile(
    r'<script src="/vendor/altcha/altcha-obfuscation\.min\.js" defer></script>\s*'
    r'<script src="/vendor/altcha/altcha\.min\.js" defer></script>\s*<script>\s*/\* gate: .*?</script>',
    flags=re.S,
)


def site_fragment(fragment: str, data: dict, systems_html: str) -> str:
    """The same page as a paramv.com fragment: absolute font paths, dark only, the site's
    load gate, a way back to /systems, and the toolbox inlined. paramv.com's build.py wraps it."""
    top, bottom = GATE_TOP.search(systems_html), GATE_BOTTOM.search(systems_html)
    if not (top and bottom):
        raise ValueError("systems.html: couldn't find the load-gate block to copy")
    m = re.match(r"^<title>.*?</title>\n", fragment)
    if not m:
        raise ValueError("index.html: line 1 must be the <title>")
    out = fragment[: m.end()] + SITE_NOTE + fragment[m.end():]
    out, n = re.subn(r"\s*/\* light:start.*?/\* light:end \*/", "", out, count=1, flags=re.S)
    if not n:
        raise ValueError("index.html: no light:start/light:end block to drop")
    out = out.replace('url("fonts/', 'url("/fonts/')
    out = out.replace("<!--SITE-NAV-->", '<a class="crumb" href="/systems">← systems</a>')
    first_style_end = out.index("</style>") + len("</style>")
    out = out[:first_style_end] + "\n" + top.group(0) + out[first_style_end:]
    out = out.replace(PLACEHOLDER, payload(data))
    return out.rstrip() + "\n" + bottom.group(0) + "\n"


def main() -> int:
    data = load()
    print(f"{len(data['tools'])} tools in {len(data['families'])} families, {len(data['lenses'])} lenses")
    if "--check" in sys.argv:
        return 0
    fragment = (ROOT / "index.html").read_text()
    if re.search(r"<(!doctype|html|head|body)\b", fragment, flags=re.I):
        raise ValueError("index.html is a fragment: no doctype/html/head/body tags")
    PUB.mkdir(exist_ok=True)
    (PUB / "index.html").write_text(wrap(fragment, data))
    shutil.copytree(ROOT / "fonts", PUB / "fonts", dirs_exist_ok=True)
    print(f"wrote {PUB / 'index.html'}")
    if "--site" in sys.argv:
        site = pathlib.Path(sys.argv[sys.argv.index("--site") + 1]).expanduser()
        systems = (site / "systems.html").read_text(encoding="utf-8")
        (site / SITE_PAGE).write_text(site_fragment(fragment, data, systems), encoding="utf-8")
        print(f"wrote {site / SITE_PAGE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
