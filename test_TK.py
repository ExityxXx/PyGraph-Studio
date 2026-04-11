import tkinter as tk
from tkinter import ttk
from tkinter import *

root = tk.Tk()
root.title("Растягиваемая боковая панель")
root.geometry("600x400")

# 1. Создаем PanedWindow (горизонтальное разделение)
paned_window = ttk.PanedWindow(root, orient="horizontal")
paned_window.pack(fill="both", expand=True)

# 2. Боковая панель (левая)
sidebar = Frame(paned_window, width=150, bg="#2b2b2b")
# Добавляем виджеты на боковую панель
label_side = ttk.Label(sidebar, text="Меню", padding=10)
label_side.pack()
button1 = ttk.Button(sidebar, text="Кнопка 1")
button1.pack(pady=5)

# 3. Основная панель (правая)
main_area = Frame(paned_window, bg="#666666")
label_main = ttk.Label(main_area, text="Основной контент")
label_main.pack()

# 4. Добавляем панели в PanedWindow
paned_window.add(sidebar, weight=0) # weight=0 - не растягивать панель при увеличении окна
paned_window.add(main_area, weight=1) # weight=1 - растягивать основную область

root.mainloop()
