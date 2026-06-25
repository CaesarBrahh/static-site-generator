import os

def main():
    static_to_public()

def static_to_public():
    # define paths to source and destination directories
    src_dir = "static"
    dst_dir = "public"

    # delete all contents of destination directory
    delete_contents(dst_dir)

    # copy and paste all contents of the source directory to destination directory
    copy_contents(src_dir, dst_dir)

def delete_contents(dst):
    # ensure path is real
    if not os.path.exists(dst):
        raise ValueError("Destination path does not exist")

    # create a list of all contents within given directory
    contents = os.listdir(dst)

    # loop through given directory's content
    for content in contents:
        # if this piece of content is a file, delete it
        if os.path.isfile(os.path.join(dst, content)):
            os.remove(os.path.join(dst, content))

        # if this piece of content is a folder, recursively go back into the function
        else:
            # delete all contents of the directory
            delete_contents(os.path.join(dst, content))

            # delete the directory itself
            os.rmdir(os.path.join(dst,content))

    return

def copy_contents(src, dst):
    # ensure path is real
    if not os.path.exists(src):
        print(src)
        raise ValueError("Source path does not exist")

    # copy contents in given src directory
    contents = os.listdir(src)

    for content in contents:
        if os.path.isfile(os.path.join(src, content)):
            # copy each line of the src/content file to a list
            with open(os.path.join(src, content), "rb") as file:
                lines = file.readlines()

            # write each line of that list to the dst/content file (doing this creates the file too)
            with open(os.path.join(dst, content), "wb") as file:
                for line in lines:
                    file.write(line)
        else:
            # create new directory within dst/
            os.mkdir(os.path.join(dst, content)) 

            # recurse into function to copy this directory's contents
            copy_contents(os.path.join(src, content), os.path.join(dst, content))

    return

if __name__=="__main__":
    main()
