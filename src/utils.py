from textnode import TextNode, TextType
from leafnode import LeafNode
import re

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
        
    
def text_to_textnodes(text):
    if text == "":
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            res.extend(__split_node(old_node, delimiter, text_type))
        else:
            res.append(old_node)
    return res

def __split_node(old_node, delimiter, text_type):
    if(old_node.text == ""):
        return []
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


def extract_markdown_images(text):
    
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #print(f"extracted images: {matches}")
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    #print(f"extracted links: {matches}")
    return matches

def split_nodes_image(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            res.extend(__split_node_image(old_node))
        else:
            res.append(old_node)
    return res

def split_nodes_link(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            res.extend(__split_node_link(old_node))
        else:
            res.append(old_node)
    return res

def __split_node_image(old_node):
    if(old_node.text == ""):
        return []
    res = []
    matches = extract_markdown_images(old_node.text)
    cur_text = old_node.text
    if len(matches) == 0:
        return [old_node]
    for match in matches:
        split_text = cur_text.split(f"![{match[0]}]({match[1]})", 1)
        if(len(split_text) >=2):
            res.append(TextNode(split_text[0], TextType.TEXT))
        res.append(TextNode(match[0], TextType.IMAGE, match[1]))
        cur_text = split_text[-1]
    if cur_text != "":
        res.append(TextNode(cur_text, TextType.TEXT))
    return res

def __split_node_link(old_node):
    if(old_node.text == ""):
        return []
    res = []
    matches = extract_markdown_links(old_node.text)
    cur_text = old_node.text
    if len(matches) == 0:
        return [old_node]
    for match in matches:
        split_text = cur_text.split(f"[{match[0]}]({match[1]})", 1)
        if(len(split_text) >=2):
            res.append(TextNode(split_text[0], TextType.TEXT))
        res.append(TextNode(match[0], TextType.LINK, match[1]))
        cur_text = split_text[-1]
    if cur_text != "":
        res.append(TextNode(cur_text, TextType.TEXT))
    return res
    

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    fileterd_blocks = list(filter(lambda block: block != "", split_blocks))
    stripped_blockes = list(map(lambda block: block.strip(), fileterd_blocks))
    return stripped_blockes

    
    