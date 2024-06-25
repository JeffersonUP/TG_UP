import pandas as pd
import re
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
    lista_interfaces = []
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
                print("puertos del switch",editables_puertos)
                lista_interfaces.append(editables_puertos.tolist())
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
    print(f"lista previa:{lista_switches}\n{lista_interfaces}")
    return lista_switches, lista_rangos, lista_codigos, lista_interfaces

def escribir_script(rango, cambios, vlan, puertos):

    if cambios == 0:
        swit = int(re.search(r'\d+', rango).group())
        script = ""
        for interface in puertos:
            script += f"show run int g{swit}/0/{interface}\nshow int g{swit}/0/{interface}\nshow int g{swit}/0/{interface} status\n"
    else:
        script = "conf t\n"
        if cambios == 3 or cambios == 4:
            script += f"default {rango}\n"
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
        elif cambios == 4:
            script += (f"switchport mode access\n"
                         f"switchport port-security violation restrict\n"
                         f"switchport port-security mac-address sticky\n"
                         f"switchport port-security\n"
                         f"spanning-tree portfast\n"
                         f"spanning-tree bpduguard enable\n")
        elif cambios == 5:
            script += "shutdown\n"

        elif cambios == 6:
            script += "no shutdown\n"
        elif cambios == 7:
            script += "no switchport portsecurity sticky\n"
        elif cambios == 8:
            script += "switchport portsecurity sticky\n"

        script += "end\n"
    return script

def guardar_cambios(equipos, cambios,vlan):
    print("cambios realizados")


def listar_vlans():
    df = pd.read_excel("vlans.xlsx")
    print(df)
    vlans_id = df['Id'].tolist()
    return vlans_id

def listar_vlans_nombre():
    df = pd.read_excel("vlans.xlsx")
    vlans_id = df['Id'].tolist()
    vlans_id =[str(n) for n in vlans_id]
    vlans_nombre = df['Nombre'].tolist()
    vlans_full = []
    for i in range(len(vlans_id)):
        vlans_full.append(vlans_id[i] +" "+ vlans_nombre[i])
    vlans_full.insert(0, "")
    return vlans_full

def crear_tabla_vlans(index):
    if index == 0:
        df1 = pd.read_excel("vlans.xlsx")
        df2 = pd.read_excel("dataframe2.xlsx")
        df2_grouped = df2.groupby('Vlan')['Ise'].count().reset_index()
        df = pd.merge(df1, df2_grouped, left_on='Id', right_on='Vlan', how='left')
        df.rename(columns={'Value': 'SumValue'}, inplace=True)
        df.drop(columns=['Vlan'], inplace=True)
        df.rename(columns={'Ise': 'Num. Equipos', 'Id': 'Codigo VLAN', 'Nombre': 'Descripción'}, inplace=True)

        width = 145
    else:
        df = pd.read_excel("dataframe2.xlsx")
        df = df.loc[df['Vlan'] == index]
        df = df[["Equipo", "Piso", "Cuarto", "Switch", "Puerto"]]
        width = 145
    return df, width

def mostrar_vlan_editable(id):
    df = pd.read_excel("vlans.xlsx")
    nombre = df.loc[df['Id'] == id, 'Nombre'].values[0]
    dir = df.loc[df['Id'] == id, 'Direccion'].values[0]
    mask = df.loc[df['Id'] == id, 'Mascara'].values[0]
    return nombre,dir,mask


def crear_vlan(data):
    #[id, nombre, dir, mask]
    df = pd.read_excel("vlans.xlsx")

    if data[0] in df['Id'].values:
        return False, data[0]
    elif data[1] in df['Nombre'].values:
        return False, data[1]
    elif data[2] in df['Direccion'].values:
        return False, data[2]
    nueva_fila = {'Id': data[0], 'Nombre': data[1], 'Direccion': data[2], 'Mascara': data[3]}
    print(nueva_fila)
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_excel("vlans.xlsx", index=False)
    return True, data[0]

def editar_vlan(data):
    #[id, nombre, dir, mask]
    df = pd.read_excel("vlans.xlsx")

    for i, row in df.iterrows():
        if row['Id'] != data[0]:
            if (row['Nombre'] == data[1] or
                    row['Direccion'] == data[2] or
                    row['Mascara'] == data[3]):
                print("coincide")
                return False

    df.loc[df['Id'] == data[0], ['Nombre', 'Direccion', 'Mascara']] = data[1], data[2], data[3]
    df.to_excel("vlans.xlsx", index=False)
    return True

def eliminar_vlan(id):
    df = pd.read_excel("vlans.xlsx")
    df = df[df['Id'] != id]
    df.to_excel("vlans.xlsx", index=False)


def buscar_equipo(equipo):

    df = pd.read_excel("dataframe2.xlsx")
    if (df['Equipo'] == equipo).any():
        data = df[df['Equipo'] == equipo].iloc[0].tolist()
        print(data)
        return True, data
    else:
        patron = r'^ED-\d{4}$'
        if not re.match(patron, equipo) and equipo != '':
            return True, 0
        if equipo !='':
            return False,0
        return False, []


def generar_texto_equipo(data):
    #[VLAN, PORT, ISE]
    texto=f"switchport access vlan {data[0]}\nswitchport mode access\n"
    if data[2] == "Activo":
        texto+=(f"authentication event fail action next-method\n"
                f"authentication event server dead action authorize\n"
                f"authentication event server alive action reinitialize\n"
                f"authentication host-mode multi-domain\n"
                f"authentication order dot1x mab\n"
                f"authentication priority dot1x mab\n"
                f"authentication port-control auto\n"
                f"authentication violation restrict\n"
                f"mab\n"
                f"dot1x pae authenticator\n"
                f"dot1x timeout tx-period 10\n"
                f"dot1x timeout supp-timeout 5\n")
    if data[1] == "Activo":
        texto+=(f"switchport port-security violation restrict\n"
                f"switchport port-security mac-address sticky\n"
                f"switchport port-security\n")
    texto+=("spanning-tree portfast\nspanning-tree bpduguard enable")
    return texto

def desglosarUbicacion(puerto):
    #P4C1R1S3P20
    #P2C1R1STACK1SW3P32
    try:
        puerto = list(puerto)
        codigos = []
        i = 0;
        holder=""
        while i < len(puerto):
            if puerto[i].isnumeric():
                holder += puerto[i]
            else:
                if holder != "":
                    codigos.append(int(holder))
                holder = ""
            i += 1
        codigos.append(int(holder))
        df = pd.read_excel("dataframe2.xlsx")
        for i, row in df.iterrows():
            if row['Piso'] == codigos[0]:
                if row['Cuarto'] == codigos[1]:
                    if row['Switch'] == codigos[-2]:
                        if row['Puerto'] == codigos[-1]:
                            print("coincide")
                            return False, 0
        return True, [codigos[0], codigos[1], codigos[-2], codigos[-1]]
    except:
        return False, 1

def editar_Equipo(nombre, codigo, list):
    print(nombre, codigo, list)
    df = pd.read_excel("dataframe2.xlsx")
    df.loc[df['Equipo'] == nombre, ['Codigo', 'Piso', 'Cuarto', 'Switch', 'Puerto']] = codigo, list[0], list[1], list[2], list[3]
    print(df.loc[df['Equipo'] == nombre])
    df.to_excel("dataframe2.xlsx", index=False)

def agregar_equipo(nombre, codigo, list):
    print(nombre, codigo, list)
    df = pd.read_excel("dataframe2.xlsx")
    df.loc[df['Equipo'] == nombre, ['Codigo', 'Piso', 'Cuarto', 'Switch', 'Puerto']] = codigo, list[0], list[1], list[2], list[3]
    print(df.loc[df['Equipo'] == nombre])
    df.to_excel("dataframe2.xlsx", index=False)
    nueva_fila = {'Equipo': nombre, 'Codigo': codigo, 'Piso': list[0], 'Cuarto': list[1], 'Switch': list[2],
                  'Puerto': list[3], 'Stack': 'no', 'Vlan': 1, 'Portsecurity': 'No activo', 'Ise': 'No activo'}
    print(nueva_fila)
    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_excel("dataframe2.xlsx", index=False)

def eliminar_pc(equipo):
    df = pd.read_excel("dataframe2.xlsx")
    df = df[df['Equipo'] != equipo]
    df.to_excel("dataframe2.xlsx", index=False)

def guardar_cambios(lista, cambio):
    print(lista, cambio)