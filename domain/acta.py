class ActaCambios:
    def __init__(self, titulo, numero, fecha_actual, lugar):
        self.titulo = titulo
        self.numero = numero
        self.fecha_actual = fecha_actual
        self.lugar = lugar
        self.cambios = []

    def agregar_cambio(self, cambio):
        if cambio.validar():
            self.cambios.append(cambio)
        else:
            raise ValueError("Cambio con datos incompletos")
