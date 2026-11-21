
import sqlite3
import os

# Ruta de la base de datos
RUTA_DB = os.path.join("data", "gestion_libros.db")


def conectar():
    os.makedirs("data", exist_ok=True)

    conexion = sqlite3.connect(RUTA_DB)

    # Activar las relaciones entre tablas
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla de proveedores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT,
            correo TEXT,
            direccion TEXT
        )
    """)

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK (
                rol IN ('administrador', 'empleado', 'proveedor')
            ),
            id_proveedor INTEGER,
            FOREIGN KEY (id_proveedor)
                REFERENCES proveedores(id_proveedor)
        )
    """)

    # Tabla de libros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            editorial TEXT,
            isbn TEXT UNIQUE,
            precio REAL NOT NULL DEFAULT 0,
            stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
        )
    """)

    # Tabla de entradas de libros
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entradas (
            id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
            id_proveedor INTEGER NOT NULL,
            id_usuario INTEGER NOT NULL,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_proveedor)
                REFERENCES proveedores(id_proveedor),
            FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id_usuario)
        )
    """)

    # Detalle de cada entrada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_entradas (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_entrada INTEGER NOT NULL,
            id_libro INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad > 0),
            FOREIGN KEY (id_entrada)
                REFERENCES entradas(id_entrada),
            FOREIGN KEY (id_libro)
                REFERENCES libros(id_libro)
        )
    """)

    # Tabla de ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id_usuario)
        )
    """)

    # Detalle de los libros vendidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_libro INTEGER NOT NULL,
            cantidad INTEGER NOT NULL CHECK (cantidad > 0),
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (id_venta)
                REFERENCES ventas(id_venta),
            FOREIGN KEY (id_libro)
                REFERENCES libros(id_libro)
        )
    """)

    # Historial de movimientos de inventario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_libro INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (
                tipo IN ('entrada', 'venta', 'ajuste')
            ),
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            descripcion TEXT,
            FOREIGN KEY (id_libro)
                REFERENCES libros(id_libro)
        )
    """)

    conexion.commit()
    conexion.close()

    print("¡Base de datos creada correctamente!")
    print("¡Todas las tablas están listas!")


if __name__ == "__main__":
    crear_tablas()
