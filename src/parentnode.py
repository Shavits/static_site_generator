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
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        
            
