from blocks import markdown_to_html_node
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read and store contents of from_path
    with open(from_path, "r") as file:
        from_path_md = file.read()

    # read and store contents of template_path
    with open(template_path, "r") as file:
        template_path_html = file.read()

    # convert from_path_lines to one html node
    from_path_html_node = markdown_to_html_node(from_path_md) 

    # convert from_path_html_node to one massive html string
    from_path_html = from_path_html_node.to_html()

    # extract title of page
    title = extract_title(from_path_md)

    # replace template title with actual title
    template_path_html = template_path_html.replace("{{ Title }}", title)

    # replace template content with actual content
    template_path_html = template_path_html.replace("{{ Content }}", from_path_html)

    # write full html page to a file at dest_path
    with open(dest_path, "w") as file:
        file.write(template_path_html)
