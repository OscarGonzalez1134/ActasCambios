import argparse
from pathlib import Path
from datetime import datetime

from services.data_loader import CSVLoader
from services.generador_word import GeneradorActaWord
from services.document_processor import DocumentProcessor
from domain.acta import ActaCambios

def main():
    parser = argparse.ArgumentParser(
        description="Generador automático de actas de comité de cambios"
    )

    parser.add_argument("csv", help="Ruta del archivo CSV con los cambios")
    parser.add_argument("--titulo", default="ACTA COMITÉ DE CAMBIOS")
    parser.add_argument("--salida", default="output/")
    parser.add_argument("--plantilla", default="templates/acta_cambios.docx")
    parser.add_argument("--lugar", default="WhatsApp")
    parser.add_argument("numero")

    args = parser.parse_args()

    titulo = Path(args.titulo)
    ruta_csv = Path(args.csv)
    salida = Path(args.salida)
    plantilla = Path(args.plantilla)
    numeroActa=str(Path(args.numero)).split("=")[-1]
    lugar=Path(args.lugar)

    salida.mkdir(exist_ok=True)

    print("Cargando cambios...")
    loader = CSVLoader()
    cambios = loader.cargar_cambios(ruta_csv)

    print(f"✔ {len(cambios)} cambios cargados")

    acta = ActaCambios(
        titulo=titulo,
        numero=numeroActa,
        lugar=lugar,
        fecha_actual=datetime.now().strftime("%Y-%m-%d")
    )

    for c in cambios:
        acta.agregar_cambio(c)

    nombre_archivo = acta.numero+".docx"# f"ACTA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    temp = salida / ("temp_" + nombre_archivo)
    final = salida / nombre_archivo

    print("📝 Generando acta...")
    generador = GeneradorActaWord(plantilla)
    generador.generar(acta, temp)

    print("🧹 Limpiando documento...")
    procesador = DocumentProcessor()
    procesador.limpiar_filas_vacias(temp, final)

    if final.exists():
        temp.unlink()
        print("✔ Acta generada correctamente:")
        print("   ", final)

    else:
        print("❌ Error: no se pudo generar el acta final")

if __name__ == "__main__":
    main()
