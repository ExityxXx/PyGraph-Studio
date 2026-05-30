from ..value_node import ValueNode

class TransferDataNode(ValueNode):
    def __init__(self, uid : int, header : str,
                 code : str, x : int, y : int,
                 in_port_enable : bool,
                 out_port_enable : bool, value : str) \
          -> None:
        super().__init__(uid, header,
                         code, x, y,
                         in_port_enable,
                         out_port_enable,
                         value)
    
    def on_disconnect(self, canvas, restore_data : bool, restore_text : str) -> None:
        # Заглушка при удалений этого узла
        pass

    def generate_code(self):
        return f"{self.data}"    

    def __repr__(self):
        return f"TransferDataNode(uid={self.uid}, header={self.header}, code={self.code}, x={self.x}, y={self.y}, in_port={self.in_port_enable}, out_port={self.out_port_enable}, value={self.value})"
