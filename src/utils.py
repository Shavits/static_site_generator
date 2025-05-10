from textnode import TextNode, TextType
from parentnode import ParentNode
from blocknode import BlockType
from leafnode import LeafNode
from string import digits
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
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    if __check_heading(block):
        return BlockType.HEADING
    elif __check_code(block):
        return BlockType.CODE
    elif __check_quote(block):
        return BlockType.QUOTE
    elif __check_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif __check_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH



def __check_heading(block):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))
        
def __check_code(block):
    return block.startswith("```") and block.endswith("```")

def __check_quote(block):
    lines = block.split("\n")
    res = True
    for line in lines:
        if not line.startswith('>'):
            res = False
    return res

def __check_unordered_list(block): 
    lines = block.split("\n")
    res = True
    for line in lines:
        if not line.startswith("- "):
            res = False
    return res

def __check_ordered_list(block):
    lines = block.split("\n")
    res = True
    last_num = 0
    for line in lines:
        if not line.startswith(f"{last_num+1}. "):
            res = False
        last_num+=1
    return res
        
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(__block_to_html_node(block, block_type))
    

    return ParentNode("div", children)

def __block_to_html_node(block, block_type):
    tag = ""
    children = []
    match block_type:
        case BlockType.HEADING:
            tag =f"h{__count_heading_hashes(block)}"
            children = __heading_to_html_children(block)
        case BlockType.UNORDERED_LIST:
            tag = "ul"
            children = __unordered_list_to_html_children(block)
        case BlockType.ORDERED_LIST:
            tag = "ol"
            children = __ordered_list_to_html_children(block)
        case BlockType.CODE:
            tag = "pre"
            children = [LeafNode("code", block[3:-3].lstrip("\n"))]
        case BlockType.QUOTE:
            tag = "blockquote"
            children = __blockquote_to_html_children(block)
        case BlockType.PARAGRAPH:
            tag = "p"
            lines = block.split("\n")
            paragraph = " ".join(lines)
            text_nodes = text_to_textnodes(paragraph)
            children = list(map(text_node_to_html_node, text_nodes))

    return ParentNode(tag, children)
        

def __heading_to_html_children(block):
    stripped = block.strip("# ")
    text_nodes= text_to_textnodes(stripped)
    return list(map(text_node_to_html_node, text_nodes))

def __unordered_list_to_html_children(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        stripped = line[2:]
        text_nodes= text_to_textnodes(stripped)
        children.append(ParentNode("li", (list(map(text_node_to_html_node, text_nodes)))))
    return children
def __ordered_list_to_html_children(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        stripped = line.lstrip(digits + ". ")
        text_nodes= text_to_textnodes(stripped)
        children.append(ParentNode("li", (list(map(text_node_to_html_node, text_nodes)))))
    return children

def __blockquote_to_html_children(block):
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        text_nodes= text_to_textnodes(content)
        children = ((list(map(text_node_to_html_node, text_nodes))))
        return children
    

    


def __count_heading_hashes(text):
    count = 0
    for char in text:
        if char == '#':
            count += 1
        else:
            break
    return count
