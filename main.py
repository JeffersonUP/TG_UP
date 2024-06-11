import tkinter
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Pestañas")
        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.geometry("760x400")

        # Variables para almacenar datos
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()

        # Crear las pestañas
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
    def create_tab1(self):
        frame1 = tk.Frame(self.notebook)
        self.notebook.add(frame1, text='Configuración')

        #Columna 1
        frame_columna1 = tk.Frame(frame1)
        frame_columna1.grid(row=0, column=0, sticky="nsew")

        texto_buscar = tk.Text(frame_columna1, width=10, wrap="word")
        texto_buscar.grid(row=0, column=0, sticky="nsew")

        scroll_buscar = tk.Scrollbar(frame_columna1, orient="vertical", command=texto_buscar.yview)
        scroll_buscar.grid(row=0, column=1, sticky="ns")
        texto_buscar.config(yscrollcommand=scroll_buscar.set)

        boton_buscar = tkinter.Button(frame_columna1, text="Buscar", command=self.frame1_buscar)
        boton_buscar.grid(row=1, column=0, sticky="ew")

        frame1.grid_rowconfigure(0, weight=1)
        frame_columna1.grid_rowconfigure(0, weight=1)

        #Columna 2
        frame_columna2 = tk.Frame(frame1)
        frame_columna2.grid(row=0, column=1, sticky="nsew")

        label_informacion = tk.Label(frame_columna2, text="\nEquipos consultados: \n\nEquipos no encontrados:\n\nSwitches involucrados:\n", relief="raised")
        label_informacion.grid(row=0, column=0, pady=1, sticky="nsew")

        frame_botones = tk.Frame(frame_columna2, borderwidth=1, relief="solid")
        frame_botones.grid(row=1, column=0, pady=7, sticky="ew")

        boton_op1 = tk.Button(frame_botones, text="Cambiar VLAN", command=self.frame1_boton1())
        boton_op1.grid(row=0, column=0, padx=1, pady=1, sticky="ew")

        boton_op2 = tk.Button(frame_botones, text="Actualizar PortSecurity ", command=self.frame1_boton2())
        boton_op2.grid(row=1, column=0, padx=1, pady=1, sticky="ew")
        frame_botones.grid_columnconfigure(0, weight=1)
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

    def frame1_buscar(self):
        print("Buscar presionado")
    def frame1_boton1(self):
        print("test")

    def frame1_boton2(self):
        print("test")

    def frame1_boton3(self):
        print("test")

    def frame1_boton4(self):
        print("test")

    def frame1_boton5(self):
        print("test")

    def frame1_boton6(self):
        print("test")

    def frame1_boton7(self):
        print("test")
    def save_var2(self):
        value = self.var2.get()
        self.result_label2.config(text=value)

    def save_var3(self):
        value = self.var3.get()
        self.result_label3.config(text=value)


if __name__ == "__main__":
    app = App()
    app.mainloop()
