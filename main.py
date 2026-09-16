import tkinter as tk
from tkinter import ttk

from interfaz.formulario_generico import FormularioGenerico
from modelos.gasto import Gasto
from modelos.ingreso import Ingreso


def iniciar_aplicacion():

    ventana = tk.Tk()

    ventana.title("Gestión Financiera")
    ventana.geometry("800x600")

    pestañas = ttk.Notebook(ventana)
    pestañas.pack(
        fill="both",
        expand=True
    )

    pestaña_gastos = ttk.Frame(pestañas)
    pestaña_ingresos = ttk.Frame(pestañas)

    pestañas.add(
        pestaña_gastos,
        text="Gastos"
    )

    pestañas.add(
        pestaña_ingresos,
        text="Ingresos"
    )

    FormularioGenerico(
        pestaña_gastos,
        Gasto
    )

    FormularioGenerico(
        pestaña_ingresos,
        Ingreso
    )

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()