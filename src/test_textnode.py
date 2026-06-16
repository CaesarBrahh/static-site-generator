import unittest
from textnode import TextNode, TextType

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

# url is none
# different text type property

if __name__=="__main__":
    unittest.main()
