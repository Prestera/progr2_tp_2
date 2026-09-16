import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from repositorios.repositorio_generico import RepositorioGenerico


class FormularioGenerico:

    def __init__(self, ventana, modelo):

        self.ventana = ventana
        self.modelo = modelo
        self.campos = modelo.campos

        self.entradas = {}
        self.id_seleccionado = None

        self.repositorio = RepositorioGenerico(modelo)

        self.crear_interfaz()
        self.mostrar_registros()

  
    def crear_interfaz(self):

        # FORMULARIO

        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

        for fila, (nombre, etiqueta) in enumerate(self.campos):

            tk.Label(
                formulario,
                text=etiqueta
            ).grid(
                row=fila,
                column=0,
                padx=5,
                pady=5,
                sticky="e"
            )

            entrada = tk.Entry(formulario)

            entrada.grid(
                row=fila,
                column=1,
                padx=5,
                pady=5
            )

            # Guardamos el Entry en el diccionario
            self.entradas[nombre] = entrada

        # BOTONES
        
        botones = tk.Frame(self.ventana)
        botones.pack(pady=10)

        tk.Button(
            botones,
            text="Agregar",
            command=self.agregar
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            botones,
            text="Modificar",
            command=self.modificar
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            botones,
            text="Eliminar",
            command=self.eliminar
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(
            botones,
            text="Limpiar",
            command=self.limpiar
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # TABLA    

        columnas = ["id"]

        for nombre, etiqueta in self.campos:
            columnas.append(nombre)

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=columnas,
            show="headings"
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Columna ID
        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.column(
            "id",
            width=50
        )

        # Columnas de los campos
        for nombre, etiqueta in self.campos:

            self.tabla.heading(
                nombre,
                text=etiqueta
            )

            self.tabla.column(
                nombre,
                width=120
            )

        # Detectar selección de una fila
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_registro
        )

    
    # VALIDAR DATOS

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
                        "El monto debe ser mayor a 0."
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

             
                # La fecha no puede ser futura
                if fecha > datetime.now():

                    messagebox.showwarning(
                        "Validación",
                        "La fecha no puede ser futura."
                    )

                    return None

                # Guardamos la fecha en formato YYYY-MM-DD
                datos["fecha"] = fecha.strftime(
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showwarning(
                    "Validación",
                    "La fecha debe tener el formato DD/MM/AAAA y ser una fecha válida."
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


    # MOSTRAR REGISTROS

    def mostrar_registros(self):

        # Eliminar las filas actuales
        for fila in self.tabla.get_children():

            self.tabla.delete(fila)

        registros = self.repositorio.listar()

        for registro in registros:

            valores = [
                registro["id"]
            ]

            for nombre, etiqueta in self.campos:

                valor = registro[nombre]

                # Mostrar las fechas como DD/MM/AAAA
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

    # SELECCIONAR REGISTRO

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

        # Guardamos el ID seleccionado
        self.id_seleccionado = valores[0]

        # Cargamos los datos en los Entry
        for posicion, (nombre, etiqueta) in enumerate(self.campos):

            valor = valores[posicion + 1]

            self.entradas[nombre].delete(
                0,
                tk.END
            )

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

        for entrada in self.entradas.values():
            entrada.delete(
                0,
                tk.END
            )

        self.id_seleccionado = None

        # Quitar selección de la tabla
        seleccion = self.tabla.selection()

        if seleccion:

            self.tabla.selection_remove(
                seleccion
            )