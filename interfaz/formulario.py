import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry #Calendario

from repositorios.repositorio import Repositorio


class Crud:
    def __init__(self, ventana, modelo):
        self.ventana = ventana
        self.modelo = modelo
        self.campos = modelo.campos

        self.entradas = {}
        self.id_seleccionado = None

        self.repositorio = Repositorio(modelo)

        self.crear_interfaz()
        self.mostrar_registros()

    
    # INTERFAZ
    def crear_interfaz(self):

        # FORMULARIO
        
        formulario = ttk.LabelFrame(
            self.ventana,
            text="Datos",
            padding=10
        )

        formulario.pack(
            fill="x",
            padx=10,
            pady=10
        )

        for fila, (nombre, etiqueta) in enumerate(self.campos):
            ttk.Label(
                formulario,
                text=etiqueta
            ).grid(
                row=fila,
                column=0,
                padx=5,
                pady=5,
                sticky="e"
            )

            if nombre == "fecha":
                entrada = DateEntry(
                    formulario,
                    width=32,
                    date_pattern="dd/mm/yyyy"
                )

            else:
                entrada = ttk.Entry(
                    formulario,
                    width=35
                )

            entrada.grid(
                row=fila,
                column=1,
                padx=5,
                pady=5,
                sticky="w"
            )

            self.entradas[nombre] = entrada

        # BOTONES

        botones = ttk.Frame(
            self.ventana
        )

        botones.pack(
            pady=10
        )

        ttk.Button(
            botones,
            text="Agregar",
            command=self.agregar
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        ttk.Button(
            botones,
            text="Modificar",
            command=self.modificar
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        ttk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # TABLA

        tabla_frame = ttk.LabelFrame(
            self.ventana,
            text="Registros",
            padding=10
        )

        tabla_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columnas = ["id"]

        for nombre, etiqueta in self.campos:
            columnas.append(nombre)

        self.tabla = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        self.tabla.pack(
            fill="both",
            expand=True
        )

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.column(
            "id",
            width=50
        )

        for nombre, etiqueta in self.campos:
            self.tabla.heading(
                nombre,
                text=etiqueta
            )
            self.tabla.column(
                nombre,
                width=150
            )
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_registro
        )

    # VALIDACIONES
    def validar_datos(self):
        datos = {}

        # CAMPOS OBLIGATORIOS

        for nombre, etiqueta in self.campos:
            valor = self.entradas[nombre].get().strip()

            if valor == "":
                messagebox.showwarning(
                    "Validación",
                    f"El campo '{etiqueta}' es obligatorio."
                )
                return None

            datos[nombre] = valor

        # VALIDAR MONTO
        if "monto" in datos:
            try:
                monto = float(datos["monto"])

                if monto <= 0:
                    messagebox.showwarning(
                        "Validación",
                        "El monto debe ser mayor que 0."
                    )
                    return None
                datos["monto"] = monto
            except ValueError:
                messagebox.showwarning(
                    "Validación",
                    "El monto debe ser numérico."
                )
                return None

        # VALIDAR FECHA

        if "fecha" in datos:
            try:
                fecha = datetime.strptime(
                    datos["fecha"],
                    "%d/%m/%Y"
                )

                if fecha > datetime.now():
                    messagebox.showwarning(
                        "Validación",
                        "La fecha no puede ser futura."
                    )
                    return None

                datos["fecha"] = fecha.strftime(
                    "%Y-%m-%d"
                )
            except ValueError:
                messagebox.showwarning(
                    "Validación",
                    "La fecha no es válida."
                )
                return None
        return datos

    # AGREGAR
    def agregar(self):
        datos = self.validar_datos()

        if datos is None:
            return

        self.repositorio.crear(datos)

        messagebox.showinfo(
            "Éxito",
            "Registro agregado correctamente."
        )

        self.limpiar()
        self.mostrar_registros()

    # LISTAR
    
    def mostrar_registros(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = self.repositorio.listar()

        for registro in registros:
            valores = [
                registro["id"]
            ]

            for nombre, etiqueta in self.campos:
                valor = registro[nombre]
                if nombre == "fecha" and valor:
                    try:
                        fecha = datetime.strptime(
                            valor,
                            "%Y-%m-%d"
                        )

                        valor = fecha.strftime(
                            "%d/%m/%Y"
                        )
                    except ValueError:
                        pass

                valores.append(valor)

            self.tabla.insert(
                "",
                "end",
                values=valores
            )
    # SELECCIONAR

    def seleccionar_registro(self, evento):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        fila = self.tabla.item(
            seleccion[0]
        )

        valores = fila["values"]

        if not valores:
            return

        self.id_seleccionado = valores[0]
        
        for posicion, (nombre, etiqueta) in enumerate(self.campos):
            valor = valores[posicion + 1]
            self.entradas[nombre].set_date(
                valor
            ) if nombre == "fecha" else self.entradas[nombre].delete(
                0,
                tk.END
            )

            if nombre != "fecha":
                self.entradas[nombre].insert(
                    0,
                    valor
                )
    # MODIFICAR

    def modificar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Validación",
                "Seleccione un registro para modificar."
            )
            return

        datos = self.validar_datos()
        if datos is None:
            return

        self.repositorio.actualizar(
            self.id_seleccionado,
            datos
        )
        messagebox.showinfo(
            "Éxito",
            "Registro modificado correctamente."
        )
        self.limpiar()
        self.mostrar_registros()

    # ELIMINAR
    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "Validación",
                "Seleccione un registro para eliminar."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de eliminar el registro?"
        )

        if not confirmar:
            return

        self.repositorio.eliminar(
            self.id_seleccionado
        )

        messagebox.showinfo(
            "Éxito",
            "Registro eliminado correctamente."
        )

        self.limpiar()
        self.mostrar_registros()

       # LIMPIAR
  
    def limpiar(self):

        for nombre, entrada in self.entradas.items():

            if nombre == "fecha":

                entrada.set_date(
                    datetime.now()
                )

            else:

                entrada.delete(
                    0,
                    tk.END
                )

        self.id_seleccionado = None

        seleccion = self.tabla.selection()

        if seleccion:

            self.tabla.selection_remove(
                seleccion
            )