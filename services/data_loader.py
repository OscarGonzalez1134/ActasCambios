import pandas as pd
from domain.cambio import Cambio
from domain.solicitante import Solicitante
class ExcelLoader:
    
    def cargar_cambios(self, ruta_excel):
        cambios = []
        solicitantes_dic = {} 
        
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
            
            nombre_lider = str(datos["lider"]).strip()
            cargo_lider = str(datos["cargo_lider"]).strip()
            
            clave = f"{nombre_lider.lower()}|{cargo_lider.lower()}"

            if clave not in solicitantes_dic:
                solicitantes_dic[clave] = Solicitante(nombre_lider, cargo_lider)

            solicitante = solicitantes_dic[clave]

            ## Fecha
            fecha_raw = datos["fecha_ejecucion"]
            if pd.isna(fecha_raw):
                fecha = None
            else:
                # Convertimos a datetime si viene como Timestamp
                fecha = pd.to_datetime(fecha_raw).to_pydatetime()


            cambio = Cambio(
                codigo=str(datos["codigo"]).strip(),
                nombre=str(datos["nombre"]).strip(),
                fecha_ejecucion=fecha,
                descripcion=str(datos["descripcion"]).strip(),
                entidad=str(datos["entidad"]).strip(),
                solicitante = solicitante,
                plataforma=str(datos["plataforma"]).strip(),
                crm=str(datos["crm"]).strip()
            )

            cambio.n = i
            cambios.append(cambio)

        return cambios, list(solicitantes_dic.values())
