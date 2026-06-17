import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_initialization(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_1(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_2(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "onClick": True, "id": "link"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" onClick="True" id="link"')

    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "hello world")
        self.assertEqual(repr(node), "HTMLNode(p, hello world, None, None)")

if __name__=="__main__":
    unittest.main()
