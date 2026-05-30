from tkinter import Canvas
from node.node import Node
from constants import StdColors

class NodeDragger:
    def __init__(self, parent, port_connector):
        self.parent = parent
        self.port_connector = port_connector

    def node_drag_start(self, event, *args):
        """
        Перемещение узла по полю (начало события)
        Аргументы:
        node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text
        
        Аргументы соответственны args[i] т.е
        node_rect_id = args[0] а run_code_text = args[4]
        """
        canvas : Canvas = self.parent.get_current_canvas()
        canvas.itemconfig(args[0], outline=StdColors.FLOW_NODE_DRAGGING)
        self.parent.drag_info = {
            "x": event.x,
            "y": event.y
        }

        clicked_node = self.parent.find_node_at_cursor(event)
        if clicked_node:
            self.parent.update_inspector_panel(clicked_node)

    def node_drag_motion(self, event, node, *args):
        canvas = self.parent.get_current_canvas()

        dx = event.x - self.parent.drag_info["x"]
        dy = event.y - self.parent.drag_info["y"]
        
        for item in args:
            if item is not None:
                canvas.move(item, dx, dy)
        
        self.parent.drag_info["x"] = event.x
        self.parent.drag_info["y"] = event.y
        
        if node:
            self.port_connector.update_connection_lines(event, node)

    def node_drag_end(self, event, rect, node : Node):
        canvas : Canvas = self.parent.get_current_canvas()

        states = {
            True: StdColors.START_NODE_NORMAL,
            False: StdColors.FLOW_NODE_ACTIVE
        }
        change_color = states[node.is_start_node]

        canvas.itemconfig(rect, outline=change_color)
        if node:
            self.port_connector.update_connection_lines_end(event, node)
            