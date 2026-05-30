from tkinter import Canvas
from gfield import Gfield
from tkinter.messagebox import showwarning
from tkinter import TclError
from node.node import Node
from constants import StdColors

class NodePortConnector:
    def __init__(self, parent):
        self.parent = parent

    def port_connection_start(self, event, port_id):
        canvas : Canvas = self.parent.get_current_canvas()
        port = canvas.find_closest(event.x, event.y)[0]
        node = self.parent.find_node_at_port(canvas, port_id, self.parent.get_current_gfield())
        if node is None:
            return
        tags = canvas.gettags(port_id)
        
        if "in_port" in tags:
            if node.input_node is not None:
                return
            
        elif "out_port" in tags:
            if node.output_node is not None:
                return
            
        canvas.itemconfig(port_id, fill=StdColors.FLOW_NODE_ACTIVE)
        self.parent.connection_data = {
            "temp_line": None,
            "start_port": port,
            "temp_port_point": None
        }

    def port_connection_process(self, event, port_id):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        if self.parent.connection_data["temp_line"]:
            canvas.delete(self.parent.connection_data["temp_line"])

        x1, y1, x2, y2 = canvas.coords(port_id)
        port_center_x = (x1 + x2) // 2
        port_center_y = (y1 + y2) // 2
        mouse_x = canvas.canvasx(event.x)
        mouse_y = canvas.canvasy(event.y)
        self.parent.connection_data["temp_line"] = self.create_bezier_line(
            canvas, port_center_x, port_center_y, mouse_x, mouse_y,
            color=StdColors.FLOW_NODE_ACTIVE, tags="temp_line"
        )

        current_canvas_obj = self.parent.find_port_at_position(canvas, mouse_x, mouse_y, gfield)
        if current_canvas_obj in gfield.ports and (canvas.itemcget(current_canvas_obj, "tags") in ("in_port", "out_port")):
            self.parent.connection_data["temp_port_point"] = current_canvas_obj
            canvas.itemconfig(current_canvas_obj, fill=StdColors.FLOW_NODE_ACTIVE)
        else:
            canvas.itemconfig(self.parent.connection_data["temp_port_point"], fill=StdColors.FLOW_NODE_NORMAL)

    def port_connection_end(self, event, from_port):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()
        mouse_x = canvas.canvasx(event.x)
        mouse_y = canvas.canvasy(event.y)
        """
        from_port - ID порта (точки) с которого начинается соединение т.е from_port
        to_port - ID порта с которым соединяется начальный порт
        """

        if self.parent.connection_data and self.parent.connection_data["temp_line"]:
            canvas.delete(self.parent.connection_data["temp_line"])
        
        to_port = self.parent.find_port_at_position(canvas, mouse_x, mouse_y, gfield)
        
        if not to_port:
            canvas.itemconfig(to_port, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.FLOW_NODE_NORMAL)

        try:
            tags = canvas.gettags(to_port)
        except TclError:
            if self.parent.connection_data:
                self.parent.connection_data = None
            return
        
        is_port = any(tag in ("in_port", "out_port") for tag in tags)

        if is_port and from_port != to_port:
            self.create_connection(from_port, to_port)
        else:
            canvas.itemconfig(to_port, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.FLOW_NODE_NORMAL)
            self.parent.select_node_menu(event)

    def create_connection(self, from_port, to_port):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        from_node = self.parent.find_node_at_port(canvas, from_port, gfield)
        to_node = self.parent.find_node_at_port(canvas, to_port, gfield)

        from_tag = canvas.itemcget(from_port, "tags")
        to_tag = canvas.itemcget(to_port, "tags")

        is_from_output = "out_port current" == from_tag
        is_to_input = "in_port" in to_tag
        is_inverted = (from_tag == "in_port current") and (to_tag == "out_port")

        if not (is_from_output and is_to_input) and not is_inverted:
            showwarning(   
                "Ошибка создания связи",
                "Неверное направление связи!\n\n"
                "Допустимо только: ВЫХОД → ВХОД\n"
                f"Попытка: {'ВЫХОД' if is_from_output else 'ВХОД'} → {'ВХОД' if is_to_input else 'ВЫХОД'}"
            )
            canvas.itemconfig(to_port, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.FLOW_NODE_NORMAL)
            return None
        
        if from_node == to_node:
            showwarning(
                "Ошибка создания связи",
                "Один и тот же узел\n\n"
                "ВЫХОД одного узла соединили со ВХОДОМ того же узла\n"
            )
            canvas.itemconfig(to_port, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.FLOW_NODE_NORMAL)
            return None

        fpx1, fpy1, fpx2, fpy2 = canvas.coords(from_port)
        tpx1, tpy1, tpx2, tpy2 = canvas.coords(to_port)

        final_line = self.create_bezier_line(
            canvas, (fpx1 + fpx2) // 2, (fpy1 + fpy2) // 2, ((tpx1 + tpx2) // 2), (tpy1 + tpy2) // 2,
            color=StdColors.FLOW_NODE_NORMAL, tags="line"
        )
        
        # Если была попытка создания обратной связи
        # Просто инвертируем связь
        if is_inverted:
            to_node.connection_line_id = final_line
            to_node.create_output_connection(from_node)
        else:
            from_node.connection_line_id = final_line
            from_node.create_output_connection(to_node)

        canvas.itemconfig(to_port, fill=StdColors.FLOW_NODE_NORMAL)
        canvas.itemconfig(from_port, fill=StdColors.FLOW_NODE_NORMAL)
        canvas.itemconfig(self.parent.connection_data["temp_port_point"], fill=StdColors.FLOW_NODE_NORMAL)
    
    def update_connection_lines(self, event, node : Node):
        canvas : Canvas = self.parent.get_current_canvas()
        if node.input_node:
            x1, y1, x2, y2 = canvas.coords(node.input_node.out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2             
            
            canvas.delete(node.input_node.connection_line_id)
            new_line = self.create_bezier_line(
                canvas, from_x, from_y,
                to_x, to_y, color=StdColors.FLOW_NODE_ACTIVE, tags="line")
            node.input_node.connection_line_id = new_line
            canvas.itemconfig(node.in_port_id, fill=StdColors.FLOW_NODE_ACTIVE)
            
        if node.output_node:
            x1, y1, x2, y2 = canvas.coords(node.out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.output_node.in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2
            
            canvas.delete(node.connection_line_id)
            new_line = self.create_bezier_line(
                canvas, from_x, from_y,
                to_x, to_y, color=StdColors.FLOW_NODE_ACTIVE, tags="line")
            node.connection_line_id = new_line
            canvas.itemconfig(node.out_port_id, fill=StdColors.FLOW_NODE_ACTIVE)
        if node.data_input_node:
            x1, y1, x2, y2 = canvas.coords(node.data_input_node.data_out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.data_in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2             
            canvas.delete(node.data_input_node.data_connection_line_id)
            new_line = self.create_bezier_line(
                canvas, from_x, from_y,
                to_x, to_y, color=StdColors.DATA_NODE_ACTIVE, tags="data_line")
            node.data_input_node.data_connection_line_id = new_line
            canvas.itemconfig(node.data_in_port_id, fill=StdColors.DATA_NODE_ACTIVE)
        
        if node.data_output_node:
            x1, y1, x2, y2 = canvas.coords(node.data_out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.data_output_node.data_in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2
            canvas.delete(node.data_connection_line_id)
            new_line = self.create_bezier_line(
                canvas, from_x, from_y,
                to_x, to_y, color=StdColors.DATA_NODE_ACTIVE, tags="data_line")
            node.data_connection_line_id = new_line
            canvas.itemconfig(node.data_out_port_id, fill=StdColors.DATA_NODE_ACTIVE)

    def update_connection_lines_end(self, event, node : Node):
        canvas : Canvas = self.parent.get_current_canvas()
        if node.input_node:
            canvas.itemconfig(node.input_node.connection_line_id, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(node.in_port_id, fill=StdColors.FLOW_NODE_NORMAL)
        if node.output_node:
            canvas.itemconfig(node.connection_line_id, fill=StdColors.FLOW_NODE_NORMAL)
            canvas.itemconfig(node.out_port_id, fill=StdColors.FLOW_NODE_NORMAL)
        if node.data_input_node:
            canvas.itemconfig(node.data_input_node.data_connection_line_id, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(node.data_in_port_id, fill=StdColors.DATA_NODE_NORMAL)
        if node.data_output_node:
            canvas.itemconfig(node.data_connection_line_id, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(node.data_out_port_id, fill=StdColors.DATA_NODE_NORMAL)
        
    # data ports
    def data_port_connection_start(self, event, port_id):
        canvas : Canvas = self.parent.get_current_canvas()
        port = canvas.find_closest(event.x, event.y)[0]
        node = self.parent.find_node_at_data_port(canvas, port_id, self.parent.get_current_gfield())
        if node is None:
            return
        tags = canvas.gettags(port_id)
        
        if "in_data_port" in tags:
            if node.data_input_node is not None:
                return
            
        elif "out_data_port" in tags:
            if node.data_output_node is not None:
                return
            
        self.parent.connection_data = {
            "temp_line": None,
            "start_port": port,
            "temp_port_point": None
        }
        canvas.itemconfig(port_id, fill=StdColors.DATA_NODE_ACTIVE)

    def data_port_connection_process(self, event, port_id):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        if self.parent.connection_data["temp_line"]:
            canvas.delete(self.parent.connection_data["temp_line"])

        x1, y1, x2, y2 = canvas.coords(port_id)
        port_center_x = (x1 + x2) // 2
        port_center_y = (y1 + y2) // 2
        
        mouse_x = canvas.canvasx(event.x)
        mouse_y = canvas.canvasy(event.y)
        self.parent.connection_data["temp_line"] = self.create_bezier_line(canvas,
            port_center_x, port_center_y, mouse_x, mouse_y,
            color=StdColors.DATA_NODE_ACTIVE, tags="data_line"
        )

        current_canvas_obj = self.parent.find_data_port_at_position(canvas, mouse_x, mouse_y, gfield)
        if current_canvas_obj in gfield.data_ports and (canvas.itemcget(current_canvas_obj, "tags") in ("in_data_port", "out_data_port")):
            self.parent.connection_data["temp_port_point"] = current_canvas_obj
            canvas.itemconfig(current_canvas_obj, fill=StdColors.DATA_NODE_ACTIVE)
        else:
            canvas.itemconfig(self.parent.connection_data["temp_port_point"], fill=StdColors.DATA_NODE_NORMAL)

    def data_port_connection_end(self, event, from_port):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()
        
        mouse_x = canvas.canvasx(event.x)
        mouse_y = canvas.canvasy(event.y)
        """
        from_port - ID порта (точки) с которого начинается соединение т.е from_port
        to_port - ID порта с которым соединяется начальный порт
        """

        if self.parent.connection_data and self.parent.connection_data["temp_line"]:
            canvas.delete(self.parent.connection_data["temp_line"])
        
        to_port = self.parent.find_data_port_at_position(canvas, mouse_x, mouse_y, gfield)
        
        if not to_port:
            canvas.itemconfig(to_port, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.DATA_NODE_NORMAL)

        try:
            tags = canvas.gettags(to_port)
        except TclError:
            if self.parent.connection_data:
                self.parent.connection_data = None
            return
        
        is_port = any(tag in ("in_data_port", "out_data_port") for tag in tags)

        if is_port and from_port != to_port:
            self.data_create_connection(from_port, to_port)
        else:
            canvas.itemconfig(to_port, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.DATA_NODE_NORMAL)

    def data_create_connection(self, from_port, to_port):
        canvas : Canvas = self.parent.get_current_canvas()
        gfield : Gfield = self.parent.get_current_gfield()

        from_node = self.parent.find_node_at_data_port(canvas, from_port, gfield)
        to_node = self.parent.find_node_at_data_port(canvas, to_port, gfield)
        
        from_tag = canvas.itemcget(from_port, "tags")
        to_tag = canvas.itemcget(to_port, "tags")

        is_from_output = "out_data_port current" == from_tag
        is_to_input = "in_data_port" in to_tag
        is_inverted = (from_tag == "in_data_port current") and (to_tag == "out_data_port")
        
        if not (is_from_output and is_to_input) and not is_inverted:
            showwarning(   
                "Ошибка создания связи",
                "Неверное направление связи!\n\n"
                "Допустимо только: ВЫХОД → ВХОД\n"
                f"Попытка: {'ВЫХОД' if is_from_output else 'ВХОД'} → {'ВХОД' if is_to_input else 'ВЫХОД'}"
            )
            canvas.itemconfig(to_port, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.DATA_NODE_NORMAL)
            return None
        
        if from_node == to_node:
            showwarning(
                "Ошибка создания связи",
                "Один и тот же узел\n\n"
                "ВЫХОД одного узла соединили со ВХОДОМ того же узла\n"
            )
            canvas.itemconfig(to_port, fill=StdColors.DATA_NODE_NORMAL)
            canvas.itemconfig(from_port, fill=StdColors.DATA_NODE_NORMAL)
            return None

        fpx1, fpy1, fpx2, fpy2 = canvas.coords(from_port)
        tpx1, tpy1, tpx2, tpy2 = canvas.coords(to_port)

        from_x = (fpx1 + fpx2) // 2
        from_y = (fpy1 + fpy2) // 2
        to_x = (tpx1 + tpx2) // 2
        to_y = (tpy1 + tpy2) // 2

        final_line = self.create_bezier_line(
            canvas, from_x, from_y, to_x, to_y,
            color=StdColors.DATA_NODE_NORMAL, tags="data_line"
        )
        # Если была попытка создания обратной связи
        # Просто инвертируем связь
        target_node = None
        if is_inverted:
            to_node.data_connection_line_id = final_line
            to_node.create_data_output_connection(from_node)
            target_node = from_node
            start_node = to_node
        else:
            from_node.data_connection_line_id = final_line
            from_node.create_data_output_connection(to_node)
            target_node = to_node
            start_node = from_node
        
        # * start_node - Передача Данных
        # * target_node - Функция print()
        # ? приоритет у start_node 
        # ! Если функция print() уже имела данные
        # ! то передача данных их перезапишет

        # * Если функция print() имела данные
        # * но передача данных НЕ имела их,
        # * то передача данных теряет приоритет
        # * и текст с target_node перезапишется в start_node
        self.parent.node_builder.smart_delete_input_fields(target_node, start_node)
        
        canvas.itemconfig(to_port, fill=StdColors.DATA_NODE_NORMAL)
        canvas.itemconfig(from_port, fill=StdColors.DATA_NODE_NORMAL)
        canvas.itemconfig(self.parent.connection_data["temp_port_point"], fill=StdColors.DATA_NODE_NORMAL)

    def create_bezier_line(self, canvas, from_x, from_y, to_x, to_y, color, tags):
        """Создаёт кривую линию Безье между двумя точками"""
        
        dx = abs(to_x - from_x)
        bend = min(dx // 2, 100)
        
        if from_x < to_x:
            ctrl1_x = from_x + bend
            ctrl2_x = to_x - bend
        else:
            ctrl1_x = from_x - bend
            ctrl2_x = to_x + bend
        
        ctrl1_y = from_y
        ctrl2_y = to_y
        
        points = []
        steps = 20
        
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**3 * from_x + 3*(1-t)**2*t * ctrl1_x + 3*(1-t)*t**2 * ctrl2_x + t**3 * to_x
            y = (1-t)**3 * from_y + 3*(1-t)**2*t * ctrl1_y + 3*(1-t)*t**2 * ctrl2_y + t**3 * to_y
            points.extend([x, y])
        
        return canvas.create_line(points, fill=color, width=3, smooth=False, tags=tags)
    