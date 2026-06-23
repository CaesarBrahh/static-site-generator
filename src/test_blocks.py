import unittest
from blocks import markdown_to_blocks

class TextMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = '''
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )

    def test_individual_lines_trimmed(self):
        md = '''
line one
line two
'''
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "line one\nline two"
            ]
        )
