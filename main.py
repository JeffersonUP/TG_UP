import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Pestañas")

# Crear un Notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Crear el primer frame/pestaña
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text='Pestaña 1')

# Añadir contenido a la primera pestaña
label1 = tk.Label(frame1, text="Contenido de la Pestaña 1", font=("Arial", 20))
label1.pack(pady=20)

# Crear el segundo frame/pestaña
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text='Pestaña 2')

# Añadir contenido a la segunda pestaña
label2 = tk.Label(frame2, text="Contenido de la Pestaña 2", font=("Arial", 20))
label2.pack(pady=20)

# Crear el tercer frame/pestaña
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text='Pestaña 3')

# Añadir contenido a la tercera pestaña
label3 = tk.Label(frame3, text="Contenido de la Pestaña 3", font=("Arial", 20))
label3.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
