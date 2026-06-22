import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def main():
    text = "this is text with a ![rick roll](https://i.imgur.com/fejiwofe.gif) and ![obi wan](https://i.imgur.com/fjeiose.jpeg)"
    #print(extract_markdown_images(text))
    text_2 = "this is text with a link to [boot dev](https://www.boot.dev) and [to google](google.com)"
    print(extract_markdown_links(text_2))

if __name__=="__main__":
    main()
