import argparse
from pathlib import Path
from datetime import datetime, timedelta

from services.data_loader import ExcelLoader
from services.generador_word import GeneradorActaWord
from services.document_processor import DocumentProcessor
from domain.acta import ActaCambios

def main():

    parser = argparse.ArgumentParser(
        description="Generador automático de actas de comité de cambios"
    )

    parser.add_argument("entrada")
    parser.add_argument("numero")
    parser.add_argument("--titulo", default="ACTA COMITÉ DE CAMBIOS")
    parser.add_argument("--salida", default="output/")
    parser.add_argument("--plantilla", default="templates/acta_cambios.docx")
    parser.add_argument("--lugar", default="WhatsApp")
    parser.add_argument("--dia", default=None)

    args = parser.parse_args()

    ruta_csv = Path(args.entrada)
    salida = Path(args.salida)
    plantilla = Path(args.plantilla)

    titulo = args.titulo
    numeroActa = args.numero
    lugar = args.lugar

    if args.dia:
        try:
            # Formato esperado: 28/03/2026
            dia = datetime.strptime(args.dia, "%d/%m/%Y")
        except ValueError:
            try:
                # Formato alternativo: 2026-03-28
                dia = datetime.strptime(args.dia, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "Formato de fecha inválido. Use DD/MM/AAAA o YYYY-MM-DD"
                )
    else:
        dia = datetime.now() - timedelta(days=1)

    dia_formateado = dia.strftime("%d/%m/%Y")

    salida.mkdir(exist_ok=True)

    print("Cargando cambios...")
    loader = ExcelLoader()
    cambios, solicitantes = loader.cargar_cambios(ruta_csv)

    print(f"{len(cambios)} cambios cargados")

    acta = ActaCambios(
        titulo=titulo,
        numero=numeroActa,
        lugar=lugar,
        fecha_actual=dia_formateado
    )

    for c in cambios:
        acta.agregar_cambio(c)

    nombre_archivo = acta.numero + ".docx"
    temp = salida / ("temp_" + nombre_archivo)
    final = salida / nombre_archivo

    print("Generando acta...")
    generador = GeneradorActaWord(plantilla)
    generador.generar(acta, temp)

    print("Limpiando documento...")
    procesador = DocumentProcessor()
    procesador.limpiar_filas_vacias(temp, final)

    if final.exists():
        temp.unlink()
        print("Acta generada correctamente:")
        print(final)
    else:
        print("Error: no se pudo generar el acta final")

if __name__ == "__main__":
    main()