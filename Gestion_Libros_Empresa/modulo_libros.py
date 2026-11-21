
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


RUTA_DB = Path(__file__).resolve().parent / "data" / "gestion_libros.db"


def mostrar_formulario_libro(area_contenido):

    # Limpiar el contenido anterior
    for widget in area_contenido.winfo_children():
        widget.destroy()

    area_contenido.configure(bg="white")

    tk.Label(
        area_contenido,
        text="REGISTRAR LIBRO",
        font=("Arial", 23, "bold"),
        fg="#17365D",
        bg="white"
    ).pack(anchor="w", padx=35, pady=(30, 10))

    tk.Label(
        area_contenido,
        text="Completa los datos del nuevo libro.",
        font=("Arial", 11),
        fg="#555555",
        bg="white"
    ).pack(anchor="w", padx=35, pady=(0, 20))

    formulario = tk.Frame(area_contenido, bg="white")
    formulario.pack(anchor="w", padx=35)

    entradas = {}

    campos = [
        ("Título:", "titulo"),
        ("Autor:", "autor"),
        ("Editorial:", "editorial"),
        ("ISBN (opcional):", "isbn"),
        ("Precio:", "precio")
    ]

    for fila, (etiqueta, clave) in enumerate(campos):
        tk.Label(
            formulario,
            text=etiqueta,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#17365D"
        ).grid(row=fila, column=0, sticky="w", pady=9)

        entrada = tk.Entry(
            formulario,
            font=("Arial", 11),
            width=38
        )
        entrada.grid(row=fila, column=1, padx=15, pady=9)

        entradas[clave] = entrada

    def guardar_libro():

        titulo = entradas["titulo"].get().strip()
        autor = entradas["autor"].get().strip()
        editorial = entradas["editorial"].get().strip()
        isbn = entradas["isbn"].get().strip()
        precio_texto = entradas["precio"].get().strip()

        if not titulo or not autor or not precio_texto:
            messagebox.showwarning(
                "Datos incompletos",
                "Debes ingresar el título, el autor y el precio."
            )
            return

        try:
            precio = float(precio_texto.replace(",", "."))

            if precio < 0:
                messagebox.showwarning(
                    "Precio incorrecto",
                    "El precio no puede ser negativo."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Precio incorrecto",
                "Escribe un precio válido. Ejemplo: 35000"
            )
            return

        try:
            with sqlite3.connect(RUTA_DB) as conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    INSERT INTO libros
                    (titulo, autor, editorial, isbn, precio, stock)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (
                    titulo,
                    autor,
                    editorial,
                    isbn if isbn else None,
                    precio
                ))

            messagebox.showinfo(
                "Registro exitoso",
                f"El libro '{titulo}' fue registrado correctamente."
            )

            # Limpiar los campos después de guardar
            for entrada in entradas.values():
                entrada.delete(0, tk.END)

            entradas["titulo"].focus()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "ISBN duplicado",
                "Ya existe un libro registrado con ese ISBN."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudo registrar el libro:\n{error}"
            )

    tk.Button(
        area_contenido,
        text="GUARDAR LIBRO",
        font=("Arial", 11, "bold"),
        bg="#2874A6",
        fg="white",
        activebackground="#1B4F72",
        activeforeground="white",
        relief="flat",
        padx=20,
        pady=10,
        command=guardar_libro
    ).pack(anchor="w", padx=35, pady=25)

    tk.Label(
        area_contenido,
        text="Nota: el libro se registra con existencias en cero. "
             "Las cantidades se agregarán al registrar entradas.",
        font=("Arial", 9),
        fg="#777777",
        bg="white",
        wraplength=650
    ).pack(anchor="w", padx=35)
