from enum import Enum
import re
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, text_node_to_html_node, TextType
from split import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:
    # empty strings are paragraphs
    if markdown == "":
        return BlockType.PARAGRAPH

    # headings
    if re.match(r"^#{1,6} .*", markdown):
        return BlockType.HEADING

    # multiline code
    if re.match(r"^```.*```$", markdown, re.DOTALL):
        return BlockType.CODE

    # quote block
    split_markdown = markdown.split("\n")
    i = 0
    for m in split_markdown:
        if m.startswith(">"):
            i += 1
    if i == len(split_markdown):
        return BlockType.QUOTE

    # unordered list
    i = 0
    for m in split_markdown:
        if re.match(r"^- .*", m):
            i += 1
    if i == len(split_markdown):
        return BlockType.UNORDERED_LIST

    # ordered list
    i = 1
    for m in split_markdown:
        if re.match(fr"^{i}\. .*", m):
            i += 1
    if i-1 == len(split_markdown):
        return BlockType.ORDERED_LIST

    # if none pass, it's a paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")

    new_markdown_list = []
    for m in markdown_split:
        if m == "":
            continue
        new_markdown_list.append(m.strip())

    return new_markdown_list

# input: markdown text | ouptut: one ParentNode object
def markdown_to_html_node(markdown: str) -> ParentNode:
    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # loop over each block
    nodes = []
    for block in blocks:
        # determine the type of block
        block_type = block_to_block_type(block)

        # create a new htmlnode based on block type
        if block_type == BlockType.HEADING:
            parent_node = get_heading_node(block)
        elif block_type == BlockType.CODE:
            parent_node = ParentNode("pre", None)
        else:
            parent_node = get_parent_node(block_type)

        # find leafnodes
        if block_type == BlockType.UNORDERED_LIST or block_type == BlockType.ORDERED_LIST:
            leaf_nodes = text_to_children_li(block)
        elif block_type == BlockType.CODE:
            code_text = block[3:-3]
            if code_text.startswith("\n"):
                code_text = code_text[1:]
            if code_text.endswith("\n"):
                code_text = code_text[:-1]
            leaf_nodes = [LeafNode("code", code_text)]
        elif block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.split("\n"))
            leaf_nodes = text_to_children(paragraph_text)
        elif block_type == BlockType.HEADING:
            prefix, main_text = block.split(' ', 1)
            leaf_nodes = text_to_children(main_text)
        elif block_type == BlockType.QUOTE:
            split_block = block.split("\n")
            for i in range(len(split_block)):
                split_block[i] = split_block[i][1:]
                try:
                    if split_block[i][0] == " ":
                        split_block[i] = split_block[i][1:]
                except IndexError:
                    pass
            quote_block = " ".join(split_block)
            leaf_nodes = text_to_children(quote_block)
        else:
            leaf_nodes = text_to_children(block)

        # assign leafnodes to parent_node
        parent_node.children = leaf_nodes

        # append parent_node to nodes[]
        nodes.append(parent_node)

    # surround all parent_nodes in one div
    final_node = ParentNode("div", nodes)

    return final_node

def text_to_children_li(text: str) -> list[ParentNode]:
    # split text upon each new line
    split_text = text.split("\n")

    # loop through each bullet point
    nodes = []
    for line in split_text:
        # remove - and #.
        if line.startswith("-"):
            line = line[2:]
        elif line[1] == ".":
            line = line[3:]

        # turn line -> textnode -> leafnode
        leaf_nodes = text_to_children(line)

        # create parentnode with leafnode object
        parent_node = ParentNode("li", leaf_nodes)

        # add to nodes[]
        nodes.append(parent_node)

    return nodes


# takes in text and returns the html nodes
def text_to_children(text: str) -> list[LeafNode]:
    # convert text to a list of textnodes
    textnodes = text_to_textnodes(text)

    # loop through textnodes
    leafnodes = []
    for node in textnodes:
        # convert node -> leafnode
        leafnode = text_node_to_html_node(node)

        # append leafnode to leafnodes[]
        leafnodes.append(leafnode)

    return leafnodes

# input: block type | output: corresponding ParentNode
def get_parent_node(block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", None)
        case BlockType.CODE:
            return ParentNode("code", None)
        case BlockType.QUOTE:
            return ParentNode("blockquote", None)
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", None)
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", None)
        case _:
            raise ValueError("Not a real block type")

# find number of #'s and return proper tag
def get_heading_node(block):
    total = block.find(" ")
    return ParentNode(f"h{total}", None)


def main():
    md_1 = '''
```
This is text that _should_ remain
the **same** even with inline stuff
```
'''
    print(markdown_to_html_node(md_1).to_html())

if __name__=="__main__":
    main()
