import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import md_to_html as m


class TestFencedCode(unittest.TestCase):
    def test_sql_block_renders_code_box_with_language_label(self):
        md = "Intro\n\n```sql\nSELECT * FROM t WHERE a < 5;\n```\n\nAfter\n"
        html = m.md_to_html_body(md)
        self.assertIn("class='codeblock'", html)
        self.assertIn(">SQL<", html)                 # language label, uppercased
        self.assertIn("<pre><code", html)
        self.assertIn("language-sql", html)
        # content is HTML-escaped inside the code box
        self.assertIn("SELECT * FROM t WHERE a &lt; 5;", html)
        # the fence markers themselves do not leak into the output
        self.assertNotIn("```", html)

    def test_untitled_fence_labels_text(self):
        html = m.md_to_html_body("```\nplain\n```\n")
        self.assertIn(">TEXT<", html)

    def test_arcade_label_preserved(self):
        html = m.md_to_html_body("```arcade\nvar x = 1;\nreturn x;\n```\n")
        self.assertIn(">ARCADE<", html)
        self.assertIn("language-arcade", html)

    def test_multiline_code_preserves_newlines(self):
        html = m.md_to_html_body("```sql\nSELECT 1\nFROM dual\n```\n")
        self.assertIn("SELECT 1\nFROM dual", html)

    def test_inline_code_still_renders(self):
        html = m.md_to_html_body("Use the `gwss_action` field.\n")
        self.assertIn("<code>gwss_action</code>", html)

    def test_code_block_after_paragraph_without_blank_line(self):
        # A fenced block immediately after a prose line (no blank line between)
        # must still render as a code box, not be swallowed into the paragraph.
        md = "The script is stored at:\n```text\n\\\\server\\path\\file\n```\n"
        html = m.md_to_html_body(md)
        self.assertIn("class='codeblock'", html)
        self.assertIn(">TEXT<", html)
        self.assertIn("server", html)


if __name__ == "__main__":
    unittest.main()
