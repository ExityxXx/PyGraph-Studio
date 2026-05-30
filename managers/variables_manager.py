from tkinter import *
from tkinter import ttk
from variable import PGSVariable
from tkinter.messagebox import showwarning
from tkinter.messagebox import askyesno
class VariablesManager:
    def __init__(self, parent):
        self.parent = parent
    
    def open(self):
        def select(event=None):
            if self.parent.variables_counter == 0:
                return
            selection = table_view.selection()
            if selection:
                item = table_view.item(selection, "values")
                for id, widget in enumerate([var_name, var_type, var_value]):
                    widget.set(str(item[id]))
                var_name_entry.config(state="enabled")
                var_type_combobox.config(state="readonly")
                var_value_entry.config(state="enabled")
        def create_variable():
            table_view.insert("", "end", values=(generate_name(), "Автоматически", 0, self.parent.variables_counter))
            self.parent.struct.add_variable(self.parent.variables_counter, PGSVariable(generate_name(), "auto_type", 0))
            self.parent.variables_counter += 1
            
        def delete_selected():
            if self.parent.variables_counter == 0:
                return
            
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[3])
            table_view.delete(selected)
            self.parent.struct.remove_variable(selected_item_id)
            input_field_block()
            self.parent.variables_counter -= 1

            refrash_table()    
        def delete_all():
            if self.parent.variables_counter == 0:
                return
            answer = askyesno(title="Подтверждение", message="Вы точно хотите удалить все переменные?\nЭто необратимое действие и может повлечь за собой поломку всей программы.")
            if not answer:
                return
            
            for item in table_view.get_children():
                table_view.delete(item)
            
            self.parent.struct.remove_all_variables()
            input_field_block()
            self.parent.variables_counter = 0
        def refrash_table():
            if self.parent.variables_counter == 0:
                return
            
            for item in table_view.get_children():
                table_view.delete(item)

            for id, item in enumerate(self.parent.struct.get_variables().values()):
                type_ = "Автоматически" if item.get_type() == "auto_type" else item.get_type()
                table_view.insert("", "end", \
                    values=(item.get_name(), type_, item.get_value(), id))
        def start_draw():
            for id, item in enumerate(self.parent.struct.get_variables().values()):
                type_ = "Автоматически" if item.get_type() == "auto_type" else item.get_type()
                table_view.insert("", "end", \
                    values=(item.get_name(), type_, item.get_value(), id))
        def save_changes():
            if self.parent.variables_counter == 0:
                return
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[3])
            target_item = self.parent.struct.get_variable(selected_item_id)
            if var_name.get() and var_type.get() and var_value.get():
                table_view.item(selected, values=(var_name.get(), var_type.get(), var_value.get(), selected_item_id))
                target_item.name = var_name.get()
                target_item.type = var_type.get()
                target_item.value = var_value.get()

        def generate_name():
            candidate = f"Variable_{self.parent.variables_counter}"
            temp_vars_names : list[str] = []
            for existing in self.parent.struct.get_variables().values():
                temp_vars_names.append(existing.get_name())
            
            if candidate in temp_vars_names:
                showwarning("Предупреждение", "Переменная с таким именем уже существует")
                return f"Variable_000{self.parent.variables_counter}"
            
            return candidate       
        def cancel_choice():
            selection = table_view.selection()
            if selection:
                table_view.selection_remove(selection)
                input_field_block()
        def input_field_block():
            var_name.set("")
            var_type.set("")
            var_value.set("")
            var_name_entry.config(state="disabled")
            var_type_combobox.config(state="disabled")
            var_value_entry.config(state="disabled")
            
        window = Toplevel(self.parent)
        window.geometry(f"850x505+500+300")
        window.title(f"Менеджер переменных")
        window.focus()
        window.grab_set()
        window.transient(self.parent)
        window.resizable(0, 0)
        window.configure(bg="#2b2b2b")

        toolbar_frame = Frame(window, height=50, bg="#3a3a3a")
        toolbar_frame.pack(fill="x")
        toolbar_frame.pack_propagate(False)
        
        Button(toolbar_frame, text="+ Добавить переменную",
               bg="#4a6a8a", fg="white", padx=10, cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=create_variable).pack(side=LEFT, padx=(6, 2))
        
        Button(toolbar_frame, text="🗑 Удалить выбранное",
               bg="#6a3a3a", fg="white", padx=10, cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=delete_selected).pack(side=LEFT, padx=2)
        
        Button(toolbar_frame, text="🗑 Удалить все",
               bg="#6a3a3a", fg="white", padx=10, cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=delete_all).pack(side=LEFT, padx=2)

        Label(toolbar_frame, text="Управление глобальными переменными", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(side=RIGHT, padx=10)
        
        # name - Имя
        # type - Тип
        # value - Значение
        columns = ("name", "type", "value", "id")
        types = ["Автоматически", "int", "float", "bool", "str", "list", "dict", "set", "class"]
        scopes = ["Глобальная (проект)", "Локальное (граф)"]
        table_frame = Frame(window, width=250, relief="raised")
        table_frame.pack(expand=1, fill="both", padx=6, pady=6, side="left", anchor="nw")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        table_view = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=table_view.yview)
        table_view.pack(expand=1, fill="both")
        table_view.heading("name", text="Имя переменной")
        table_view.heading("type", text="Тип")
        table_view.heading("value", text="Значение")
        table_view.heading("id", text="ID")
        table_view.column("name", width=125)
        table_view.column("type", width=65)
        table_view.column("value", width=90)
        table_view.column("id", width=0, minwidth=0, stretch=False)
        table_view.bind("<<TreeviewSelect>>", select)
        
        # options
        options_panel_frame = Frame(window, relief="raised", bd=1, bg="#3a3a3a")
        options_panel_frame.pack(expand=1, fill="both", padx=6, pady=6, side="right")
        Label(options_panel_frame, text="Свойства", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(anchor=W, padx=10, pady=(5, 0))
        
        options_elements_frame = Frame(options_panel_frame, bg="#3a3a3a", bd=1)
        options_elements_frame.pack(expand=1, fill="both", padx=6, pady=(6, 0))
        options_elements_frame.grid_propagate(False)
        options_elements_frame.columnconfigure(0, weight=0)
        options_elements_frame.columnconfigure(1, weight=1)

        # Строка 1
        row1 = Frame(options_elements_frame, bg="#3a3a3a")
        row1.grid(row=0, column=0, sticky="ew", columnspan=2)
        row1.columnconfigure(1, weight=1)
        Label(row1, text="Имя переменной: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        
        var_name = StringVar()
        var_name_entry = ttk.Entry(row1, textvariable=var_name, state="disabled")
        var_name_entry.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

        # Строка 2
        row2 = Frame(options_elements_frame, bg="#3a3a3a")
        row2.grid(row=1, column=0, sticky="ew", columnspan=2)
        row2.columnconfigure(1, weight=1)
        Label(row2, text="Тип: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        
        var_type = StringVar()
        var_type_combobox = ttk.Combobox(row2, values=types, state="disabled", textvariable=var_type)
        var_type_combobox.grid(row=0, column=1, padx=4, pady=2, sticky="ew")
        
        # Строка 3
        row3 = Frame(options_elements_frame, bg="#3a3a3a")
        row3.grid(row=2, column=0, sticky="ew", columnspan=2)
        row3.columnconfigure(1, weight=1)
        Label(row3, text="Значение: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        
        var_value = StringVar()
        var_value_entry = ttk.Entry(row3, textvariable=var_value, state="disabled")
        var_value_entry.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

        # Конечные кнопки
        Button(options_panel_frame, text="Сохранить",
               bd=1, bg="#516a3a", fg="white",
               font=("Segoe UI", 9, "bold"), cursor="hand2", command=save_changes).\
            pack(padx=6, pady=0,  fill="x")
        Button(options_panel_frame, text="Отменить выбор",
               bd=1, bg="#696a3a", fg="white",
               font=("Segoe UI", 9, "bold"), cursor="hand2", command=cancel_choice).\
            pack(padx=6, pady=(4, 6),  fill="x")
        start_draw()
