import unittest
from textnode import TextNode, TextType
from split import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_center(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )       

    def test_start_end(self):
        node = TextNode('`code` and more `code`', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("code", TextType.CODE),
                TextNode(" and more ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ]
        )

    def test_one(self):
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD)
            ]
        )

    def test_indent(self):
        node = TextNode("only _this_ and _this_ are italic", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("only ", TextType.TEXT),
                TextNode("this", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("this", TextType.ITALIC),
                TextNode(" are italic", TextType.TEXT)
            ]
        )

    def test_unclosed(self):
        node = TextNode("this **block is not closed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
       
    def test_already_typed(self):
        node = TextNode("italic", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("italic", TextType.ITALIC)
            ]
        )

    def test_no_delimiter(self):
        node = TextNode("this is normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("this is normal text", TextType.TEXT)
            ]
        )

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("hello `code`", TextType.TEXT),
            TextNode(" and **bold**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and **bold**", TextType.TEXT)
            ]
        )

        newer_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(
            newer_nodes,
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD)
            ]
        )
