import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # ensure dir_path_content exists
    if not os.path.exists(dir_path_content):
        raise ValueError("Directory path of content does not exist")

    # store dir_path_contents
    contents = os.listdir(dir_path_content)

    for content in contents:
        from_path = os.path.join(dir_path_content, content)
        to_path = os.path.join(dest_dir_path, content)

        if os.path.isfile(from_path):
            generate_page(from_path, template_path, os.path.join(dest_dir_path, "index.html"), basepath)
        else:
            # make the to_path directory real
            os.mkdir(to_path)

            # recurse into the file
            generate_pages_recursive(from_path, template_path, to_path, basepath)

    return
