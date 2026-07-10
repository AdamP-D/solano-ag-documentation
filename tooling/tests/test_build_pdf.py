import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import build_pdf as bp


class TestBuildPdf(unittest.TestCase):
    def test_find_edge_returns_str_or_none(self):
        r = bp.find_edge()
        self.assertTrue(r is None or isinstance(r, str))

    def test_command_uses_headless_and_print_flag(self):
        cmd = bp.edge_command("C:/edge.exe", "in.html", "out.pdf")
        self.assertIn("--headless", cmd)
        self.assertTrue(any(a.startswith("--print-to-pdf=") for a in cmd))


if __name__ == "__main__":
    unittest.main()
