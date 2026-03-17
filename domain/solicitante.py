class Solicitante:
    def __init__(self, nombre, cargo):
        self.nombre = nombre
        self.cargo = cargo

    def clave(self):
        return f"{self.nombre.strip().lower()}|{self.cargo.strip().lower()}"

    def __eq__(self, other):
        return isinstance(other, Solicitante) and self.clave() == other.clave()

    def __hash__(self):
        return hash(self.clave())