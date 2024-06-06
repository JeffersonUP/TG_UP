import tkinter as tk

def boton_funcion(dato):
    print(f"Botón presionado para: {dato}")


def buscar():
    # Acción a realizar cuando se presione el botón Buscar
    print("Buscar presionado")

root = tk.Tk()
root.title("Switch manager")
root.geometry("760x400")
# Crear un frame para contener la caja de texto y el scrollbar
frame_texto = tk.Frame(root)
frame_texto.grid(row=0, column=0, sticky="nsew")

# Crear la caja de texto con ancho de 10 caracteres
texto = tk.Text(frame_texto, width=10, wrap="word")
texto.grid(row=0, column=0, sticky="nsew")

# Crear el scrollbar y asociarlo a la caja de texto
scrollbar = tk.Scrollbar(frame_texto, orient="vertical", command=texto.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
texto.config(yscrollcommand=scrollbar.set)

# Crear el botón "Buscar" y colocarlo debajo de la caja de texto
boton_buscar = tk.Button(frame_texto, text="Buscar", command=buscar)
boton_buscar.grid(row=1, column=0, sticky="ew")


frame_opciones = tk.Frame(root, bg="gray", pady=2, padx=2,borderwidth=1)
frame_opciones.grid(row=0, column=1, sticky="nsew")
# Crear el label
label = tk.Label(frame_opciones, text="\nEquipos consultados: \n\nEquipos no encontrados: \n\nSwitches involucrados:\n", relief="raised")
label.grid(row=0, column=1, pady=5, sticky="nsew")

# Crear un frame para contener los botones
boton_frame = tk.Frame(frame_opciones, borderwidth=1, relief="solid")
boton_frame.grid(row=1, column=1, pady=5, sticky="nsew")

# Crear los 7 botones
for i in range(1, 7):
    boton = tk.Button(boton_frame, text=f"Funcionalidadkkkk {i}")
    boton.grid(row=i-1, column=0, padx=5, pady=2, sticky="ew")
boton = tk.Button(boton_frame, text=f"Fukk {i}")
boton.grid(row=7, column=0, padx=5, pady=2, sticky="ew")


# Crear un canvas
canvas = tk.Canvas(root, bg="cyan")
canvas.grid(row=0, column=2, sticky="nsew")

# Crear un scrollbar vertical y asociarlo con el canvas
scrollbar = tk.Scrollbar(orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=3, sticky="nsew")
canvas.configure(yscrollcommand=scrollbar.set)

# Crear un frame dentro del canvas
frame_contenido = tk.Frame(canvas)

# Crear un window dentro del canvas para contener el frame
canvas.create_window((0, 0), window=frame_contenido, anchor="nw")


# Función para configurar el scrollregion del canvas
def configurar_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


frame_contenido.bind("<Configure>", configurar_scrollregion)

# Datos de ejemplo
datos = [f"Dato {i}\nunificador de anchor, esta primera linea tendrá artificialmente el anchor maximo disponible" for i
         in range(1, 51)]
# Crear la tabla de datos con botones
for i, dato in enumerate(datos):

    celda_frame = tk.Frame(frame_contenido, height=30, borderwidth=1, relief="solid")
    celda_frame.grid(row=i, column=0, padx=5, pady=5)
    if i == 1:
        etiqueta = tk.Label(celda_frame, text="miau")
    else:
        etiqueta = tk.Label(celda_frame, text=dato)
    etiqueta.pack(expand=True, fill='both')

    boton = tk.Button(celda_frame, text="Botón", command=lambda d=dato: boton_funcion(d))
    boton.pack(expand=True, fill='both')
#11


# Configurar la columna 0 para que mantenga su ancho fijo y ajustable en alto
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=0)
root.columnconfigure(2, weight=1)


root.minsize(400, 200)

# Configurar la fila 0 para que sea ajustable en alto
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Configurar el frame de la caja de texto para que ajuste su alto
frame_texto.rowconfigure(0, weight=1)
frame_texto.columnconfigure(0, weight=1)


frame_opciones.rowconfigure(0, weight=1)  # Label
frame_opciones.rowconfigure(1, weight=7)  # Frame de botones
frame_opciones.columnconfigure(0, weight=1)
boton_frame.columnconfigure(0, weight=1)

# Evitar que los botones se deformen
for i in range(7):
    boton_frame.rowconfigure(i, weight=1)
root.mainloop()

