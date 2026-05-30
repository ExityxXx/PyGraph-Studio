from tkinter import *
from tkinter import ttk
from gfield import Gfield
from node.node import Node
from variable import PGSVariable
import sys
import io
class DebuggerInterface:
    def __init__(self, parent):
        self.parent = parent
    
    def developer_debug(self):
        """
        Меню отладки
        """
        # Генерация отладочного контента
        items_count = self.parent.struct.items_length()
        items : dict = self.parent.struct.get_items()
        generated_result = "Отсутствуют графические поля для отладки"
        current_item = None
        if items:
            current_tab_index = self.parent.notebook.index(self.parent.notebook.select())
            current_item = self.parent.struct.get_item(current_tab_index)["data"]
            generated_result = f"Общее количество: {items_count}\n" \
                               f"Текущий объект: \"{current_item.get_name()}\"\n" \
                               f"Кол-во полей: {self.parent.gfields_counter}\n" \
                               f"Кол-во редакторов кода: {self.parent.code_places_counter}\n"

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

        if self.parent.struct.items_length() > 0:
            current_tab_index = self.parent.notebook.index(self.parent.notebook.select())
            current_item = self.parent.struct.get_item(current_tab_index)

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
        
    def debug_variables(self):
        """
        Меню отладки переменных
        """

        generated_result = "Отсутствуют переменные для отладки\nДобавить их можно в менеджере переменных"

        if self.parent.variables_counter > 0:
            for id, variable in enumerate(self.parent.struct.get_variables().values()):
                generated_result += \
                    f"Переменная №{id}:\n" \
                    f"    Имя: {variable.get_name()}\n" \
                    f"    Тип: {variable.get_type()}\n" \
                    f"    Значение: {variable.get_value()}\n"
                generated_result += "\n"

        # Настройка окна
        window = Toplevel()
        window.title("Отладка переменных")
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
    
    def compile_and_run(self):
        """
        Меню отладки переменных
        """
        if not self.parent.gfields_counter:
            return
        
        gfield : Gfield = self.parent.get_current_gfield()
        start_node : Node = gfield.get_nodes()[0]
        variables : dict[int, PGSVariable] = self.parent.struct.get_variables()

        if not start_node.output_node:
            start_node = None
        
        generated_result = f"# Graph \"{gfield.get_name()}\"\n"
        if gfield.get_description():
            generated_result += f"# \"{gfield.get_description()}\"\n"    
        
        for variable in variables.values():
            generated_result += f"{variable.get_name()} = {variable.get_value()}\n"

        while start_node is not None:
            generated_result += f"# Node {start_node.header}\n"
            generated_result += f"{start_node.generate_code()}\n\n"
            start_node = start_node.output_node if start_node.output_node else None

        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()

        exec(generated_result)

        sys.stdout = old_stdout
        final_result = buffer.getvalue().strip()

        # Настройка окна
        window = Toplevel()
        window.title("Компиляция и выполнение кода")
        window.geometry("690x550+650+250")
        window.resizable(1, 0)
        window.focus()

        # Размещение центрального текста
        text = Text(window, bg="#404040", fg="#00D10A", font=("Courier New", 12))
        text.pack(padx=8, pady=8, fill=X)
        # text.insert("1.0", str(generated_result))
        text.insert("1.0", str(final_result))

        # Кнопка очистки
        clear_button = ttk.Button(window, text="Очистить", command=lambda : text.delete("1.0", END))
        clear_button.pack(padx=8, pady=8)
    
    def debug_connections(self):
        if not self.parent.gfields_counter:
            return
        
        gfield : Gfield = self.parent.get_current_gfield()
        start_node : Node = gfield.get_nodes()[0]
        # Настройка окна
        window = Toplevel()
        window.title("Отладка связей в текущем графе")
        window.geometry("690x550+650+250")
        window.resizable(1, 0)
        window.focus()
        generated_result = ""
        i = 0
        while start_node is not None:
            if i > 0 and not start_node.output_node: break
            generated_result += f"\nПроход #{i+1}\n"
            generated_result += f"{start_node}"
            if start_node.output_node:
                generated_result += f"\n    Связана с\n{start_node.output_node}"
            start_node = start_node.output_node if start_node.output_node else None
            i += 1

        # Размещение центрального текста
        text = Text(window, bg="#404040", fg="#00D10A", font=("Courier New", 12))
        text.pack(padx=8, pady=8, fill=X)
        text.insert("1.0", str(generated_result))

        # Кнопка очистки
        clear_button = ttk.Button(window, text="Очистить", command=lambda: text.delete("1.0", END))
        clear_button.pack(padx=8, pady=8)
    
    def debug_data_connections(self):
        if not self.parent.gfields_counter:
            return
        
        gfield : Gfield = self.parent.get_current_gfield()
        nodes = gfield.get_nodes()
        
        # Настройка окна
        window = Toplevel()
        window.title("Отладка ДАТА-связей в текущем графе")
        window.geometry("690x550+650+250")
        window.resizable(1, 0)
        window.focus()
        
        generated_result = ""
        
        # Проходим по ВСЕМ узлам, чтобы найти начала дата-цепочек
        for node in nodes.values():
            # Если у узла есть data_output_node, он не является началом цепочки
            # Ищем узел, у которого нет data_input_node (начало цепочки)
            has_incoming_data = hasattr(node, 'data_input_node') and node.data_input_node is not None
            if has_incoming_data:
                continue
                
            # Это начало дата-цепочки
            current_node = node
            chain_length = 0
            chain_result = f"\n{'='*50}\n"
            chain_result += f"Цепочка дата-связей (начало: {node.header}):\n"
            chain_result += f"{'='*50}\n"
            
            while current_node is not None:
                chain_length += 1
                chain_result += f"\n[{chain_length}] {current_node}\n"
                
                # Показываем значение, если есть
                if hasattr(current_node, 'get_data'):
                    chain_result += f"     Данные: {current_node.get_data()}\n"
                elif hasattr(current_node, 'get_text'):
                    chain_result += f"     Данные: {current_node.get_text()}\n"
                
                # Показываем связи
                if hasattr(current_node, 'data_output_node') and current_node.data_output_node:
                    chain_result += f"     ↓ передаёт данные в\n"
                    chain_result += f"     {current_node.data_output_node}\n"
                else:
                    chain_result += f"     ↓ КОНЕЦ ЦЕПОЧКИ\n"
                
                current_node = current_node.data_output_node if hasattr(current_node, 'data_output_node') else None
            
            chain_result += f"\nДлина цепочки: {chain_length}\n"
            generated_result += chain_result
        
        # Если нет дата-связей вообще
        if not generated_result:
            generated_result = "Нет дата-связей в текущем графе.\n\n"
            generated_result += "Чтобы создать дата-связь:\n"
            generated_result += "1. Создайте узел 'Передать данные'\n"
            generated_result += "2. Создайте узел 'Функция print()'\n"
            generated_result += "3. Соедините выходной дата-порт (фиолетовый) с входным дата-портом"
        
        # Размещение текста
        from tkinter import Text
        text = Text(window, bg="#404040", fg="#00D10A", font=("Courier New", 10))
        text.pack(padx=8, pady=8, fill="both", expand=True)
        text.insert("1.0", generated_result)
        
        # Кнопка закрытия
        from tkinter import ttk
        close_button = ttk.Button(window, text="Закрыть", command=window.destroy)
        close_button.pack(padx=8, pady=8)
        