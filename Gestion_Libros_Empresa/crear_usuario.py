from firebase_config import db
from firebase_admin import auth
from getpass import getpass

print("=== CREAR USUARIO ===")

nombre = input("Nombre: ").strip()
usuario = input("Nombre de usuario: ").strip()
email = input("Correo electrónico: ").strip()
contrasena = getpass("Contraseña: ")

try:
    # Crear usuario en Firebase Authentication
    nuevo_usuario = auth.create_user(
        email=email,
        password=contrasena
    )

    # Crear automáticamente su documento en Firestore
    db.collection("usuarios").document(nuevo_usuario.uid).set({
        "nombre": nombre,
        "usuario": usuario,
        "email": email,
        "rol": "administrador"
    })

    print("\n¡Usuario creado correctamente!")
    print("Nombre:", nombre)
    print("Usuario:", usuario)
    print("Rol: administrador")

except Exception as error:
    print("\nError al crear usuario:", error)