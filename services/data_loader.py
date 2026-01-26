import csv
from domain.cambio import Cambio

class CSVLoader:

    def cargar_cambios(self, ruta_csv):
        cambios = []

        with open(ruta_csv, newline='', encoding='utf-8-sig') as archivo:
            reader = csv.DictReader(archivo, delimiter=';')

            columnas = reader.fieldnames
            esperadas = [
                "codigo", "nombre", "fecha_ejecucion", "descripcion",
                "entidad", "lider", "cargo_lider", "plataforma", "crm"
            ]

            if columnas != esperadas:
                raise ValueError(f"Columnas incorrectas: {columnas}")

            for i, fila in enumerate(reader, start=1):
                cambio = Cambio(
                    codigo=fila["codigo"].strip(),
                    nombre=fila["nombre"].strip(),
                    fecha_ejecucion=fila["fecha_ejecucion"].strip(),
                    descripcion=fila["descripcion"].strip(),
                    entidad=fila["entidad"].strip(),
                    lider=fila["lider"].strip(),
                    cargo_lider=fila["cargo_lider"].strip(),
                    plataforma=fila["plataforma"].strip(),
                    crm=fila["crm"].strip()
                )

                cambio.n = i
                cambios.append(cambio)

        return cambios
