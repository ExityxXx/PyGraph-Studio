from tkinter import *
from tkinter import ttk

class GraphsManager:
    def __init__(self, parent):
        self.parent = parent
    
    def open(self):
        def select(event=None):
            selection = table_view.selection()
            if selection:
                item = table_view.item(selection, "values")
                graph_name.set(str(item[1]))
                graph_desc.set(str(item[2]))
                graph_name_entry.config(state="enabled")
                graph_desc_entry.config(state="enabled")
        def create_gfield_at_table():
            temp_window = self.parent.creating_new_gfield_menu()
            self.parent.wait_window(temp_window)
            current_item = self.parent.struct.get_item(self.parent.gfields_counter - 1)
            if current_item["type"] == "gfield":
                table_view.insert("", "end", values=(self.parent.gfields_counter - 1,
                                                     current_item["data"].get_name(),
                                                     current_item["data"].get_description()))
        def save_changes():
            if self.parent.gfields_counter == 0:
                return
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[0])
            target_item = self.parent.struct.get_item(selected_item_id)
            if target_item["type"] == "gfield" and graph_name.get():
                table_view.item(selected, values=(selected_item_id, graph_name.get(), graph_desc.get()))
                target_item["data"].name = graph_name.get()
                target_item["data"].description = graph_desc.get()
                self.parent.notebook.tab(selected_item_id, text=f"📊 {graph_name.get()}")
        def delete_selected():
            if self.parent.items_counter == 0:
                return
            
            selected = table_view.selection()[0]
            selected_item_id = int(table_view.item(selected, "values")[0])
            table_view.delete(selected)
            self.parent.notebook.forget(selected_item_id)
            self.parent.struct.remove_item(selected_item_id)
            graph_name.set("")
            graph_desc.set("")
            graph_name_entry.config(state="disabled")
            graph_desc_entry.config(state="disabled")
            self.parent.items_counter -= 1
            self.parent.gfields_counter -= 1

            refrash_table()
            
            if self.parent.struct.items_length() == 0:
                self.parent.notebook.pack_forget()
                self.parent.config(bg="#2b2b2b")
        def delete_all_table():
            if self.parent.items_counter == 0:
                return
            
            for item in table_view.get_children():
                table_view.delete(item)
        def draw_table():
            if self.parent.items_counter == 0:
                return
            
            for id, item in self.parent.struct.get_items().items():
                if item["type"] == "gfield":
                    table_view.insert("", "end", \
                        values=(id, item["data"].get_name(), item["data"].get_description()))    
        def refrash_table():
            delete_all_table()
            draw_table()
        def cancel_choice():
            selection = table_view.selection()
            if selection:
                table_view.selection_remove(selection[0])
                input_field_block()
        def input_field_block():
            graph_name.set("")
            graph_desc.set("")
            graph_name_entry.config(state="disabled")
            graph_desc_entry.config(state="disabled")

        window = Toplevel(self.parent)
        window.geometry(f"850x505+500+300")
        window.title(f"Менеджер графических полей")
        window.focus()
        window.grab_set()
        window.transient(self.parent)
        window.resizable(0, 0)
        window.configure(bg="#2b2b2b")

        toolbar_frame = Frame(window, height=50, bg="#3a3a3a")
        toolbar_frame.pack(fill="x")
        toolbar_frame.pack_propagate(False)
        
        Button(toolbar_frame, text="+ Добавить графу",
               bg="#4a6a8a", fg="white", padx=10, cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=create_gfield_at_table).pack(side=LEFT, padx=(6, 2))
        
        Button(toolbar_frame, text="🗑 Удалить выбранное",
               bg="#6a3a3a", fg="white", padx=10, cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=delete_selected).pack(side=LEFT, padx=2)

        Label(toolbar_frame, text="Управление графическими полями", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(side=RIGHT, padx=10)
        
        # id - ID графического поля
        # name - Имя графического поля
        columns = ("id", "name", "description")
        table_frame = Frame(window, width=250, relief="raised")
        table_frame.pack(expand=1, fill="both", padx=6, pady=6, side="left", anchor="nw")
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        table_view = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=table_view.yview)
        table_view.pack(expand=1, fill="both")
        table_view.heading("id", text="ID графы")
        table_view.heading("name", text="Название")
        table_view.heading("description", text="Описание")
        table_view.column("id", width=85)
        table_view.bind("<<TreeviewSelect>>", select)

        # options
        options_panel_frame = Frame(window, relief="raised", bd=1, bg="#3a3a3a")
        options_panel_frame.pack(expand=1, fill="both", padx=6, pady=6, side="right")
        Label(options_panel_frame, text="Свойства", bg="#3a3a3a", 
              fg="#cccccc", font=("Segoe UI", 10, "bold")).pack(anchor=W, padx=10, pady=(5, 0))
        
        options_elements_frame = Frame(options_panel_frame, bg="#3a3a3a", bd=1)
        options_elements_frame.pack(expand=1, fill="both", padx=6, pady=(6, 0))
        options_elements_frame.pack_propagate(False)
        options_elements_frame.columnconfigure(0, weight=0)
        options_elements_frame.columnconfigure(1, weight=1)
        # Строка 1
        row1 = Frame(options_elements_frame, bg="#3a3a3a")
        row1.grid(row=0, column=0, sticky="ew", columnspan=2)
        row1.columnconfigure(1, weight=1)
        Label(row1, text="Название поля: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        
        graph_name = StringVar()
        graph_name_entry = ttk.Entry(row1, textvariable=graph_name, state="disabled")
        graph_name_entry.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

        # Строка 2
        row2 = Frame(options_elements_frame, bg="#3a3a3a")
        row2.grid(row=1, column=0, sticky="ew", columnspan=2)
        row2.columnconfigure(1, weight=1)
        Label(row2, text="Описание: ",
              font=("Segoe UI", 10), bg="#3a3a3a", fg="#cccccc").grid(row=0, column=0, padx=4, pady=2, sticky="nw")
        
        graph_desc = StringVar()
        graph_desc_entry = ttk.Entry(row2, textvariable=graph_desc, state="disabled")
        graph_desc_entry.grid(row=0, column=1, padx=4, pady=2, sticky="ew")

        Button(options_panel_frame, text="Сохранить",
               bd=1, bg="#516a3a", fg="white", cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=save_changes).\
            pack(padx=6, pady=0, side="top", fill="x")
        
        Button(options_panel_frame, text="Отменить выбор",
               bd=1, bg="#696a3a", fg="white", cursor="hand2",
               font=("Segoe UI", 9, "bold"), command=cancel_choice).\
            pack(padx=6, pady=(4, 6), side="top", fill="x")
        
        draw_table()