from firebase_config import db

try:
    db.collection("pruebas").document("conexion").set({
        "mensaje": "Python conectado correctamente",
        "estado": True
    })

    print("¡Conexión exitosa con Firebase!")

except Exception as error:
    print("Error de conexión:", error)