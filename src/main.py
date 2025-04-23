from textnode import *

def main():
    node = TextNode("hello world", TextType.LINK, "https://www.boot.dev")
    print(node)

main()