from static_to_public import static_to_public
from generate_page import generate_page

def main():
    static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__=="__main__":
    main()
