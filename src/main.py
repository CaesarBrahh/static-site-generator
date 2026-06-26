from static_to_public import static_to_public
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

def main():
    static_to_public()
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__=="__main__":
    main()
