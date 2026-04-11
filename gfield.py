from node import Node

class Gfield:
    def __init__(self, id, name, description, canvas, nodes):
        self.id = id
        self.name = name
        self.description = description
        self.canvas = canvas
        self.nodes : dict[int, Node] = {}
        self.node_uid = 0

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_canvas(self):
        return self.canvas
    
    def get_nodes(self):
        return self.nodes

    def add_node(self, name, code):
        self.nodes[self.node_uid] = Node(self.node_uid, name, code)
        self.node_uid += 1
        return self.node_uid
    