import unittest
from textnode import TextNode, TextType
from split import split_nodes_delimiter,split_nodes_link, split_nodes_image

class TestSplitNodesLink(unittest.TestCase):
    def test_base(self):
        node = TextNode(
            "This is text with a cat [cat](google.com) <-- here",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a cat ", TextType.TEXT),
                TextNode("cat", TextType.LINK, "google.com"),
                TextNode(" <-- here", TextType.TEXT)
            ]
        )

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a cat [cat](google.com) and dog [dog](youtube.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a cat ", TextType.TEXT),
                TextNode("cat", TextType.LINK, "google.com"),
                TextNode(" and dog ", TextType.TEXT),
                TextNode("dog", TextType.LINK, "youtube.com")
            ]
        )

    def test_no_images(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no links", TextType.TEXT)
            ]
        )

    def test_start(self):
        node = TextNode(
            "[cat](google.com) a cat image has been placed at the start of this text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("cat", TextType.LINK, "google.com"),
                TextNode(" a cat image has been placed at the start of this text", TextType.TEXT)
            ]
        )

    def test_multiple_input_nodes(self):
        node = TextNode(
            "[cat](google.com) is my favorite animal",
            TextType.TEXT
        )
        node_2 = TextNode(
            "this is my second favorite animal [dog](google.com)",
            TextType.TEXT
        )
        node_3 = TextNode(
            "and of course [turtle](google.com) is my 3rd favorite",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node, node_2, node_3])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("cat", TextType.LINK, "google.com"),
                TextNode(" is my favorite animal", TextType.TEXT),
                TextNode("this is my second favorite animal ", TextType.TEXT),
                TextNode("dog", TextType.LINK, "google.com"),
                TextNode("and of course ", TextType.TEXT),
                TextNode("turtle", TextType.LINK, "google.com"),
                TextNode(" is my 3rd favorite", TextType.TEXT)
            ]
        )

    def test_preserves_non_text_nodes(self):
        node = TextNode(
            "[cat](google.com)", 
            TextType.BOLD
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("[cat](google.com)", TextType.BOLD)
            ]
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_base(self):
        node = TextNode(
            "This is text with a cat ![cat](google.com/cat.jpg) <-- here",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a cat ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "google.com/cat.jpg"),
                TextNode(" <-- here", TextType.TEXT)
            ]
        )

    def test_multiple_images(self):
        node = TextNode(
            "This is text with a cat ![cat](google.com/cat.jpg) and dog ![dog](youtube.com/dog.gif)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a cat ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "google.com/cat.jpg"),
                TextNode(" and dog ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "youtube.com/dog.gif")
            ]
        )

    def test_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no images", TextType.TEXT)
            ]
        )

    def test_start(self):
        node = TextNode(
            "![cat](google.com/cat.jpg) a cat image has been placed at the start of this text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("cat", TextType.IMAGE, "google.com/cat.jpg"),
                TextNode(" a cat image has been placed at the start of this text", TextType.TEXT)
            ]
        )

    def test_multiple_input_nodes(self):
        node = TextNode(
            "![cat](google.com/cat.jpg) is my favorite animal",
            TextType.TEXT
        )
        node_2 = TextNode(
            "this is my second favorite animal ![dog](google.com/dog.jpg)",
            TextType.TEXT
        )
        node_3 = TextNode(
            "and of course ![turtle](google.com/turtle.jpg) is my 3rd favorite",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node, node_2, node_3])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("cat", TextType.IMAGE, "google.com/cat.jpg"),
                TextNode(" is my favorite animal", TextType.TEXT),
                TextNode("this is my second favorite animal ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "google.com/dog.jpg"),
                TextNode("and of course ", TextType.TEXT),
                TextNode("turtle", TextType.IMAGE, "google.com/turtle.jpg"),
                TextNode(" is my 3rd favorite", TextType.TEXT)
            ]
        )

    def test_preserves_non_text_nodes(self):
        node = TextNode(
            "![cat](google.com/cat.jpg)", 
            TextType.BOLD
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("![cat](google.com/cat.jpg)", TextType.BOLD)
            ]
        )
    
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
