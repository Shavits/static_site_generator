from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    
    def testNode(self):
        node = HTMLNode(tag="p", value="test value", props= {"href": "https://www.google.com","target": "_blank"})
        print(node)
        props = node.props_to_html()
        self.assertEqual(props, " href=\"https://www.google.com\" target=\"_blank\"")

