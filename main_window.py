from tkinter import *
from tkinter import ttk

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        
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
        self.file_tab.add_cascade(label="Создать новую графу", command=self.creating_new_graph_menu)
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

    def creating_new_graph_menu(self):
        """
        Меню создания новой графы
        """
        print("Вы нажали создать новую графу")
        self.notebook.pack(expand=1, fill=BOTH)
    
