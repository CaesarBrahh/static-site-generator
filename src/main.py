from static_to_public import static_to_public
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    static_to_public()
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__=="__main__":
    main()
