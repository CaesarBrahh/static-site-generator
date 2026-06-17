import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a code node", TextType.CODE)
        node2 = TextNode("This is an italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_method(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_method_2(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        node2 = TextNode("Google", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_link(self):
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        self.assertEqual(node.url, "https://www.google.com")

    def test_link_2(self):
        node = TextNode("This contains no link", TextType.ITALIC)
        self.assertEqual(node.url, None)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Google", TextType.LINK, {"href": "https://www.google.com"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(None, TextType.IMAGE, {"src": "https://example.com/image.png", "alt": "Alt Text"})
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt Text"})

    def test_invalid(self):
        node = TextNode("hello", "INVALID")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__=="__main__":
    unittest.main()
