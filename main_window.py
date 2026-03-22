from tkinter import *
from tkinter import ttk

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        # Данные
        self.node_template_list = [
            "Печатать в консоль",
            "Создать переменную",
            "Изменить переменную"
        ]
        # Настройка окна приложения
        self.title("PyGraph Studio")
        self.geometry("1080x720+480+100")
        self.config(background="#4E4E4E")

        # Создание набора вкладок
        self.notebook = ttk.Notebook()

        # Инициализация вкладок меню
        self.setup_menu()

        # Создание левой панели
        # self.left_panel = Frame(borderwidth=1, relief=SOLID, width=250, bg="#333333")
        # self.left_panel.pack(side=LEFT, fill="y")

    def setup_menu(self):
        """
        Настройка меню
        Верхняя панель.
        """

        self.main_menu = Menu(tearoff=0)            # Основное меню
        self.file_tab = Menu(tearoff=0)             # Вкладка "Файл"
        self.editing_tab = Menu(tearoff=0)          # Вкладка "Правка"
        self.run_tab = Menu(tearoff=0)              # Вкладка "Выполнить"
        self.ref_tab = Menu(tearoff=0)              # Вкладка "Справка"

        # Настройка основного меню и привязка вкладок к подменю
        self.main_menu.add_cascade(label="Файл", menu=self.file_tab)
        self.main_menu.add_cascade(label="Правка", menu=self.editing_tab)
        self.main_menu.add_cascade(label="Выполнить", menu=self.run_tab)
        self.main_menu.add_cascade(label="Справка", menu=self.ref_tab)

        # Настройка вкладки "Файл"
        self.file_tab.add_cascade(label="Создать новое графическое поле", command=self.creating_new_graphic_field_menu)
        self.file_tab.add_separator()
        self.file_tab.add_cascade(label="Выход", command=exit)

        # Настройка вкладки "Правка"
        self.editing_tab.add_cascade(label="Отменить последнее действие")
        self.editing_tab.add_separator()
        self.editing_tab.add_cascade(label="Вырезать")
        self.editing_tab.add_cascade(label="Копировать")
        self.editing_tab.add_cascade(label="Вставить")
        self.editing_tab.add_separator()
        self.editing_tab.add_cascade(label="Найти")
        # Настройка вкладки "Выполнить"
        self.run_tab.add_cascade(label="Запустить код")
        self.run_tab.add_cascade(label="Запустить окно отладки")
        self.run_tab.add_cascade(label="Запустить отладку кода")

        # Настройка вкладки "Справка"
        self.ref_tab.add_cascade(label="О программе")
        self.config(menu=self.main_menu)

    def creating_new_graphic_field_menu(self):
        """
        Меню создания нового графического поля
        """

        # Настройка окна
        window = Toplevel()
        window.title("Создание графического поля")
        window.geometry("490x300+650+250")
        window.resizable(0, 0) 
        window.focus()
        
        # Настройка элементов
        
        # Поле "Имя графического поля: "
        ttk.Label(window, text="Имя графического поля: ").grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        gfield_name_entry = ttk.Entry(window, width=35)
        gfield_name_entry.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        
        # Поле "Описание (необязательно): "
        ttk.Label(window, text="Описание (необязательно): ").grid(row=1, column=0, padx=6, pady=6, sticky=EW)
        gfield_description_entry = ttk.Entry(window, width=50)
        gfield_description_entry.grid(row=1, column=1, padx=6, pady=6, sticky=EW)
        
        # Поле "Выберите стартовые ноды:"
        ttk.Label(window, text="Выберите стартовые ноды:").grid(row=2, column=0, padx=6, pady=6, sticky=EW)
        combobox = ttk.Combobox(window, values=self.node_template_list, height=7)
        combobox.grid(row=2, column=1, padx=6, pady=6, sticky=EW)
        
        listbox = Listbox(window, height=6)
        listbox.grid(row=3, column=0, padx=6, pady=6, sticky=EW, columnspan=2)
        
        def add_values(event): listbox.insert(0, combobox.get())
        def del_all_values(event): listbox.delete(0, listbox.size())
        def del_values(event):
            if not listbox.curselection():
                return
            listbox.delete(listbox.curselection()[0])
        

        button_frame = ttk.Frame(window)
        button_frame.grid(row=4, column=0, columnspan=2, sticky=EW, padx=6, pady=6)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        select_start_node_button = ttk.Button(button_frame, text="Добавить")
        select_start_node_button.grid(row=0, column=0, padx=6, pady=6, sticky=EW)
        select_start_node_button.bind("<Button-1>", add_values)
        
        delete_start_node_button = ttk.Button(button_frame, text="Удалить")
        delete_start_node_button.grid(row=0, column=1, padx=6, pady=6, sticky=EW)
        delete_start_node_button.bind("<Button-1>", del_values)

        delete_all_node_button = ttk.Button(button_frame, text="Удалить все")
        delete_all_node_button.grid(row=0, column=2, padx=6, pady=6, sticky=EW)
        delete_all_node_button.bind("<Button-1>", del_all_values)

        create_start_node_button = ttk.Button(button_frame, text="Создать")
        create_start_node_button.grid(row=1, column=0, padx=6, pady=6, sticky=EW,columnspan=3)
        create_start_node_button.bind("<Button-1>", del_values)
        