import os

def main():
    static_to_public()

def static_to_public():
    # define paths to source and destination directories
    src_dir = "./static"
    dst_dir = "./public"

    # delete all contents of destination directory
    delete_contents(dst_dir)

    # copy all contents of the source directory
    # copied_contents = copy_contents(src_dir)

def delete_contents(dst):
    # ensure path is real
    if not os.path.exists(dst):
        raise ValueError("Destination path does not exist")

    # create a list of all contents within given directory
    contents = os.listdir()

    # loop through given directory's content
    for content in contents:
        # if this piece of content is a file, delete it
        if os.path.isfile(os.path.join(dst, content)):
            os.remove(os.path.join(dst, content))
        # if this piece of content is a folder, recursively go into this function
        else:
            delete_contents(os.path.join(dst, content))

    return

def copy_contents(src):
    # ensure path is real
    if not os.path.exists(src):
        raise ValueError("Source path does not exist")

    # copy contents in given src directory
    contents = os.listdir()

    for content in contents:
        if os.path.isfile(os.path.join(src, content)):
            pass
        else:
            os.mkdir()

if __name__=="__main__":
    main()
