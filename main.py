from datetime import datetime, timedelta

def main():

    parser = argparse.ArgumentParser(
        description="Generador automático de actas de comité de cambios"
    )

    parser.add_argument("csv")
    parser.add_argument("numero")
    parser.add_argument("--titulo", default="ACTA COMITÉ DE CAMBIOS")
    parser.add_argument("--salida", default="output/")
    parser.add_argument("--plantilla", default="templates/acta_cambios.docx")
    parser.add_argument("--lugar", default="WhatsApp")
    parser.add_argument("--dia", default=None)

    args = parser.parse_args()

    ruta_csv = Path(args.csv)
    salida = Path(args.salida)
    plantilla = Path(args.plantilla)

    titulo = args.titulo
    numeroActa = args.numero
    lugar = args.lugar

    if args.dia:
        dia = datetime.strptime(args.dia, "%Y-%m-%d")
    else:
        dia = datetime.now() - timedelta(days=1)

    salida.mkdir(exist_ok=True)

    print("Cargando cambios...")
    loader = ExcelLoader()
    cambios, solicitantes = loader.cargar_cambios(ruta_csv)

    print(f"{len(cambios)} cambios cargados")

    acta = ActaCambios(
        titulo=titulo,
        numero=numeroActa,
        lugar=lugar,
        fecha_actual=dia.strftime("%d/%m/%Y")
    )

    acta.agregar_solicitantes(solicitantes)

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