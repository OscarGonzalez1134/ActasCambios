

class Cambio:
    def __init__(self, codigo, nombre, fecha_ejecucion, descripcion,
                 entidad, solicitante, plataforma, crm):

        self.codigo = codigo
        self.nombre = nombre
        self.fecha_ejecucion = fecha_ejecucion
        self.descripcion = descripcion
        self.entidad = entidad
        self.solicitante = solicitante
        self.plataforma = plataforma
        self.crm = crm

    def validar(self): 
        return all([
            self.codigo,
            self.nombre,
            self.fecha_ejecucion,
            self.descripcion,
            self.entidad,
            self.solicitante,
            self.plataforma,
            self.crm
        ])
    

    def tema_acta(self, n):
        return {
            "n": n,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "entidad": self.entidad,
            "solicitante": self.solicitante
        }

    def bloque_narrativo(self, n):
        fecha_formateada = (
            self.fecha_ejecucion.strftime("%d/%m/%Y")
            if self.fecha_ejecucion
            else ""
        )

        return {
            "n": n,
            "codigo": self.codigo,
            "crm": self.crm,
            "nombre": self.nombre,
            "solicitante": self.solicitante,
            "descripcion": self.descripcion,
            "fecha": fecha_formateada,
            "plataforma": self.plataforma
        }

    def fila_resumen(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "solicitante": self.solicitante,
            "estado": "Aprobado"
        }
