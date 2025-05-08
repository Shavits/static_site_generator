import os
import shutil
from utils import markdown_to_html_node
from textnode import *

def main():
    populate_public()
    generate_page("content/index.md", "template.html", "public/index.html")


def populate_public():
    print("populating")
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")
    copy_all_children_to_public("")


def copy_all_children_to_public(folder):
    src_folder = os.path.join("./static", folder)
    dst_folder = os.path.join("./public", folder)
    if(not os.path.exists(dst_folder)):
        os.mkdir(dst_folder)
    print(f"checking {src_folder}")
    entries = os.listdir(src_folder)
    for entry in entries:
        src_path = os.path.join(src_folder,entry)
        if os.path.isfile(src_path):
            print(src_path)
            dst_path = os.path.join(dst_folder, entry)
            print(f"copying {src_path} to {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            new_folder = os.path.join(folder, entry)
            copy_all_children_to_public(new_folder)


def extract_title(markdown):
    lines = markdown.split("\n")
    res = None
    for line in lines:
        if line.startswith("#"):
            res = line[1:].strip()
            break
    if res is None:
        raise Exception("Markdwon Error: No Title Detected!")
    return res


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as src_file, open(template_path, "r") as tmplt_file:
        src_md = src_file.read()
        src_nodes = markdown_to_html_node(src_md) 
        print(src_nodes)
        src_html = src_nodes.to_html()
        tmplt_html = tmplt_file.read
        title = extract_title(src_file)
        res_html = tmplt_html.replace("{{ Title }}", title).replace("{{ Content }}", src_html)
        dest_dir = os.path.join(dest_path.split()[:-1])
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        res_file = open(dest_path, 'x')
        res_file.write(res_html)
        res_file.close()






if __name__ == "__main__":
    main()