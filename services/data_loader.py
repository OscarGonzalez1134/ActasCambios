import pandas as pd
from domain.cambio import Cambio

class ExcelLoader:
    
    def cargar_cambios(self, ruta_excel):
        cambios = []
        
        # Leemos el archivo xlsm. Por defecto lee la primera hoja.
        # engine='openpyxl' es necesario para archivos .xlsm / .xlsx
        df = pd.read_excel(ruta_excel, engine='openpyxl', sheet_name="Data")

        # Definimos las columnas esperadas
        esperadas = [
            "codigo", "nombre", "fecha_ejecucion", "descripcion",
            "entidad", "lider", "cargo_lider", "plataforma", "crm"
        ]

        # Validamos que todas las columnas necesarias existan (independientemente del orden)
        columnas_actuales = df.columns.tolist()
        if not all(col in columnas_actuales for col in esperadas):
            raise ValueError(f"Columnas incorrectas. Se esperaba: {esperadas}")

        # Iteramos sobre las filas del DataFrame
        # itertuples es más rápido que iterrows para estos casos
        for i, fila in enumerate(df.itertuples(index=False), start=1):
            # Convertimos la fila a diccionario para facilitar el acceso por nombre
            datos = fila._asdict()
            
            cambio = Cambio(
                codigo=str(datos["codigo"]).strip(),
                nombre=str(datos["nombre"]).strip(),
                fecha_ejecucion=str(datos["fecha_ejecucion"]).strip(),
                descripcion=str(datos["descripcion"]).strip(),
                entidad=str(datos["entidad"]).strip(),
                lider=str(datos["lider"]).strip(),
                cargo_lider=str(datos["cargo_lider"]).strip(),
                plataforma=str(datos["plataforma"]).strip(),
                crm=str(datos["crm"]).strip()
            )

            cambio.n = i
            cambios.append(cambio)

        return cambios
