import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Pestañas")

        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Variables para almacenar datos
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()

        # Crear las pestañas
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

    def create_tab1(self):
        frame1 = ttk.Frame(self.notebook)
        self.notebook.add(frame1, text='Pestaña 1')

        label1 = tk.Label(frame1, text="Contenido de la Pestaña 1", font=("Arial", 20))
        label1.pack(pady=20)

        entry1 = tk.Entry(frame1, textvariable=self.var1)
        entry1.pack(pady=10)

        button1 = tk.Button(frame1, text="Guardar", command=self.save_var1)
        button1.pack(pady=10)

        self.result_label1 = tk.Label(frame1, text="", font=("Arial", 20))
        self.result_label1.pack(pady=10)

    def create_tab2(self):
        frame2 = ttk.Frame(self.notebook)
        self.notebook.add(frame2, text='Pestaña 2')

        label2 = tk.Label(frame2, text="Contenido de la Pestaña 2", font=("Arial", 20))
        label2.pack(pady=20)

        entry2 = tk.Entry(frame2, textvariable=self.var2)
        entry2.pack(pady=10)

        button2 = tk.Button(frame2, text="Guardar", command=self.save_var2)
        button2.pack(pady=10)

        self.result_label2 = tk.Label(frame2, text="", font=("Arial", 20))
        self.result_label2.pack(pady=10)

    def create_tab3(self):
        frame3 = ttk.Frame(self.notebook)
        self.notebook.add(frame3, text='Pestaña 3')

        label3 = tk.Label(frame3, text="Contenido de la Pestaña 3", font=("Arial", 20))
        label3.pack(pady=20)

        entry3 = tk.Entry(frame3, textvariable=self.var3)
        entry3.pack(pady=10)

        button3 = tk.Button(frame3, text="Guardar", command=self.save_var3)
        button3.pack(pady=10)

        self.result_label3 = tk.Label(frame3, text="", font=("Arial", 20))
        self.result_label3.pack(pady=10)

    def save_var1(self):
        value = self.var1.get()
        self.result_label1.config(text=value)

    def save_var2(self):
        value = self.var2.get()
        self.result_label2.config(text=value)

    def save_var3(self):
        value = self.var3.get()
        self.result_label3.config(text=value)


if __name__ == "__main__":
    app = App()
    app.mainloop()
