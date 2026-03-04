import whisper
import os
from pathlib import Path


class TranscriptorAudio:
    """
    Clase responsable de transcribir archivos de audio a texto.
    Sigue el principio de responsabilidad única: solo se encarga de la transcripción.
    """
    
    def __init__(self, modelo="base", idioma="es"):
        """
        Constructor: se ejecuta cuando creamos una instancia de la clase.
        Aquí configuramos las propiedades iniciales y cargamos el modelo.
        """
        self.modelo_nombre = modelo
        self.idioma = idioma
        self.modelo = None  # Aún no cargamos el modelo en memoria
        
    def cargar_modelo(self):
        """
        Carga el modelo de Whisper en memoria.
        Lo hacemos en un método separado porque es una operación pesada
        y queremos controlar CUÁNDO ocurre.
        """
        if self.modelo is None:
            print(f"🧠 Cargando modelo '{self.modelo_nombre}' en memoria...")
            self.modelo = whisper.load_model(self.modelo_nombre)
            print("✅ Modelo listo")
        return self.modelo
    
    def transcribir(self, ruta_audio):
        """
        Método principal: toma una ruta de audio y devuelve el texto.
        Separa la lógica de 'obtener texto' de la lógica de 'guardar archivo'.
        """
        # Validación: ¿existe el archivo?
        if not os.path.exists(ruta_audio):
            raise FileNotFoundError(f"No existe: {ruta_audio}")
        
        # Cargamos modelo si no está cargado
        modelo = self.cargar_modelo()
        
        print(f"🎧 Procesando: {os.path.basename(ruta_audio)}")
        
        # Llamada a la librería Whisper
        resultado = modelo.transcribe(
            audio=ruta_audio,
            language=self.idioma,
            verbose=False  # Silenciamos logs internos de Whisper
        )
        
        return resultado
    
    def extraer_texto_plano(self, resultado_whisper):
        """
        Extrae solo el texto completo del resultado de Whisper.
        Whisper devuelve un diccionario con mucha info; nosotros solo queremos el texto.
        """
        return resultado_whisper["text"].strip()


class GestorArchivos:
    """
    Clase responsable de todas las operaciones de archivos.
    Separa la lógica de 'manejar archivos' de la lógica de 'transcribir'.
    """
    
    def __init__(self, carpeta_salida=None):
        self.carpeta_salida = carpeta_salida or os.getcwd()
    
    def generar_ruta_txt(self, ruta_audio):
        """
        Genera automáticamente la ruta de salida .txt basada en el nombre del audio.
        Ejemplo: 'mi_audio.ogg' → 'mi_audio.txt'
        """
        nombre_base = Path(ruta_audio).stem  # Nombre sin extensión
        ruta_salida = os.path.join(self.carpeta_salida, f"{nombre_base}.txt")
        return ruta_salida
    
    def guardar_texto(self, texto, ruta_destino):
        """
        Guarda el texto en un archivo con codificación UTF-8 (soporta ñ, tildes, etc.)
        """
        with open(ruta_destino, "w", encoding="utf-8") as archivo:
            archivo.write(texto)
        return ruta_destino
    
    def listar_audios_ogg(self, carpeta):
        """
        Devuelve lista de archivos .ogg en una carpeta.
        """
        return [f for f in os.listdir(carpeta) if f.endswith('.ogg')]


class PipelineTranscripcion:
    """
    Clase orquestadora: coordina al TranscriptorAudio y al GestorArchivos.
    Es la interfaz principal que usará el usuario.
    Implementa el patrón Facade (fachada): simplifica un sistema complejo.
    """
    
    def __init__(self, modelo="base", idioma="es", carpeta_salida=None):
        # Composición: creamos instancias de las otras clases
        self.transcriptor = TranscriptorAudio(modelo, idioma)
        self.gestor = GestorArchivos(carpeta_salida)
    
    def procesar_archivo(self, ruta_audio, ruta_salida=None):
        """
        Flujo completo para un solo archivo: transcribe y guarda.
        """
        # Paso 1: Transcribir
        resultado = self.transcriptor.transcribir(ruta_audio)
        texto = self.transcriptor.extraer_texto_plano(resultado)
        
        # Paso 2: Determinar dónde guardar
        if ruta_salida is None:
            ruta_salida = self.gestor.generar_ruta_txt(ruta_audio)
        
        # Paso 3: Guardar
        self.gestor.guardar_texto(texto, ruta_salida)
        
        return {
            "texto": texto,
            "ruta_txt": ruta_salida,
            "duracion_audio": resultado.get("duration")
        }
    
    def procesar_carpeta(self, carpeta_entrada):
        """
        Procesa todos los audios OGG de una carpeta.
        """
        archivos = self.gestor.listar_audios_ogg(carpeta_entrada)
        resultados = []
        
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_entrada, archivo)
            try:
                resultado = self.procesar_archivo(ruta_completa)
                resultados.append(resultado)
                print(f"✅ {archivo} → {resultado['ruta_txt']}")
            except Exception as e:
                print(f"❌ Error en {archivo}: {e}")
        
        return resultados


# ============ USO ============

if __name__ == "__main__":
    
    # Creamos una instancia del pipeline (orquestador principal)
    mi_pipeline = PipelineTranscripcion(
        modelo="base",      # Modelo de Whisper
        idioma="es",        # Español
        carpeta_salida="./transcripciones/"
    )
    
    # Procesar un solo archivo
    resultado = mi_pipeline.procesar_archivo("mi_audio.ogg")
    print(f"\nTexto transcrito:\n{resultado['texto'][:200]}...")

