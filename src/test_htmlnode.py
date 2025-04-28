from htmlnode import HTMLNode
from leafnode import LeafNode
import unittest

class TestHTMLNode(unittest.TestCase):
    
    def testNode(self):
        node = HTMLNode(tag="p", value="test value", props= {"href": "https://www.google.com","target": "_blank"})
        props = node.props_to_html()
        self.assertEqual(props, " href=\"https://www.google.com\" target=\"_blank\"")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),"<a href=\"https://www.google.com\">Click me!</a>")


