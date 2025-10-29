from respuestas import RESPUESTAS
from menu import MENU_PRINCIPAL, RESPUESTAS_MENU
from tramites import SUBMENU_TRAMITES, RESPUESTAS_TRAMITES
from corrimiento_bt import RESPUESTAS_CORRIMIENTO_BT
from datetime import datetime
import unicodedata
import re
import pandas as pd

# URL pública de la pestaña "Copia de Expedientes" en formato CSV
URL_EXPEDIENTES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-SqDDf8sr4Ip_cpL1Szp80HIsrVhqbYZToNEFroZO7_ZcOGlgqHl3nCZ08pvk6cIe1YdfZpOLozVi/pub?gid=1687177676&single=true&output=csv"

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.strip().rstrip(".")

# Diccionarios normalizados
RESPUESTAS_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS.items()}
RESPUESTAS_MENU_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS_MENU.items()}
RESPUESTAS_TRAMITES_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS_TRAMITES.items()}
RESPUESTAS_CORRIMIENTO_BT_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS_CORRIMIENTO_BT.items()}

# Mapeo de estados a columnas de fecha
ESTADO_FECHA_COLUMNAS = {
    "OFICINA COMERCIAL": 9,     # Columna J
    "RA EJECUCIÓN": 10,         # Columna K
    "REALIZADO": 11,            # Columna L
    "RA NORMALIZAR": 12,        # Columna M
    "FINALIZADO": 13            # Columna N
}

# Glosa explicativa por estado
GLOSA_ESTADO = {
    "OFICINA COMERCIAL": "Informe elaborado desde UT Mantenimiento de Redes hacia la oficina comercial correspondiente.",
    "RA EJECUCIÓN": "Pedido elaborado desde UT Mantenimiento de Redes hacia el sector Redes Aéreas para ejecutar el corrimiento.",
    "REALIZADO": "El sector Redes Aéreas informó que la LABT se encuentra alejada de la Línea Municipal.",
    "RA NORMALIZAR": "Pedido elaborado desde UT Mantenimiento de Redes hacia el sector Redes Aéreas para normalizar la LABT a su electroducto original.",
    "FINALIZADO": "El trámite fue enviado a su oficina comercial inicializadora para archivo definitivo."
}

def consultar_expediente(numero_expediente):
    try:
        df = pd.read_csv(URL_EXPEDIENTES)
        fila = df[df.iloc[:, 0] == numero_expediente]  # Columna A

        if not fila.empty:
            direccion = fila.iloc[0, 4]  # Columna E
            estado = fila.iloc[0, 3]     # Columna D
            estado_normalizado = estado.strip().upper()

            # Buscar fecha según estado
            columna_fecha = ESTADO_FECHA_COLUMNAS.get(estado_normalizado, None)
            if columna_fecha is not None:
                fecha = fila.iloc[0, columna_fecha]
                fecha = fecha if pd.notna(fecha) and str(fecha).strip() else "Sin especificar"
                glosa = GLOSA_ESTADO.get(estado_normalizado, "")
            else:
                fecha = "Sin especificar"
                glosa = ""

            return f"""Expediente N° {numero_expediente}
 • Dirección: {direccion}
 • Estado: {estado}
 • Fecha asociada: {fecha}
 • Significado del estado: {glosa}"""
        else:
            return f"Expediente N° {numero_expediente} no encontrado."
    except Exception as e:
        return f"No se pudo acceder a la base de expedientes. Verificá la conexión o el número ingresado."

def responder(mensaje):
    mensaje = normalizar(mensaje)

    # Consulta directa por número de expediente (formato: 1-2025-1234567)
    match = re.search(r"\b\d{1,4}-\d{4}-\d+\b", mensaje)
    if match:
        numero = match.group(0)
        return consultar_expediente(numero)

    # Saludo inicial → presentación institucional + menú
    if mensaje in ["hola", "buenas", "inicio", "menu", "menú"]:
        return "¡Hola! Mi nombre es SophIA, asistente virtual de la Empresa Provincial de la Energía Santa Fe. ¿Cómo puedo ayudarte? 😊<br><br>" + MENU_PRINCIPAL

    # Trámite frecuente (opción 3 del menú principal)
    if mensaje == "3":
        return SUBMENU_TRAMITES

    # Subtrámite dentro de trámites frecuentes (letras)
    if mensaje in RESPUESTAS_TRAMITES_NORMALIZADAS:
        return RESPUESTAS_TRAMITES_NORMALIZADAS[mensaje] + "<br><br>↩️ Escribí 'volver' para ver el menú principal."

    # Retorno al menú principal
    if mensaje == "volver":
        return "🔁 Volvemos al menú principal.<br><br>" + MENU_PRINCIPAL

    # Opción del menú principal (números)
    if mensaje in RESPUESTAS_MENU_NORMALIZADAS:
        return RESPUESTAS_MENU_NORMALIZADAS[mensaje]

    # Detección de palabras clave
    if any(palabra in mensaje for palabra in ["hora", "horario", "atencion"]):
        return "Nuestro horario de atención es de Lunes a Viernes de 7 a 14 hs."

    # Coincidencias generales
    for clave_normalizada in RESPUESTAS_NORMALIZADAS:
        if clave_normalizada in mensaje:
            return RESPUESTAS_NORMALIZADAS[clave_normalizada]

    # Coincidencias específicas: corrimiento de línea BT
    for clave_bt in RESPUESTAS_CORRIMIENTO_BT_NORMALIZADAS:
        if clave_bt in mensaje:
            return RESPUESTAS_CORRIMIENTO_BT_NORMALIZADAS[clave_bt]

    return "No entiendo lo que decís. Escribí 'volver' para ver el menú principal."
