import tkinter as tk
from tkinter import ttk

from interfaz.formulario import Crud
from modelos.gasto import Gasto
from modelos.ingreso import Ingreso
from modelos.balance import Balance #Lo importamos al ser creado


def iniciar_aplicacion():
    ventana = tk.Tk()

    ventana.title("Gestión Financiera")
    ventana.geometry("500x400")

    pestañas = ttk.Notebook(ventana)
    pestañas.pack(
        fill="both",
        expand=True
    )

    pestaña_gastos = ttk.Frame(pestañas)
    pestaña_ingresos = ttk.Frame(pestañas)
    pestaña_balance = ttk.Frame(pestañas) #Agregado

    pestañas.add(
        pestaña_gastos,
        text="Gastos"
    )

    pestañas.add(
        pestaña_ingresos,
        text="Ingresos"
    )
    #Agregado
    pestañas.add(
            pestaña_balance,
            text="Balance"
        )

    Crud(
        pestaña_gastos,
        Gasto
    )

    Crud(
        pestaña_ingresos,
        Ingreso
    )
    #Agregado
    Crud(
        pestaña_balance,
        Balance
    )    
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()