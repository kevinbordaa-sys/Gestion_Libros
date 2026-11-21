import tkinter as tk
from tkinter import messagebox
import requests
import threading

from google.cloud.firestore_v1.base_query import FieldFilter

from firebase_config import db
from modulo_libros import mostrar_formulario_libro
# Ubicación de la base de datos
FIREBASE_API_KEY = "AIzaSyDVB5d2f6SYMnOql9vhUwDyY8qVRxOnC5E"



# -----------------------------------------
# VERIFICAR CONTRASEÑA
# -----------------------------------------
def autenticar(usuario, contrasena):
    try:
        print("1. Buscando usuario en Firestore...")

        resultados = (
            db.collection("usuarios")
            .where(filter=FieldFilter("usuario", "==", usuario))
            .limit(1)
            .get(timeout=10)
        )

        print("2. Consulta de Firestore finalizada.")

        if not resultados:
            print("3. Usuario no encontrado.")
            return None

        documento = resultados[0]
        datos = documento.to_dict()

        email = datos.get("email")

        if not email:
            print("3. El usuario no tiene correo.")
            return None

        print("4. Usuario encontrado. Validando contraseña...")

        url = (
            "https://identitytoolkit.googleapis.com/v1/"
            "accounts:signInWithPassword"
            f"?key={FIREBASE_API_KEY}"
        )

        respuesta = requests.post(
            url,
            json={
                "email": email,
                "password": contrasena,
                "returnSecureToken": True
            },
            timeout=15
        )

        print("5. Firebase Authentication respondió.")

        if respuesta.status_code != 200:
            print("6. Credenciales rechazadas.")
            return None

        usuario_auth = respuesta.json()

        if usuario_auth.get("localId") != documento.id:
            print("7. Los UID no coinciden.")
            return None

        nombre = datos.get("nombre")
        rol = datos.get("rol")

        if rol not in ("administrador", "empleado", "proveedor"):
            print("8. Rol no válido.")
            return None

        print("9. Inicio de sesión exitoso.")
        return nombre, rol

    except requests.RequestException as error:
        raise Exception(
            "No se pudo conectar con Firebase Authentication."
        ) from error

    except Exception as error:
        print("ERROR EN AUTENTICAR:", repr(error))
        raise
# -----------------------------------------
# MOSTRAR CONTENIDO DE CADA SECCIÓN
# -----------------------------------------
def cambiar_vista(titulo, descripcion):
    for widget in area_contenido.winfo_children():
        widget.destroy()

    tk.Label(
        area_contenido,
        text=titulo,
        font=("Arial", 23, "bold"),
        fg="#17365D",
        bg="white"
    ).pack(anchor="w", padx=35, pady=(35, 15))

    tk.Label(
        area_contenido,
        text=descripcion,
        font=("Arial", 12),
        fg="#555555",
        bg="white",
        justify="left",
        wraplength=620
    ).pack(anchor="w", padx=35, pady=5)


# -----------------------------------------
# CREAR BOTÓN DEL MENÚ LATERAL
# -----------------------------------------
def crear_boton_menu(texto, titulo, descripcion, accion=None):
    boton = tk.Button(
        menu_lateral,
        text=texto,
        font=("Arial", 11),
        bg="#17365D",
        fg="white",
        activebackground="#2874A6",
        activeforeground="white",
        relief="flat",
        anchor="w",
        padx=20,
        pady=12,
        command=accion if accion else
        lambda: cambiar_vista(titulo, descripcion)
    )
    boton.pack(fill="x", padx=10, pady=3)


# -----------------------------------------
# PANEL PRINCIPAL SEGÚN EL ROL
# -----------------------------------------
def mostrar_panel(nombre, rol):
    for widget in ventana.winfo_children():
        widget.destroy()

    ventana.unbind("<Return>")
    ventana.title("Sistema de Gestión de Libros")
    ventana.geometry("1000x600")
    ventana.minsize(850, 500)
    ventana.resizable(True, True)

    global menu_lateral, area_contenido

    # Menú lateral izquierdo
    menu_lateral = tk.Frame(
        ventana,
        bg="#17365D",
        width=230
    )
    menu_lateral.pack(side="left", fill="y")
    menu_lateral.pack_propagate(False)

    tk.Label(
        menu_lateral,
        text="GESTIÓN\nDE LIBROS",
        font=("Arial", 19, "bold"),
        fg="white",
        bg="#17365D",
        justify="center"
    ).pack(pady=(30, 10))

    tk.Label(
        menu_lateral,
        text=f"Usuario: {nombre}",
        font=("Arial", 10),
        fg="#D6EAF8",
        bg="#17365D",
        wraplength=200
    ).pack(pady=(5, 20))

    tk.Label(
        menu_lateral,
        text=f"ROL: {rol.upper()}",
        font=("Arial", 10, "bold"),
        fg="#AED6F1",
        bg="#17365D"
    ).pack(pady=(0, 20))

    # Área de contenido a la derecha
    area_contenido = tk.Frame(
        ventana,
        bg="white"
    )
    area_contenido.pack(side="right", fill="both", expand=True)

    # Opciones según el rol
    if rol == "administrador":
        crear_boton_menu(
            "Inicio",
            "Panel del administrador",
            "Bienvenido al sistema. Desde aquí podrás administrar los libros, "
            "proveedores, entradas, inventario y ventas."
        )
        crear_boton_menu(
            "Registrar libros",
            "Registrar libros",
            "Formulario para agregar libros a la base de datos.",
             accion=lambda: mostrar_formulario_libro(area_contenido)
        )



        crear_boton_menu(
            "Proveedores",
            "Gestión de proveedores",
            "Aquí podrás registrar y consultar los proveedores de la empresa."
        )

        crear_boton_menu(
            "Entradas de libros",
            "Entradas de inventario",
            "Aquí registraremos los libros que entregan los proveedores "
            "y aumentaremos las existencias."
        )

        crear_boton_menu(
            "Consultar inventario",
            "Inventario de libros",
            "Aquí podrás consultar los libros disponibles y sus cantidades."
        )

        crear_boton_menu(
            "Ventas",
            "Consulta de ventas",
            "Aquí podrás consultar las ventas registradas por los empleados."
        )

    elif rol == "empleado":
        crear_boton_menu(
            "Inicio",
            "Panel del empleado",
            "Bienvenido. Desde aquí podrás acceder a las funciones de ventas."
        )

        crear_boton_menu(
            "Registrar venta",
            "Registrar venta",
            "Aquí construiremos el formulario para registrar libros vendidos "
            "y descontar las cantidades del inventario."
        )

        crear_boton_menu(
            "Consultar inventario",
            "Inventario de libros",
            "Aquí podrás consultar los libros disponibles."
        )

    elif rol == "proveedor":
        crear_boton_menu(
            "Inicio",
            "Panel del proveedor",
            "Bienvenido. Desde aquí podrás acceder a las funciones de entregas."
        )

        crear_boton_menu(
            "Registrar entrega",
            "Registrar entrega de libros",
            "Aquí construiremos la sección para registrar los libros "
            "entregados a la empresa."
        )

    else:
        messagebox.showerror("Error", "El rol del usuario no es válido.")
        mostrar_login()
        return

    # Botón para cerrar sesión
    tk.Button(
        menu_lateral,
        text="Cerrar sesión",
        font=("Arial", 11, "bold"),
        bg="#C0392B",
        fg="white",
        activebackground="#922B21",
        activeforeground="white",
        relief="flat",
        command=mostrar_login
    ).pack(side="bottom", fill="x", padx=10, pady=20)

    # Vista inicial
    cambiar_vista(
        f"Bienvenido, {nombre}",
        "Selecciona una opción del menú de la izquierda para comenzar."
    )


# -----------------------------------------
# REGRESAR AL INICIO DE SESIÓN
# -----------------------------------------
def mostrar_login():
    for widget in ventana.winfo_children():
        widget.destroy()

    construir_login()


# -----------------------------------------
# INICIAR SESIÓN
# -----------------------------------------
def iniciar_sesion():
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get()

    if not usuario or not contrasena:
        messagebox.showwarning(
            "Datos incompletos",
            "Debes ingresar usuario y contraseña."
        )
        return

    boton_login.config(state="disabled", text="CONECTANDO...")

    def ejecutar_autenticacion():
        try:
            resultado = autenticar(usuario, contrasena)
            error = None

        except Exception as excepcion:
            resultado = None
            error = str(excepcion)

        ventana.after(
            0,
            lambda: finalizar_autenticacion(resultado, error)
        )

    threading.Thread(
        target=ejecutar_autenticacion,
        daemon=True
    ).start()


def finalizar_autenticacion(resultado, error):
    if not ventana.winfo_exists():
        return

    boton_login.config(state="normal", text="INICIAR SESIÓN")

    if error:
        messagebox.showerror(
            "Error de conexión",
            error
        )
        return

    if resultado:
        nombre, rol = resultado
        mostrar_panel(nombre, rol)

    else:
        messagebox.showerror(
            "Acceso denegado",
            "Usuario o contraseña incorrectos."
        )
        entrada_contrasena.delete(0, tk.END)


# -----------------------------------------
# CONSTRUIR INICIO DE SESIÓN
# -----------------------------------------
def construir_login():
    global entrada_usuario, entrada_contrasena

    ventana.title("Inicio de sesión - Gestión de Libros")
    ventana.geometry("500x430")
    ventana.resizable(False, False)

    titulo = tk.Label(
        ventana,
        text="GESTIÓN DE LIBROS",
        font=("Arial", 23, "bold"),
        fg="#17365D"
    )
    titulo.pack(pady=30)

    tk.Label(
        ventana,
        text="Inicia sesión para continuar",
        font=("Arial", 12)
    ).pack(pady=5)

    tk.Label(
        ventana,
        text="Usuario:",
        font=("Arial", 12)
    ).pack(pady=(20, 5))

    entrada_usuario = tk.Entry(
        ventana,
        font=("Arial", 13),
        width=30
    )
    entrada_usuario.pack()

    tk.Label(
        ventana,
        text="Contraseña:",
        font=("Arial", 12)
    ).pack(pady=(15, 5))

    entrada_contrasena = tk.Entry(
        ventana,
        font=("Arial", 13),
        width=30,
        show="*"
    )
    entrada_contrasena.pack()

    global boton_login

    boton_login = tk.Button(
        ventana,
        text="INICIAR SESIÓN",
        font=("Arial", 12, "bold"),
        bg="#2874A6",
        fg="white",
        width=22,
        command=iniciar_sesion
    )
    boton_login.pack(pady=30)

    ventana.bind("<Return>", lambda event: iniciar_sesion())
    entrada_usuario.focus()


# -----------------------------------------
# INICIAR APLICACIÓN
# -----------------------------------------
ventana = tk.Tk()
construir_login()
ventana.mainloop()