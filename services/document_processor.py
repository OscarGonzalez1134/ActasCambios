from docx import Document

class DocumentProcessor:
        
    def fila_vacia(self, row):
        texto = ""
        for cell in row.cells:
            texto += cell.text.strip()
        return texto == ""

    def limpiar_filas_vacias(self, ruta_entrada, ruta_salida):
        doc = Document(ruta_entrada)

        for table in doc.tables:
            filas_a_borrar = []
            for i, row in enumerate(table.rows):
                if self.fila_vacia(row):
                    filas_a_borrar.append(i)

            # borrar de abajo hacia arriba
            for i in reversed(filas_a_borrar):
                tbl = table._tbl
                tr = table.rows[i]._tr
                tbl.remove(tr)

        doc.save(ruta_salida)
