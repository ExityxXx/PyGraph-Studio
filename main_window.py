from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo
from tkinter import filedialog
from struct import Struct # структура
from gfield import Gfield # поле
from node import Node     # узел
from tooltip import ToolTip # тултип
from code_place import CodePlace # место кода
from io import StringIO
import os
import sys

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Инициализация элементов окна
        self.init_elements()

        # Инициализация вкладок меню
        self.setup_menu()

        # Инициализация тулбара
        self.setup_toolbar()

    def init_elements(self):
        # Создание структуры проекта
        self.struct : Struct = Struct()
        self.items_counter = 0
        self.gfields_counter = 0
        self.code_places_counter = 0
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
        self.terminal_tab = Menu(tearoff=0)         # Вкладка "Терминал"
        self.ref_tab = Menu(tearoff=0)              # Вкладка "Справка"

        # Настройка основного меню и привязка вкладок к подменю
        self.main_menu.add_cascade(label="Файл", menu=self.file_tab)
        self.main_menu.add_cascade(label="Правка", menu=self.editing_tab)
        self.main_menu.add_cascade(label="Выполнить", menu=self.run_tab)
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
        self.editing_tab.add_separator()
        self.editing_tab.add_command(label="Найти")

        # Настройка вкладки "Выполнить"
        self.run_tab.add_command(label="Запустить код")
        self.run_tab.add_command(label="Запустить окно отладки")
        self.run_tab.add_command(label="Запустить отладку кода")

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
            command=self.debug_current_gfield
        )
        current_item_buttom.pack(side=LEFT)
        ToolTip(current_item_buttom, "Информация о текущем объекте")

        debug_button = Button(
            toolbar_frame, text="🐞",
            width=4, height=1,
            command=self.developer_debug
        )
        debug_button.pack(side=LEFT)
        ToolTip(debug_button, "Запустить отладку")

        connect_button = Button(
            toolbar_frame, text="🔗", 
            width=4, height=1,
            command=self.set_connection_node_menu
        )
        connect_button.pack(side=LEFT)
        ToolTip(connect_button, "Установить связь между узлами")

        code_editor_create_button = Button(
            toolbar_frame,text="📝", 
            width=4, height=1,
            command=self.create_new_code_editor_menu 
        )
        code_editor_create_button.pack(side=LEFT)
        ToolTip(code_editor_create_button, "Создать вкладку для написания кода")
        toolbar_frame.pack(fill=X, side=TOP)
    
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
    
    def create_gfield(self, gfield_name, gfield_description):
        """
        Создание графического поля и сохранение его в структуре проекта
        """
        # Создаем фрейм и канвас
        frame = ttk.Frame(self.notebook)
        canvas = Canvas(frame)
        canvas.config(bg="#2b2b2b")
        
        # Добавляем в структуру проекта графическое поле
        new_gfield = Gfield(self.items_counter - 1, gfield_name, gfield_description, canvas, list())
        self.struct.add_gfield(self.items_counter - 1, new_gfield)

        canvas.pack(expand=1, fill=BOTH)
        self.notebook.add(frame, text=f"📊 {gfield_name}")
        self.notebook.pack(expand=1, fill=BOTH)

        # Биндинг контекстного меню
        canvas.bind("<Button-3>", lambda e: self.context_menu(new_gfield, e))
        canvas.bind("<Configure>", lambda e: self.grid_line(e))

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
         
    def developer_debug(self):
        """
        Меню отладки
        """
        # Генерация отладочного контента
        items_count = self.struct.items_length()
        items : dict = self.struct.get_items()
        generated_result = "Отсутствуют графические поля для отладки"
        current_item = None
        if items:
            current_tab_index = self.notebook.index(self.notebook.select())
            current_item = self.struct.get_item(current_tab_index)["data"]
            generated_result = f"Общее количество: {items_count}\n" \
                               f"Текущий объект: \"{current_item.get_name()}\"\n" \
                               f"Кол-во полей: {self.gfields_counter}\n" \
                               f"Кол-во редакторов кода: {self.code_places_counter}\n"

        for i in range(len(items)):
            item = items[i]
            
            generated_result += \
                f"Отчёт по объекту №{i+1}:\n" \
                f"    Тип объекта: {"Графическое поле" if item["type"] == "gfield" else "Редактор кода"}\n" \
                f"    Название: {item["data"].get_name()}\n"
                
            if item["type"] == "gfield":
                generated_result += \
                    f"    Описание: {item["data"].get_description()}\n" \
                    f"    Узлы:   " 
                for i in items[i]["data"].get_nodes().values():
                    generated_result += \
                        f"{i}\n           "
                generated_result+="\n"

        # Настройка окна
        window = Toplevel()
        window.title("Отладка")
        window.geometry("690x500+650+250")
        window.resizable(1, 0)
        window.focus()

        # Размещение центрального текста
        text = Text(window, bg="#404040", fg="#00D10A", font=("Courier New", 12))
        text.pack(padx=8, pady=8, fill=X)
        text.insert("1.0", str(generated_result))

        # Кнопка очистки
        clear_button = ttk.Button(window, text="Очистить", command=lambda : text.delete("1.0", END))
        clear_button.pack(padx=8, pady=8)
    
    def debug_current_gfield(self):
        """
        Меню отладки текущего поля
        """

        generated_result = "Отсутствуют графические поля для отладки"
        title = "Отладка"
        current_item = None

        if self.struct.items_length() > 0:
            current_tab_index = self.notebook.index(self.notebook.select())
            current_item = self.struct.get_item(current_tab_index)

            if current_item["type"] == "gfield":
                title = f"Отладка поля \"{current_item["data"].get_name()}\""
                generated_result = \
                        f"Название: {current_item["data"].get_name()}\n" \
                        f"Описание: {current_item["data"].get_description()}\n" \
                        f"Узлы:   "
                for i in current_item["data"].get_nodes().values():
                    generated_result += \
                        f"{i}\n        "
                generated_result += "\n"

            elif current_item["type"] == "code_place":
                title = f"Отладка редактора кода \"{current_item["data"].get_name()}\""
                generated_result = f"Название: {current_item["data"].get_name()}\n" \
                        f"Код: \n{current_item["data"].get_code()}"
            

        # Настройка окна
        window = Toplevel()
        window.title(title)
        window.geometry("690x250+650+250")
        window.resizable(1, 0)
        window.focus()

        # Размещение центрального текста
        text = Text(window, bg="#404040", fg="#00D10A", font=("Courier New", 12))
        text.pack(padx=8, pady=8, fill=X)
        text.insert("1.0", str(generated_result))

        # Кнопка очистки
        clear_button = ttk.Button(window, text="Очистить", command=lambda : text.delete("1.0", END))
        clear_button.pack(padx=8, pady=8)
        
    def context_menu(self, gfield, event):
        """
        Контекстное меню
        """
        menu = Menu(tearoff=0)
        menu.add_command(label="Добавить узел", command=lambda: self.add_node_menu(event))
        menu.post(event.x_root, event.y_root)
    
    def add_node_menu(self, event):
        """
        Окно создания узла
        """
        
        window = Toplevel(self)
        window.geometry(f"650x455+{event.x_root - 50}+{event.y_root - 50}")
        window.title(f"Создание узла ({self.get_current_gfield().get_name()})")
        window.focus()
        window.grab_set()
        window.transient(self)
        window.resizable(0, 0)
        window.columnconfigure(0, weight=0)
        window.columnconfigure(1, weight=1)
        window.node_selected_file = None

        def ref():
            showinfo("Справка об узле",
                     "нету еще")
        def update_preview_node(event=None, *args):
            self.update()
            preview_canvas.coords(rect, 20, 20, window.temp_node_width.get() + 20, window.temp_node_height.get() + 20)
            if event is not None and not isinstance(event, int):
                if event.widget == node_name_entry:
                    preview_canvas.itemconfig(header, text=event.widget.get())
                elif event.widget == code_place:
                    preview_canvas.itemconfig(code, text=event.widget.get("1.0", END))

        def update_label_width(val):
            window.temp_node_width.set(round(float(val)))
        
        def update_label_height(val):
            window.temp_node_height.set(round(float(val)))

        def select_file_as_reference():
            filepath = filedialog.askopenfilename(
                title="Выберите файл",
                initialdir="/",
                filetypes=(
                    ("Все файлы", "*.*"),
                    ("Текстовые файлы", "*.txt"),
                    ("Python код", "*.py"),
                )   
            )
            if filepath:
                window.node_selected_file = filepath

        def draw_small_grid():
            preview_canvas.delete("grid_line")
            w = 325
            h = 160
            step = 12

            if w <= 10 or h <= 10:
                return
            
            for i in range(0, w, step):
                preview_canvas.create_line(i, 0, i, w, tags="grid_line", fill="#4a4a4a", width=1)
            for i in range(0, h, step):
                preview_canvas.create_line(0, i, w, i, tags="grid_line", fill="#4a4a4a", width=1)
            for i in range(0, w, step * 5):
                preview_canvas.create_line(i, 0, i, w, tags="grid_line", fill="#666666", width=2)
            for i in range(0, h, step * 5):
                preview_canvas.create_line(0, i, w, i, tags="grid_line", fill="#666666", width=2)
            
            preview_canvas.tag_raise("preview_node")
        
        def create_rect():
            self.update()
            pc_x = preview_canvas.winfo_x()
            pc_y = preview_canvas.winfo_y()
            rect = preview_canvas.create_rectangle(
                20,
                20,
                240,
                140,
                fill="#363636",
                outline="#FFD000",
                tags="preview_node"
            )
            header = preview_canvas.create_text(
                30,
                30,
                text="",
                fill="#FFFFFF",
                anchor=NW,
                font=("Arial", 11, "bold"),
                tags="node"
            )
            code = preview_canvas.create_text(
                30,
                55,
                text="",
                fill="#08D63C",
                anchor=NW,
                font=("Consolas", 10),
                tags="node"
            )
            return rect, header, code
        
        # Настройка элементов
        # Поле "Имя узла: "
        name_frame = ttk.Frame(window)
        name_frame.grid(row=0, column=0, columnspan=2, padx=6, pady=6, sticky=EW)
        name_frame.columnconfigure(1, weight=1)
        
        ttk.Label(name_frame, text="Имя узла").grid(row=0, column=0, padx=(0, 15), sticky=W)
        node_name_entry = ttk.Entry(name_frame)
        node_name_entry.grid(row=0, column=1, sticky=EW)
        node_name_entry.focus()
        node_name_entry.bind('<KeyRelease>', update_preview_node)
        ref_button = ttk.Button(name_frame, text="Справка", width=25, command=ref)
        ref_button.grid(row=0, column=2, sticky=EW, padx=4)

        # Поле "Код"
        ttk.Label(window, text="Код").grid(row=1, column=0, padx=6, pady=2, sticky=EW)
        code_place = Text(window, height=10, width=42, bg="#1b1b1b", fg="#54E475", font=("Cascadia Code", 9), padx=6, pady=2)
        code_place.grid(row=2, column=0, padx=6, pady=6, sticky=EW)
        code_place.bind('<KeyRelease>', update_preview_node)

        # Холст предпросмотра
        ttk.Label(window, text="Предпросмотр").grid(row=1, column=1, padx=6, pady=2, sticky=EW)
        preview_canvas = Canvas(window, bg="#2b2b2b", height=165)
        preview_canvas.grid(row=2, column=1, padx=6, pady=6, sticky=EW)
        draw_small_grid()
        rect, header, code = create_rect()

        # Общий фрейм для опций
        setting_frame = ttk.Frame(window)

        # Фрейм "Порты связей"
        connect_point_frame = ttk.LabelFrame(setting_frame, text="Порты связей", width=250, height=120)
        
        window.in_port_enable = IntVar(value=0)
        window.out_port_enable = IntVar(value=0)

        in_port_checkbutton = ttk.Checkbutton(connect_point_frame, text="Входной порт", variable=window.in_port_enable)
        out_port_checkbutton = ttk.Checkbutton(connect_point_frame, text="Выходной порт", variable=window.out_port_enable)

        in_port_checkbutton.pack(anchor=NW, padx=10, pady=10)
        out_port_checkbutton.pack(side=LEFT, anchor=NW, padx=10, pady=10)

        connect_point_frame.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        # Фрейм "Геометрия"
        geometry_frame = ttk.LabelFrame(setting_frame, text="Геометрия узла", width=235, height=120)
        
        window.temp_node_width = IntVar(value=220) # 220 - стандартная ширина
        window.temp_node_height = IntVar(value=120) # 120 - стандартная высота
        window.temp_node_width.trace_add("write", lambda name, index, mode: update_preview_node(rect))
        window.temp_node_height.trace_add("write", lambda name, index, mode: update_preview_node(rect))
        
        ttk.Label(geometry_frame, text="Ширина").grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        width_spinbox = ttk.Scale(geometry_frame, orient=HORIZONTAL, from_=190.0, to=325.0, value=220, command=update_label_width)
        width_spinbox.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        ttk.Label(geometry_frame, textvariable=window.temp_node_width).grid(row=0, column=2, padx=3, pady=10)

        ttk.Label(geometry_frame, text="Высота").grid(row=1, column=0, sticky="nw", padx=10, pady=10)
        height_spinbox = ttk.Scale(geometry_frame, orient=HORIZONTAL, from_=90.0, to=250.0, value=120, command=update_label_height)
        height_spinbox.grid(row=1, column=1, sticky="nw", padx=10, pady=10)
        ttk.Label(geometry_frame, textvariable=window.temp_node_height).grid(row=1, column=2, padx=3, pady=10)

        geometry_frame.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        # Фрейм "Дополнительно"
        other_options_frame = ttk.LabelFrame(setting_frame, text="Дополнительно", width=235, height=120)
        
        other_options_frame.grid(row=0, column=2, padx=6, pady=6, sticky="nsew")
        
        geometry_frame.grid_propagate(False)
        connect_point_frame.grid_propagate(False)
        other_options_frame.grid_propagate(False)
        
        setting_frame.grid(row=4, column=0, columnspan=2, padx=6, pady=6, sticky="nsew")

        def collect_data_and_create(e):
            name = node_name_entry.get().strip()
            code = code_place.get("1.0", END).strip()
            
            if not name:
                showwarning("Предупреждение", f"Имя узла не должно быть пустым!\nИмя изменено на Узел")
                name = "Узел"
                node_name_entry.insert(0, name)
            else:
                self.add_node(event, name, code, window.in_port_enable, window.out_port_enable, window.temp_node_width.get(), window.temp_node_height.get())
                window.destroy()

        # Кнопка "Создать"
        create_button = ttk.Button(
            window,
            text="Создать",
        )
        create_button.grid(
            row=5, column=0,
            padx=6, pady=6,
            sticky=EW, columnspan=2
        )
        create_button.bind("<Button-1>", collect_data_and_create)
    def add_node(self, event, name, code, in_port_enable, out_porn_enable, width, height):
        """
        Сохранение ноды в текущем графическом поле и отрисовка ее на холсте
        """
        current_gfield : Gfield = self.get_current_gfield()
        canvas : Canvas = current_gfield.get_canvas()
        this_node_uid = current_gfield.add_node(name, code) - 1
        # Стандартная ширина: 220
        # Стандартная длина: 120
        node_rect_id = canvas.create_rectangle(
            event.x,
            event.y,
            event.x + width,
            event.y + height,
            fill="#363636",
            outline="#FFD000",
            tags="node"
        )
        node_header_id = canvas.create_text(
            event.x + 10,
            event.y + 10,
            text=name,
            fill="#FFFFFF",
            anchor=NW,
            font=("Arial", 11, "bold"),
            tags="node"
        )
        node_code_id = canvas.create_text(
            event.x + 10,
            event.y + 35,
            text=code,
            fill="#08D63C",
            anchor=NW,
            font=("Consolas", 10),
            tags="node"
        )
        set_node_button = canvas.create_rectangle(
            event.x + width - 35,
            event.y + 8,
            event.x + width - 10,
            event.y + 33,
            fill="#575656", outline="#FFD000",
            tags="node"
        )
        set_node_text = canvas.create_text(
            event.x + width - 22,
            event.y + 21,
            text="⚙️", fill="#FFD000",
            font=("Arial", 10, "bold"),
            tags="node"
        )
        run_code_button = canvas.create_rectangle(
            event.x + width - 35,
            event.y + 38,
            event.x + width - 10,
            event.y + 63,
            fill="#575656", outline="#FFD000",
            tags="node"
        )
        run_code_text = canvas.create_text(
            event.x + width - 22,
            event.y + 50,
            text="▶︎", fill="#FFD000",
            font=("Arial", 10, "bold"),
            tags="node"
        )
        if in_port_enable.get():
            print("Входной порт включен")

        if out_porn_enable.get():
            print("Выходной порт включен")

        canvas.tag_bind(set_node_button, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(set_node_text, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(run_code_button, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        canvas.tag_bind(run_code_text, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        
        # Настройка подсветки узлов при их нажатий
        canvas.tag_bind(node_rect_id, "<ButtonPress-1>", lambda e: self.node_drag_start(e, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text,))
        canvas.tag_bind(node_rect_id, "<B1-Motion>", lambda e: self.node_drag_motion(e, node_header_id, node_rect_id, node_code_id, set_node_button, run_code_button, set_node_text, run_code_text))
        canvas.tag_bind(node_rect_id, "<ButtonRelease-1>", lambda e: self.node_drag_end(e, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text))

    def edit_node_menu(self, event, name_id, code_id, node_id):
        window = Toplevel(self)
        window.geometry(f"350x305+{event.x_root - 100}+{event.y_root + 100}")
        window.title(f"Редактирование узла")
        window.focus()
        window.grab_set()
        window.transient(self)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)

        current_gfield : Gfield = self.get_current_gfield()
        current_canvas : Canvas = current_gfield.get_canvas()
        
        ttk.Label(window, text="Имя узла: ").grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        node_name_entry = ttk.Entry(window, width=45)
        node_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        node_name_entry.insert(0, current_canvas.itemcget(name_id, "text"))
        node_name_entry.focus()

        # Поле "Код"
        ttk.Label(window, text="Код:").grid(row=1, column=0, padx=6, pady=2, sticky=EW)
        code_place = Text(window, height=12)
        code_place.grid(row=2, column=0, padx=6, pady=6, sticky=EW, columnspan=2)
        code_place.insert("1.0", current_canvas.itemcget(code_id, "text"))

        def collect_data_and_edit_node(e):
            name = node_name_entry.get().strip()
            code = code_place.get("1.0", END).strip()
            if not name:
                showwarning("Предупреждение", f"Имя узла не должно быть пустым!")
            else:
                current_canvas.itemconfig(name_id, text=name)
                current_canvas.itemconfig(code_id, text=code)
                current_gfield.get_nodes()[node_id].header = name
                current_gfield.get_nodes()[node_id].code = code
                window.destroy()
        
        ok_button = ttk.Button(window, text="Отмена")
        ok_button.grid(row=3, column=0, padx=6, pady=6, sticky=EW)
        ok_button.bind("<Button-1>", lambda e: window.destroy())

        cancel_button = ttk.Button(window, text="Применить")
        cancel_button.grid(row=3, column=1, padx=6, pady=6, sticky=EW)
        cancel_button.bind("<Button-1>", collect_data_and_edit_node)

    def run_code(self, event, name_id, code_id):
        """
        Запуск кода
        """
        # Получение текущего холста и ноды код которой мы будем запускать
        current_canvas : Canvas = self.get_current_canvas()
        code = current_canvas.itemcget(code_id, "text")

        # Настройка окна
        window = Toplevel(self)
        window.geometry(f"650x400+{event.x_root - 50}+{event.y_root - 50}")
        window.title(f"Запуск кода \"{current_canvas.itemcget(name_id, "text")}\"")
        window.focus()
        window.grab_set()
        window.transient(self)

        # Сохраняем старый поток и определяем поток в буфер
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        ttk.Label(window, text="Результат выполнения кода: ").pack(padx=6, pady=6, anchor=NW)
        frame = Frame(window)
        text = Text(frame)

        try:
            exec(code)
            result = sys.stdout.getvalue()
            text.insert(END, result)
        except Exception as e:
            text.insert(END, f"Ошибка: {e}")
        finally:
            sys.stdout = old_stdout

        text.config(state=DISABLED)
        text.pack(expand=1, fill=BOTH)
        frame.pack(expand=1, fill=BOTH, padx=6, pady=6)
    
    def grid_line(self, e=None):
        canvas : Canvas = self.get_current_canvas()
        canvas.delete("grid_line")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        step = 30

        if w <= 10 or h <= 10:
            return
        
        for i in range(0, w, step):
            canvas.create_line(i, 0, i, w, tags="grid_line", fill="#4a4a4a", width=1)

        for i in range(0, h, step):
            canvas.create_line(0, i, w, i, tags="grid_line", fill="#4a4a4a", width=1)
        
        for i in range(0, w, step * 5):
            canvas.create_line(i, 0, i, w, tags="grid_line", fill="#666666", width=2)

        for i in range(0, h, step * 5):
            canvas.create_line(0, i, w, i, tags="grid_line", fill="#666666", width=2)
         
        canvas.tag_raise("node")
    
    def node_drag_start(self, event, *args):
        """
        Перемещение узла по полю (начало события)
        Аргументы:
        node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text
        
        Аргументы соответственны args[i] т.е
        node_rect_id = args[0] а run_code_text = args[4]
        """
        canvas : Canvas = self.get_current_canvas()
        change_color = "#08D63C"
        for item in [args[0], args[1], args[2]]:
            canvas.itemconfig(item, outline=change_color)
        for button in [args[3], args[4]]:
            canvas.itemconfig(button, fill=change_color)
        self.drag_info = {
            "x": event.x,
            "y": event.y
        }

    def node_drag_motion(self, event, *args):
        canvas : Canvas = self.get_current_canvas()
        dx = event.x - self.drag_info["x"]
        dy = event.y - self.drag_info["y"]
        for item in args:
            canvas.move(item, dx, dy)
        self.drag_info["x"] = event.x
        self.drag_info["y"] = event.y
        
    def node_drag_end(self, event, *args):
        canvas : Canvas = self.get_current_canvas()
        change_color = "#FFD000"
        for item in [args[0], args[1], args[2]]:
            canvas.itemconfig(item, outline=change_color)
        for button in [args[3], args[4]]:
            canvas.itemconfig(button, fill=change_color)
    
    def set_connection_node_menu(self):
        """
        Меню настройки связей узлов
        """
        if self.struct.items_length() == 0:
            return
        # Настройка окна
        window = Toplevel(self)
        window.title("Установка связей узлов")
        window.geometry("490x310+650+250")
        window.resizable(0, 0) 
        window.focus()
        window.transient(self)
        window.grab_set()

        ttk.Label(window, text="ID узла: ").grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        node_id_entry = ttk.Entry(window, width=35)
        node_id_entry.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        node_id_entry.focus()

        ttk.Label(window, text="Входной порт\n(ссылка на внешний узел)").grid(row=1, column=0, padx=6, pady=6, sticky=EW)
        ref_of_in_port = ttk.Entry(window, width=50)
        ref_of_in_port.grid(row=1, column=1, padx=6, pady=6, sticky=EW)

        ttk.Label(window, text="Выходной порт\n(ссылка на внешний узел)").grid(row=2, column=0, padx=6, pady=6, sticky=EW)
        ref_of_out_port = ttk.Entry(window, width=50)
        ref_of_out_port.grid(row=2, column=1, padx=6, pady=6, sticky=EW)

        