import re

def main():
    extract_title(md)

def extract_title(markdown):
    heading = re.search(r"^# (.*)", markdown, re.MULTILINE)

    if heading == None:
        raise ValueError("No h1 header found.")

    return heading.group(1).strip()

if __name__=="__main__":
    main()
