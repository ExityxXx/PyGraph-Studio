from node.node import Node

# ValueNode - базовый класс для узлов передачи данных
class ValueNode(Node):
    def __init__(self, uid : int, header : str,
                 code : str, x : int, y : int,
                 in_port_enable : bool,
                 out_port_enable : bool, value : str) \
        -> None:
        super().__init__(uid, header,
                         code, x, y,
                         in_port_enable,
                         out_port_enable)
        self._value = value
        self._widget = None
    
    def update_widget_display(self, new_value):
        if hasattr(self.widget, "delete") and hasattr(self.widget, "insert"):
            self.widget.delete(0, "end")
            self.widget.insert(0, new_value)

    def bind_widget(self, widget) -> None:
        self._widget = widget
        self.update_widget_display(self.value)
    
    def on_connect(self, canvas, start_node) -> None:
        raise NotImplementedError
    
    def on_disconnect(self, canvas, restore_data, restore_text) -> None:
        raise NotImplementedError
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def widget(self):
        if self._widget:
            return self._widget
        else:
            raise ValueError("ValueNode Error: self._widget not exists (is None).")
    
    @widget.setter
    def widget(self, new_widget):
        self.bind_widget(new_widget)
