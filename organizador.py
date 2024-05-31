import tkinter as tk
from tkinter import messagebox

# Variable global para almacenar las líneas de texto
lineas_texto = []


def registrar_texto():
    global lineas_texto
    texto = entrada_texto.get("1.0", tk.END).strip()
    if texto:
        lineas_texto = texto.split('\n')
        print(lineas_texto)
        actualizar_lista()
    else:
        messagebox.showwarning("Entrada vacía", "Por favor, ingrese algún texto antes de registrar.")


def borrar_linea(index):
    global lineas_texto
    del lineas_texto[index]
    actualizar_lista()


def actualizar_lista():
    for widget in frame_lista.winfo_children():
        widget.destroy()

    for i, linea in enumerate(lineas_texto):
        frame_linea = tk.Frame(frame_lista)
        frame_linea.pack(fill=tk.X, pady=2)

        etiqueta = tk.Label(frame_linea, text=linea, anchor="w")
        etiqueta.pack(side=tk.LEFT, fill=tk.X, expand=True)

        boton_borrar = tk.Button(frame_linea, text="x", command=lambda a=i: borrar_linea(a))
        boton_borrar.pack(side=tk.RIGHT)

def actualizar_numeracion(event=None):
    lineas = entrada_texto.get("1.0", "end-1c").split("\n")
    numeracion.config(state=tk.NORMAL)
    numeracion.delete("1.0", tk.END)
    for i, _ in enumerate(lineas, start=1):
        numeracion.insert(tk.END, f"{i}\n")
    numeracion.config(state=tk.DISABLED)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Registro de Texto")
ventana.geometry("600x400")

# Crear el contenedor de texto con barra de desplazamiento
frame_texto = tk.Frame(ventana)
frame_texto.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.Y, expand=False)

# Crear la barra de desplazamiento
scrollbar = tk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Crear el cuadro de texto numerado
numeracion = tk.Text(frame_texto, width=4, padx=3, takefocus=0, border=0, background='lightgrey', state=tk.DISABLED)
numeracion.pack(side=tk.LEFT, fill=tk.Y)

entrada_texto = tk.Text(frame_texto, width=10, height=10, undo=True, yscrollcommand=scrollbar.set)
entrada_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
entrada_texto.bind("<KeyRelease>", actualizar_numeracion)

scrollbar.config(command=entrada_texto.yview)

# Inicializar la numeración
actualizar_numeracion()

# Crear el frame para la lista registrada
frame_lista_container = tk.Frame(ventana)
frame_lista_container.pack(side=tk.RIGHT, pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar_lista = tk.Scrollbar(frame_lista_container)
scrollbar_lista.pack(side=tk.RIGHT, fill=tk.Y)

frame_lista = tk.Frame(frame_lista_container)
frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas_lista = tk.Canvas(frame_lista, yscrollcommand=scrollbar_lista.set)
canvas_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_lista.config(command=canvas_lista.yview)

# Crear un frame interno para contener la lista dentro del canvas
frame_lista_interior = tk.Frame(canvas_lista)
canvas_lista.create_window((0,0), window=frame_lista_interior, anchor='nw')

def actualizar_scroll_region(event):
    canvas_lista.configure(scrollregion=canvas_lista.bbox("all"))

frame_lista_interior.bind("<Configure>", actualizar_scroll_region)

# Crear y colocar el botón de registro
boton_frame = tk.Frame(ventana)
boton_frame.pack(side=tk.BOTTOM, pady=10)
boton_registrar = tk.Button(boton_frame, text="Registrar", command=registrar_texto)
boton_registrar.pack()

# Iniciar el bucle principal de la ventana
ventana.mainloop()
