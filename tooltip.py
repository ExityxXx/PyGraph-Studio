from tkinter import Toplevel, Label

class ToolTip:
    """Всплывающая подсказка для виджетов"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.window = None
        self.delay = 0.2
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        
    def show_tip(self, event=None):
        if self.window:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 20
        self.window = Toplevel(self.widget)
        self.window.wm_overrideredirect(True)
        self.window.wm_geometry(f"+{x}+{y}")
        label = Label(self.window, text=self.text,
                     bg="#ffffcc", fg="#333333",
                     relief="solid", borderwidth=1,
                     font=("Arial", 9), padx=5, pady=2)
        label.pack()

    def hide_tip(self, event=None):
        if self.window:
            self.window.destroy()
            self.window = None
