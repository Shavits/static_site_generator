

class HTMLNode:

    def __init__(self, tag=None, value, children, props):
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
    
    
