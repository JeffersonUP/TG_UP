import pandas as pd
import tkinter as tk
from tkinter import messagebox
editables_puertos = ['ED-0434', 'ED-0435', 'ED-0436', 'ED-0437', 'ED-0438', 'ED-0439', 'ED-0440', 'ED-0441',
                     'ED-0442', 'ED-0443', 'ED-0444', 'ED-0445', 'ED-0446', 'ED-0447', 'ED-0448', 'ED-0449',
                     'ED-0450', 'ED-0451', 'ED-0452', 'ED-0453', 'ED-0454', 'ED-0455', 'ED-0456', 'ED-0457',
                     'ED-0458', 'ED-0459', 'ED-0460', 'ED-0461', 'ED-0462', 'ED-0463', 'ED-0464', 'ED-0465',
                     'ED-0466', 'ED-0467', 'ED-0468', 'ED-0469', 'ED-0470', 'ED-0471', 'ED-0472', 'ED-0473',
                     'ED-0474', 'ED-0475', 'ED-0476', 'ED-0477', 'ED-0478', 'ED-0479', 'ED-0480', 'ED-1842']

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