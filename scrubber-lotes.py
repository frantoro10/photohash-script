import os
from PIL import Image, ImageEnhance
import uuid
import random
from datetime import datetime # <--- Nueva importación

def obtener_valores_unicos(n, minimo, maximo):
    valores = set()
    while len(valores) < n:
        val = round(random.uniform(minimo, maximo), 4)
        valores.add(val)
    lista = list(valores)
    random.shuffle(lista)
    return lista

def procesar_por_lotes_unicos(directorio_origen, directorio_destino_base, cantidad_lotes=5):
    extensiones_validas = ('.jpg', '.jpeg', '.png', '.webp')
    
    # 1. Generamos un timestamp para esta ejecución (Ej: 20251231_1840)
    # Esto asegura que cada "corrida" del script sea única
    timestamp_ejecucion = datetime.now().strftime("%Y%m%d_%H%M")

    # 2. Listar imágenes originales
    try:
        archivos = [f for f in os.listdir(directorio_origen) if f.lower().endswith(extensiones_validas)]
    except FileNotFoundError:
        print(f" Error: No se encontró la carpeta {directorio_origen}")
        return

    print(f"🚀 Iniciando sesión de procesamiento: {timestamp_ejecucion}")

    for archivo in archivos:
        ruta_origen = os.path.join(directorio_origen, archivo)
        nombre_base = os.path.splitext(archivo)[0]

        brillos = obtener_valores_unicos(cantidad_lotes, 0.97, 1.03)
        contrastes = obtener_valores_unicos(cantidad_lotes, 0.97, 1.03)
        nitideces = obtener_valores_unicos(cantidad_lotes, 0.95, 1.05)

        for i in range(cantidad_lotes):
            try:
                # 3. Crear la carpeta del lote si no existe
                carpeta_lote = os.path.join(directorio_destino_base, f"Lote_{i+1}")
                os.makedirs(carpeta_lote, exist_ok=True)

                img = Image.open(ruta_origen).convert('RGB')
                
                # Variaciones (la lógica que ya tenías)
                img = ImageEnhance.Brightness(img).enhance(brillos[i])
                img = ImageEnhance.Contrast(img).enhance(contrastes[i])
                img = ImageEnhance.Sharpness(img).enhance(nitideces[i])
                img = img.rotate(random.uniform(-0.4, 0.4))

                # 4. NOMBRE ÚNICO: Incluimos el timestamp y un hash corto
                # Ejemplo: anillo-plata_20251231_v1_a1b2.jpg
                hash_corto = uuid.uuid4().hex[:4]
                nombre_final = f"{nombre_base}_{timestamp_ejecucion}_v{i+1}_{hash_corto}.jpg" 
                ruta_final = os.path.join(carpeta_lote, nombre_final)
                
                img.save(ruta_final, "JPEG", quality=random.randint(94, 97))
            except Exception as e:
                print(f" Error con {archivo} en Lote {i+1}: {e}")

    print(f"\n✨ ¡Proceso terminado! Revisá la carpeta '{directorio_destino_base}'.")

# --- CONFIGURACIÓN ---
ORIGEN = "assets/stock"
DESTINO = "fb-lotes"

procesar_por_lotes_unicos(ORIGEN, DESTINO, 5)