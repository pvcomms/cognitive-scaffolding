"""python3 -m unittest — the content parses, every tool cites something, the page builds."""
import json, pathlib, re, shutil, subprocess, tempfile, unittest

import build

ROOT = pathlib.Path(__file__).parent


class Content(unittest.TestCase):
    def setUp(self):
        self.data = build.load()

    def test_counts(self):
        self.assertEqual(len(self.data["families"]), 6)
        self.assertEqual(len(self.data["tools"]), 17)
        self.assertEqual(len(self.data["lenses"]), 6)

    def test_every_tool_is_complete_and_cited(self):
        fams = {f["id"] for f in self.data["families"]}
        for t in self.data["tools"]:
            with self.subTest(tool=t["id"]):
                self.assertIn(t["family"], fams)
                for field in build.TOOL_FIELDS:
                    self.assertTrue(t[field], field)
                self.assertTrue(t["body"])
                self.assertTrue(t["grounding"])

    def test_tools_sorted_by_family_then_order(self):
        order = [f["id"] for f in self.data["families"]]
        keys = [(order.index(t["family"]), t["order"]) for t in self.data["tools"]]
        self.assertEqual(keys, sorted(keys))

    def test_run_links_point_at_real_tools(self):
        page = (ROOT / "index.html").read_text()
        ids = {t["id"] for t in self.data["tools"]}
        for target in re.findall(r"#toolbox/([a-z-]+)", page):
            self.assertIn(target, ids)


class Parsing(unittest.TestCase):
    def test_inline_escapes_then_emphasises(self):
        self.assertEqual(build.inline("a <b> *c*"), "a &lt;b&gt; <em>c</em>")
        self.assertEqual(build.inline("_d_"), "<em>d</em>")
        self.assertEqual(build.inline("it's 2 * 3 * 4"), "it's 2 * 3 * 4")

    def test_inline_links_a_doi(self):
        out = build.inline("x. https://doi.org/10.1037/a0035173")
        self.assertIn('href="https://doi.org/10.1037/a0035173"', out)
        self.assertIn(">doi:10.1037/a0035173</a>", out)

    def test_frontmatter_unwraps_a_formatter_quote_only(self):
        p = pathlib.Path("x.md")
        meta, _ = build.split_frontmatter('---\na: "quoted"\nb: say "always" or "never"\nc: x: y\n---\nbody', p)
        self.assertEqual(meta["a"], "quoted")
        self.assertEqual(meta["b"], 'say "always" or "never"')
        self.assertEqual(meta["c"], "x: y")

    def test_grounding_split(self):
        paras, sources = build.parse_body("one\n\ntwo\n\n## Grounding\n\n- A (2000). T.\n- B (2001). U.\n")
        self.assertEqual(paras, ["one", "two"])
        self.assertEqual(len(sources), 2)


class Page(unittest.TestCase):
    def test_fragment_format(self):
        page = (ROOT / "index.html").read_text()
        self.assertTrue(page.startswith("<title>"))
        self.assertIsNone(re.search(r"<(!doctype|html|head|body)\b", page, flags=re.I))
        self.assertIn(build.PLACEHOLDER, page)

    def test_wrap_inlines_parseable_data(self):
        html = build.wrap((ROOT / "index.html").read_text(), build.load())
        self.assertTrue(html.startswith("<!doctype html>"))
        m = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, flags=re.S)
        self.assertIsNotNone(m)
        self.assertEqual(len(json.loads(m.group(1))["tools"]), 17)
        self.assertLess(html.index("<style>"), html.index("<body>"))

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_app_script_parses(self):
        page = (ROOT / "index.html").read_text()
        js = page.split("<script>", 1)[1].split("</script>", 1)[0]
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
            f.write(js)
        r = subprocess.run(["node", "--check", f.name], capture_output=True, text=True)
        pathlib.Path(f.name).unlink()
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_third_party_requests(self):
        page = (ROOT / "index.html").read_text()
        for src in re.findall(r'(?:src|href)="(https?://[^"]+)"', page):
            self.assertTrue(src.startswith("https://doi.org/"), src)

    def test_build_writes_public(self):
        with tempfile.TemporaryDirectory() as tmp:
            build.PUB = pathlib.Path(tmp) / "public"
            try:
                self.assertEqual(build.main(), 0)
                self.assertTrue((build.PUB / "index.html").is_file())
                self.assertTrue(list((build.PUB / "fonts").glob("*.woff2")))
            finally:
                build.PUB = ROOT / "public"


if __name__ == "__main__":
    unittest.main()
