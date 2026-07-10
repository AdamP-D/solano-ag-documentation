import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build_site as bs


class TestBuildSite(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        c = os.path.join(self.root, "source", "apps", "gwss", "content")
        os.makedirs(c)
        open(os.path.join(c, "knowledge-base.md"), "w", encoding="utf-8").write(
            "# GWSS KB\n\n## Overview\n\nText about traps and findings.\n")
        open(os.path.join(c, "requirements.md"), "w", encoding="utf-8").write(
            "# GWSS Requirements\n\n## Background\n\nStuff.\n")
        self.out = os.path.join(self.root, "build", "site")

    def test_discover_finds_pages(self):
        pages = bs.discover(os.path.join(self.root, "source"))
        docs = sorted(p["doc"] for p in pages)
        self.assertEqual(docs, ["knowledge-base", "requirements"])

    def test_build_writes_index_pages_and_search_index(self):
        written = bs.build(os.path.join(self.root, "source"), self.out)
        self.assertTrue(os.path.exists(os.path.join(self.out, "index.html")))
        self.assertTrue(os.path.exists(os.path.join(self.out, "gwss", "knowledge-base.html")))
        idx = json.load(open(os.path.join(self.out, "search-index.json"), encoding="utf-8"))
        self.assertTrue(any("traps" in e["text"].lower() for e in idx))
        html = open(os.path.join(self.out, "index.html"), encoding="utf-8").read()
        self.assertIn("GWSS", html)


if __name__ == "__main__":
    unittest.main()
