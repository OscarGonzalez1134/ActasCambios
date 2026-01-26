from domain.cambio import Cambio
from domain.acta import ActaCambios
from services.generador_word import GeneradorActaWord
from services.document_processor import DocumentProcessor
from datetime import date
from pathlib import Path

# ===== METADATOS DEL ACTA =====

acta = ActaCambios(
    titulo="ACTA DE COMITÉ DE CAMBIOS AJUSTE EN AMBIENTE PRODUCTIVO",
    numero="1390",
    fecha_actual=date.today().strftime("%d/%m/%Y"),
    lugar="WhatsApp"
)
"""
c1 = Cambio(
    codigo = "",
    nombre="",
    fecha_ejecucion="",
    descripcion="",
    entidad="",
    lider="",
    cargo_lider="",
    plataforma="",
    crm=""
)
"""
c1 = Cambio(
    codigo = "CB-NO-EX-N/A-77337-PDCL",
    nombre="Aplicación IC de parametrización nuevo BIN",
    fecha_ejecucion="23/01/2026",
    descripcion="a",
    entidad="BPO Banco Coopcentral",
    lider="Sebastián Fernandez",
    cargo_lider="Analista de certificación",
    plataforma="AS400",
    crm="77337"
)

c2 = Cambio(
    codigo = "CB-NO-EX-N/A-CRM77344-PRD",
    nombre="Actualización usuario de captura de novedades de afiliación",
    fecha_ejecucion="23/01/2026",
    descripcion=" a",
    entidad="BPO Banco Coopcentral",
    lider="Cesar Galán",
    cargo_lider="Analista de gestión de incidentes",
    plataforma="AS400",
    crm="77344"
)

c3 = Cambio(
    codigo = "CB-NO-EX-N/A-77355-PRD",
    nombre="Solicitud creación CRM - parametrización comisión consulta de saldo en cajeros",
    fecha_ejecucion="23/01/2026",
    descripcion="a ",
    entidad="BPO Ban 100",
    lider="Ángel Romero",
    cargo_lider="Analista de gestión de incidentes",
    plataforma="AS400",
    crm="77355"
)

acta.agregar_cambio(c1)
acta.agregar_cambio(c2)
acta.agregar_cambio(c3)


# ===== GENERAR DOCUMENTO =====
temp = Path("output/temp.docx")
final = Path(f"output/{acta.numero}.docx")

generador = GeneradorActaWord("templates/acta_cambios.docx")
procesador = DocumentProcessor()

generador.generar(acta, temp)
procesador.limpiar_filas_vacias(temp, final)

# borrar temporal
if temp.exists():
    temp.unlink()

print(f"Acta numero {acta.numero} generada correctamente.")
