import pandas as pd

def validar_listado(listado):
    validos = []
    no_validos = []
    df = pd.read_excel("dataframe2.xlsx")
    df_busqueda = df[df['Equipo'].isin(listado)]
    for puerto in listado:
        if df['Equipo'].isin([puerto]).any():
            validos.append(puerto)
        else:
            no_validos.append(puerto)
    return validos, no_validos

def generar_rangos(listado, accion=1):
    lista_switches = []
    lista_rangos = []
    lista_codigos = []
    df = pd.read_excel("dataframe2.xlsx")
    df_busqueda = df[df['Equipo'].isin(listado)]
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
            # print("cuarto", cuarto, end=" ")
            for switch in editables_Switches:
                df_switch = df_cuarto[df_cuarto["Switch"] == switch].sort_values(by="Puerto")
                lista_codigos.append(list(df_switch["Equipo"].unique()))
                editables_puertos = df_switch["Puerto"].unique()
                editables_puertos.sort()
                print(editables_puertos)
                lista_switches.append(f"Piso {piso}, Cuarto {cuarto}, switch {switch}")
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
                    if piso == 2:
                        interface = switch
                    else:
                        interface = 1
                    interface_range += f"g{interface}/0/{intervalos[i]}"
                    if i + 1 < len(intervalos):
                        interface_range += " , "
                    cont += 1
                    if cont == 7:
                        print(interface_range)
                        interface_range = "int range "
                        cont = 0
                if cont != 0:
                    if accion != 0:
                        lista_rangos.append(interface_range)
    return lista_switches, lista_rangos, lista_codigos

def escribir_script(rango, cambios, vlan):
    script = "conf t\n"
    script += f"{rango}\n"
    if cambios == 1:
        script += f"vlan-config remove all\nswitchport access vlan {vlan}\n"
    elif cambios == 2:
        script += f"no switchport portsecurity sticky\nshutdown\nswitchport portsecurity sticky\nno shutdown\n"
    elif cambios == 3:
        script += ("switchport mode access\nno authentication open\nauthentication event fail action next-method\n"
                    f"authentication event server dead action authorize\nauthentication event server alive action reinitialize\n"
                    f"authentication host-mode multi-domain\nauthentication order dot1x mab\nauthentication priority dot1x mab\n"
                    f"authentication port-control auto\nauthentication violation restrict\nmab\ndot1x pae authenticator\n"
                    f"dot1x timeout tx-period 10\ndot1x timeout supp-timeout 5\nspanning-tree portfast\nspanning-tree bpduguard enable\n")

    script += "end\n"
    return script

def guardar_cambios(equipos, cambios,vlan):
    print("cambios realizados")


def listar_vlans():
    vlans = ["","104", "998", "906", "904", "938"]
    return vlans