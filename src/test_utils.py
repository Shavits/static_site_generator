from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from utils import *
import unittest

class TestUtils(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
    
    def test_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")
    
    def test_code(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "https://www.google.com")
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://www.google.com/image.png")
        self.assertEqual(html_node.props["alt"], "This is an image")
    
    def test_invalid_type(self):
        node = TextNode("This is an invalid type", "invalid_type")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ])
    
    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This is text with a **bold** and *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is text with no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delimiter_other_types_in_input(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is a bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            node2
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links(
        "This is text with no link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images(
        "This is text with no image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://www.google.com) and [another link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.google.com"), ("another link", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ])
    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text with no image", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node]) 

    def test_split_nodes_image_multiple(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ])

    def test_split_nodes_image_other_types_in_input(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node2 = TextNode("This is a bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node, node2])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            node2
        ])
    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com")
        ])
    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with no link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node]) 
    def test_split_nodes_link_multiple(self):
        node = TextNode("This is text with a [link](https://www.google.com) and [another link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://www.boot.dev")
        ])

    def test_split_nodes_link_other_types_in_input(self):
        node = TextNode("This is text with a [link](https://www.google.com)", TextType.TEXT)
        node2 = TextNode("This is a bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node, node2])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            node2
        ])
    def test_split_nodes_link_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])



        


if __name__ == "__main__":
    unittest.main()

    
    