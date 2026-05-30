from node.node import Node
from node.unique.print_node import PrintNode
from node.unique.transfer_data_node import TransferDataNode
from node.unique.get_variable_node import GetVariableNode
from node.unique.set_variable_node import SetVariableNode
from node.unique.new_variable_node import NewVariableNode
from pg_item import PG_Item
from constants import PGS_NODE_CLASSES_STR

class Gfield(PG_Item):
    def __init__(self, id : int, name : str, description : str, canvas):
        super().__init__(id, name)
        self.description : str = description
        self.canvas = canvas
        self.nodes : dict[int, Node] = {}
        self.node_uid : int = 0
        self.ports : list[int] = []
        self.data_ports : list[int] = []
        # Это переменная хранит текущую выбранную ноду
        # Необходимо для инспекций
        self.selected_node : Node | None = None
    
    def get_description(self):
        return self.description
    
    def get_canvas(self):
        return self.canvas
    
    def get_nodes(self):
        return self.nodes

    def get_ports(self):
        return self.ports
    
    def get_data_ports(self):
        return self.data_ports
    
    def add_node(self, name, code, x, y, in_port, out_port, node_type : str, **node_args : list):
        if node_type not in PGS_NODE_CLASSES_STR:
            raise ValueError("Entered node type not exists in PGS_NODE_CLASSES_STR (source: constants.py)")
        
        if node_type == "Node":
            self.nodes[self.node_uid] = Node(self.node_uid, name, code, x, y, in_port, out_port)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        elif node_type == "PrintNode":
            print_node_text = node_args["print_node_text"]
            self.nodes[self.node_uid] = PrintNode(self.node_uid, name, code, x, y, in_port, out_port, print_node_text)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        elif node_type == "TransferDataNode":
            data = node_args["data"]
            self.nodes[self.node_uid] = TransferDataNode(self.node_uid, name, code, x, y, in_port, out_port, data)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        elif node_type == "GetVariableNode":
            variable = node_args["variable"]
            self.nodes[self.node_uid] = GetVariableNode(self.node_uid, name, code, x, y, in_port, out_port, variable)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        elif node_type == "SetVariableNode":
            variable = node_args["variable"]
            value = node_args["value"]
            self.nodes[self.node_uid] = SetVariableNode(self.node_uid, name, code, x, y, in_port, out_port, variable, value)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        elif node_type == "NewVariableNode":
            variable = node_args["variable"]
            value = node_args["value"]
            self.nodes[self.node_uid] = NewVariableNode(self.node_uid, name, code, x, y, in_port, out_port, variable, value)
            self.node_uid += 1
            return self.node_uid, self.nodes[self.node_uid - 1]
        
    def add_port(self, port_id):
        self.ports.append(port_id)
    
    def add_data_port(self, port_id):
        self.data_ports.append(port_id)
        
    def set_selected_node(self, selected_node : Node) -> None:
        if selected_node:
            self.selected_node = selected_node

    def __sort_nodes_keys(self) -> None:
        sorted_keys = sorted(self.get_nodes().keys())
        new_dict = {}
        new_id = 0

        for key in sorted_keys:
            item = self.get_nodes()[key]
            item.uid = new_id
            new_dict[new_id] = item
            new_id += 1

        self.nodes = new_dict  

    def remove_node(self, uid : int) -> None:
        if uid in self.get_nodes().keys():
            del self.nodes[uid]
        self.__sort_nodes_keys()
    
    def remove_port(self, port_id):
        if port_id in self.ports:
            self.ports.remove(port_id)

    def remove_data_port(self, port_id):
        if port_id in self.data_ports:
            self.data_ports.remove(port_id)
            