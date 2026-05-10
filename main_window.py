from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from tkinter import filedialog
from struct import Struct # структура
from gfield import Gfield # поле
from node import Node     # узел
from tooltip import ToolTip # тултип
from code_place import CodePlace # место кода
from io import StringIO
import os
import sys


"""
Проблемы которые нужно исправить:

При перемещений узла его значения x и y не изменяются
а остаются изначальными
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
                               command=self.create_new_project_menu)
            
        self.create_project_button.bind("<Enter>", lambda e: highlight_event(e, "#dbdbdb"))
        self.create_project_button.bind("<Leave>", lambda e: highlight_event(e, "white"))
        self.create_project_button.grid(row=2, column=0, padx=4, pady=8, sticky="nw")

    def update_structure_panel(self):
        canvas : Canvas = self.get_current_canvas()
        self.struct_panel.columnconfigure(0, weight=1)

        self.struct_panel.columnconfigure(1, weight=0)
        Button(self.struct_panel, text="Графические поля",
                                    bg="#4a4a4a", fg="white",
                                    cursor="hand2", font=("Segoe UI", 10),
                                    activebackground="#383838",
                                    activeforeground="white",
                                    command=self.graphs_manager) \
            .grid(row=3, column=0, columnspan=2, padx=6, pady=4, sticky="nsew")
    def setup_inspector_panel(self):
        # Создание панели инспектора (Правая панель)
        self.inspector_panel = Frame(self, width=300, relief=SOLID, bg="#1b1b1b")
        self.inspector_panel.pack(fill="both", anchor="nw", side=RIGHT)
        self.inspector_panel.grid_propagate(False)
        self.inspector_panel.columnconfigure(0, weight=0)  # колонка с Label - не расширяется
        self.inspector_panel.columnconfigure(1, weight=1)  # колонка с Entry - расширяется
        Label(self.inspector_panel, text="Инспектор", font=("Segoe UI", 18, "bold"), fg="white", background="#1b1b1b") \
            .grid(row=0, column=0, padx=6, pady=6, sticky="sw",columnspan=2)
        self.not_inspection_data_label = Label(self.inspector_panel, text="Нет данных для инспекций", \
              font=("Segoe UI", 12), fg="#808080", background="#1b1b1b", anchor="sw", justify="left")
        self.not_inspection_data_label.grid(row=1, column=0, padx=6, pady=2, sticky="sw")
        self.inspector_data = {}

    def update_inspector_panel(self, node : Node) -> None:
        def update_node_name(event=None) -> None:
            text = event.widget.get()
            if text:
                node.header = text
                canvas.itemconfig(node.header_id, text=text)
                
        canvas : Canvas = self.get_current_canvas()
        self.not_inspection_data_label.destroy()

        if self.inspector_data:
            self.inspector_data["node_name_label"].destroy()
            self.inspector_data["node_name_entry"].destroy()

        node_name_label = Label(self.inspector_panel, text=f"Имя узла:",
                          font=("Arial", 12), fg="#808080", background="#1b1b1b", anchor="sw", justify="left")
        node_name_label.grid(row=1, column=0, padx=6, pady=6, sticky="sw")
        
        node_name_entry = ttk.Entry(self.inspector_panel, width=25)
        node_name_entry.grid(row=1, column=1, padx=6, pady=6, sticky="ew")
        node_name_entry.insert(0, node.header)
        node_name_entry.bind("<KeyRelease>", update_node_name)

        self.inspector_data["node_name_label"] = node_name_label
        self.inspector_data["node_name_entry"] = node_name_entry
        
    def create_new_project_menu(self) -> None:
        """
        Меню создания нового проекта
        """
        # Настройка окна
        window = Toplevel(self)
        window.title("Создание проекта")
        window.geometry("490x200+650+250")
        window.resizable(0, 0)
        window.focus()
        window.transient(self)
        window.grab_set()
        window.columnconfigure(1, weight=1)
        
        def browse_folder() -> None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt", # Расширение по умолчанию
                filetypes=[("Текстовые файлы", "*.txt"), ("Файл проекта .pgstd", "*.pgstd")], # Типы файлов
                title="Сохранить файл как..."
            )
            if file_path:
                path_entry.insert(0, file_path)
                
        def collect_data_and_create_project(event=None) -> None:
            name : str = project_name_entry.get().strip()
            desc : str = project_desc_entry.get().strip()
            if not name:
                showwarning("Предупреждение", "Имя проекта не должно быть пустым!")
                notebook.select(0)
                project_name_entry.focus()
            else:
                self.struct.set_struct_name(name)
                self.struct.set_struct_desc(desc)
                window.destroy()
                self.not_struct_data_label.destroy()
                self.create_project_button.destroy()
                Label(self.struct_panel, text=name,
                    font=("Arial", 13, "bold"), fg="#A8A8A8",
                    background="#1b1b1b", anchor="nw",
                    justify="left") \
                    .grid(row=1, column=0, padx=8, pady=4, sticky="nw")
                
                Label(self.struct_panel, text=self.struct.project_desc or "Без описания",
                    font=("Arial", 10), fg="#808080",
                    bg="#1b1b1b", anchor="w").grid(row=2, column=0, padx=8, pady=(0, 8), sticky="nw" \
                    "")
                self.title(f"PyGraph Studio ({name})")
                self.setup_toolbar()
                self.update_structure_panel()

        # Настройка элементов
        # Поле "Название проекта: "
        notebook = ttk.Notebook(window, height=125)
        main_frame = Frame(notebook)

        ttk.Label(main_frame, text="Название проекта: ").grid(row=0, column=0, padx=6, pady=6, sticky="ew")
        project_name_entry = ttk.Entry(main_frame, width=48)
        project_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
        project_name_entry.focus()

        # Поле "Описание (необязательно): "
        ttk.Label(main_frame, text="Описание (необязательно): ").grid(row=1, column=0, padx=6, pady=6, sticky="ew")
        project_desc_entry = ttk.Entry(main_frame, width=48)
        project_desc_entry.grid(row=1, column=1, padx=6, pady=6, sticky="ew")

        file_frame = Frame(notebook)
        ttk.Label(file_frame, text="Сохранить проект:").grid(row=0, column=0, padx=6, pady=6, sticky="w")

        path_entry = ttk.Entry(file_frame, width=42)
        path_entry.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        browse_btn = ttk.Button(file_frame, text="Обзор...", command=browse_folder)
        browse_btn.grid(row=0, column=2, padx=6, pady=6)

        repo_frame = Frame(notebook)
        ttk.Label(repo_frame, text="Здесь вы сможете инициализировать систему контроля версий Git").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        
        notebook.add(main_frame, text="Основное")
        notebook.add(file_frame, text="Файл")
        notebook.add(repo_frame, text="Репозиторий Git")
        notebook.grid(row=3, column=0, columnspan=2, padx=6, pady=6, sticky="ew")
        notebook.grid_propagate(False)

        # Кнопка "Создать"
        create_btn = ttk.Button(window, text="Создать")
        create_btn.grid(row=4, column=0, columnspan=2, padx=6, pady=6, sticky="ew")
        create_btn.bind("<Button-1>", collect_data_and_create_project)
        window.bind("<Return>", collect_data_and_create_project)

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
        canvas = Canvas(frame)
        canvas.config(bg="#2b2b2b")
        
        # Добавляем в структуру проекта графическое поле
        new_gfield = Gfield(self.items_counter - 1, gfield_name, gfield_description, canvas)
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
            x1, y1, x2, y2 = preview_canvas.coords(rect)
            if window.in_port_enable.get():
                preview_canvas.delete("in_port")
                pos_y = (y1 + y2) // 2
                preview_canvas.create_oval(
                    x1 - 5, pos_y - 5,
                    x1 + 5, pos_y + 5,
                    fill="#1C7700", outline="white",
                    tags="in_port"
                )
            if window.out_port_enable.get():
                preview_canvas.delete("out_port")
                pos_y = ((y1 + y2) // 2) + 30
                preview_canvas.create_oval(
                    x2 - 5, pos_y - 5,
                    x2 + 5, pos_y + 5,
                    fill="#1C7700", outline="white",
                    tags="out_port"
                )
            if event is not None and not isinstance(event, int):
                if event.widget == node_name_entry:
                    preview_canvas.itemconfig(header, text=event.widget.get())
                elif event.widget == code_place:
                    preview_canvas.itemconfig(code, text=event.widget.get("1.0", END))
        def update_ports_preview(node_rect=None):
            x1, y1, x2, y2 = preview_canvas.coords(rect)
            in_port_point = None
            out_port_point = None
            
            preview_canvas.delete("in_port")
            preview_canvas.delete("out_port")

            if window.in_port_enable.get():
                pos_y = (y1 + y2) // 2
                in_port_point = preview_canvas.create_oval(
                    x1 - 5, pos_y - 5,
                    x1 + 5, pos_y + 5,
                    fill="#1C7700", outline="white",
                    tags="in_port"
                )
            else:
                preview_canvas.delete(in_port_point)

            if window.out_port_enable.get():
                pos_y = ((y1 + y2) // 2) + 30
                out_port_point = preview_canvas.create_oval(
                    x2 - 5, pos_y - 5,
                    x2 + 5, pos_y + 5,
                    fill="#1C7700", outline="white",
                    tags="out_port"
                )
            else:
                preview_canvas.delete(out_port_point)
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

        in_port_checkbutton = ttk.Checkbutton(connect_point_frame, text="Входной порт", variable=window.in_port_enable, command=update_ports_preview)
        out_port_checkbutton = ttk.Checkbutton(connect_point_frame, text="Выходной порт", variable=window.out_port_enable, command=update_ports_preview)

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
                preview_canvas.itemconfig(header, text=name)
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

    def add_node_at_position(self, x, y, node):
        pass

    def add_node(self, event, name, code, in_port_enable, out_port_enable, width, height):
        """
        Сохранение ноды в текущем графическом поле и отрисовка ее на холсте
        """


        current_gfield : Gfield = self.get_current_gfield()
        canvas : Canvas = current_gfield.get_canvas()
        result = current_gfield.add_node(name, code, event.x, event.y, False, False)
        this_node_uid : int = result[0] - 1
        node : Node = result[1]
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
        
        x1, y1, x2, y2 = canvas.coords(node_rect_id)
        in_port_point = None
        out_port_point = None

        node.rect_id = node_rect_id
        node.header_id = node_header_id
        node.code_id = node_code_id
        node.set_node_button = set_node_button
        node.set_node_text = set_node_text
        node.run_code_button = run_code_button
        node.run_code_text = run_code_text

        if in_port_enable.get():
            pos_y = (y1 + y2) // 2
            in_port_point = canvas.create_oval(
                x1 - 5, pos_y - 5,
                x1 + 5, pos_y + 5,
                fill="#1C7700", outline="white",
                tags="in_port"
            )
            node.in_port_enable = True
            node.in_port_id = in_port_point
            current_gfield.add_port(in_port_point)
            canvas.tag_bind(in_port_point, "<ButtonPress-1>", lambda e: self.port_connection_start(e, in_port_point))
            canvas.tag_bind(in_port_point, "<B1-Motion>", lambda e: self.port_connection_process(e, in_port_point))
            canvas.tag_bind(in_port_point, "<ButtonRelease-1>", lambda e: self.port_connection_end(e, in_port_point))
            
        if out_port_enable.get():
            pos_y = ((y1 + y2) // 2) + 30
            out_port_point = canvas.create_oval(
                x2 - 5, pos_y - 5,
                x2 + 5, pos_y + 5,
                fill="#1C7700", outline="white",
                tags="out_port"
            )
            node.out_port_enable = True
            node.out_port_id = out_port_point
            current_gfield.add_port(out_port_point)
            canvas.tag_bind(out_port_point, "<ButtonPress-1>", lambda e: self.port_connection_start(e, out_port_point))
            canvas.tag_bind(out_port_point, "<B1-Motion>", lambda e: self.port_connection_process(e, out_port_point))
            canvas.tag_bind(out_port_point, "<ButtonRelease-1>", lambda e: self.port_connection_end(e, out_port_point))
        
        canvas.tag_bind(set_node_button, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(set_node_text, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(run_code_button, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        canvas.tag_bind(run_code_text, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        
        # Настройка подсветки узлов при их нажатий
        canvas.tag_bind(node_rect_id, "<ButtonPress-1>", lambda e: self.node_drag_start(e, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text, in_port_point, out_port_point))
        canvas.tag_bind(node_rect_id, "<B1-Motion>", lambda e: self.node_drag_motion(e, node, node_header_id, node_rect_id, node_code_id, set_node_button, run_code_button, set_node_text, run_code_text, in_port_point, out_port_point))
        canvas.tag_bind(node_rect_id, "<ButtonRelease-1>", lambda e: self.node_drag_end(e, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text, in_port_point, out_port_point, node))

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
        canvas.tag_raise("in_port")
        canvas.tag_raise("out_port")
        canvas.tag_raise("title_panel")
        canvas.tag_raise("title_text")

    def node_drag_start(self, event, *args):
        """
        Перемещение узла по полю (начало события)
        Аргументы:
        node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text
        
        Аргументы соответственны args[i] т.е
        node_rect_id = args[0] а run_code_text = args[4]
        """
        canvas : Canvas = self.get_current_canvas()
        change_color = "#33FF00"
        for item in [args[0], args[1], args[2]]:
            canvas.itemconfig(item, outline=change_color)
        for button in [args[3], args[4]]:
            canvas.itemconfig(button, fill=change_color)
        self.drag_info = {
            "x": event.x,
            "y": event.y
        }

        clicked_node = self.find_node_at_cursor(event)
        self.update_inspector_panel(clicked_node)

    def node_drag_motion(self, event, node, *args):
        canvas : Canvas = self.get_current_canvas()
        dx = event.x - self.drag_info["x"]
        dy = event.y - self.drag_info["y"]
        
        for item in args:
            if item is not None:
                canvas.move(item, dx, dy)
        self.drag_info["x"] = event.x
        self.drag_info["y"] = event.y
        if node:
            self.update_connection_lines(event, node)
            

    def node_drag_end(self, event, *args):
        canvas : Canvas = self.get_current_canvas()
        change_color = "#FFD000"
        for item in [args[0], args[1], args[2]]:
            canvas.itemconfig(item, outline=change_color)
        for button in [args[3], args[4]]:
            canvas.itemconfig(button, fill=change_color)
        node = args[7]
        if node:
            self.update_connection_lines_end(event, node)
            
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

    def port_connection_start(self, event, port_id):
        canvas : Canvas = self.get_current_canvas()
        canvas.itemconfig(port_id, fill="#FFD000")
        port = canvas.find_closest(event.x, event.y)[0]
        self.connection_data = {
            "temp_line": None,
            "start_port": port,
            "temp_port_point": None
        }

    def port_connection_process(self, event, port_id):
        canvas : Canvas = self.get_current_canvas()
        gfield : Gfield = self.get_current_gfield()

        if self.connection_data["temp_line"]:
            canvas.delete(self.connection_data["temp_line"])

        x1, y1, x2, y2 = canvas.coords(port_id)
        port_center_x = (x1 + x2) // 2
        port_center_y = (y1 + y2) // 2

        self.connection_data["temp_line"] =  canvas.create_line(
            port_center_x, port_center_y, event.x, event.y,
            fill="#FFD000", tags="line", dash=(4, 4)
        )

        current_canvas_obj = self.find_port_at_position(canvas, event.x, event.y, gfield)
        if current_canvas_obj in gfield.ports and (canvas.itemcget(current_canvas_obj, "tags") in ("in_port", "out_port")):
            self.connection_data["temp_port_point"] = current_canvas_obj
            canvas.itemconfig(current_canvas_obj, fill="#FFD000")
        else:
            canvas.itemconfig(self.connection_data["temp_port_point"], fill="#1C7700")

    def port_connection_end(self, event, from_port):
        canvas : Canvas = self.get_current_canvas()
        gfield : Gfield = self.get_current_gfield()

        """
        from_port - ID порта (точки) с которого начинается соединение т.е from_port
        to_port - ID порта с которым соединяется начальный порт
        """

        if self.connection_data and self.connection_data["temp_line"]:
            canvas.delete(self.connection_data["temp_line"])
        
        to_port = self.find_port_at_position(canvas, event.x, event.y, gfield)

        try:
            tags = canvas.gettags(to_port)
        except TclError:
            if self.connection_data:
                self.connection_data = None
            return
        
        is_port = any(tag in ("in_port", "out_port") for tag in tags)

        if is_port and from_port != to_port:
            self.create_connection(from_port, to_port)
        else:
            canvas.itemconfig(to_port, fill="#1C7700")
            canvas.itemconfig(from_port, fill="#1C7700")

    def create_connection(self, from_port, to_port):
        canvas : Canvas = self.get_current_canvas()
        gfield : Gfield = self.get_current_gfield()

        from_node = self.find_node_at_port(canvas, from_port, gfield)
        to_node = self.find_node_at_port(canvas, to_port, gfield)

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
            canvas.itemconfig(to_port, fill="#1C7700")
            canvas.itemconfig(from_port, fill="#1C7700")
            return None
        
        if from_node == to_node:
            showwarning(
                "Ошибка создания связи",
                "Один и тот же узел\n\n"
                "ВЫХОД одного узла соединили со ВХОДОМ того же узла\n"
            )
            canvas.itemconfig(to_port, fill="#1C7700")
            canvas.itemconfig(from_port, fill="#1C7700")
            return None

        fpx1, fpy1, fpx2, fpy2 = canvas.coords(from_port)
        tpx1, tpy1, tpx2, tpy2 = canvas.coords(to_port)

        final_line = canvas.create_line(
            (fpx1 + fpx2) // 2, (fpy1 + fpy2) // 2,
            ((tpx1 + tpx2) // 2), (tpy1 + tpy2) // 2,
            fill="#1C7700", tags="line", dash=(4, 4)
        )
        
        # Если была попытка создания обратной связи
        # Просто инвертируем связь
        if is_inverted:
            to_node.connection_line_id = final_line
            to_node.create_output_connection(from_node)
        else:
            from_node.connection_line_id = final_line
            from_node.create_output_connection(to_node)

        canvas.itemconfig(to_port, fill="#1C7700")
        canvas.itemconfig(from_port, fill="#1C7700")
        canvas.itemconfig(self.connection_data["temp_port_point"], fill="#1C7700")
    
    def update_connection_lines(self, event, node : Node):
        canvas : Canvas = self.get_current_canvas()
        if node.input_node:
            x1, y1, x2, y2 = canvas.coords(node.input_node.out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2             
            
            canvas.itemconfig(node.input_node.connection_line_id, fill="#FFD000")
            canvas.itemconfig(node.in_port_id, fill="#FFD000")
            canvas.coords(node.input_node.connection_line_id, from_x, from_y, to_x, to_y)
        
        if node.output_node:
            x1, y1, x2, y2 = canvas.coords(node.out_port_id)
            from_x = (x1 + x2) // 2
            from_y = (y1 + y2) // 2

            x1, y1, x2, y2 = canvas.coords(node.output_node.in_port_id)
            to_x = (x1 + x2) // 2
            to_y = (y1 + y2) // 2
            
            canvas.itemconfig(node.connection_line_id, fill="#FFD000")
            canvas.itemconfig(node.out_port_id, fill="#FFD000")
            canvas.coords(node.connection_line_id, from_x, from_y, to_x, to_y)

    def update_connection_lines_end(self, event, node : Node):
        canvas : Canvas = self.get_current_canvas()
        if node.input_node:
            canvas.itemconfig(node.input_node.connection_line_id, fill="#1C7700")
            canvas.itemconfig(node.in_port_id, fill="#1C7700")
        if node.output_node:
            canvas.itemconfig(node.connection_line_id, fill="#1C7700")
            canvas.itemconfig(node.out_port_id, fill="#1C7700")

    def find_port_at_position(self, canvas : Canvas, x : int, y : int, gfield : Gfield):
        for port_id in gfield.ports:
            x1, y1, x2, y2 = canvas.coords(port_id)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return port_id
        return None
    
    def find_node_at_port(self, canvas : Canvas, port_id : int, gfield : Gfield):
        for node in gfield.get_nodes().values():
            if node.in_port_id == port_id or node.out_port_id == port_id:
                    return node
        return None
    
    def find_node_at_cursor(self, event):
        gfield : Gfield = self.get_current_gfield()
        canvas : Canvas = gfield.get_canvas()
        item = canvas.find_closest(event.x, event.y)[0]
        
        for node in gfield.get_nodes().values():
            if node.rect_id == item:
                gfield.set_selected_node(node)
                return node
            
        return None
    
    # Managers
    def graphs_manager(self):
        """
        Проблемы:
        1. Составить сортировку ID после удаления одного графа
        2. После перезахода перерисовывать каждый раз таблицу
        """
        def select(event=None):
            selection = table_view.selection()
            if selection:
                item = table_view.item(selection, "values")
                graph_name.set(str(item[1]))
        
        def create_gfield_at_table():
            temp_window = self.creating_new_gfield_menu()
            self.wait_window(temp_window)
            current_item = self.struct.get_item(self.gfields_counter - 1)
            if current_item["type"] == "gfield":
                table_view.insert("", "end", values=(self.gfields_counter - 1, current_item["data"].get_name()))
                
        def save_changes():
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[0])
            target_item = self.struct.get_item(selected_item_id)
            if target_item["type"] == "gfield" and graph_name.get():
                table_view.item(selected, values=(selected_item_id, graph_name.get()))
                target_item["data"].name = graph_name.get()
                self.notebook.tab(selected_item_id, text=f"📊 {graph_name.get()}")

        def delete_selected():
            if self.items_counter == 0:
                return
            
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[0])
            table_view.delete(selected)
            self.notebook.forget(selected_item_id)
            self.struct.remove_item(selected_item_id)
            graph_name.set("")
            self.items_counter -= 1
            self.gfields_counter -= 1

            refrash_table()
            
            if self.struct.items_length() == 0:
                self.notebook.pack_forget()
                self.config(bg="#2b2b2b")

        def refrash_table():
            if self.items_counter == 0:
                return
            
            for item in table_view.get_children():
                table_view.delete(item)

            for id, item in enumerate(self.struct.get_items().values()):
                if item["type"] == "gfield":
                    table_view.insert("", "end", \
                        values=(id, item["data"].get_name()))
                    
        def start_draw():
            for id, item in enumerate(self.struct.get_items().values()):
                if item["type"] == "gfield":
                    table_view.insert("", "end", \
                        values=(id, item["data"].get_name()))
                    
        window = Toplevel(self)
        window.geometry(f"850x505+500+300")
        window.title(f"Менеджер графических полей")
        window.focus()
        window.grab_set()
        window.transient(self)
        window.resizable(0, 0)
        window.configure(bg="#2b2b2b")

        toolbar_frame = Frame(window, height=50, bg="#3a3a3a")
        toolbar_frame.pack(fill="x")
        toolbar_frame.pack_propagate(False)
        
        Button(toolbar_frame, text="+ Добавить графу",
               bg="#4a6a8a", fg="white", padx=10, cursor="hand2", font=("Segoe UI", 9, "bold"), command=create_gfield_at_table).pack(side=LEFT, padx=12)
        
        Button(toolbar_frame, text="🗑 Удалить выбранное",
               bg="#6a3a3a", fg="white", padx=10, cursor="hand2", font=("Segoe UI", 9, "bold"), command=delete_selected).pack(side=LEFT, padx=2)

        Label(toolbar_frame, text="Менеджер графических полей", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(side=RIGHT, padx=10)
        
        # id - ID графического поля
        # name - Имя графического поля
        columns = ("id", "name")
        table_frame = Frame(window, width=250, relief="raised")
        table_frame.pack(expand=1, fill="both", padx=6, pady=6, side="left", anchor="nw")

        table_view = ttk.Treeview(table_frame, columns=columns, show="headings")
        table_view.pack(expand=1, fill="both")
        table_view.heading("id", text="ID графы")
        table_view.heading("name", text="Название")
        table_view.bind("<<TreeviewSelect>>", select)

        # options
        options_panel_frame = Frame(window, relief="raised", bd=1, bg="#3a3a3a")
        options_panel_frame.pack(expand=1, fill="both", padx=6, pady=6, side="right")
        Label(options_panel_frame, text="Свойства", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(anchor=W, padx=10, pady=(5, 0))
        
        options_elements_frame = Frame(options_panel_frame, bg="#3a3a3a", bd=1)
        options_elements_frame.pack(expand=1, fill="both", padx=6, pady=(6, 0))
        options_elements_frame.pack_propagate(False)

        Label(options_elements_frame, text="Имя графы: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").pack(padx=4, pady=6, anchor="nw", side="left")
        
        graph_name = StringVar()
        ttk.Entry(options_elements_frame, textvariable=graph_name).pack(padx=4, pady=6, anchor="nw", side="right")

        Button(options_panel_frame, text="Сохранить",
               bd=1, bg="#516a3a", fg="white",
               font=("Segoe UI", 9, "bold"), command=save_changes).\
            pack(padx=6, pady=6, side="top", fill="x")
        
        start_draw()
        