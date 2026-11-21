
import sqlite3
import hashlib
import secrets
import getpass

# Conectar con nuestra base de datos
conexion = sqlite3.connect("data/gestion_libros.db")
cursor = conexion.cursor()

print("\n================================")
print(" REGISTRO DEL ADMINISTRADOR")
print("================================")

nombre = input("Nombre completo: ").strip()
usuario = input("Nombre de usuario: ").strip()

# Comprobar que los datos no estén vacíos
if not nombre or not usuario:
    print("Error: debes completar todos los datos.")
    conexion.close()
    exit()

# Comprobar si el usuario ya existe
cursor.execute(
    "SELECT id_usuario FROM usuarios WHERE usuario = ?",
    (usuario,)
)

if cursor.fetchone():
    print("Este nombre de usuario ya existe.")
    conexion.close()
    exit()

# Solicitar contraseña
contrasena = getpass.getpass("Crear contraseña: ")
confirmacion = getpass.getpass("Confirmar contraseña: ")

if len(contrasena) < 8:
    print("La contraseña debe tener al menos 8 caracteres.")
    conexion.close()
    exit()

if contrasena != confirmacion:
    print("Las contraseñas no coinciden.")
    conexion.close()
    exit()

# Proteger contraseña mediante hash
salt = secrets.token_hex(16)

hash_contrasena = hashlib.pbkdf2_hmac(
    "sha256",
    contrasena.encode("utf-8"),
    salt.encode("utf-8"),
    310000
).hex()

contrasena_protegida = (
    f"pbkdf2_sha256$310000${salt}${hash_contrasena}"
)

# Registrar administrador
cursor.execute("""
    INSERT INTO usuarios (nombre, usuario, contrasena, rol)
    VALUES (?, ?, ?, ?)
""", (
    nombre,
    usuario,
    contrasena_protegida,
    "administrador"
))

conexion.commit()
conexion.close()

print("\n¡Administrador registrado correctamente!")
print("Ya puedes utilizar este usuario para iniciar sesión.")
