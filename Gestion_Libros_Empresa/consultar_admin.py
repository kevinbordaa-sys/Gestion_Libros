
import sqlite3
from pathlib import Path

# Buscar la base de datos desde la ubicación de este archivo
CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_DB = CARPETA_PROYECTO / "data" / "gestion_libros.db"

print("\n===== DIAGNÓSTICO DE LA BASE DE DATOS =====")
print("Ruta utilizada:", RUTA_DB)
print("¿Existe el archivo?:", RUTA_DB.exists())

# No crear una base nueva accidentalmente
if not RUTA_DB.exists():
    print("\nERROR: No se encontró la base de datos.")
else:
    conexion = sqlite3.connect(RUTA_DB)
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """)

    tablas = cursor.fetchall()
    print("\nTablas encontradas:")

    for tabla in tablas:
        print("-", tabla[0])

    # Comprobar si existe la tabla usuarios
    nombres_tablas = [tabla[0] for tabla in tablas]

    if "usuarios" in nombres_tablas:
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total = cursor.fetchone()[0]

        print("\nTotal de usuarios registrados:", total)

        cursor.execute("""
            SELECT id_usuario, nombre, usuario, rol
            FROM usuarios
        """)

        usuarios = cursor.fetchall()

        print("\n===== USUARIOS REGISTRADOS =====")

        for usuario in usuarios:
            print("ID:", usuario[0])
            print("Nombre:", usuario[1])
            print("Usuario:", usuario[2])
            print("Rol:", usuario[3])
            print("-------------------------")
    else:
        print("\nERROR: No existe la tabla usuarios.")

    conexion.close()

print("\n===== FIN DEL DIAGNÓSTICO =====")
