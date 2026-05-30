from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showwarning

class ProjectManager:
    def __init__(self, parent):
        self.parent = parent
        
    def create_new_project_menu(self) -> None:
        """
        Меню создания нового проекта
        """
        # Настройка окна
        window = Toplevel(self.parent)
        window.title("Создание проекта")
        window.geometry("490x200+650+250")
        window.resizable(0, 0)
        window.focus()
        window.transient(self.parent)
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
                self.parent.struct.set_struct_name(name)
                self.parent.struct.set_struct_desc(desc)
                window.destroy()
                self.parent.not_struct_data_label.destroy()
                self.parent.create_project_button.destroy()
                Label(self.parent.struct_panel, text=name,
                    font=("Arial", 13, "bold"), fg="#A8A8A8",
                    background="#1b1b1b", anchor="nw",
                    justify="left") \
                    .grid(row=1, column=0, padx=8, pady=4, sticky="nw")
                
                Label(self.parent.struct_panel, text=self.parent.struct.project_desc or "Без описания",
                    font=("Arial", 10), fg="#808080",
                    bg="#1b1b1b", anchor="w").grid(row=2, column=0, padx=8, pady=(0, 8), sticky="nw" \
                    "")
                self.parent.title(f"PyGraph Studio ({name})")
                self.parent.setup_toolbar()
                self.parent.update_structure_panel()

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
