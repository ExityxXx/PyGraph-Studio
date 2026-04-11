from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from tkinter.messagebox import showinfo
from struct import Struct # структура
from gfield import Gfield # поле
from node import Node     # узел
from io import StringIO
import sys

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Инициализация элементов окна
        self.init_elements()

        # Инициализация вкладок меню
        self.setup_menu()

    def init_elements(self):
        # Создание структуры проекта
        self.struct : Struct = Struct()
        self.gfields_counter = 0
        
        # Настройка окна приложения
        self.title("PyGraph Studio")
        self.geometry("1080x720+480+100")
        self.config(background="#2b2b2b")

        # Создание набора вкладок
        self.notebook = ttk.Notebook(self)
    
    def get_current_canvas(self):
        if self.struct.gfields_count() == 0:
            return
        return self.struct.get_gfield \
            (self.notebook.index(self.notebook.select())).get_canvas()
        
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
        self.ref_tab = Menu(tearoff=0)              # Вкладка "Справка"
        self.test_debug_tab = Menu(tearoff=0)       # Вкладка "Отладка разработчика"

        # Настройка основного меню и привязка вкладок к подменю
        self.main_menu.add_cascade(label="Файл", menu=self.file_tab)
        self.main_menu.add_cascade(label="Правка", menu=self.editing_tab)
        self.main_menu.add_cascade(label="Выполнить", menu=self.run_tab)
        self.main_menu.add_cascade(label="Справка", menu=self.ref_tab)
        self.main_menu.add_cascade(label="Отладка разработчика",command=self.developer_debug)

        # Настройка вкладки "Файл"
        self.file_tab.add_command(label="Создать новое графическое поле", command=self.creating_new_gfield_menu)
        self.file_tab.add_command(label="Удалить текущее графическое поле", command=self.delete_current_gfield)
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

        # Настройка вкладки "Справка"
        self.ref_tab.add_command(label="О программе")
        self.config(menu=self.main_menu)

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
                for existing in self.struct.get_dict().values():
                    if existing.get_name() == gfield_name:
                        showwarning("Предупреждение", "Графическое поле с таким именем уже существует")
                        return
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
        frame = Frame(self.notebook)
        canvas = Canvas(frame)
        canvas.config(bg="#2b2b2b")
        
        # Добавляем в структуру проекта графическое поле
        new_gfield = Gfield(self.gfields_counter - 1, gfield_name, gfield_description, canvas, list())
        self.struct.add_gfield(self.gfields_counter - 1, new_gfield)

        canvas.pack(expand=1, fill=BOTH)
        self.notebook.add(frame, text=gfield_name)
        self.notebook.pack(expand=1, fill=BOTH)

        # Биндинг контекстного меню
        canvas.bind("<Button-3>", lambda e: self.context_menu(new_gfield, e))
        canvas.bind("<Configure>", lambda e: self.grid_line(e))

    def delete_current_gfield(self):
        """
        Удаление графического поля
        """
        if self.struct.gfields_count() <= 0:
            return
        
        current_selected_index = self.notebook.index(self.notebook.select())
        self.notebook.forget(current_selected_index)
        self.struct.remove_gfield(current_selected_index)
        self.gfields_counter -= 1
        
        if self.struct.gfields_count() == 0:
            self.notebook.pack_forget()
            self.config(bg="#2b2b2b")
        
    def developer_debug(self):
        """
        Меню отладки
        """
        # Генерация отладочного контента
        gfields_count = self.struct.gfields_count()
        gfields : dict = self.struct.get_dict()
        generated_result = "Отсутствуют графические поля для отладки"
        current_gfield = None
        if gfields:
            current_gfield = self.struct.get_gfield(self.notebook.index(self.notebook.select())).get_name()
            generated_result = f"Общее количество: {gfields_count}\nТекущее графическое поле: \"{current_gfield }\"\n"

        for i in range(len(gfields)):
            generated_result += \
                f"Отчёт по графическому полю №{i+1}:\n" \
                f"    Название: {gfields[i].get_name()}\n" \
                f"    Описание: {gfields[i].get_description()}\n" \
                f"    Узлы:   "
            for i in gfields[i].get_nodes().values():
                generated_result += \
                    f"{i}\n            "
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
        window.geometry(f"350x305+{event.x_root - 50}+{event.y_root - 50}")
        window.title(f"Создание узла ({self.struct.get_gfield(self.notebook.index(self.notebook.select())).get_name()})")
        window.focus()
        window.grab_set()
        window.transient(self)
        window.resizable(0, 0)
        window.columnconfigure(0, weight=0)
        window.columnconfigure(1, weight=1)
        # Настройка элементов
        # Поле "Имя узла: "
        ttk.Label(window, text="Имя узла: ").grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        node_name_entry = ttk.Entry(window, width=35)
        node_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        node_name_entry.focus()

        # Поле "Код"
        ttk.Label(window, text="Код:").grid(row=2, column=0, padx=6, pady=2, sticky=EW)
        code_place = Text(window, height=12)
        code_place.grid(row=3, column=0, padx=6, pady=6, sticky=EW, columnspan=2)

        def collect_data_and_create(e):
            name = node_name_entry.get().strip()
            code = code_place.get("1.0", END).strip()
            
            if not name:
                showwarning("Предупреждение", f"Имя узла не должно быть пустым!\nИмя изменено на Узел")
                name = "Узел"
                node_name_entry.insert(0, name)
            else:
                self.add_node(event, name, code)
                window.destroy()

        # Кнопка "Создать"
        create_button = ttk.Button(
            window,
            text="Создать",
        )
        create_button.grid(
            row=4, column=0,
            padx=6, pady=6,
            sticky=EW, columnspan=2
        )
        create_button.bind("<Button-1>", collect_data_and_create)

    def add_node(self, event, name, code):
        """
        Сохранение ноды в текущем графическом поле и отрисовка ее на холсте
        """
        current_gfield = self.struct.get_gfield(self.notebook.index(self.notebook.select()))
        canvas : Canvas = current_gfield.get_canvas()
        this_node_uid = current_gfield.add_node(name, code) - 1

        node_rect_id = canvas.create_rectangle(
            event.x,
            event.y,
            event.x + 220,
            event.y + 120,
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
            event.x + 185,
            event.y + 8,
            event.x + 210,
            event.y + 33,
            fill="#575656", outline="#FFD000",
            tags="node"
        )
        set_node_text = canvas.create_text(
            event.x + 198,
            event.y + 21,
            text="⚙️", fill="#FFD000",
            font=("Arial", 10, "bold"),
            tags="node"
        )
        run_code_button = canvas.create_rectangle(
            event.x + 185,
            event.y + 38,
            event.x + 210,
            event.y + 63,
            fill="#575656", outline="#FFD000",
            tags="node"
        )
        run_code_text = canvas.create_text(
            event.x + 198,
            event.y + 50,
            text="▶︎", fill="#FFD000",
            font=("Arial", 10, "bold"),
            tags="node"
        )
        
        canvas.tag_bind(set_node_button, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(set_node_text, "<Button-1>", lambda e: self.edit_node_menu(e, node_header_id, node_code_id, this_node_uid))
        canvas.tag_bind(run_code_button, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        canvas.tag_bind(run_code_text, "<Button-1>", lambda e: self.run_code(e, node_header_id, node_code_id))
        
        # Настройка подсветки узлов при их нажатий
        canvas.tag_bind(node_rect_id, "<ButtonPress-1>", lambda e: self.node_drag_start(e, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text))
        canvas.tag_bind(node_rect_id, "<B1-Motion>", lambda e: self.node_drag_motion(e, node_header_id, node_rect_id, set_node_button, run_code_button, set_node_text, run_code_text))
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

        current_gfield : Gfield = self.struct.get_gfield \
            (self.notebook.index(self.notebook.select()))
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