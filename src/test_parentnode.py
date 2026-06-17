import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_multiple_children(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello "),
            LeafNode("b", "bold"),
            LeafNode(None, " world")
        ])
        self.assertEqual(node.to_html(), "<p>Hello <b>bold</b> world</p>")

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "bold")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        node = ParentNode("a", [LeafNode(None, "Click me")], {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')
