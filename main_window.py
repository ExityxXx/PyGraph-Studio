from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo

from pgstruct.struct import Struct # структура
from gfield import Gfield # поле
from node.node import Node     # узел
from node.unique.print_node import PrintNode
from tooltip import ToolTip # тултип
from code_place import CodePlace # место кода
from variable import PGSVariable # переменная
from node.node_builder import NodeBuilder
from managers.project_manager import ProjectManager
from debugger_interface import DebuggerInterface

# Импорт интерфейсов менеджеров
from managers.graphs_manager import GraphsManager
from managers.variables_manager import VariablesManager

import constants

"""
Проблемы которые нужно исправить:

При перемещений узла его значения x и y не изменяются
а остаются изначальными
"""

"""
ПРИМЕЧАНИЕ ПО ФУНКЦИЯМ
Функций node_drag_start, motion и end (а точнее их реализация)
перенесена в файл node_drag.py

Они вызываются (точнее как бинд) в файле node_builder.py
в функций bind_events


Функций port_connection_start, process и end (а точнее их реализация)
перенесена в файл node_port_connection.py

Они вызываются в файле node_builder.py в классе NodeBuilder
Также вызываются в файле node_drag.py в функциях
    node_drag_motion и node_drag_end (для обновления линий во время перемещения узла)

В классе NodeDragger (который отвечает за перемещение узла) есть ссылка
на класс NodePortConnector

"""
class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Инициализация элементов окна
        self.init_elements()

        # Инициализация вкладок меню
        self.setup_menu()

        # Инициализация панели структуры
        self.setup_structure_panel()

        # Инициализация панели инспектора
        self.setup_inspector_panel()
        
    def init_elements(self):
        # Создание структуры проекта
        self.struct : Struct = Struct()
        self.node_builder : NodeBuilder = NodeBuilder(self)
        self.project_manager : ProjectManager = ProjectManager(self)
        self.debugger_interface : DebuggerInterface = DebuggerInterface(self)
        self.graphs_manager : GraphsManager = GraphsManager(self)
        self.variables_manager : VariablesManager = VariablesManager(self)
        self.items_counter = 0
        self.gfields_counter = 0
        self.code_places_counter = 0
        self.variables_counter = 0

        # Настройка окна приложения
        self.title("PyGraph Studio")
        self.geometry("1080x720+480+100")
        self.minsize(700, 400)
        self.config(background="#2b2b2b")
        
        # Создание набора вкладок
        self.notebook = ttk.Notebook(self)

    def get_current_canvas(self):
        if self.struct.items_length() == 0:
            return
        current_tab_index = self.notebook.index(self.notebook.select())
        item = self.struct.get_item(current_tab_index)
        if item["type"] != "gfield":
            return None
        return item["data"].get_canvas()
    
    def get_current_gfield(self):
        if self.struct.items_length() == 0:
            return
        current_tab_index = self.notebook.index(self.notebook.select())
        item = self.struct.get_item(current_tab_index)
        if item["type"] != "gfield":
            return None
        return item["data"]
    
    def get_current_code_place(self):
        if self.struct.code_places_count() == 0:
            return
        current_tab_index = self.notebook.index(self.notebook.select())
        item = self.struct.get_item(current_tab_index)
        if item["type"] != "code_place":
            return None
        return item["data"]

    def setup_menu(self):
        """
        Настройка меню
        Верхняя панель.
        """

        # Создание всех меню
        self.main_menu = Menu(tearoff=0)            # Основное меню
        self.file_tab = Menu(tearoff=0)             # Вкладка "Файл"
        self.editing_tab = Menu(tearoff=0)          # Вкладка "Правка"
        self.run_tab = Menu(tearoff=0)              # Вкладка "Выполнить"
        self.compile_tab = Menu(tearoff=0)
        self.terminal_tab = Menu(tearoff=0)         # Вкладка "Терминал"
        self.ref_tab = Menu(tearoff=0)              # Вкладка "Справка"

        # Настройка основного меню и привязка вкладок к подменю
        self.main_menu.add_cascade(label="Файл", menu=self.file_tab)
        self.main_menu.add_cascade(label="Правка", menu=self.editing_tab)
        self.main_menu.add_cascade(label="Выполнить", menu=self.run_tab)
        self.main_menu.add_cascade(label="Компиляция", menu=self.compile_tab)
        self.main_menu.add_cascade(label="Терминал", menu=self.terminal_tab)
        self.main_menu.add_cascade(label="Справка", menu=self.ref_tab)

        # Настройка вкладки "Файл"
        self.file_tab.add_command(label="Создать новое графическое поле", command=self.creating_new_gfield_menu)
        self.file_tab.add_command(label="Удалить текущее графическое поле", command=self.delete_current_item)
        self.file_tab.add_separator()
        self.file_tab.add_command(label="Выход", command=exit)

        # Настройка вкладки "Правка"
        self.editing_tab.add_command(label="Отменить последнее действие")
        self.editing_tab.add_separator()
        self.editing_tab.add_command(label="Вырезать")
        self.editing_tab.add_command(label="Копировать")
        self.editing_tab.add_command(label="Вставить")
        self.editing_tab.add_command(label="Найти")
        self.editing_tab.add_separator()
        self.editing_tab.add_command(label="Подогнать размер графы", command=self.update_scrollregion)

        # Настройка вкладки "Выполнить"
        self.run_tab.add_command(label="Запустить код")
        self.run_tab.add_command(label="Запустить окно отладки")
        self.run_tab.add_command(label="Запустить отладку кода")

        # Настройка вкладки "Компиляция"
        self.compile_tab.add_command(label="Скомпилировать графическое поле")
        self.compile_tab.add_command(label="Скомпилировать проект")

        # Настройка вкладки "Терминал"
        self.terminal_tab.add_command(label="Создать терминал")

        # Настройка вкладки "Справка"
        self.ref_tab.add_command(label="О программе")
        self.config(menu=self.main_menu)
    
    def setup_toolbar(self):
        toolbar_frame = Frame(self, relief=SOLID, bg="#2b2b2b")
        
        add_gfield_button = Button(
            toolbar_frame, text="➕",
            width=4, height=1,
            command=self.creating_new_gfield_menu
        )
        add_gfield_button.pack(side=LEFT)
        ToolTip(add_gfield_button, "Добавить графическое поле")
        
        del_gfield_button = Button(
            toolbar_frame, text="❌",
            width=4, height=1,
            command=self.delete_current_item
        )
        del_gfield_button.pack(side=LEFT)
        ToolTip(del_gfield_button, "Удалить графическое поле")

        current_item_buttom = Button(
            toolbar_frame, text="📊", 
            width=4, height=1,
            command=self.debugger_interface.debug_current_gfield
        )
        current_item_buttom.pack(side=LEFT)
        ToolTip(current_item_buttom, "Информация о текущем объекте")

        debug_button = Button(
            toolbar_frame, text="🐞",
            width=4, height=1,
            command=self.debugger_interface.developer_debug
        )
        debug_button.pack(side=LEFT)
        ToolTip(debug_button, "Запустить отладку")
        vars_debug_button = Button(
            toolbar_frame, text="🐞 var 🧾",
            width=4, height=1,
            command=self.debugger_interface.debug_variables
        )
        vars_debug_button.pack(side=LEFT)
        ToolTip(vars_debug_button, "Запустить отладку переменных")

        code_editor_create_button = Button(
            toolbar_frame,text="📝", 
            width=4, height=1,
            command=self.create_new_code_editor_menu 
        )
        code_editor_create_button.pack(side=LEFT)
        ToolTip(code_editor_create_button, "Создать вкладку для написания кода")

        compile_and_run_button = Button(
            toolbar_frame,text="Compile and run", 
            width=14, height=1,
            command=self.debugger_interface.compile_and_run 
        )
        compile_and_run_button.pack(side=LEFT)
        ToolTip(compile_and_run_button, "Скомпилировать графу и выполнить код (бета)")

        
        dbg_cnctions_btn = Button(
            toolbar_frame,text="Отладка связей", 
            width=14, height=1,
            command=self.debugger_interface.debug_connections 
        )
        dbg_cnctions_btn.pack(side=LEFT)
        ToolTip(dbg_cnctions_btn, "Отладка связей в текущей графе")
        dbg_dtcnc_btn = Button(
            toolbar_frame,text="Отладка дата связей", 
            width=14, height=1,
            command=self.debugger_interface.debug_data_connections 
        )
        dbg_dtcnc_btn.pack(side=LEFT)
        ToolTip(dbg_dtcnc_btn, "Отладка дата связей")
        toolbar_frame.pack(fill=X, side=TOP)

    def setup_structure_panel(self):
        # Создание панели структуры (Левая панель)
        self.struct_panel = Frame(self, width=250, bg="#1b1b1b")
        self.struct_panel.pack(fill="both", anchor="nw", side=LEFT)
        self.struct_panel.grid_propagate(False)
        self.struct_title = Label(self.struct_panel, text="Структура",
                                  font=("Arial", 18, "bold"), fg="white", background="#1b1b1b") \
            .grid(row=0, column=0, columnspan=2, padx=6, pady=6, sticky="nw")
        
        self.not_struct_data_label = Label(self.struct_panel, text="Нет данных\nдля структурирования",
              font=("Arial", 12), fg="#808080", background="#1b1b1b", anchor="nw", justify="left")
        self.not_struct_data_label.grid(row=1, column=0, padx=6, pady=2, sticky="nw")
        
        highlight_event = lambda e, color : self.create_project_button.config(fg=color)

        self.create_project_button = Button(self.struct_panel, text="Создать проект",
                               bg="#1b1b1b", fg="white", font=("Arial", 12, "bold"),
                               relief="flat", bd=0, cursor="hand2",
                               activebackground="#1b1b1b", activeforeground="#dbdbdb",
                               command=self.project_manager.create_new_project_menu)
            
        self.create_project_button.bind("<Enter>", lambda e: highlight_event(e, "#dbdbdb"))
        self.create_project_button.bind("<Leave>", lambda e: highlight_event(e, "white"))
        self.create_project_button.grid(row=2, column=0, padx=4, pady=8, sticky="nw")

    def update_structure_panel(self):
        self.struct_panel.columnconfigure(0, weight=1)
        self.struct_panel.columnconfigure(1, weight=0)

        Button(self.struct_panel, text="Графические поля",
                                    bg="#4a6a8a", fg="white",
                                    cursor="hand2", font=("Segoe UI", 9, "bold"),
                                    activebackground="#537da7",
                                    activeforeground="white",
                                    command=self.graphs_manager.open) \
            .grid(row=3, column=0, columnspan=2, padx=6, pady=4, sticky="nsew")
        
        Button(self.struct_panel, text="Переменные",
                                    bg="#798a4a", fg="white",
                                    cursor="hand2", font=("Segoe UI", 9, "bold"),
                                    activebackground="#89a53b",
                                    activeforeground="white",
                                    command=self.variables_manager.open) \
            .grid(row=4, column=0, columnspan=2, padx=6, pady=4, sticky="nsew")
        
    def setup_inspector_panel(self):
        # Создание панели инспектора (Правая панель)
        self.inspector_panel = Frame(self, width=300, relief=SOLID, bg="#1b1b1b")
        self.inspector_panel.pack(fill="both", anchor="nw", side=RIGHT)
        self.inspector_panel.grid_propagate(False)
        self.inspector_panel.columnconfigure(0, weight=0)  # колонка с Label - не расширяется
        self.inspector_panel.columnconfigure(1, weight=1)  # колонка с Entry - расширяется
        self.inspector_title = Label(self.inspector_panel, text="Инспектор", font=("Segoe UI", 18, "bold"),
                                     fg="white", background="#1b1b1b")
        self.inspector_title.grid(row=0, column=0, padx=6, pady=6, sticky="sw",columnspan=2)
        self.not_inspection_data_label = Label(self.inspector_panel, text="Нет данных для инспекций", \
              font=("Segoe UI", 12), fg="#808080", background="#1b1b1b", anchor="sw", justify="left")
        self.not_inspection_data_label.grid(row=1, column=0, padx=6, pady=2, sticky="sw")

    def update_inspector_panel(self, node : Node) -> None:
        for widget in self.inspector_panel.winfo_children():
            if widget != self.inspector_title:
                widget.destroy()

        def update_node_name(event=None) -> None:
            text = event.widget.get()
            if text:
                node.header = text
                canvas.itemconfig(node.header_id, text=text)
        
        def update_node_value(event=None) -> None:
            text = event.widget.get()
            node.text = text
            entry_widget = node.get_entry_field()
            entry_widget.delete(0, END)
            entry_widget.insert(0, text)

        canvas : Canvas = self.get_current_canvas()

        row1 = Frame(self.inspector_panel, bg="#1b1b1b")
        row1.grid(row=1, column=0, sticky="ew", columnspan=2)
        row1.columnconfigure(1, weight=1)
        node_name_label = Label(row1, text=f"Узел:",
                          font=("Arial", 12), fg="#808080", background="#1b1b1b", anchor="sw", justify="left")
        node_name_label.grid(row=0, column=0, padx=6, pady=6, sticky="sw")
        
        self.node_name_entry = ttk.Entry(row1, width=25)
        self.node_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        self.node_name_entry.insert(0, node.header)
        self.node_name_entry.bind("<KeyRelease>", update_node_name)
        self.node_name_entry.bind("<Return>", lambda event: self.focus_set())

        if isinstance(node, PrintNode):
            row2 = Frame(self.inspector_panel, bg="#1b1b1b")
            row2.grid(row=2, column=0, sticky="ew", columnspan=2)
            row2.columnconfigure(1, weight=1)
            value_label = Label(row2, text=f"Значение:",
                     font=("Arial", 12), fg="#808080", background="#1b1b1b", anchor="sw", justify="left")
            value_label.grid(row=0, column=0, padx=6, pady=(0, 2), sticky="sw")
            
            self.value_entry : ttk.Entry = ttk.Entry(row2, width=25)
            self.value_entry.grid(row=0, column=1, padx=6, pady=(0, 2), sticky="ew")
            self.value_entry.insert(0, node.value)
            self.value_entry.bind("<KeyRelease>", update_node_value)
            self.value_entry.bind("<Return>", lambda event: self.focus_set())
            row3 = Frame(self.inspector_panel, bg="#1b1b1b")
            row3.grid(row=3, column=0, sticky="ew", columnspan=2)
            row3.columnconfigure(1, weight=1)
            Label(row3, text=f"Примечание:",
                     font=("Arial", 10, "bold"), fg="#808080",
                     background="#1b1b1b", anchor="sw", justify="left") \
                     .grid(row=0, column=0, padx=6, pady=(0, 2), sticky="nw")
            Label(row3, text=f"В поле ввода значения\nможно не вводить кавычки,\nно если в этом есть\nнеобходимость можете\nвоспользоваться сырой\nстрокой.",
                     font=("Arial", 10), fg="#808080",
                     background="#1b1b1b", anchor="sw", justify="left") \
                     .grid(row=0, column=1, padx=2, pady=(0, 2), sticky="sw")
    def creating_new_gfield_menu(self):
        """
        Меню создания нового графического поля
        """
        # Настройка окна
        window = Toplevel(self)
        window.title("Создание графического поля")
        window.geometry("490x110+650+250")
        window.resizable(0, 0) 
        window.focus()
        window.transient(self)
        window.grab_set()

        # Настройка элементов
        # Поле "Имя графического поля: "
        ttk.Label(window, text="Имя графического поля: ").grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        gfield_name_entry = ttk.Entry(window, width=35)
        gfield_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        gfield_name_entry.focus()

        # Поле "Описание (необязательно): "
        ttk.Label(window, text="Описание (необязательно): ").grid(row=1, column=0, padx=6, pady=6, sticky=EW)
        gfield_description_entry = ttk.Entry(window, width=50)
        gfield_description_entry.grid(row=1, column=1, padx=6, pady=6, sticky=EW)
        
        def ref_menu(event):
            showinfo("Справка о графическом поле",
                     "Графическое поле - это холст(графа), где вы можете рисовать\nпрямоугольники (узлы),"\
                     "соединять их между собой и\nполучать последовательность кода на Python.\n",)

        def collect_data_and_create_gfield(event):
            gfield_name = gfield_name_entry.get().strip()
            gfield_description = gfield_description_entry.get().strip()

            if not gfield_name:
                showwarning("Предупреждение", f"Имя графического поля не должно быть пустым!\nИмя изменено на Графическое поле {self.gfields_counter + 1}")
                gfield_name = f"Графическое поле {self.gfields_counter + 1}"
                gfield_name_entry.insert(0, gfield_name)
                gfield_name_entry.focus()
            else:
                temp_gfields_names : list[str] = []
                for existing in self.struct.get_items().values():
                    if existing["type"] == "gfield":
                        temp_gfields_names.append(existing["data"].get_name())
                
                if gfield_name in temp_gfields_names:
                        showwarning("Предупреждение", "Графическое поле с таким именем уже существует")
                        return
                
                self.items_counter += 1
                self.gfields_counter += 1
                self.create_gfield(gfield_name, gfield_description)
                window.destroy()
            
        button_frame = ttk.Frame(window)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=EW, padx=6, pady=6)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        ref_button = ttk.Button(button_frame, text="Справка")
        ref_button.grid(row=1, column=0, padx=6, pady=6, sticky=EW)
        ref_button.bind("<Button-1>", ref_menu)

        create_start_node_button = ttk.Button(button_frame, text="Создать")
        create_start_node_button.grid(row=1, column=1, padx=6, pady=6, sticky=EW)
        create_start_node_button.bind("<Button-1>", collect_data_and_create_gfield)
        window.bind("<Return>", collect_data_and_create_gfield)
        return window
    
    def create_gfield(self, gfield_name, gfield_description):
        """
        Создание графического поля и сохранение его в структуре проекта
        """
        # Создаем фрейм и канвас
        frame = ttk.Frame(self.notebook)
        canvas = Canvas(frame, bg="#2b2b2b", scrollregion=(-1250, -1250, 1250, 1250))

        new_gfield = Gfield(self.items_counter - 1, gfield_name, gfield_description, canvas)
        self.struct.add_gfield(self.items_counter - 1, new_gfield)
        
        self.add_node_at_position(new_gfield, 30, 30,
                                  "Стартовый узел", "", False, True,
                                  170, 55, True)
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Добавляем горизонтальную полосу прокрутки
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=h_scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настраиваем веса для фрейма
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.notebook.add(frame, text=f"📊 {gfield_name}")
        self.notebook.pack(expand=1, fill=BOTH)

        def on_pan_start(event):
            canvas.scan_mark(event.x, event.y)
            canvas.config(cursor="fleur")
    
        def on_pan_move(event):
            canvas.scan_dragto(event.x, event.y, gain=1)
            self.redraw_grid(canvas)
        
        def on_pan_end(event):
            canvas.config(cursor="")

        canvas.bind("<ButtonPress-2>", on_pan_start)
        canvas.bind("<B2-Motion>", on_pan_move)
        canvas.bind("<ButtonRelease-2>", on_pan_end)
        canvas.bind("<Double-Button-1>", lambda e: self.fast_create_node(e, "Узел", "", True, True, 170, 55))
        canvas.bind("<Button-3>", self.on_right_click)
        canvas.bind("<Configure>", lambda e: self.redraw_grid(canvas))

    def redraw_grid(self, canvas):
        """Перерисовывает только сетку (порты не трогает)"""
        if not canvas:
            return
        
        canvas.delete("grid_line")
        
        # Получаем видимую область
        x1 = int(canvas.canvasx(0))
        y1 = int(canvas.canvasy(0))
        x2 = int(canvas.canvasx(canvas.winfo_width()))
        y2 = int(canvas.canvasy(canvas.winfo_height()))
        
        margin = 500
        start_x = (x1 // 25) * 25 - margin
        start_y = (y1 // 25) * 25 - margin
        end_x = (x2 // 25) * 25 + margin
        end_y = (y2 // 25) * 25 + margin
        
        step = 25
        big_step = 125
        
        # Вертикальные линии
        for x in range(start_x, end_x + step, step):
            if x % big_step == 0:
                canvas.create_line(x, start_y, x, end_y, fill="#555555", width=2, tags="grid_line")
            else:
                canvas.create_line(x, start_y, x, end_y, fill="#3a3a3a", width=1, tags="grid_line")
        
        # Горизонтальные линии
        for y in range(start_y, end_y + step, step):
            if y % big_step == 0:
                canvas.create_line(start_x, y, end_x, y, fill="#555555", width=2, tags="grid_line")
            else:
                canvas.create_line(start_x, y, end_x, y, fill="#3a3a3a", width=1, tags="grid_line")
        
        canvas.tag_lower("grid_line")

    def update_scrollregion(self):
        canvas : Canvas = self.get_current_canvas()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_new_code_editor_menu(self):
        """
        Меню создания нового редактора кода
        """
        # Настройка окна
        window = Toplevel(self)
        window.title("Создание редактора кода")
        window.geometry("660x305+650+250")
        window.resizable(1, 1) 
        window.focus()
        window.transient(self)
        window.grab_set()
        window.columnconfigure(0, weight=0)
        window.columnconfigure(1, weight=1)

        # Поле "Имя редактора:"
        ttk.Label(window, text="Имя вкладки:").grid(row=0, column=0, padx=6, pady=2, sticky=EW)
        code_name_entry = Entry(window)
        code_name_entry.grid(row=0, column=1, columnspan=2, padx=6, pady=6, sticky="nsew")

        # Поле "Код"
        ttk.Label(window, text="Код:").grid(row=1, column=0, padx=6, pady=2, sticky=EW)
        code_place = Text(window, height=12)
        code_place.grid(row=2, column=0, columnspan=2, padx=6, pady=6, sticky="nsew")


        def collect_data_and_create(event=None):
            name = code_name_entry.get().strip()
            code = code_place.get("1.0", END).strip()
            if not name:
                showwarning("Предупреждение", f"Имя вкладки не должно быть пустым!\nИмя изменено на Редактор кода {self.code_places_counter + 1}")
                name = f"Редактор кода {self.code_places_counter + 1}"
                code_name_entry.insert(0, name)
                code_name_entry.focus()
            else:
                temp_cp_names : list[str] = []
                for existing in self.struct.get_items().values():
                    if existing["type"] == "code_place":
                        temp_cp_names.append(existing["data"].get_name())
                if name in temp_cp_names:
                        showwarning("Предупреждение", "Редактор кода с таким именем уже существует")
                        return
                self.items_counter += 1
                self.code_places_counter += 1
                self.create_code_editor(name, code)
                window.destroy()
        
        create_button = ttk.Button(window, text="Создать")
        create_button.grid(row=3, column=0, padx=6, pady=2, sticky=EW, columnspan=2)
        create_button.bind("<Button-1>", collect_data_and_create)

    def create_code_editor(self, name, code):
        """
        Создание редактора кода
        """
        # Создаем фрейм и канвас
        frame = Frame(self.notebook)
        text = Text(frame, bg="#1b1b1b", fg="#54E475", font=("Cascadia Code", 16), padx=10, pady=5)
        text.insert(END, code)
        # Добавляем в структуру проекта графическое поле
        new_code_place = CodePlace(self.items_counter - 1, name, code)
        self.struct.add_code_place(self.items_counter - 1, new_code_place)
        
        text.pack(expand=1, fill=BOTH)
        self.notebook.add(frame, text=f"📝 {name}")
        self.notebook.pack(expand=1, fill=BOTH)

    def delete_current_item(self):
        """
        Удаление графического поля
        """
        if self.struct.items_length() == 0:
            return
        
        current_selected_index = self.notebook.index(self.notebook.select())
        if self.struct.get_item(current_selected_index)["type"] == "gfield": self.gfields_counter -= 1
        elif self.struct.get_item(current_selected_index)["type"] == "code_place": self.code_places_counter -= 1
        self.notebook.forget(current_selected_index)
        self.struct.remove_item(current_selected_index)
        self.items_counter -= 1
        
        if self.struct.items_length() == 0:
            self.notebook.pack_forget()
            self.config(bg="#2b2b2b")

    def select_node_menu(self, event):
        def change(*args):
            value = input_val.get().strip().lower()
            listbox.delete(0, "end")

            for item in constants.PGS_NODE_ITEMS:
                if value in item.lower():
                    listbox.insert("end", item)

        def on_select(event):
            selected = event.widget.curselection()
            window.selected_node_name = event.widget.get(selected[0])
        
        def on_double_click(e):
            selected = e.widget.curselection()
            if selected:
                window.destroy()
                canvas : Canvas = self.get_current_canvas()
                real_x = canvas.canvasx(event.x)
                real_y = canvas.canvasy(event.y)
                self.add_node_at_position(self.get_current_gfield(), real_x, real_y,
                                          window.selected_node_name, "",
                                          True, True, 170, 55, False)
            
        window = Toplevel(self)
        window.title("Выбор узлов")
        window.geometry(f"300x500+{event.x_root - 100}+{event.y_root - 50}")
        window.focus()
        window.grab_set()
        window.transient(self)
        window.resizable(0, 0)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=0)
        window.grid_columnconfigure(1, weight=1)
        window.selected_node_name = None

        Label(window, text="Поиск узлов", font=("Segoe UI", 11)).grid(row=0, column=0, padx=(7, 4), pady=(6, 1), sticky="nsew")

        input_val = StringVar()
        input_val.trace("w", change)
        
        entry = ttk.Entry(window, textvariable=input_val)
        entry.grid(row=0, column=1, padx=10, pady=(6, 1), sticky="ew")
        entry.focus()

        listbox = Listbox(window, font=("Segoe UI", 11), activestyle="none", selectbackground="#81407C")
        listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

        for item in constants.PGS_NODE_ITEMS:
            listbox.insert("end", item)

        listbox.bind('<<ListboxSelect>>', on_select)
        listbox.bind("<Double-Button-1>", on_double_click)

    def on_right_click(self, event=None):
        canvas : Canvas = self.get_current_canvas()
        x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
        items_in_area = canvas.find_overlapping(x-10, y-10, x+10, y+10)
        for item in items_in_area: 
            tags = canvas.gettags(item)
            if "node" in tags:
                self.node_context_menu(event, item)
                return
            elif "line" in tags:
                self.connection_context_menu(event, item, "flow")
                return
            elif "data_line" in tags:
                self.connection_context_menu(event, item, "data")
                return
            
        self.select_node_menu(event)
    
    def node_context_menu(self, event, item) -> None:
        canvas : Canvas = self.get_current_canvas()
        menu = Menu(canvas, tearoff=0)
        menu.add_command(label="❌ Удалить узел", command=lambda: self.node_builder.delete_node(event, item))
        menu.post(event.x_root, event.y_root)

    def connection_context_menu(self, event, line, line_type) -> None:
        canvas : Canvas = self.get_current_canvas()
        menu = Menu(canvas, tearoff=0)
        menu.add_command(label="❌ Удалить связь", command=lambda: self.node_builder.delete_connection(event, line, line_type))
        menu.post(event.x_root, event.y_root)

    def add_node_at_position(self, gfield, x, y, name, code, in_port_enable, out_port_enable, width, height, is_start_node):
        """Создание узла в конкретных координатах"""
        canvas : Canvas = gfield.get_canvas()
        self.node_builder.build_node(canvas, gfield,
                              x, y, name, code,
                              in_port_enable, out_port_enable,
                              width, height, "#5A6FE4" if is_start_node else "#FFD000", is_start_node)
    def fast_create_node(self, event, name, code, in_port_enable, out_port_enable, width, height):
        item = event.widget.find_closest(event.x, event.y)[0]
        tags = event.widget.gettags(item)

        if "node" in tags:
            return
        
        current_gfield : Gfield = self.get_current_gfield()
        canvas : Canvas = current_gfield.get_canvas()
        mouse_x = canvas.canvasx(event.x)
        mouse_y = canvas.canvasy(event.y)
        self.node_builder.build_node(canvas, current_gfield,
                              mouse_x - 20, mouse_y - 25, name, code,
                              in_port_enable, out_port_enable,
                              width, height, "#FFD000")  

    def find_port_at_position(self, canvas : Canvas, x : int, y : int, gfield : Gfield):
        for port_id in gfield.get_ports():
            x1, y1, x2, y2 = canvas.coords(port_id)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return port_id
        return None

    def find_data_port_at_position(self, canvas : Canvas, x : int, y : int, gfield : Gfield):
        for port_id in gfield.get_data_ports():
            x1, y1, x2, y2 = canvas.coords(port_id)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return port_id
        return None
    
    def find_node_at_port(self, canvas : Canvas, port_id : int, gfield : Gfield):
        for node in gfield.get_nodes().values():
            if node.in_port_id == port_id or node.out_port_id == port_id:
                return node
        return None
    
    def find_node_at_data_port(self, canvas : Canvas, port_id : int, gfield : Gfield):
        for node in gfield.get_nodes().values():
            if hasattr(node, "data_out_port_id") and node.data_out_port_id == port_id:
                return node
            if hasattr(node, "data_in_port_id") and node.data_in_port_id == port_id:
                return node

        return None
    
    def find_node_at_cursor(self, event):
        gfield : Gfield = self.get_current_gfield()
        canvas : Canvas = gfield.get_canvas()
        item = canvas.find_closest(canvas.canvasx(event.x), canvas.canvasy(event.y))[0]
        
        for node in gfield.get_nodes().values():
            if node.rect_id == item:
                gfield.set_selected_node(node)
                return node
            
        return None
    