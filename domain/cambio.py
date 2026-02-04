class Cambio:
    def __init__(self, codigo, nombre, fecha_ejecucion, descripcion,
                 entidad, lider, cargo_lider, plataforma, crm):

        self.codigo = codigo
        self.nombre = nombre
        self.fecha_ejecucion = fecha_ejecucion
        self.descripcion = descripcion
        self.entidad = entidad
        self.lider = lider
        self.cargo_lider = cargo_lider
        self.plataforma = plataforma
        self.crm = crm

    def validar(self): 
        return all([
            self.codigo,
            self.nombre,
            self.fecha_ejecucion,
            self.descripcion,
            self.entidad,
            self.lider,
            self.cargo_lider,
            self.plataforma,
            self.crm
        ])
    
    def datos_lider(self):
        return {
            "nombre": self.lider,
            "cargo": self.cargo_lider
        }

    def tema_acta(self, n):
        return {
            "n": n,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "entidad": self.entidad,
            "lider": self.lider
        }

    def bloque_narrativo(self, n):
        return {
            "n": n,
            "codigo": self.codigo,
            "crm": self.crm,
            "nombre": self.nombre,
            "lider": self.lider,
            "descripcion": self.descripcion,
            "fecha": self.fecha_ejecucion,
            "plataforma": self.plataforma
        }

    def fila_resumen(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "solicitante": self.lider,
            "estado": "Aprobado"
        }
