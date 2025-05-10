import os

from utils import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating pages for {dir_path_content}")
    entries = os.listdir(dir_path_content)
    for entry in entries:
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry.replace("md", "html"))
        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path)
        else:
            generate_pages_recursive(src_path, template_path, dest_path)


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
        #print(src_nodes)
        src_html = src_nodes.to_html()
        tmplt_html = tmplt_file.read()
        title = extract_title(src_md)
        res_html = tmplt_html.replace("{{ Title }}", title).replace("{{ Content }}", src_html)
        dest_dir = os.path.dirname(dest_path)
        if dest_dir != "":
            os.makedirs(dest_dir, exist_ok=True)
        res_file = open(dest_path, 'x')
        res_file.write(res_html)
        res_file.close()