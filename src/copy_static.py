import os
import shutil


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