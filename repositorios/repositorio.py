import sqlite3
import os


class Repositorio:
    def __init__(self, modelo):
        self.tabla = modelo.tabla
        # Crear la carpeta base_datos si no existe
        os.makedirs("base_datos", exist_ok=True)
        # Conectar con la base de datos
        self.conexion = sqlite3.connect(
            "base_datos/gestion_financiera.db"
        )
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conexion.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.tabla} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                monto REAL NOT NULL,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)
        self.conexion.commit()

    def crear(self, datos):
        cursor = self.conexion.cursor()
        cursor.execute(
            f"""
            INSERT INTO {self.tabla}
            (monto, fecha, descripcion)
            VALUES (?, ?, ?)
            """,
            (
                datos["monto"],
                datos["fecha"],
                datos["descripcion"]
            )
        )
        self.conexion.commit()

    def listar(self):
        cursor = self.conexion.cursor()
        cursor.execute(
            f"""
            SELECT id, monto, fecha, descripcion
            FROM {self.tabla}
            """
        )
        registros = cursor.fetchall()
        resultados = []
        for registro in registros:
            resultados.append({
                "id": registro[0],
                "monto": registro[1],
                "fecha": registro[2],
                "descripcion": registro[3]
            })
        return resultados

    def actualizar(self, id, datos):
        cursor = self.conexion.cursor()
        cursor.execute(
            f"""
            UPDATE {self.tabla}
            SET monto = ?,
                fecha = ?,
                descripcion = ?
            WHERE id = ?
            """,
            (
                datos["monto"],
                datos["fecha"],
                datos["descripcion"],
                id
            )
        )
        self.conexion.commit()

    def eliminar(self, id):
        cursor = self.conexion.cursor()
        cursor.execute(
            f"""
            DELETE FROM {self.tabla}
            WHERE id = ?
            """,
            (id,)
        )
        self.conexion.commit()