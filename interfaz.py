import tkinter as tk

ventana = tk.Tk()
ventana.title("Switch manager")
ventana.geometry("800x400")

frame1 = tk.Frame(ventana, bg="white")
frame1.pack(fill="both", expand=True, side="left")

frame2 = tk.Frame(ventana, bg="gray")
frame2.pack(fill="both", expand=True,side="left")

scrollbar = tk.Scrollbar(frame2)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frame_texto = tk.Frame(frame2)
frame_texto.pack(side=tk.LEFT, pady=50, padx=50, fill=tk.Y, expand=False)


entrada_texto = tk.Text(frame_texto, width=10, height=10, undo=True, yscrollcommand=scrollbar.set)
entrada_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=entrada_texto.yview)


# Crear la barra de desplazamiento


frame3 = tk.Frame(ventana, bg="cyan")
frame3.pack(fill="both", expand=True,side="left")
ventana.mainloop()

