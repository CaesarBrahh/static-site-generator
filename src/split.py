from textnode import TextNode, TextType
from extract import extract_markdown_images, extract_markdown_links

# inputs: a list of old node, a delimiter, text type; outputs: a list of new nodes
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []

    for node in old_nodes:
        # skip non-text type nodes
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        # split nodes upon delimiter
        split_node = node.text.split(delimiter)
        
        # error checking
        if len(split_node) % 2 == 0:
            raise ValueError("Matching delimiter not found")

        # loop through the split node list
        for i in range(len(split_node)):
            # skip empty strings
            if split_node[i] == "":
                continue

            # create new TextNode
            if i % 2 == 0:
                new_node = TextNode(split_node[i], TextType.TEXT)
            else:
                new_node = TextNode(split_node[i], text_type)

            # add TextNode to list
            new_list.append(new_node)

    return new_list

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []

    for node in old_nodes:
        # skip non-text type nodes
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        # skip empty text nodes
        if node.text == "":
            continue

        # extract image link and alt text
        matches = extract_markdown_images(node.text)
        
        # loop through each match
        text = node.text
        for match in matches:
            # split upon each match
            sections = text.split(f"![{match[0]}]({match[1]})", 1)

            # add TextNodes to new_list
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.IMAGE, match[1]))
            
            # set text to other half
            text = sections[1]

        # add remaining section
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))

    return new_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []

    for node in old_nodes:
        # skip non-text type nodes
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue

        # skip empty text nodes
        if node.text == "":
            continue

        # extract image link and alt text
        matches = extract_markdown_links(node.text)
        
        # loop through each match
        text = node.text
        for match in matches:
            # split upon each match
            sections = text.split(f"[{match[0]}]({match[1]})", 1)

            # add TextNodes to new_list
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(TextNode(match[0], TextType.LINK, match[1]))
            
            # set text to other half
            text = sections[1]

        # add remaining section
        if text != "":
            new_list.append(TextNode(text, TextType.TEXT))

    return new_list

def main():
    node = TextNode("This is a text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(new_nodes)


if __name__=="__main__":
    main()
