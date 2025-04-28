

class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")

    def props_to_html(self):
        res = ""
        for key, value in self.props.items():
                res += f' {key}="{value}"'
        return res
    
    def __repr__(self):
         return f"HTML Node = tag - {self.tag}, value - {self.value}, children - {self.children}, props - {self.props}"
    
    
