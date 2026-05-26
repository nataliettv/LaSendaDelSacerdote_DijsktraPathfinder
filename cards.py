#constantes y Utilidades sobre las cartas del juego

# identificadores especiales
APRENDIZ = 0          # la carta del Aprendiz vive en una posición de la senda.
DEIDAD = -1           # la Deidad NO ocupa una posición de la lista; siempre está al final de la senda. la representamos como -1 cuando necesitamos referirnos a ella

# clasificación de cartas 
MAESTROS = frozenset({5, 7, 8, 9, 10, 12, 13, 14})
FALSOS_MAESTROS = frozenset({1, 2, 3, 4, 6, 11})
ORDEN_FALSOS = (1, 2, 3, 4, 6, 11)

NOMBRES = {
    0:  "★ APRENDIZ ★",
    1:  "Duda",
    2:  "Rencor",
    3:  "Miedo",
    4:  "Pereza",
    5:  "Ejercicio",
    6:  "Cizañoso",
    7:  "Filosofía",
    8:  "Herbolaria",
    9:  "Meditación",
    10: "Oración",
    11: "Envidia",
    12: "Peregrino",
    13: "Magia",
    14: "Cuerpo Astral",
    15: "⏢ DEIDAD ⏢",
}

# estas funciones sirven para debug, no es parte de la lógica del juego lo que hacen es reconstruir y mostrar el paso a paso de una ronda completa, 
# mostrando la senda antes y después de la jugada del jugador, 
# y luego cada activación de los Falsos Maestros, para entender cómo se llega al estado final de la ronda.
def es_maestro(carta: int) -> bool:
    return carta in MAESTROS

def es_falso_maestro(carta: int) -> bool:
    return carta in FALSOS_MAESTROS

def nombre(carta: int) -> str:
    return NOMBRES.get(carta, str(carta))
