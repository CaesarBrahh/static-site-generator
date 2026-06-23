from enum import Enum
from leafnode import LeafNode
from split import split_nodes_link, split_nodes_image, split_nodes_delimiter

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        if self.url != None:
            return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"
        return f"TextNode(\"{self.text}\", {self.text_type})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, text_node.url)
        case TextType.IMAGE:
            return LeafNode("img", text_node.text, text_node.url)
        case _:
            raise ValueError("Text node doesn't exist")

def text_to_textnodes(text):
    # links
    nodes = split_nodes_link([text])

    # images
    nodes = split_nodes_image(nodes)

    # italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # code text
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
