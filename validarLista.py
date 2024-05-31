import pandas as pd
import tkinter as tk
from tkinter import messagebox
lista=['ED-0017', 'ED-0018', 'ED-0019', 'ED-0021', 'ED-0022', 'ED-0023', 'ED-0024', 'ED-0025', 'ED-0026', 'ED-0027',
       'ED-0028', 'ED-0029', 'ED-0030', 'ED-0031', 'ED-0032', 'errors', 'ED-0034', 'ED-0035', 'ED-0036', 'ED-0037',
       'ED-0038', 'ED-0039']
lista_op = []
no_encontrada = []

df = pd.read_excel("dataframe2.xlsx")

df_busqueda=df[df['Equipo'].isin(lista)]
for i, puerto in enumerate(lista):
    if df['Equipo'].isin([puerto]).any():
        lista_op.append(puerto)
    else:
        no_encontrada.append(puerto)
print(df_busqueda)
switches = df_busqueda["Switch"].unique()
print(switches)

