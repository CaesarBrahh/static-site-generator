import unittest
from blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, text_to_children, get_heading_node, text_to_children_li
from parentnode import ParentNode
from leafnode import LeafNode

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = '''
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = '''
```
This is text that _should_ remain
the **same** even with inline stuff
```
'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        )

    def test_h1(self):
        md = "# This is a **heading**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>heading</b></h1></div>"
        )

    def test_h2(self):
        md = "## Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h2>Heading</h2></div>"
        )

    def test_h3(self):
        md = "### Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h3>Heading</h3></div>"
        )

    def test_h4(self):
        md = "#### Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h4>Heading</h4></div>"
        )

    def test_h5(self):
        md = "##### Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h5>Heading</h5></div>"
        )

    def test_h6(self):
        md = "###### Heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h6>Heading</h6></div>"
        )

    def test_unordered_list(self):
        md = '''
- item one
- item two with **bold**
- item three with `code`
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item two with <b>bold</b></li><li>item three with <code>code</code></li></ul></div>"
        )

    def test_ordered_list(self):
        md = '''
1. item one
2. item two with _italic_
3. item three
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item one</li><li>item two with <i>italic</i></li><li>item three</li></ol></div>"
        )

    def test_quote(self):
        md = '''
> this is a quote
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a quote</blockquote></div>"
        )

    def test_multiline_quote(self):
        md = '''
> quote 1

> quote 2

> quote 3
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote 1</blockquote><blockquote>quote 2</blockquote><blockquote>quote 3</blockquote></div>"
        )

    def test_multline_quote_2(self):
        md = '''
> quote 1
> quote 2
> quote 3
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote 1 quote 2 quote 3</blockquote></div>"
        )

    def test_multiple_blocks_mixed(self):
        md = '''
# Main Title

This is a paragraph with **bold** text.

- item one
- item two
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><p>This is a paragraph with <b>bold</b> text.</p><ul><li>item one</li><li>item two</li></ul></div>"
        )

    def test_links_and_images_inside_paragraph(self):
        md = '''
This paragraph has a [link](https://example.com) and an ![image](image.png)
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This paragraph has a <a href=\"https://example.com\">link</a> and an <img src=\"image.png\" alt=\"image\"></p></div>"
        )

    def test_single_link(self):
        md = '''
[link](url)        
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p><a href=\"url\">link</a></p></div>"
        )

    def test_single_image(self):
        md = '''
![image](src)
'''
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p><img src=\"src\" alt=\"image\"></p></div>"
        )

class TestTextToChildrenLI(unittest.TestCase):
    def test_unordered_list_node(self):
        self.assertEqual(
            text_to_children_li("- item one\n- item two"),
            [
                ParentNode(
                    "li", 
                    [LeafNode(None, "item one")]
                ),
                ParentNode(
                    "li", 
                    [LeafNode(None, "item two")]
                )
            ]
        )

    def test_ordered_list_node(self):
        self.assertEqual(
            text_to_children_li("1. item one\n2. item two"),
            [
                ParentNode(
                    "li",
                    [LeafNode(None, "item one")]
                ),
                ParentNode(
                    "li",
                    [LeafNode(None, "item two")]
                )
            ]
        )

    def test_unordered_list_node_with_mixed_line_elements(self):
        self.assertEqual(
            text_to_children_li("- text\n- **bold** text\n- text _italic_\n- `code text`\n- [link](url)\n- ![image](image.jpg)\n- Hello **bold** _italic_ `code` [link](url)"),
            [
                ParentNode(
                    "li",
                    [LeafNode(None, "text")]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("b", "bold"),
                        LeafNode(None, " text")
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "text "),
                        LeafNode("i", "italic")
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("code", "code text")
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("a", "link", {"href": "url"})
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode("img", "image", {"src": "image.jpg", "alt": "image"})
                    ]
                ),
                ParentNode(
                    "li",
                    [
                        LeafNode(None, "Hello "),
                        LeafNode("b", "bold"),
                        LeafNode(None, " "),
                        LeafNode("i", "italic"),
                        LeafNode(None, " "),
                        LeafNode("code", "code"),
                        LeafNode(None, " "),
                        LeafNode("a", "link", {"href": "url"})
                    ]
                )
            ]
        )

        def test_ordered_list_node_with_mixed_line_elements(self):
            self.assertEqual(
                text_to_children_li("1. text\n2. **bold** text\n3. text _italic_\n4. `code text`\n5. [link](url)\n6. ![image](image.jpg)\n7. Hello **bold** _italic_ `code` ![image](src)"),
                [
                     ParentNode(
                        "li",
                        [LeafNode(None, "text")]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("b", "bold"),
                            LeafNode(None, " text")
                        ]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(None, "text "),
                            LeafNode("i", "italic")
                        ]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("code", "code text")
                        ]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("a", "link", {"href": "url"})
                        ]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("img", "image", {"src": "image.jpg", "alt": "image"})
                        ]
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode(None, "Hello "),
                            LeafNode("b", "bold"),
                            LeafNode(None, " "),
                            LeafNode("i", "italic"),
                            LeafNode(None, " "),
                            LeafNode("code", "code"),
                            LeafNode(None, " "),
                            LeafNode("img", "image", {"src": "src", "alt": "image"})
                        ]
                    )
                ]
            )

class TestTextToChildren(unittest.TestCase):
    def test_plain_text(self):
        self.assertListEqual(
            text_to_children("Hello world"),
            [LeafNode(None, "Hello world", None)]
        )

    def test_bold_text(self):
        self.assertEqual(
            text_to_children("This is **bold** text"),
            [
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, " text")
            ]
        )

    def test_italic_text(self):
        self.assertEqual(
            text_to_children("This is _italic_ text"),
            [
                LeafNode(None, "This is "),
                LeafNode("i", "italic"),
                LeafNode(None, " text")
            ]
        )

    def test_link(self):
        self.assertEqual(
            text_to_children("Visit [Google](google.com)"),
            [
                LeafNode(None, "Visit "),
                LeafNode("a", "Google", {"href": "google.com"})
            ]
        )

    def test_image(self):
        self.assertEqual(
            text_to_children("![cat](cat.jpg)"),
            [
                LeafNode("img", "cat", {"src": "cat.jpg", "alt": "cat"})
            ]
        )

    def test_code_text(self):
        self.assertEqual(
            text_to_children("This is `code`"),
            [
                LeafNode(None, "This is "),
                LeafNode("code", "code")
            ]
        )

    def test_mixed_inline_elements(self):
        self.assertEqual(
            text_to_children("Hello **bold** _italic_ `code` [link](url)"),
            [
                LeafNode(None, "Hello "),
                LeafNode("b", "bold"),
                LeafNode(None, " "),
                LeafNode("i", "italic"),
                LeafNode(None, " "),
                LeafNode("code", "code"),
                LeafNode(None, " "),
                LeafNode("a", "link", {"href": "url"})
            ]
        )

class TestGetHeadingNode(unittest.TestCase):
    def test_h1(self):
        tag = get_heading_node("# Heading").tag
        self.assertEqual(
            tag,
            "h1"
        )

    def test_h2(self):
        tag = get_heading_node("## Heading").tag
        self.assertEqual(
            tag,
            "h2"
        )

    def test_h3(self):
        tag = get_heading_node("### Heading").tag
        self.assertEqual(
            tag,
            "h3"
        )

    def test_h4(self):
        tag = get_heading_node("#### Heading").tag
        self.assertEqual(
            tag,
            "h4"
        )

    def test_h5(self):
        tag = get_heading_node("##### Heading").tag
        self.assertEqual(
            tag,
            "h5"
        )

    def test_h6(self):
        tag = get_heading_node("###### Heading").tag
        self.assertEqual(
            tag,
            "h6"
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_empty_string_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_plain_text_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is just a normal paragraph."),
            BlockType.PARAGRAPH
        )

    def test_multiline_plain_text_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is line one\nThis is line two"),
            BlockType.PARAGRAPH
        )

    def test_heading_h1(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING
        )

    def test_heading_h6(self):
        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING
        )

    def test_heading_h7_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH
        )

    def test_heading_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("#Heading"),
            BlockType.PARAGRAPH
        )

    def test_heading_with_inline_markdown(self):
        self.assertEqual(
            block_to_block_type("## Heading with **bold** text"),
            BlockType.HEADING
        )

    def test_code_block_single_line(self):
        self.assertEqual(
            block_to_block_type("```print('hello')```"),
            BlockType.CODE
        )

    def test_code_block_multiline(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\nprint('world')\n```"),
            BlockType.CODE
        )

    def test_code_block_not_closed_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("```print('hello')"),
            BlockType.PARAGRAPH
        )

    def test_code_block_not_opened_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("print('hello')\n```"),
            BlockType.PARAGRAPH
        )

    def test_quote_single_line(self):
        self.assertEqual(
            block_to_block_type("> this is a quote"),
            BlockType.QUOTE
        )

    def test_quote_multiple_lines(self):
        self.assertEqual(
            block_to_block_type("> line one\n> line two> line three"),
            BlockType.QUOTE
        )

    def test_quote_missing_marker_on_second_line_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("> line one\nline two"),
            BlockType.PARAGRAPH
        )

    def test_quote_empty_quote_line(self):
        self.assertEqual(
            block_to_block_type(">\n> still quoted"),
            BlockType.QUOTE
        )

    def test_unordered_list_single_item(self):
        self.assertEqual(
            block_to_block_type("- item one"),
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_multiple_items(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two\n- item three"),
            BlockType.UNORDERED_LIST
        )

    def test_unordered_list_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("-item one"),
            BlockType.PARAGRAPH
        )

    def test_unordered_list_one_bad_line_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("- item one\nitem two"),
            BlockType.PARAGRAPH
        )

    def test_unordered_list_wtihin_inline_markdown(self):
        self.assertEqual(
            block_to_block_type("- **bold item**\n- _italic item_"),
            BlockType.UNORDERED_LIST
        )

    def test_ordered_list_single_item(self):
        self.assertEqual(
            block_to_block_type("1. item one"),
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_multiple_items(self):
        self.assertEqual(
            block_to_block_type("1. item one\n2. item two\n3. item three"),
            BlockType.ORDERED_LIST
        )

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(
            block_to_block_type("2. item two\n3. item three"),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_must_increment_by_one(self):
        self.assertEqual(
            block_to_block_type("1. item one\n3. item three"),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_without_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1.item one"),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_one_bad_line_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1. item one\nnot item two\n3. item three"),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_with_inline_markdown(self):
        self.assertEqual(
            block_to_block_type("1. **bold item**\n2. `code item`"),
            BlockType.ORDERED_LIST
        )

    def test_mixed_unordered_and_ordered_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("- item one\n2. item two"),
            BlockType.PARAGRAPH
        )

    def test_heading_takes_priority_over_paragraph(self):
        self.assertEqual(
            block_to_block_type("# - not a list, heading"),
            BlockType.HEADING
        )

    def test_code_takes_priority_over_other_markdown_inside(self):
        self.assertEqual(
            block_to_block_type("```\n# heading inside\n- list inside code\n```"),
            BlockType.CODE
        )

    def test_quote_with_list_syntax_inside_is_quote(self):
        self.assertEqual(
            block_to_block_type("> - quote list item\n> - quote list item two"),
            BlockType.QUOTE
        )

    def test_unordered_list_with_extra_leading_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type(" - item one\n - item two"),
            BlockType.PARAGRAPH
        )

    def test_ordered_list_with_extra_leading_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type(" 2. item one\n 2. item two"),
            BlockType.PARAGRAPH
        )

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
