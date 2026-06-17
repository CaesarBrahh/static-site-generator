import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_initialization(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_2(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
