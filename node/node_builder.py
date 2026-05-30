from node.node import Node
from node.value_node import ValueNode
from gfield import Gfield
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from node.node_drag import NodeDragger
from node.node_port_connector import NodePortConnector
from constants import PGS_NODE_ITEMS

PRINT_TO_SCREEN_NODE_NAME = PGS_NODE_ITEMS[0]
TRANSFER_DATA_NODE_NAME = PGS_NODE_ITEMS[1]
GET_VARIABLE_NODE_NAME = PGS_NODE_ITEMS[2]
SET_VARIABLE_NODE_NAME = PGS_NODE_ITEMS[3]
NEW_VARIABLE_NODE_NAME = PGS_NODE_ITEMS[4]

class NodeBuilder:
    """
    Строитель узлов (Builder pattern) для создания визуальных узлов на Canvas.
    
    Этот класс инкапсулирует всю логику создания узлов: отрисовку графических
    элементов (прямоугольник, заголовок, код), создание портов ввода/вывода,
    а также привязку событий для перетаскивания и редактирования.
    
    Основная цель — вынести сложную логику создания узлов из класса MainWindow
    для улучшения читаемости и поддерживаемости кода.
    
    Attributes
    ----------
    parent : MainWindow
        Ссылка на родительское окно приложения. Необходима для доступа к методам
        обработки событий (port_connection_start, node_drag_start и т.д.).
    
    Methods
    -------
    build_node(canvas, gfield, x, y, name, code, in_port_enable, out_port_enable,
          width, height, outline_color, is_start_node=False)
        Основной метод, создающий узел и возвращающий объект Node.
    
    create_ports(canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable)
        Создаёт порты ввода/вывода для узла и привязывает события.
    
    bind_events(canvas, node, node_rect_id, node_header_id, node_code_id)
        Привязывает события перетаскивания к элементам узла.
    
    Notes
    -----
    Класс использует паттерн "Строитель" (Builder), где метод build() является
    "директором", который последовательно вызывает вспомогательные методы для
    построения узла. Такой подход позволяет легко расширять функциональность
    (например, добавить новые типы узлов) без изменения основного кода.
    
    Examples
    --------
    >>> builder = NodeBuilder(main_window)
    >>> node = builder.build(
    ...     canvas=canvas,
    ...     gfield=gfield,
    ...     x=100, y=100,
    ...     name="Печать",
    ...     code='print("Hello")',
    ...     in_port_enable=True,
    ...     out_port_enable=True,
    ...     width=170, height=55,
    ...     outline_color="#FFD000"
    ... )
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.node_port_connector : NodePortConnector = NodePortConnector(self.parent)
        self.node_dragger : NodeDragger = NodeDragger(self.parent, self.node_port_connector)

    def build_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color, is_start_node=False):
        
        names_functions = {
            PRINT_TO_SCREEN_NODE_NAME: self.build_print_node,
            TRANSFER_DATA_NODE_NAME: self.transfer_data_node,
            GET_VARIABLE_NODE_NAME: self.get_variable_node,
            SET_VARIABLE_NODE_NAME: self.set_variable_node,
            NEW_VARIABLE_NODE_NAME: self.new_variable_node
        }

        if name in PGS_NODE_ITEMS:
            # ! Создание уникального узла
            return names_functions[name](canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color)
            
        
        result = gfield.add_node(name, code, x, y, False, False, "Node")
        node : Node = result[1]
        if is_start_node:
            node.is_start_node = True
                    
        # Стандартная ширина: 170
        # Стандартная длина: 55
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name,
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.width = width
        node.height = height
        self.create_ports(canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable, height)
        self.bind_events(canvas, node, node_rect_id, node_header_id, None)
        return node
    
    def build_print_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color):
        
        def on_text_change(event=None):
            node.value = event.widget.get()
            self.parent.update_inspector_panel(node)
            self.parent.value_entry.delete(0, "end")
            self.parent.value_entry.insert(0, node.value)
            
        from .unique.print_node import PrintNode
        result = gfield.add_node(name, code, x, y, False, False, "PrintNode", print_node_text="")
        node : PrintNode = result[1]
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width + 65,
            y + height + 35,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name, 
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 18,
            text="Значение: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )
        entry = Entry(canvas,
                      font=("Segoe UI", 10), bg="#242424",
                      fg="#D8D8D8", bd=0, insertbackground="white")
        
        entry.bind("<KeyRelease>", on_text_change)
        entry.bind("<Return>", lambda event: self.parent.focus_set())

        entry_window = canvas.create_window(
            x + 90, (y + height // 2) + 17, window=entry, anchor="nw", width=130, height=19
        )
        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.width = width + 65
        node.height = height + 35
        node.widget = entry
        node.add_canvas_element(node_value_label)
        node.add_canvas_element(entry_window)
        
        self.create_ports(canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable, height)
        self.create_in_data_port(canvas, gfield, node, node_rect_id)
        self.bind_events(canvas, node, node_rect_id, node_header_id, node.get_node_elements())
        return node
    
    def transfer_data_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color):
        def on_text_change(event=None):
            node.value = event.widget.get()
            if node.data_output_node:
                if hasattr(node.data_output_node, "target_value"):
                    node.data_output_node.target_value = node.value
                else:
                    node.data_output_node.value = node.value
            # self.parent.update_inspector_panel(node)
            # self.parent.value_entry.delete(0, "end")
            # self.parent.value_entry.insert(0, node.get_data())
            
        from .unique.transfer_data_node import TransferDataNode
        result = gfield.add_node(name, code, x, y, False, False, "TransferDataNode", data="")
        node : TransferDataNode = result[1]
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width + 65,
            y + height + 35,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name, 
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 18,
            text="Значение: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )
        entry = Entry(canvas,
                      font=("Segoe UI", 10), bg="#242424",
                      fg="#D8D8D8", bd=0, insertbackground="white")
        
        entry.bind("<KeyRelease>", on_text_change)
        entry.bind("<Return>", lambda event: self.parent.focus_set())

        entry_window = canvas.create_window(
            x + 90, (y + height // 2) + 17, window=entry, anchor="nw", width=130, height=19
        )
        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.width = width + 65
        node.height = height + 35
        node.widget = entry
        node.add_canvas_element(node_value_label)
        node.add_canvas_element(entry_window)
        self.create_out_data_port(canvas, gfield, node, node_rect_id)
        self.bind_events(canvas, node, node_rect_id, node_header_id, node.get_node_elements())
        return node
    def get_variable_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color):
        def on_select(event=None):
            node.value = event.widget.get()
            if node.data_output_node:
                node.data_output_node.value = node.value
                self.parent.focus_set()

        def update_box_values(box):
            box["values"] = self.parent.struct.get_variables_names_list()

        from .unique.get_variable_node import GetVariableNode
        result = gfield.add_node(name, code, x, y, False, False, "GetVariableNode", variable="")
        node : GetVariableNode = result[1]
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width + 65,
            y + height + 35,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name, 
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 18,
            text="Выбрать: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )
        box = ttk.Combobox(
            canvas, 
            values=self.parent.struct.get_variables_names_list(), 
            state="readonly")
        box.bind("<<ComboboxSelected>>", on_select)
        box.bind("<Return>", self.parent.focus_set())
        box.bind("<ButtonPress-1>", lambda e: update_box_values(box))

        entry_window = canvas.create_window(
            x + 85, (y + height // 2) + 17, window=box, anchor="nw", width=130, height=19
        )
        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.width = width + 65
        node.height = height + 35
        node.widget = box
        node.add_canvas_element(node_value_label)
        node.add_canvas_element(entry_window)
        self.create_out_data_port(canvas, gfield, node, node_rect_id)
        self.bind_events(canvas, node, node_rect_id, node_header_id, node.get_node_elements())
    def set_variable_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color):

        def on_text_change(event=None):
            node.target_value = event.widget.get()

        def on_select(event=None):
            node.value = event.widget.get()
            # if node.data_input_node:
            #     node.data_input_node.value = node.target_value
            #     self.parent.focus_set()

        def update_box_values(box):
            box["values"] = self.parent.struct.get_variables_names_list()

        from .unique.set_variable_node import SetVariableNode
        result = gfield.add_node(name, code, x, y, False, False, "SetVariableNode", variable="", value="")
        node : SetVariableNode = result[1]
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width + 65,
            y + height + 60,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name, 
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 20,
            text="Выбрать: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )

        box = ttk.Combobox(
            canvas, 
            values=self.parent.struct.get_variables_names_list(), 
            state="readonly")
        
        box.bind("<<ComboboxSelected>>", on_select)
        box.bind("<Return>", self.parent.focus_set())
        box.bind("<ButtonPress-1>", lambda e: update_box_values(box))
        
        box_window = canvas.create_window(
            x + 85, (y + height // 2) + 20, window=box, anchor="nw", width=130, height=19
        )
        node_new_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 45,
            text="Значение: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )
        entry = Entry(canvas,
                      font=("Segoe UI", 10), bg="#242424",
                      fg="#D8D8D8", bd=0, insertbackground="white")
        
        entry_window = canvas.create_window(
            x + 85, (y + height // 2) + 45, window=entry, anchor="nw", width=130, height=19
        )

        entry.bind("<KeyRelease>", on_text_change)
        entry.bind("<Return>", lambda event: self.parent.focus_set())

        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.widget = box
        node.add_canvas_element(node_value_label)
        node.add_canvas_element(box_window)
        node.add_canvas_element(node_new_value_label)
        node.add_canvas_element(entry_window)
        self.create_in_data_port(canvas, gfield, node, node_rect_id)
        self.create_ports(canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable, height)
        self.bind_events(canvas, node, node_rect_id, node_header_id, node.get_node_elements())
    def new_variable_node(self, canvas, gfield, x, y, name, code,
                         in_port_enable, out_port_enable,
                         width, height, outline_color):
        
        def value_on_text_change(event=None):
            node.value = event.widget.get()

        def name_on_text_change(event=None):
            node.target_value = event.widget.get()
        from .unique.new_variable_node import NewVariableNode
        result = gfield.add_node(name, code, x, y, False, False, "NewVariableNode", variable="", value="")
        node : NewVariableNode = result[1]
        node_rect_id = canvas.create_rectangle(
            x,
            y,
            x + width + 65,
            y + height + 60,
            fill="#242424",
            outline=outline_color,
            tags=("node", "rect")
        )
        node_header_id = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) - 10,
            text=name, 
            fill="#FFFFFF",
            anchor=NW,
            font=("Segoe UI", 11),
            tags=("node", "header")
        )
        node_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 20,
            text="Имя: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )

        name_entry = Entry(canvas,
                      font=("Segoe UI", 10), bg="#242424",
                      fg="#D8D8D8", bd=0, insertbackground="white")
        
        name_entry.bind("<KeyRelease>", value_on_text_change)
        name_entry.bind("<Return>", lambda event: self.parent.focus_set())
        
        name_entry_window = canvas.create_window(
            x + 55, (y + height // 2) + 20, window=name_entry, anchor="nw", width=130, height=19
        )
        node_new_value_label = canvas.create_text(
            x + 20 if in_port_enable else x + 10,
            (y + height // 2) + 45,
            text="Значение: ", 
            fill="#8D8D8D",
            anchor=NW,
            font=("Segoe UI", 10),
            tags=("node", "label")
        )
        value_entry = Entry(canvas,
                      font=("Segoe UI", 10), bg="#242424",
                      fg="#D8D8D8", bd=0, insertbackground="white")
        
        value_entry_window = canvas.create_window(
            x + 85, (y + height // 2) + 45, window=value_entry, anchor="nw", width=130, height=19
        )

        value_entry.bind("<KeyRelease>", name_on_text_change)
        value_entry.bind("<Return>", lambda event: self.parent.focus_set())

        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.widget = name_entry
        node.add_canvas_element(node_value_label)
        node.add_canvas_element(name_entry_window)
        node.add_canvas_element(node_new_value_label)
        node.add_canvas_element(value_entry_window)
        self.create_in_data_port(canvas, gfield, node, node_rect_id)
        self.create_ports(canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable, height)
        self.bind_events(canvas, node, node_rect_id, node_header_id, node.get_node_elements())
    def create_in_data_port(self, canvas, gfield, node, node_rect_id):
        x1, y1, x2, y2 = canvas.coords(node_rect_id)
        pos_y = (y1 + y2) // 2
        in_data_port_point = canvas.create_oval(
            x1 - 5, pos_y + 5,
            x1 + 5, pos_y + 15,
            fill="#7E4396", outline="white",
            tags="in_data_port"
        )
        node.data_in_port_id = in_data_port_point
        gfield.add_data_port(in_data_port_point)
        canvas.tag_bind(in_data_port_point, "<ButtonPress-1>", lambda e: self.node_port_connector.data_port_connection_start(e, in_data_port_point))
        canvas.tag_bind(in_data_port_point, "<B1-Motion>", lambda e: self.node_port_connector.data_port_connection_process(e, in_data_port_point))
        canvas.tag_bind(in_data_port_point, "<ButtonRelease-1>", lambda e: self.node_port_connector.data_port_connection_end(e, in_data_port_point))
   
    def create_out_data_port(self, canvas, gfield, node, node_rect_id):
        x1, y1, x2, y2 = canvas.coords(node_rect_id)
        pos_y = (y1 + y2) // 2
        out_data_port_point = canvas.create_oval(
            x2 - 5, pos_y + 5,
            x2 + 5, pos_y + 15,
            fill="#7E4396", outline="white",
            tags="out_data_port"
        )
        node.data_out_port_id = out_data_port_point
        gfield.add_data_port(out_data_port_point)
        canvas.tag_bind(out_data_port_point, "<ButtonPress-1>", lambda e: self.node_port_connector.data_port_connection_start(e, out_data_port_point))
        canvas.tag_bind(out_data_port_point, "<B1-Motion>", lambda e: self.node_port_connector.data_port_connection_process(e, out_data_port_point))
        canvas.tag_bind(out_data_port_point, "<ButtonRelease-1>", lambda e: self.node_port_connector.data_port_connection_end(e, out_data_port_point))
        
    def create_ports(self, canvas, gfield, node, node_rect_id, in_port_enable, out_port_enable, height):
        x1, y1, x2, y2 = canvas.coords(node_rect_id)
        in_port_point = None
        out_port_point = None
        
        if in_port_enable:
            pos_y = (y1 + y2) // 2
            in_port_point = canvas.create_oval(
                x1 - 5, (y1 + height // 2) - 5,
                x1 + 5, (y1 + height // 2) + 5,
                fill="#1C7700", outline="white",
                tags="in_port"
            )

            node.in_port_enable = True
            node.in_port_id = in_port_point
            gfield.add_port(in_port_point)
            canvas.tag_bind(in_port_point, "<ButtonPress-1>", lambda e: self.node_port_connector.port_connection_start(e, in_port_point))
            canvas.tag_bind(in_port_point, "<B1-Motion>", lambda e: self.node_port_connector.port_connection_process(e, in_port_point))
            canvas.tag_bind(in_port_point, "<ButtonRelease-1>", lambda e: self.node_port_connector.port_connection_end(e, in_port_point))
            
        if out_port_enable:
            pos_y = (y1 + y2) // 2
            out_port_point = canvas.create_oval(
                x2 - 5, pos_y - 5,
                x2 + 5, pos_y + 5, 
                fill="#1C7700", outline="white",
                tags="out_port"
            )
            node.out_port_enable = True
            node.out_port_id = out_port_point
            gfield.add_port(out_port_point)
            canvas.tag_bind(out_port_point, "<ButtonPress-1>", lambda e: self.node_port_connector.port_connection_start(e, out_port_point))
            canvas.tag_bind(out_port_point, "<B1-Motion>", lambda e: self.node_port_connector.port_connection_process(e, out_port_point))
            canvas.tag_bind(out_port_point, "<ButtonRelease-1>", lambda e: self.node_port_connector.port_connection_end(e, out_port_point))
        
    def bind_events(self, canvas, node : Node, node_rect_id, node_header_id, node_elements):
        node_elements = node_elements or []
        canvas.tag_bind(node_rect_id, "<ButtonPress-1>", lambda e: self.node_dragger.node_drag_start(e, node_rect_id))
        canvas.tag_bind(node_rect_id, "<B1-Motion>", 
                        lambda e: self.node_dragger.node_drag_motion(
                            e, node, node_header_id, node_rect_id,
                            node.in_port_id, node.out_port_id,
                            node.data_in_port_id, node.data_out_port_id,
                            *node_elements))
        canvas.tag_bind(node_rect_id, "<ButtonRelease-1>", lambda e: self.node_dragger.node_drag_end(e, node_rect_id, node))
        canvas.tag_bind(node_header_id, "<Double-Button-1>", lambda e: self.node_entry(e, node))
    
    def node_entry(self, event, node : Node):
        def save_data(event=None):
            name = node_name_entry.get().strip()
            if not name:
                showwarning("Предупреждение",
                            "Имя узла пустое")
                node_name_entry.destroy()
                return
            canvas.itemconfig(node_header_id, text=name)
            node.header = name
            node_name_entry.destroy()
            canvas.itemconfig(node.header_id, state="normal")
            self.parent.node_name_entry.delete(0, "end")
            self.parent.node_name_entry.insert(0, node.header)
        
        canvas : Canvas = self.parent.get_current_canvas()
        self.parent.update_inspector_panel(node)
        node_header_id = node.header_id
        x1, y1 = canvas.coords(node_header_id)
        node_name_entry = ttk.Entry(canvas)
        node_name_entry.place(x=x1, y=y1)
        node_name_entry.insert(0, canvas.itemcget(node_header_id, "text"))
        canvas.itemconfig(node.header_id, state="hidden")
        node_name_entry.bind("<Return>", save_data)
        node_name_entry.bind("<FocusOut>", save_data)

    def delete_connection(self, event, line, line_type):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        if line_type == "data":
            self.delete_data_connection(event, line)
            return

        for node in gfield.get_nodes().values():
            if node.connection_line_id == line:
                break

        canvas.delete(node.connection_line_id)
        node.connection_line_id = None
        node.output_node.input_node = None
        node.output_node = None
    
    def delete_data_connection(self, event, line):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        for node in gfield.get_nodes().values():
            if node.data_connection_line_id == line:
                break
        
        self.restore_input_fields(node, restore_data=False)
        canvas.delete(node.data_connection_line_id)
        node.data_connection_line_id = None
        node.data_output_node.data_input_node = None
        node.data_output_node = None

    def delete_node(self, event, item):
        from .unique.transfer_data_node import TransferDataNode
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        for node in gfield.get_nodes().values():
            if node.rect_id == item:
                break
        
        if node.is_start_node:
            return
        
        self.restore_input_fields(node, restore_data=True)

        for other in gfield.get_nodes().values():
            if other.input_node == node:
                other.input_node = None
            if other.output_node == node:
                other.output_node = None
            if other.data_input_node == node:
                other.data_input_node = None
            if other.data_output_node == node:
                other.data_output_node = None

        if node.input_node:
            canvas.delete(node.input_node.connection_line_id)
            node.input_node.connection_line_id = None
        
        if node.output_node:
            canvas.delete(node.connection_line_id)
            node.connection_line_id = None
        
        if node.data_input_node:
            canvas.delete(node.data_input_node.data_connection_line_id)
            node.data_input_node.data_connection_line_id = None 

        if node.data_output_node:
            canvas.delete(node.data_connection_line_id)
            node.data_connection_line_id = None

        if node.input_node:
            node.input_node = None
        if node.output_node:
            node.output_node = None
        if node.data_input_node:
            node.data_input_node = None
        if node.data_output_node:
            node.data_output_node = None
        
        if node.in_port_id:
            gfield.remove_port(node.in_port_id)
        
        if node.out_port_id:
            gfield.remove_port(node.out_port_id)
        
        if node.data_in_port_id:
            gfield.remove_data_port(node.data_in_port_id)
        
        if node.data_out_port_id:
            gfield.remove_data_port(node.data_out_port_id)
            
        for item in [node.rect_id,
                     node.header_id,
                     node.in_port_id,
                     node.out_port_id,
                     node.data_in_port_id,
                     node.data_out_port_id,
                     *node.canvas_elements_id]:
            if item:
                canvas.delete(item)
        gfield.remove_node(node.uid)
        
    
    def restore_input_fields(self, target_node : ValueNode, restore_data : bool):
        canvas : Canvas = self.parent.get_current_canvas()
        if hasattr(target_node, "value"):
            text = target_node.value
        else:
            text = ""

        if target_node.data_output_node:
            target_node = target_node.data_output_node

        if not hasattr(target_node, "widget") and not target_node.widget:
            return
        
        if hasattr(target_node, "on_disconnect") and target_node.on_disconnect:
            target_node.on_disconnect(canvas, restore_data=restore_data, restore_text=text)
        
    def smart_delete_input_fields(self, target_node : Node | ValueNode, start_node : ValueNode):
        canvas : Canvas = self.parent.get_current_canvas()
        if not hasattr(target_node, "widget") or not target_node.widget:
            return
        target_node.on_connect(canvas, start_node)
