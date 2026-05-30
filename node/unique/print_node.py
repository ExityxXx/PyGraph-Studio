from ..value_node import ValueNode

class PrintNode(ValueNode):
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
    
    def on_connect(self, canvas, start_node : ValueNode) -> None:
        if self.value and not start_node.value:
            start_node.value = self.value
        else:
            self.value = start_node.value
        elements = self.get_node_elements()
        canvas.itemconfig(elements[0], text="Привязано к источнику")
        canvas.itemconfig(elements[1], state="hidden")
        start_node.update_widget_display(self.value)
    
    def on_disconnect(self, canvas, restore_data : bool, restore_text : str) -> None:
        elements = self.get_node_elements()
        canvas.itemconfig(elements[0], text="Значение: ")
        canvas.itemconfig(elements[1], state="normal")
        if restore_data:
            self.update_widget_display(restore_text)
            self.value = restore_text
        else:
            self.value = ""

    def generate_code(self):
        return f"print(f\"{self.value}\")"    

    def __repr__(self):
        return f"PrintNode(uid={self.uid},header={self.header}, code={self.code}, x={self.x}, y={self.y}, in_port={self.in_port_enable}, out_port={self.out_port_enable}, value={self.value})"
