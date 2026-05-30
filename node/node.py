class Node:
    def __init__(self, uid : int, header : str, code : str, x : int, y : int, in_port_enable : bool = False, out_port_enable : bool = False) -> None:
        self.uid : int = uid
        self.header : str = header
        self.code : str = code
        self.x : int = x
        self.y : int = y
        self.width : int = None
        self.height : int = None
        self.in_port_enable : bool = in_port_enable
        self.out_port_enable : bool = out_port_enable
        self.input_node : Node = None
        self.output_node : Node = None
        self.data_input_node : Node = None
        self.data_output_node : Node = None
        self.is_start_node : bool = False
        
        # Canvas data
        self.rect_id : int = None
        self.header_id : int = None
        self.in_port_id : int = None
        self.out_port_id : int = None
        self.data_in_port_id : int = None
        self.data_out_port_id : int = None
        
        """
        Эта переменная будет хранить id объектов
        в канвасе для unique (уникальной) ноды
        которая хранит свой текст свои поля ввода
        свои порты и т.д
        """
        self.canvas_elements_id : list[int] = []
        self.connection_line_id : int = None
        self.data_connection_line_id : int = None

    def create_output_connection(self, target_node):
        self.output_node = target_node
        target_node.input_node = self
        
    def create_data_output_connection(self, target_node):
        self.data_output_node = target_node
        target_node.data_input_node = self
        
    def add_canvas_element(self, id):
        self.canvas_elements_id.append(id)
    
    def get_node_elements(self):
        return self.canvas_elements_id
    
    def generate_code(self):
        # переопределяется у дочек
        return ""
    
    def __repr__(self):
        return f"Node(uid={self.uid}, header={self.header}, code={self.code}, x={self.x}, y={self.y}, in_port={self.in_port_enable}, out_port={self.out_port_enable})"
