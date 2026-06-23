def markdown_to_blocks(markdown):
    markdown_split = markdown.split("\n\n")

    new_markdown_list = []
    for m in markdown_split:
        if m == "":
            continue
        new_markdown_list.append(m.strip())

    return new_markdown_list

def main():
    md = '''
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    '''
    print(markdown_to_blocks(md))

if __name__=="__main__":
    main()
