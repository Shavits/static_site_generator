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
    res = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            res.extend(split_node(old_node, delimiter, text_type))
        else:
            res.append(old_node)
    return res
            

def split_node(old_node, delimiter, text_type):
    split_text = old_node.text.split(delimiter)
    #print(split_text)
    if len(split_text) ==1:
        return [old_node]
    if len(split_text) % 2 == 0:
        raise Exception("Invalid no closing delimiter")
    res = []
    for i in range(len(split_text)):
        if i%2 == 0:
            res.append(TextNode(split_text[i], TextType.TEXT))
        else:
            res.append(TextNode(split_text[i], text_type))
    return res
    