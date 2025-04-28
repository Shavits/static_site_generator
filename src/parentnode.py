from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag,None,children,props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("No Tag Provided")
        if not self.children:
            raise ValueError("No Children Provided")
        return self.to_html_helper(self)

    def to_html_helper(self, node):
        res = ""
        if not node.children:
            res = LeafNode(node.tag, node.value, node.props).to_html()
        else:
            for child in node.children:
                res += f"<{node.tag}{node.props_to_html()}>{self.to_html_helper(child)}</{node.tag}>"
        return res
        
            
