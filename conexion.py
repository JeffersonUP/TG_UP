import sqlite3
import pandas as pd
#crear la database a partir del dataframe.
conexion = sqlite3.connect("database.db")
cursor = conexion.cursor()
cursor.execute("UPDATE vlans SET direccion = '172.19.49.0' WHERE id = 104")
conexion.commit()
conexion.close()
