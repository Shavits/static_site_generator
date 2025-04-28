from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(node):
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : node.url, "alt" : node.text})
        case _:
            raise Exception("Invalid type")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    pass

