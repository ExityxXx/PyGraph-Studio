from ..value_node import ValueNode

class GetVariableNode(ValueNode):
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
    def update_widget_display(self, new_value):
        if hasattr(self.widget, "delete") and hasattr(self.widget, "insert"):
            if new_value.startswith("{") and new_value.endswith("}"):
                self.widget.set(new_value[1:len(new_value)-1])
            else:
                self.widget.set(new_value)

    def generate_code(self):
        return f"{{{self.variable}}}"

    def __repr__(self):
        return f"GetVariableNode(uid={self.uid}, header={self.header}, code={self.code}, x={self.x}, y={self.y}, in_port={self.in_port_enable}, out_port={self.out_port_enable}, value={self.value})"
    
    @property
    def value(self):
        if self._value:
            return f"{{{self._value}}}"
        return ""

    @value.setter
    def value(self, new_value):
        self._value = new_value
        