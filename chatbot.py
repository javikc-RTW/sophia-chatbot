from respuestas import RESPUESTAS
from menu import MENU_PRINCIPAL, RESPUESTAS_MENU
from tramites import SUBMENU_TRAMITES, RESPUESTAS_TRAMITES
from datetime import datetime
import unicodedata

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.strip().rstrip(".")

# Diccionarios normalizados
RESPUESTAS_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS.items()}
RESPUESTAS_MENU_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS_MENU.items()}
RESPUESTAS_TRAMITES_NORMALIZADAS = {normalizar(k): v for k, v in RESPUESTAS_TRAMITES.items()}

def responder(mensaje):
    mensaje = normalizar(mensaje)
    
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

    return "No entiendo lo que decís. Escribí 'volver' para ver el menú principal."
