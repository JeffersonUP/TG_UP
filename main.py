import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import funciones as fn
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Pestañas")
        # Crear un Notebook (pestañas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.geometry("980x600")
        self.resizable(False, False)
        # Variables para almacenar datos
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.lista_equipos = []
        self.codigo_cambio = 0
        self.lista_switches = []
        self.vlan = 0

        # Crear las pestañas
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        #self.generate_textboxes()
    def create_tab1(self):
        frame1 = tk.Frame(self.notebook)
        self.notebook.add(frame1, text='Configuración')

        #Columna 1
        frame_columna1 = tk.Frame(frame1)
        frame_columna1.grid(row=0, column=0, sticky="nsew")

        self.texto_buscar = tk.Text(frame_columna1, width=10, wrap="word")
        self.texto_buscar.grid(row=0, column=0, sticky="nsew")

        scroll_buscar = tk.Scrollbar(frame_columna1, orient="vertical", command=self.texto_buscar.yview)
        scroll_buscar.grid(row=0, column=1, sticky="ns")
        self.texto_buscar.config(yscrollcommand=scroll_buscar.set)

        boton_buscar = tkinter.Button(frame_columna1, text="Buscar", command=self.accion_btn_buscar)
        boton_buscar.grid(row=1, column=0, sticky="ew")

        frame1.grid_rowconfigure(0, weight=1)
        frame_columna1.grid_rowconfigure(0, weight=1)

        #Columna 2
        frame_columna2 = tk.Frame(frame1, width=60)
        frame_columna2.grid(row=0, column=1, sticky="nsew")

        self.label_informacion = tk.Label(frame_columna2, text="\nEquipos:\t__ \n\n"
                                                            "no encontrados:\t__\n\n"
                                                            "total switches:\t__ \n", relief="raised")
        self.label_informacion.grid(row=0, column=0, padx=3, pady=1, sticky="nsew")

        frame_botones = tk.Frame(frame_columna2, borderwidth=1, relief="solid")
        frame_botones.grid(row=1, column=0, padx=3, pady=7, sticky="ew")

        boton_op1 = tk.Button(frame_botones, text="Cambiar VLAN", command=self.accion_btn_1)
        boton_op1.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.combobox = ttk.Combobox(frame_botones, values=fn.listar_vlans(), width=3, state='readonly')
        self.combobox.grid(row=0, column=1, padx=3, pady=3)
        boton_op2 = tk.Button(frame_botones, text="Actualizar PortSecurity ", command=self.accion_btn_2)
        boton_op2.grid(row=1, column=0, padx=3, pady=3, sticky="ew", columnspan=2)

        boton_op3 = tk.Button(frame_botones, text="Aplicar Cisco ISE", command=self.accion_btn_3)
        boton_op3.grid(row=2, column=0, padx=3, pady=3, sticky="ew", columnspan=2)

        frame_botones.grid_columnconfigure(0, weight=1)

        #Columna 3
        frame_columna3 = tk.Frame(frame1)
        frame_columna3.grid(row=0, column=2, sticky="nsew")

        # Frame para las cajas de texto generadas y el scrollbar
        self.textbox_frame = tk.Frame(frame_columna3)
        self.textbox_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(self.textbox_frame)
        self.scrollbar = ttk.Scrollbar(self.textbox_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame1.grid_columnconfigure(2, weight=1)
        frame_columna3.grid_rowconfigure(0, weight=1)
        frame_columna3.grid_columnconfigure(0, weight=1)
    def create_tab2(self):
        frame2 = ttk.Frame(self.notebook)
        self.notebook.add(frame2, text='Pestaña 2')

        label2 = tk.Label(frame2, text="Contenido de la Pestaña 2", font=("Arial", 20))
        label2.pack(padx=5,pady=20)

        entry2 = tk.Entry(frame2, textvariable=self.var2)
        entry2.pack(padx=5,pady=10)

        button2 = tk.Button(frame2, text="Guardar", command=self.save_var2)
        button2.pack(padx=5,pady=10)

        self.result_label2 = tk.Label(frame2, text="", font=("Arial", 20))
        self.result_label2.pack(padx=5, pady=10)

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

    def accion_btn_buscar(self):

        texto = self.texto_buscar.get("1.0", tk.END).strip()
        if texto:
            lineas_texto = texto.split('\n')
            self.var1, self.var2 = fn.validar_listado(lineas_texto)
            print(self.var1)
            self.actualizar_texto_buscar()
            self.generate_textboxes()
            self.label_informacion.config(text=f"\nTotal Equipos:\t{len(self.var1)} \n\n"
                                          f"Total Switches:\t{len(self.lista_switches)}\n\n"
                                          f"No encontrados:\t{len(self.var2)}\n")
        else:
            messagebox.showwarning("Entrada vacía", "Por favor, ingrese algún texto antes de registrar.")


    def actualizar_texto_buscar(self):
        self.codigo_cambio = 0
        no_encontrados=""
        for elemento in self.var2:
            no_encontrados += f"{elemento}\n"
        self.lista_switches, self.lista_rangos, self.lista_equipos = fn.generar_rangos(self.var1)
        print(self.lista_equipos)
        self.texto_buscar.delete('1.0', tk.END)
        self.texto_buscar.insert(tk.END, no_encontrados)
    def accion_btn_1(self):
        if self.combobox.get() != "":
            self.vlan = int(self.combobox.get())
            self.codigo_cambio = 1
            self.generate_textboxes()
    
    def accion_btn_2(self):
        self.codigo_cambio = 2
        self.generate_textboxes()

    def accion_btn_3(self):
        self.codigo_cambio = 3
        self.generate_textboxes()

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

    def generate_textboxes(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            count = int(len(self.lista_switches))
        except ValueError:
            count = 0

        for i in range(count):
            row_frame = tk.Frame(self.scrollable_frame)
            texto = fn.escribir_script(self.lista_rangos[i], self.codigo_cambio, self.vlan)
            num_lineas = texto.count('\n')
            row_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
            titulo = tk.Label(row_frame, text=self.lista_switches[i])
            titulo.grid(row=0, column=0, columnspan=2, padx=3, pady=1, sticky="w")
            entry = tk.Text(row_frame, wrap=tk.WORD, height=num_lineas+1)
            entry.insert(tk.END, texto)
            entry.configure(state='disabled')
            entry.grid(row=1, column=0, rowspan=2, sticky="ew")

            button = tk.Button(row_frame, text="Copiar", command=lambda e=entry: self.copiar_contenido(e))
            button.grid(row=1, column=1, padx=5, sticky="nsew")

            button2 = tk.Button(row_frame, text="guardar", command=lambda index=i: self.guardar_cambios(index))
            button2.grid(row=2, column=1, padx=5, sticky="nsew")
    def copiar_contenido(self,texto):
        self.clipboard_clear()
        self.clipboard_append(texto.get("1.0", tk.END))
        self.update()
    def guardar_cambios(self, index):
        print(f"cambios en switch {index} realizados\n")
        print(self.lista_equipos[index])
if __name__ == "__main__":
    app = App()
    app.mainloop()
