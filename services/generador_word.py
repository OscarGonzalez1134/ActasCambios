from docxtpl import DocxTemplate

class GeneradorActaWord:
    def __init__(self, ruta_plantilla):
        self.doc = DocxTemplate(ruta_plantilla)

    def generar(self, acta, ruta_salida):

        context = {
            "titulo": acta.titulo,
            "numero": acta.numero,
            "fecha": acta.fecha_actual,
            "lugar": acta.lugar,
            "temas": [c.tema_acta(i+1) for i, c in enumerate(acta.cambios)],
            "bloques": [c.bloque_narrativo(i+1) for i, c in enumerate(acta.cambios)],
            "resumen": [c.fila_resumen() for c in acta.cambios],
            "lideres": [c.datos_lider() for c in acta.cambios]
        }

        self.doc.render(context)
        self.doc.save(ruta_salida)
