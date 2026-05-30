from ..value_node import ValueNode

class SetVariableNode(ValueNode):
    def __init__(self, uid : int, header : str,
                 code : str, x : int, y : int,
                 in_port_enable : bool,
                 out_port_enable : bool, value : str, target : str) \
          -> None:
        super().__init__(uid, header,
                         code, x, y,
                         in_port_enable,
                         out_port_enable,
                         value)
        # value - будет именем переменной
        # target_value - на какое зн-е изменить переменную
        self.target_value = target

    def on_connect(self, canvas, start_node : ValueNode) -> None:
        if self.target_value and not start_node.value:
            start_node.value = self.target_value
        else:
            self.target_value = start_node.value
        elements = self.get_node_elements()
        canvas.itemconfig(elements[2], text="Привязано к источнику")
        canvas.itemconfig(elements[3], state="hidden")
        start_node.update_widget_display(start_node._value)
    def on_disconnect(self, canvas, restore_data : bool, restore_text : str) -> None:
        elements = self.get_node_elements()
        canvas.itemconfig(elements[2], text=f"Значение: ")
        canvas.itemconfig(elements[3], state="normal")
                
        if restore_data:
            self.target_value = restore_text
            target_widget_name = canvas.itemcget(elements[3], "window")
            target_widget = canvas.nametowidget(target_widget_name)
            target_widget.delete(0, "end")
            target_widget.insert(0, self.target_value)
        else:
            self.target_value = ""
    def generate_code(self):
        return f"{self.value} = {self.target_value}"

    def __repr__(self):
        return f"SetVariableNode(uid={self.uid}, header={self.header}, code={self.code}, x={self.x}, y={self.y}, in_port={self.in_port_enable}, out_port={self.out_port_enable}, value={self.value}, target_value={self.target_value})"
    
    @property
    def value(self):
        if self._value:
            return self._value
        return ""

    @value.setter
    def value(self, new_value):
        self._value = new_value
        