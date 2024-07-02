import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import funciones as fn

import pandas as pd


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Controlador de redes")
        # Crear un Notebook (pestañas)
        self.style = ttk.Style(self)
        self.style.theme_create('custom_theme', parent='alt', settings={
            'TNotebook': {
                'configure': {
                    'tabmargins': [2, 5, 2, 0],  # márgenes del notebook
                    'background': '#E4E7F3',  # Fondo del Notebook
                }
            },
            'TNotebook.Tab': {
                'configure': {
                    'padding': [10, 5],  # padding de cada pestaña
                    'background': '#0BBBEF',  # color de fondo de las pestañas
                    'foreground': '#001A7B',  # color del texto de las pestañas
                    'font': ('Arial', 10, 'bold'),  # fuente del texto
                    'borderwidth': 1,  # ancho del borde
                    'relief': 'raised'  # estilo del borde
                },
                'map': {
                    'background': [('selected', '#001A7B'), ('active', '#D2D600')],
                    'foreground': [('selected', '#FFFFFF'), ('active', '#FFFFFF')],
                    'expand': [('selected', [1, 1, 1, 0])]  # expansión de la pestaña seleccionada
                }
            },
            'TFrame': {
                'configure': {
                    'background': '#001A7B',  # Fondo de los frames
                }
            },
            'TLabel': {
                'configure': {
                    'background': '#E4E7F3',  # Fondo de los labels
                    'foreground': '#001A7B',  # Color del texto de los labels
                    'font': ('Arial', 12, 'bold'),
                }
            },
            'TButton': {
                'configure': {
                    'background': '#8FB738',  # Fondo de los botones
                    'foreground': '#FFFFFF',  # Color del texto de los botones
                    'font': ('Arial', 12, 'bold'),  # Fuente del texto de los botones
                    'borderwidth': 1,
                    'relief': 'raised',
                    'anchor': 'center'
                },
                'map': {
                    'background': [('active', '#D2D600')],
                    'foreground': [('active', '#001A7B')]
                }
            },
            'TEntry': {
                'configure': {
                    'background': '#FFFFFF',  # Fondo de las entradas
                    'foreground': '#001A7B',  # Color del texto de las entradas
                }
            },
            'Treeview': {
                'configure': {
                    'font': ('Helvetica', 10),  # Fuente del texto de las celdas del Treeview
                    'background': '#E4E7F3',  # Fondo del Treeview
                    'foreground': '#001A7B',  # Color del texto de las celdas
                    'rowheight': 25,  # Altura de las filas
                    'fieldbackground': '#E4E7F3',  # Fondo de los campos
                },
                'map': {
                    'background': [('selected', '#001A7B')],
                    'foreground': [('selected', '#FFFFFF')],
                }
            },
            'Treeview.Heading': {
                'configure': {
                    'font': ('Helvetica', 14, 'bold'),  # Fuente del texto de los encabezados del Treeview
                    'background': '#0BBBEF',  # Fondo de los encabezados
                    'foreground': '#001A7B',  # Color del texto de los encabezados
                }
            },
        })
        self.style.theme_use('custom_theme')
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        self.geometry("1000x500")
        self.resizable(False, False)

        # Variables para almacenar datos
        self.lista_equipos = []
        self.codigo_cambio = 0
        self.lista_switches = []
        self.lista_interfaces = []
        self.vlan = 0
        self.vlan2 = 0
        self.opt_vlan = 0
        self.logo = tk.PhotoImage(file="imagen.png")
        self.logo2 = tk.PhotoImage(file="EMTELCOOO.png")
        # Crear las pestañas
        self.crearTab1()
        self.create_tab2()
        self.create_tab3()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # Establecer el ícono como la foto de la ventana principal
        self.iconphoto(True, self.logo)

    def crearTab1(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text='Configurar')

        #Columna 1

        tab1_col1 = ttk.Frame(tab1)
        tab1_col1.grid(row=0, column=0, sticky="nsew", padx=3, pady=6)

        self.buscar_tab1_txt = tk.Text(tab1_col1, width=10, wrap="word")
        self.buscar_tab1_txt.grid(row=0, column=0, sticky="nsew")

        buscar_tab1_scroll = tk.Scrollbar(tab1_col1, orient="vertical", command=self.buscar_tab1_txt.yview)
        buscar_tab1_scroll.grid(row=0, column=1, sticky="ns")

        self.buscar_tab1_txt.config(yscrollcommand=buscar_tab1_scroll.set)

        buscar_tab1_btn = ttk.Button(tab1_col1, text="Buscar", command=self.accion_buscar_tab1_btn)
        buscar_tab1_btn.grid(row=1, column=0, columnspan=2, sticky="ew")

        tab1.grid_rowconfigure(0, weight=1)
        tab1_col1.grid_rowconfigure(0, weight=1)

        #Columna 2

        tab1_col2 = ttk.Frame(tab1, width=60)
        tab1_col2.grid(row=0, column=1, sticky="nsew", padx=3, pady=6)

        informacion_tab1_frame = ttk.Frame(tab1_col2)
        informacion_tab1_frame.grid(row=0, column=0, padx=3, pady=1, sticky="nsew")

        label_description = tk.Label(informacion_tab1_frame, text=f"Total Equipos\nTotal Switches\n No encontrados",
                                     font=("Arial", 16), relief=tk.GROOVE)
        label_description.grid(row=0, column=0, padx=(3, 0), pady=1, sticky="ns")

        self.informacion_tab1_label = tk.Label(informacion_tab1_frame, text="__\n""__\n""__", font=("Arial", 16),
                                               width=3, relief=tk.GROOVE)
        self.informacion_tab1_label.grid(row=0, column=1, padx=(0, 3), pady=1, sticky="nsew")

        botones_tab1_frame = ttk.Frame(tab1_col2, borderwidth=1, relief="solid")
        botones_tab1_frame.grid(row=1, column=0, padx=3, pady=7, sticky="ew")

        txt_ops = ["Cambiar VLAN", "Actualizar PortSecurity", "Aplicar Cisco ISE","Aplicar vlan unica",
                   "Desactivar puerto", "Encender puerto", "Desactivar Sticky", "Encender Sticky", "ver status"]

        for i in range(9):
            cambios_tab1_btn = ttk.Button(botones_tab1_frame, text=txt_ops[i],
                                          command=lambda opt=i: self.accion_cambios_tab1_btn(opt))
            if i == 0:
                cambios_tab1_btn.grid(row=i, column=0, padx=3, pady=3, sticky="ew")
                self.vlans_tab1_combobox = ttk.Combobox(botones_tab1_frame, values=fn.listar_vlans(), width=4, state='readonly',
                                             font=("Arial", 16))
                self.vlans_tab1_combobox.grid(row=i, column=1, padx=3, pady=3)

            else:
                cambios_tab1_btn.grid(row=i, column=0, padx=3, pady=3, sticky="nsew", columnspan=2)

        imagen_tab1_frame = ttk.Frame(tab1_col2)
        imagen_tab1_frame.grid(row=2, column=0, sticky="ns")

        imagen_tab1_label = ttk.Label(imagen_tab1_frame, image=self.logo2)
        imagen_tab1_label.pack(pady=(0, 0), expand=True, fill="both")

        #Columna 3
        
        tab1_col3 = ttk.Frame(tab1)
        tab1_col3.grid(row=0, column=2, sticky="nsew", padx=3, pady=6)

        # Frame para las cajas de texto generadas y el scrollbar
        self.canvas_tab1_frame = ttk.Frame(tab1_col3)
        self.canvas_tab1_frame.grid(row=0, column=0, sticky="nsew")
        self.tab1_canvas = tk.Canvas(self.canvas_tab1_frame)
        self.tab1_canvas.config(bg="#E4E7F3")
        self.canvas_tab1_scroll = ttk.Scrollbar(self.canvas_tab1_frame, orient="vertical",
                                                command=self.tab1_canvas.yview)
        self.canvas_scroll_frame = ttk.Frame(self.tab1_canvas)

        self.canvas_scroll_frame.bind("<Configure>",
                                      lambda e: self.tab1_canvas.configure(scrollregion=self.tab1_canvas.bbox("all")))

        self.tab1_canvas.create_window((0, 0), window=self.canvas_scroll_frame, anchor="nw")
        self.tab1_canvas.configure(yscrollcommand=self.canvas_tab1_scroll.set)

        self.tab1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_tab1_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        tab1.grid_columnconfigure(2, weight=1)
        tab1_col3.grid_rowconfigure(0, weight=1)
        tab1_col3.grid_columnconfigure(0, weight=1)

    def create_tab2(self):
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text='VLANs')

        tab2_col1 = ttk.Frame(tab2)
        tab2_col1.grid(row=0, column=0, sticky="nsew", padx=3, pady=6)
        tab2_col1.grid_rowconfigure(0, minsize=180)

        frame_control = ttk.Frame(tab2_col1)
        frame_control.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        self.vlans_tab2_combobox = ttk.Combobox(frame_control, values=fn.listar_vlans_nombre(), state='readonly',
                                                font=("Arial", 10), width=28)
        self.vlans_tab2_combobox.grid(row=0, column=0, padx=10, pady=3, sticky="ew")

        frame_formulario = ttk.Frame(frame_control)
        frame_formulario.grid(row=2, column=0, padx=(3, 0), pady=5, sticky="ns")

        texlabel = ['Id VLAN', 'Descripcion', '# de equipos']
        info_label_txt = (f"--------------------------------------------------\nCodigo VLAN:\n\nNombre:\n\nDirección:"
                        f"\n\nMáscara:\n""--------------------------------------------------")

        self.info_vlan_label = tk.Label(frame_formulario,text=info_label_txt,font=("Arial", 10), relief=tk.GROOVE)
        self.info_vlan_label.grid(row=0, column=0, padx=(3, 0), pady=1)

        txt_vlans=["Buscar", "Editar vlan", "Eliminar vlan", "Añadir vlan"]
        for i in range(4):
            cambios_tab2_btn = ttk.Button(frame_control, text=txt_vlans[i],
                                          command=lambda opt=i: self.accion_cambios_tab2_btn(opt))
            if i == 0:
                cambios_tab2_btn.grid(row=i+1, column=0, padx=10, pady=5, sticky="nsew")
            else:
                cambios_tab2_btn.grid(row=i+2, column=0, padx=10, pady=5, sticky="nsew")


        imagen_tab2_frame = ttk.Frame(tab2_col1)
        imagen_tab2_frame.grid(row=1, column=0, sticky="ew", padx=1, pady=10)
        
        imagen_tab2_label = tk.Label(imagen_tab2_frame, image=self.logo2)
        imagen_tab2_label.grid(row=0, column=0, padx=(25, 0))

        self.tab2_col2 = ttk.Frame(tab2)
        self.tab2_col2.grid(row=0, column=1, sticky="nsew", padx=3, pady=6)
        self.generar_tabla_vlans()

    def create_tab3(self):
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text='Equipos')
        tab3_col1 = ttk.Frame(tab3)
        tab3_col1.grid(row=0, column=0, sticky="nsew", padx=3, pady=6)
        tab3_col1.grid_rowconfigure(0, minsize=180)
        frame_control = ttk.Frame(tab3_col1)
        frame_control.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        self.texto_equipo = ttk.Entry(frame_control, font=("Arial", 10), width=30)
        self.texto_equipo.grid(row=0, column=0, padx=10, pady=3, sticky="ew")
        buscar_vlan_tab2_btn = ttk.Button(frame_control, text="Buscar", command=self.accion_f3_boton1)
        buscar_vlan_tab2_btn.grid(row=1, column=0, padx=10, pady=3, sticky="ew")

        frame_formulario = ttk.Frame(frame_control)
        frame_formulario.grid(row=2, column=0, padx=(3, 0), pady=5, sticky="ns")

        texlabel = ['Id VLAN', 'Descripcion', '# de equipos']

        lbltext = (f"--------------------------------------------------\nHostname:\n\nCodigo puerto:\n\nVLAN:\n\n"
                   f"Portsecurity:\n\nISE:\n--------------------------------------------------")

        self.label_equipo = tk.Label(frame_formulario, text=lbltext, font=("Arial", 10), relief=tk.GROOVE)
        self.label_equipo.grid(row=0, column=0, padx=(3, 0), pady=1)

        boton_edit_ed = ttk.Button(frame_control, text="Editar Puerto", command=self.accion_f3_boton2)
        boton_edit_ed.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

        boton_delete_ed = ttk.Button(frame_control, text="Eliminar Equipo", command=self.accion_f3_boton3)
        boton_delete_ed.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")

        boton_add_ed = ttk.Button(frame_control, text="Añadir Equipo", command=self.accion_f3_boton4)
        boton_add_ed.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)

        imagen_tab3_frame = ttk.Frame(tab3_col1)
        imagen_tab3_frame.grid(row=1, column=0, sticky="ew", padx=1, pady=10)
        imagen_tab3_label = tk.Label(imagen_tab3_frame, image=self.logo2)
        imagen_tab3_label.grid(row=0, column=0, padx=(25, 0))

        self.frame_equipo = ttk.Frame(tab3)
        self.frame_equipo.grid(row=0, column=1, sticky="nsew", padx=3, pady=6)
        self.ubicacion_equipo = tk.Label(self.frame_equipo,
                                         text="PISO __ CUARTO __ SWITCH __ PUERTO __",
                                         bg='#E4E7F3',
                                         fg='#000000',
                                         font=("Neuer Weltschmerz", 12))

        self.ubicacion_equipo.grid(row=0, column=0, pady=(10, 3), sticky="w")
        self.running_conf_equipo = tk.Text(self.frame_equipo, wrap=tk.WORD, width=80, bg='#E4E7F3', fg='#000000',
                                           insertbackground='#2D2D2D', font=("Neuer Weltschmerz", 13))
        self.running_conf_equipo.insert(tk.END, "")
        self.running_conf_equipo.configure(state='disabled')
        self.running_conf_equipo.grid(row=1, column=0, sticky="ew", pady=3)

    def accion_buscar_tab1_btn(self):

        texto = self.buscar_tab1_txt.get("1.0", tk.END).strip()
        if texto:
            lineas_texto = texto.split('\n')
            lineas_texto = list(set(lineas_texto))
            self.var1, self.var2 = fn.validar_listado(lineas_texto)
            #print(self.var1)
            self.actualizar_buscar_tab1_txt()
            self.generate_textboxes()
            self.informacion_tab1_label.config(text=f"{len(self.var1)}\n"
                                                    f"{len(self.lista_switches)}\n"
                                                    f"{len(self.var2)}")
        else:
            messagebox.showwarning("Entrada vacía", "Por favor, ingrese algún texto antes de registrar.")

    def actualizar_buscar_tab1_txt(self):
        self.codigo_cambio = 8
        no_encontrados = ""
        for elemento in self.var2:
            no_encontrados += f"{elemento}\n"
        self.lista_switches, self.lista_rangos, self.lista_equipos, self.lista_interfaces = fn.generar_rangos(self.var1)
        #print("AQUI LA LISTA:",self.lista_equipos)
        self.buscar_tab1_txt.delete('1.0', tk.END)
        self.buscar_tab1_txt.insert(tk.END, no_encontrados)

    def accion_cambios_tab1_btn(self, opt):
        self.codigo_cambio = opt
        if opt == 0 and self.vlans_tab1_combobox.get() == "":
            return
        else:
            self.vlan = int(self.vlans_tab1_combobox.get())
            self.generate_textboxes()

    def accion_cambios_tab2_btn(self, opt):
        vlan = self.vlans_tab2_combobox.get().split(' ')[0]

        if opt == 0:
            print("")
        elif opt==1:
            print("")
        elif opt == 2:
            print("")
        elif opt == 3:
            print("")
        if vlan == "":
            self.vlan2 = 0
        else:
            self.vlan2 = int(vlan)
        self.actualizar_info_vlan()
        self.generar_tabla_vlans(self.vlan2)

    #editar vlan
    def accion_f2_boton2(self):
        vlan = self.vlans_tab2_combobox.get().split(' ')[0]
        if vlan == "":
            self.vlan2 = 0
            messagebox.showwarning("Alerta", "No has seleccionado una VLAN a editar")
        else:
            self.vlan2 = int(vlan)
            self.abrir_formulario(self.vlan2)
        #print(vlan)

    #eliminar vlan
    def accion_f2_boton3(self):
        vlan = self.vlans_tab2_combobox.get().split(' ')[0]
        if vlan == "":
            self.vlan2 = 0
            messagebox.showwarning("Alerta", "No has seleccionado una VLAN para eliminar")
        else:
            self.vlan2 = int(vlan)
            self.confirmar_eliminar()
        #print(vlan)
        # crear vlan

    def accion_f2_boton4(self):
        self.vlan2 = 0
        self.abrir_formulario(self.vlan2)

    def accion_f3_boton1(self):
        control, info = fn.buscar_equipo(self.texto_equipo.get())
        #print(control, info)
        if (control and info == 0) or not control:
            if self.texto_equipo.get() != '':
                messagebox.showwarning("Alerta", "No existe ese equipo")
            self.label_equipo.config(
                text=f"--------------------------------------------------\nHostname:\n\n"
                     f"Codigo puerto:\n\nVLAN:\n\nPortsecurity:\n\nISE:\n--------------------------------------------------")
            self.ubicacion_equipo.config(text="PISO __ CUARTO __ SWITCH __ PUERTO __")
            self.running_conf_equipo.configure(state='normal')
            self.running_conf_equipo.delete("1.0", tk.END)
            self.running_conf_equipo.configure(state='disabled')
        elif control and info != 0:
            self.label_equipo.config(
                text=f"--------------------------------------------------\nHostname:{info[0]}\n\n"
                     f"Codigo puerto:{info[1]}\n\nVLAN:{info[-3]}\n\nPortsecurity:{info[-2]}\n\nISE:{info[-1]}\n--------------------------------------------------")
            self.ubicacion_equipo.config(text=f"PISO {info[2]} CUARTO {info[3]} SWITCH {info[4]} PUERTO {info[5]}")
            texto = fn.generar_texto_equipo([info[-3], info[-2], info[-1]])
            self.running_conf_equipo.configure(state='normal')
            self.running_conf_equipo.delete("1.0", tk.END)
            self.running_conf_equipo.insert("1.0", texto)
            self.running_conf_equipo.configure(state='disabled')

    def accion_f3_boton2(self):

        control, info = fn.buscar_equipo(self.texto_equipo.get())
        if not control:
            messagebox.showwarning("Alerta", "No existe ese equipo")

        else:
            self.abrir_formulario2(self.texto_equipo.get(), info)
            #print(info)

    def accion_f3_boton3(self):
        control, info = fn.buscar_equipo(self.texto_equipo.get())
        if control and info != 0:
            self.confirmar_eliminar_equipo()
        else:
            messagebox.showwarning("Alerta", "No existe ese equipo")

    def confirmar_eliminar_equipo(self):
        self.ventana_eliminar = tk.Toplevel(self.notebook)
        # Crear etiquetas y campos de entrada
        ttk.Label(self.ventana_eliminar, text=f"Estás seguro de eliminar el equipo"
                                              f" {self.texto_equipo.get()}?").grid(row=0, column=0, padx=10, pady=5,
                                                                                   sticky="ew")
        btn_confirmar = ttk.Button(self.ventana_eliminar, text=" Eliminar ", command=self.eliminar_equipo)
        btn_confirmar.grid(row=1, column=0, padx=5, pady=5)

        width = 360
        height = 75

        screen_width = self.ventana_eliminar.winfo_screenwidth()
        screen_height = self.ventana_eliminar.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.ventana_eliminar.geometry(f"{width}x{height}+{x}+{y}")

        self.ventana_eliminar.transient(self.notebook)
        self.ventana_eliminar.grab_set()
        self.ventana_eliminar.wait_window()

    def eliminar_equipo(self):

        fn.eliminar_pc(self.texto_equipo.get())
        messagebox.showinfo("Cambio realizado", f"Se eliminó el equipo {self.texto_equipo.get()}")
        self.ventana_eliminar.destroy()
        self.texto_equipo.delete(0, tk.END)
        self.texto_equipo.insert(0, "")
        self.accion_f3_boton1()

    def accion_f3_boton4(self):
        self.abrir_formulario2("", 0)

    def abrir_formulario2(self, edit, info):
        self.ventana_equipo = tk.Toplevel(self.notebook)

        # Crear etiquetas y campos de entrada
        ttk.Label(self.ventana_equipo, text="Hostname: \n\nCod Puerto:").grid(row=0, pady=5, rowspan=2)
        self.hostname_entry = ttk.Entry(self.ventana_equipo, width=30)
        self.hostname_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.codigo_entry = ttk.Entry(self.ventana_equipo, width=30)
        self.codigo_entry.grid(row=1, column=1, padx=5, pady=5)

        if edit != "":
            self.ventana_equipo.title("Editar Puerto")
            self.hostname_entry.insert(0, f"{edit}")
            self.hostname_entry.config(foreground="red", state="disabled")
            self.codigo_entry.insert(0, f"{info[1]}")
            boton_guardar = ttk.Button(self.ventana_equipo, text="Guardar cambios", command=self.validar_codigo)
        else:
            self.ventana_equipo.title("Añadir equipo")
            boton_guardar = ttk.Button(self.ventana_equipo, text="añadir equipo", command=self.validar_nuevo_equipo)
        boton_guardar.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        width = 300
        height = 120
        screen_width = self.ventana_equipo.winfo_screenwidth()
        screen_height = self.ventana_equipo.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.ventana_equipo.geometry(f"{width}x{height}+{x}+{y}")

        self.ventana_equipo.transient(self.notebook)
        self.ventana_equipo.grab_set()
        self.ventana_equipo.wait_window()

    def validar_nuevo_equipo(self):
        control, info = fn.buscar_equipo(self.hostname_entry.get())
        if control:
            if info == 0:
                messagebox.showwarning("Alerta", "Formato de Hostname inválido")
            else:
                messagebox.showwarning("Alerta", "Este Equipo ya existe")
        else:
            control, info = fn.desglosarUbicacion(self.codigo_entry.get())
            if not control:
                if info == 0:
                    messagebox.showwarning("Alerta", "El Codigo coincide con otro equipo")
                elif info == 1:
                    messagebox.showwarning("Alerta", "Formato de codigo inválido")
            else:
                fn.agregar_equipo(self.hostname_entry.get(), self.codigo_entry.get(), info)
                self.texto_equipo.delete(0, tk.END)
                # Inserta el nuevo texto en el Entry
                self.texto_equipo.insert(0, self.hostname_entry.get())
                self.accion_f3_boton1()
                messagebox.showinfo("Cambio realizado", f"Se Creó el nuevo equipo")
            self.ventana_equipo.destroy()

    def validar_codigo(self):
        control, info = fn.desglosarUbicacion(self.codigo_entry.get())
        if not control:
            if info == 0:
                messagebox.showwarning("Alerta", "El Codigo coincide con otro equipo")
            elif info == 1:
                messagebox.showwarning("Alerta", "Formato de codigo inválido")
        else:
            fn.editar_Equipo(self.hostname_entry.get(), self.codigo_entry.get(), info)
            self.accion_f3_boton1()
            messagebox.showinfo("Cambio realizado", f"Se modificó la ubicación del equipo")
        self.ventana_equipo.destroy()

    def generate_textboxes(self):
        for widget in self.canvas_scroll_frame.winfo_children():
            widget.destroy()
        try:
            count = int(len(self.lista_switches))
        except ValueError:
            count = 0

        for i in range(count):
            row_frame = ttk.Frame(self.canvas_scroll_frame)
            texto = fn.escribir_script(self.lista_rangos[i], self.codigo_cambio, self.vlan, self.lista_interfaces[i])
            afectados = '\n'.join(self.lista_equipos[i]) + '\n'

            num_lineas1 = texto.count('\n')
            num_lineas2 = afectados.count('\n')
            if num_lineas1 > num_lineas2:
                num_lineas = num_lineas1
            else:
                num_lineas = num_lineas2
            row_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=3)
            titulo = tk.Label(row_frame, text=self.lista_switches[i], bg='#E4E7F3', fg='#000000',
                              font=("Neuer Weltschmerz", 12))
            titulo.grid(row=0, column=0, columnspan=3, pady=1, sticky="w")

            entry = tk.Text(row_frame, wrap=tk.WORD, height=num_lineas + 1, width=61, bg='#E4E7F3', fg='#000000',
                            insertbackground='#2D2D2D')
            entry.insert(tk.END, texto)
            entry.configure(state='disabled')
            entry.grid(row=1, column=1, rowspan=2, sticky="ew", pady=3)

            entry2 = tk.Text(row_frame, wrap=tk.WORD, height=num_lineas + 1, width=8, bg='#E4E7F3', fg='#000000',
                             insertbackground='#2D2D2D')
            afectados = '\n'.join(self.lista_equipos[i]) + '\n'
            entry2.insert(tk.END, afectados)
            entry2.configure(state='disabled')
            entry2.grid(row=1, column=0, rowspan=2, sticky="ew", pady=3)

            button = ttk.Button(row_frame, text=" Copiar", command=lambda e=entry: self.copiar_contenido(e))
            button.grid(row=1, column=2, padx=5, pady=(3, num_lineas), sticky="nsew")

            button2 = ttk.Button(row_frame, text="guardar", command=lambda index=i: self.guardar_cambios(index))
            button2.grid(row=2, column=2, padx=5, pady=(num_lineas, 3), sticky="nsew")

    def copiar_contenido(self, texto):
        self.clipboard_clear()
        self.clipboard_append(texto.get("1.0", tk.END))
        self.update()

    def guardar_cambios(self, index):
        fn.guardar_cambios(self.lista_equipos[index], self.codigo_cambio, self.vlan)
        #messagebox.showinfo(text="Cambios guardados")

    def generar_tabla_vlans(self, index=0):

        if hasattr(self, 'tabla_vlans'):
            self.tabla_vlans.destroy()

            # Crear un nuevo Frame para el Treeview
        self.tabla_vlans = ttk.Treeview(self.tab2_col2, show="headings", height=16)
        self.tabla_vlans.grid(row=0, column=0, pady=10, sticky="nsew")

        dataframe, width = fn.crear_tabla_vlans(index)
        #print(dataframe)
        # Configurar las columnas y encabezados si no están configuradas previamente
        if not self.tabla_vlans["columns"]:
            self.tabla_vlans["columns"] = list(dataframe.columns)
            for col in dataframe.columns:
                self.tabla_vlans.heading(col, text=col)
                self.tabla_vlans.column(col, width=width,
                                        anchor="center")  # Ajustar el ancho de la columna si es necesario

        # Insertar filas en el Treeview
        for _, row in dataframe.iterrows():
            self.tabla_vlans.insert("", tk.END, values=list(row))

    def abrir_formulario(self, edit):

        # Crear una nueva ventana emergente
        self.ventana_formulario = tk.Toplevel(self.notebook)

        # Crear etiquetas y campos de entrada
        txt = "Id VLAN: \n\nNombre: \n\nDirección: \n\nMascara: "
        ttk.Label(self.ventana_formulario, text=txt).grid(row=0, column=0, rowspan=4, padx=2, pady=5)

        self.id_entry = ttk.Entry(self.ventana_formulario, width=30)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.nombre_entry = ttk.Entry(self.ventana_formulario, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=5)

        self.direccion_entry = ttk.Entry(self.ventana_formulario, width=30)
        self.direccion_entry.grid(row=2, column=1, padx=5, pady=5)

        self.mask_entry = ttk.Entry(self.ventana_formulario, width=30)
        self.mask_entry.grid(row=3, column=1, padx=5, pady=5)

        if edit != 0:
            self.ventana_formulario.title("Editar VLAN")
            nombre, dir, mask = fn.mostrar_vlan_editable(edit)
            self.id_entry.insert(0, f"{edit}")
            self.id_entry.config(foreground="red", state="disabled")
            self.nombre_entry.insert(0, f"{nombre}")
            self.direccion_entry.insert(0, f"{dir}")
            self.mask_entry.insert(0, f"{mask}")

        else:
            self.ventana_formulario.title("Crear VLAN")
        boton_guardar = ttk.Button(self.ventana_formulario, text="Guardar Cambios", command=self.validar)
        boton_guardar.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        screen_width = self.ventana_formulario.winfo_screenwidth()
        screen_height = self.ventana_formulario.winfo_screenheight()

        width = 300
        height = 200

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.ventana_formulario.geometry(f"{width}x{height}+{x}+{y}")

        self.ventana_formulario.transient(self.notebook)
        self.ventana_formulario.grab_set()
        self.ventana_formulario.wait_window()

    def validar(self):
        control = False
        if self.vlan2 == 0:
            data = [int(self.id_entry.get()), self.nombre_entry.get(), self.direccion_entry.get(),
                    self.mask_entry.get()]
            control, fallo = fn.crear_vlan(data)
            if control:
                self.vlans_tab1_combobox.config(values=fn.listar_vlans())
                self.vlans_tab2_combobox.config(values=fn.listar_vlans_nombre())
                self.vlans_tab2_combobox.current(0)
                self.accion_f2_boton1()
            else:
                messagebox.showwarning("Alerta", "Los datos coinciden con una vlan existente")
        else:
            data = [int(self.id_entry.get()), self.nombre_entry.get(), self.direccion_entry.get(),
                    self.mask_entry.get()]
            control = fn.editar_vlan(data)
            if control:
                self.vlans_tab1_combobox.config(values=fn.listar_vlans())
                self.vlans_tab2_combobox.config(values=fn.listar_vlans_nombre())
                self.vlans_tab2_combobox.current(0)
                self.accion_f2_boton1()
            else:
                messagebox.showwarning("Alerta", "Los datos coinciden con una vlan existente")
        self.ventana_formulario.destroy()

    def confirmar_eliminar(self):
        self.ventana_eliminar = tk.Toplevel(self.notebook)
        # Crear etiquetas y campos de entrada
        ttk.Label(self.ventana_eliminar, text=f"Estás seguro de que quieres eliminar la VLAN {self.vlan2}?").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=10,
                                                                                                                  pady=5,
                                                                                                                  sticky="ew")

        btn_confirmar = ttk.Button(self.ventana_eliminar, text=" Eliminar ", command=self.eliminar)
        btn_confirmar.grid(row=1,column=0, padx=5, pady=5)
        width = 420
        height = 75
        screen_width = self.ventana_eliminar.winfo_screenwidth()
        screen_height = self.ventana_eliminar.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.ventana_eliminar.geometry(f"{width}x{height}+{x}+{y}")

        self.ventana_eliminar.transient(self.notebook)
        self.ventana_eliminar.grab_set()
        self.ventana_eliminar.wait_window()

    def eliminar(self):
        fn.eliminar_vlan(self.vlan2)
        self.ventana_eliminar.destroy()
        messagebox.showinfo("Cambio realizado", f"Se eliminó la VLAN{self.vlan2}")
        self.vlans_tab1_combobox.config(values=fn.listar_vlans())
        self.vlans_tab2_combobox.current(0)
        self.vlans_tab2_combobox.config(values=fn.listar_vlans_nombre())
        self.accion_f2_boton1()

    def actualizar_info_vlan(self):
        if self.vlan2 != 0:
            nombre, dir, mask = fn.mostrar_vlan_editable(self.vlan2)
            #print("HEY",self.vlan2)
            self.info_vlan_label.config(
                text=f"--------------------------------------------------\nCodigo VLAN:{self.vlan2}\n\n"
                     f"Nombre: {nombre}\n\nDirección:{dir}\n\nMáscara: {mask}\n--------------------------------------------------")

        else:
            self.info_vlan_label.config(
                text=f"--------------------------------------------------\nCodigo VLAN:\n\n"
                     f"Nombre:\n\nDirección:\n\nMáscara:\n--------------------------------------------------")

    def mostrar_equipo(self):
        self.ubicacion_equipo = tk.Label(self.frame_equipo, text="PISO CUARTO SWITCH PUERTO", bg='#E4E7F3',
                                         fg='#000000',
                                         font=("Neuer Weltschmerz", 12))
        self.ubicacion_equipo.grid(row=0, column=0, pady=1, sticky="w")


if __name__ == "__main__":
    app = App()
    app.mainloop()
