import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_base(self):
        header = '''
# Header
'''
        self.assertEqual(
            extract_title(header),
            "Header"
        )

    def test_h1_after_paragraph(self):
        md = '''
This is intro text.

# Real Title

Some paragraph.
'''
        self.assertEqual(
            extract_title(md),
            "Real Title"
        )

    def test_ignores_h2(self):
        md = '''
## Not h1

# Actual h1
'''
        self.assertEqual(
            extract_title(md),
            "Actual h1"
        )

    def test_ignores_hash_without_space(self):
        md = '''
#Not a heading

# Real Title
'''
        self.assertEqual(
            extract_title(md),
            "Real Title"
        )

    def test_strips_extra_title_whitespace(self):
        md = '''
#    Title with Extra Spaces
'''
        self.assertEqual(
            extract_title(md),
            "Title with Extra Spaces"
        )

    def test_h1_with_inline_markdown(self):
        md = '''
# Title with **bold** and `code`
'''
        self.assertEqual(
            extract_title(md),
            "Title with **bold** and `code`"
        )

    def test_no_h1_raises(self):
        md = '''
## Only H2

Paragraph text
'''
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_empty_markdown_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")
