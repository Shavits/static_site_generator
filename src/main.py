
from copy_static import populate_public
from gen_content import generate_pages_recursive
from textnode import *

def main():
    populate_public()
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    # generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")
    # generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    # generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    generate_pages_recursive("content", "template.html", "public")












if __name__ == "__main__":
    main()