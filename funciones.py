import sqlite3

import pandas as pd
import re


def validar_listado(listado):
    validos = []
    no_validos = []
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    for puerto in listado:
        cursor.execute("select COUNT(*) FROM equipos WHERE id = ?", (puerto,))
        if (cursor.fetchone()[0]) > 0:
            validos.append(puerto)
        else:
            no_validos.append(puerto)
    conexion.close()
    return validos, no_validos


'''
def generar_rangos(listado):
    lista_switches = []
    lista_interfaces = []
    lista_rangos = []
    lista_codigos = []

    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    query = "SELECT * FROM equipos WHERE id IN ({})".format(','.join('?' for _ in listado))
    cursor.execute(query, listado)
    lista = cursor.fetchall()

    df_busqueda = pd.DataFrame(lista, columns=[desc[0] for desc in cursor.description])

    editables_pisos = df_busqueda["piso"].unique()
    editables_pisos.sort()

    for piso in editables_pisos:
        df_piso = df_busqueda[df_busqueda["piso"] == piso]
        editables_cuartos = df_piso["cuarto"].unique()
        editables_cuartos.sort()
        for cuarto in editables_cuartos:
            df_cuarto = df_piso[df_piso["cuarto"] == cuarto]
            editables_Switches = df_cuarto["switch"].unique()
            editables_Switches.sort()
            for switch in editables_Switches:
                df_switch = df_cuarto[df_cuarto["switch"] == switch].sort_values(by="puerto")
                lista_codigos.append(list(df_switch["id"].unique()))
                editables_puertos = df_switch["puerto"].unique()
                editables_puertos.sort()
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

                intervalosg=[]
                if piso == 2:
                    interface = switch
                else:
                    interface = 1
                for elemento in intervalos:
                    intervalosg.append(f"g{interface}/0/{elemento}")
                if len(intervalosg)==1:
                    interface_range= f"int {intervalosg[0]}"
                else:
                    interface_range = f"int range {', '.join(intervalosg)}"
                if len(intervalosg)!=0:
                    lista_rangos.append(interface_range)
        print(lista_switches,"\n", lista_rangos, "\n",lista_codigos,"\n",lista_interfaces)
    return lista_switches, lista_rangos, lista_codigos, lista_interfaces
'''


def generar_rangos(listado):
    conexion = sqlite3.connect('database.db')
    try:
        cursor = conexion.cursor()
        formato_ids = ','.join(['?'] * len(listado))
        consulta = f"""
        SELECT piso, cuarto, switch, rack, GROUP_CONCAT(puerto) AS 'puertos_agrupados', 
        GROUP_CONCAT(id) AS 'ids_agrupados'
        FROM (
            SELECT piso, cuarto, switch, rack, puerto, id FROM equipos
            WHERE id IN ({formato_ids})  -- Se usan placeholders para SQLite
            ORDER BY piso, cuarto, switch, rack, puerto  -- Ordenar antes
        )
        GROUP BY piso, cuarto, switch, rack;
        """
        cursor.execute(consulta, listado)
        resultados = cursor.fetchall()
        encabezados = []
        lista_rangos = []
        lista_codigos = []
        lista_interfaces = []
        for fila in resultados:
            piso = fila[0]
            cuarto = fila[1]
            switch = fila[2]
            rack = fila[3]
            puertos = list(map(int, fila[4].split(",")))
            ids = list(fila[5].split(","))
            lista_interfaces.append(puertos)
            lista_codigos.append(ids)
            if piso == 2:
                encabezados.append(f"Piso {piso}, Cuarto {cuarto}, stack {rack}, switch {switch}")
            else:
                encabezados.append(f"Piso {piso}, Cuarto {cuarto}, rack {rack}, switch {switch}")
            intervalos = []
            inicio = puertos[0]
            fin = puertos[0]
            for i in range(1, len(puertos)):
                if puertos[i] == fin + 1:
                    fin = puertos[i]
                else:
                    if inicio == fin:
                        intervalos.append(str(inicio))
                    else:
                        intervalos.append(f"{inicio}-{fin}")
                    inicio = puertos[i]
                    fin = puertos[i]
            if inicio == fin:
                intervalos.append(str(inicio))
            else:
                intervalos.append(f"{inicio}-{fin}")
            intervalosg = []
            if piso == 2:
                interface = switch
            else:
                interface = 1
            for elemento in intervalos:
                intervalosg.append(f"g{interface}/0/{elemento}")
            if len(intervalosg) == 1:
                interface_range = f"int {intervalosg[0]}"
            else:
                interface_range = f"int range {', '.join(intervalosg)}"
            if len(intervalosg) != 0:
                lista_rangos.append(interface_range)
            print(encabezados, "\n", lista_rangos, "\n", lista_codigos, "\n", lista_interfaces)
    finally:
        cursor.close()
        conexion.close()
    return encabezados, lista_rangos, lista_codigos, lista_interfaces


def escribir_script(rango, cambios, vlan, puertos):
    if cambios == 8:
        swit = int(re.search(r'\d+', rango).group())
        script = ""
        for interface in puertos:
            script += f"show run int g{swit}/0/{interface}\nshow int g{swit}/0/{interface}\nshow int g{swit}/0/{interface} status\n"
    else:
        script = "conf t\n"
        if cambios == 2 or cambios == 3:
            script += f"default {rango}\n"
        script += f"{rango}\n"
        if cambios == 0:
            script += f"switchport access vlan {vlan}\n"
        elif cambios == 1:
            script += f"no switchport port-security mac-address sticky\nshutdown\nswitchport port-security mac-address sticky\nno shutdown\n"
        elif cambios == 2:
            script += (f"switchport mode access\nswitchport access vlan 998\nno authentication open\nauthentication event fail action next-method\n"
                       f"authentication event server dead action authorize\nauthentication event server alive action reinitialize\n"
                       f"authentication host-mode multi-domain\nauthentication order dot1x mab\nauthentication priority dot1x mab\n"
                       f"authentication port-control auto\nauthentication violation restrict\nmab\ndot1x pae authenticator\n"
                       f"dot1x timeout tx-period 10\ndot1x timeout supp-timeout 5\nspanning-tree portfast\nspanning-tree bpduguard enable\n")
        elif cambios == 3:
            script += (f"switchport mode access\n"
                       f"switchport access vlan {vlan}\n"
                       f"switchport port-security violation restrict\n"
                       f"switchport port-security mac-address sticky\n"
                       f"switchport port-security\n"
                       f"spanning-tree portfast\n"
                       f"spanning-tree bpduguard enable\n")
        elif cambios == 4:
            script += "shutdown\n"

        elif cambios == 5:
            script += "no shutdown\n"
        elif cambios == 6:
            script += "no switchport port-security mac-address sticky\n"
        elif cambios == 7:
            script += "switchport port-security mac-address sticky\n"

        script += "end\n"
    return script


def listar_vlans():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM vlans")
    lista = cursor.fetchall()
    vlans_id = [id[0] for id in lista]
    conexion.close()
    return vlans_id


def listar_vlans_nombre():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM vlans ORDER BY id")
    lista = cursor.fetchall()
    vlans_id = [str(id[0]) for id in lista]
    vlans_nombre = [id[1] for id in lista]
    vlans_full = [""]
    for i in range(len(vlans_id)):
        vlans_full.append(vlans_id[i] + " " + vlans_nombre[i])
    conexion.close()
    return vlans_full


def crear_tabla_vlans(index):
    conexion = sqlite3.connect('database.db')
    if index == 0:
        query = '''
        SELECT vlans.id AS 'Id', vlans.nombre AS 'Codigo VLAN', COUNT(equipos.id) AS 'Num. Equipos' FROM vlans
        LEFT JOIN equipos ON vlans.id = equipos.vlan_id
        GROUP BY vlans.id, vlans.nombre; 
        '''
        width = 245
    else:
        query = f"SELECT id AS 'EQUIPO', piso, cuarto, switch, puerto from equipos WHERE equipos.vlan_id = {index}"
        width = 145
    df = pd.read_sql_query(query, conexion)
    conexion.close()
    return df, width


def mostrar_vlan_editable(id):
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute(f"SELECT nombre, direccion, mascara from vlans WHERE id = {id}")
    data = cursor.fetchone()
    if data != None:
        nombre, dir, mask = list(data)
    else:
        nombre, dir, mask = "", "", ""
    conexion.close()
    return nombre, dir, mask


def crear_vlan(data):
    #[id, nombre, dir, mask]
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT 1 from vlans WHERE id = ? OR nombre = ? OR direccion = ?",
                   (data[0], data[1], data[2]))
    res = cursor.fetchone()
    if res is None:
        cursor.execute("insert INTO vlans(id, nombre, direccion, mascara) VALUES (?,?,?,?)", data)
        res = True
    else:
        res = False
    conexion.commit()
    conexion.close()
    return res


def editar_vlan(data):
    print("fuga")
    #[id, nombre, dir, mask]
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT 1 from vlans WHERE id = ? OR nombre = ? OR direccion = ?",
                   (data[0], data[1], data[2]))
    res = cursor.fetchone()
    if res is not None:
        cursor.execute("UPDATE vlans SET nombre = ?, direccion = ?, mascara = ? where id = ?",
                       (data[1], data[2], data[3], data[0]))
        res = True
    else:
        res = False
    conexion.commit()
    conexion.close()
    return res


def eliminar_vlan(id):
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE from vlans WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()


def buscar_equipo(equipo):
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * from equipos WHERE id = ?", (equipo,))
    res = cursor.fetchone()
    if res is not None:
        return True, list(res)
    else:
        patron = r'^ED-\d{4}$'
        if not re.match(patron, equipo) and equipo != '':
            return True, 0
        return False, []


def generar_texto_equipo(data):
    #[VLAN, PORT, ISE]
    texto = f"switchport access vlan {data[0]}\nswitchport mode access\n"
    if data[2] == "Activo":
        texto += (f"authentication event fail action next-method\n"
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
        texto += (f"switchport port-security violation restrict\n"
                  f"switchport port-security mac-address sticky\n"
                  f"switchport port-security\n")
    texto += ("spanning-tree portfast\nspanning-tree bpduguard enable")
    return texto


def desglosar_ubicacion(puerto):
    #P4C1R1S3P20
    #P2C1R1STACK1SW3P32
    try:
        puerto = list(puerto)
        codigos = []
        i = 0
        holder = ""
        while i < len(puerto):
            if puerto[i].isnumeric():
                holder += puerto[i]
            else:
                if holder != "":
                    codigos.append(int(holder))
                holder = ""
            i += 1
        codigos.append(int(holder))
        print(codigos)
    except:
        return False, 1

    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT 1 from equipos WHERE piso = ? AND cuarto = ? AND switch = ? AND puerto = ? AND rack = ?",
                   (codigos[0], codigos[1], codigos[-2], codigos[-1], codigos[2]))
    res = cursor.fetchone()
    conexion.close()
    print(res)
    if res is None:
        return True, [codigos[0], codigos[1], codigos[2], codigos[-2], codigos[-1]]
    else:
        return False, 0


def editar_equipo(nombre, codigo, list):
    #print(nombre, codigo, list)
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute("UPDATE equipos SET codigo = ?, piso = ?, cuarto = ?, switch = ?, puerto = ? WHERE id = ?",
                   (codigo, list[0], list[1], list[2], list[3], nombre))
    conexion.commit()
    conexion.close()


def agregar_equipo(nombre, codigo, list):
    print(nombre, codigo, list)
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT into equipos(id, codigo, piso, cuarto, switch, puerto, rack) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (nombre, codigo, list[0], list[1], list[3], list[4], list[2]))
    conexion.commit()
    conexion.close()


def eliminar_pc(equipo):
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE from equipos WHERE id = ?", (equipo,))
    conexion.commit()
    conexion.close()


def guardar_cambios(lista, cambio, vlan):
    print(lista, cambio, vlan)
    cambio = cambio + 1
    conexion = sqlite3.connect("database.db")
    cursor = conexion.cursor()
    for equipo in lista:
        if cambio == 1:
            cursor.execute("UPDATE equipos SET vlan_id = ? WHERE id = ?", (vlan, equipo,))
            print(cambio)
        elif cambio == 2 or cambio == 8:
            cursor.execute("UPDATE equipos SET portsecurity = 'True' WHERE id = ?", (equipo,))
        elif cambio == 3:
            cursor.execute("UPDATE equipos SET portsecurity = True WHERE id = 'equipo'")
        elif cambio == 4:
            cursor.execute("UPDATE equipos SET portsecurity = True WHERE id = 'equipo'")
        elif cambio == 5:
            cursor.execute("UPDATE equipos SET portsecurity = True WHERE id = 'equipo'")
        elif cambio == 7:
            cursor.execute("UPDATE equipos SET portsecurity = True WHERE id = 'equipo'")

    conexion.commit()
    conexion.close()
