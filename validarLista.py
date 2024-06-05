import pandas as pd
import tkinter as tk
from tkinter import messagebox
editables_puertos = ['ED-0933', 'ED-0934', 'ED-0935', 'ED-0936', 'ED-0937', 'ED-0938', 'ED-0939', 'ED-0940', 'ED-0941',
                     'ED-0942', 'ED-0943', 'ED-0944', 'ED-0945', 'ED-0946', 'ED-0947']

editables_puertos_op = []
no_encontrada = []

df = pd.read_excel("dataframe2.xlsx")

df_busqueda=df[df['Equipo'].isin(editables_puertos)]
for puerto in editables_puertos:
    if df['Equipo'].isin([puerto]).any():
        editables_puertos_op.append(puerto)
    else:
        no_encontrada.append(puerto)
print(no_encontrada)
print(df_busqueda)
editables_pisos = df_busqueda["Piso"].unique()
editables_pisos.sort()

for piso in editables_pisos:
    df_piso = df_busqueda[df_busqueda["Piso"] == piso]
    editables_cuartos = df_piso["Cuarto"].unique()
    editables_cuartos.sort()
    #print("piso", piso, end=" ")
    for cuarto in editables_cuartos:
        df_cuarto = df_piso[df_piso["Cuarto"] == cuarto]
        editables_Switches = df_cuarto["Switch"].unique()
        editables_Switches.sort()
        #print("cuarto", cuarto, end=" ")
        for switch in editables_Switches:
            df_switch = df_cuarto[df_cuarto["Switch"] == switch].sort_values(by="Puerto")
            print(f"Piso {piso}, Cuarto {cuarto}, Switch {switch}: ")
            editables_puertos = df_switch["Puerto"].unique()
            editables_puertos.sort()
            #print("puertos", editables_puertos)
            intervalos = []
            inicio = editables_puertos[0]
            fin = editables_puertos[0]
            for i in range(1, len(editables_puertos)):
                if editables_puertos[i] == fin + 1:
                    fin = editables_puertos[i]
                else:
                    if inicio == fin:
                        intervalos.append(str(inicio))
                    else:
                        intervalos.append(f"{inicio}-{fin}")
                    inicio = editables_puertos[i]
                    fin = editables_puertos[i]

            if inicio == fin:
                intervalos.append(str(inicio))
            else:
                intervalos.append(f"{inicio}-{fin}")
            #print(intervalos)
            if len(editables_puertos) == 1:
                interface_range = "int "
            else:
                interface_range = "int range "
            cont = 0
            for i in range(0, len(intervalos)):
                interface_range += f"g1/0/{intervalos[
                    i]}"
                if i+1 < len(intervalos):
                    interface_range += " , "
                cont += 1
                if cont == 7:
                    print(interface_range)
                    interface_range = "int range "
                    cont = 0
            if cont != 0:
                print(interface_range,"\n")