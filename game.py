#aqui esta la logica del juego: habilidades de cada carta y generación de sucesores

from typing import List, Tuple
from cards import APRENDIZ, ORDEN_FALSOS, es_maestro, nombre
from state import GameState
from utils import (
    Senda, indice_de, vecinos_validos, adyacente_min,
    intercambiar, destruir, mover_a, mover_a_inicio,
)

# HABILIDADES DE LOS MAESTROS

# EJERCICIO
# Intercambia de lugar con una carta de hasta 2 de distancia.
def hab_5_ejercicio(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in range(max(0, i - 2), min(len(senda), i + 3)):
        if j == i:
            continue
        res.append((f"EJERCICIO: INTERCAMBIA las cartas: {i} <-> {j}", intercambiar(senda, i, j)))
    return res

# FILOSOFIA
# 1) Una carta a 3 de distancia muevela 1 espacio
# 2) Una carta a 2 de distancia muevela 2 espacios
# 3) Una carta a 1 de distancia muevela 3 espacios
def hab_7_filosofia(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    mapa = {1: 3, 2: 2, 3: 1} #cuantos espacios mover la carta objetivo
    for dist_a_filosofia, pasos in mapa.items():
        for j in (i - dist_a_filosofia, i + dist_a_filosofia):
            if not (0 <= j < len(senda)):
                continue
            for direccion in (-pasos, +pasos):
                destino = j + direccion
                if 0 <= destino < len(senda):
                    nueva = mover_a(senda, j, destino)
                    res.append((
                        f"FILOSOFÍA: La carta {j} ({nombre(senda[j])}) que está a {dist_a_filosofia} de distancia de FILOSOFIA se mueve {direccion:+d}",
                        nueva
                    ))
    return res

# HERBOLARIA
# 1) Retrocede 1 carta adyacente 2 espacios
# 2) Adelanta 1 carta adyacente 1 espacio
def hab_8_herbolaria(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in vecinos_validos(senda, i):
        # 1)
        destino = j - 2
        if 0 <= destino < len(senda):
            res.append((
                f"HERBOLARIA: {nombre(senda[j])} en posición {j} retrocede 2 espacios",
                mover_a(senda, j, destino)
            ))
        # 2)
        destino = j + 1
        if 0 <= destino < len(senda):
            res.append((
                f"HERBOLARIA: {nombre(senda[j])} en posición {j} adelanta 1 espacio",
                mover_a(senda, j, destino)
            ))
    return res

# MEDITACIÓN
# Intercambia esta carta de lugar con otra que este exactamente a 3 espacios de distancia de esta
def hab_9_meditacion(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in (i - 3, i + 3):
        if 0 <= j < len(senda):
            res.append((f"MEDITACIÓN: INTERCAMBIA las cartas {i} <-> {j}", intercambiar(senda, i, j)))
    return res

# ORACIÓN
# Intercambia esta carta de lugar con otra adyacente
def hab_10_oracion(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in vecinos_validos(senda, i):
        res.append((
            f"ORACIÓN: INTERCAMBIA las cartas {i} <-> {j}",
            intercambiar(senda, i, j)
        ))
    return res

# PEREGRINO
# Mueve una carta adyacente exactamente 2 espacios.
def hab_12_peregrino(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in vecinos_validos(senda, i):
        for direc in (-2, +2):
            destino = j + direc
            if 0 <= destino < len(senda):
                res.append((
                    f"PEREGRINO: La carta {nombre(senda[j])} en posición {j} se mueve {direc:+d}",
                    mover_a(senda, j, destino)
                ))
    return res

# MAGIA
# 1) Retrocede una carta adyacene exactamente 3 espacios 
# 2) Adelanta una carta adyacente exactamente 2 espacios
def hab_13_magia(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
  
    res = []
    for j in vecinos_validos(senda, i):
        # 1)
        destino = j - 3
        if 0 <= destino < len(senda):
            res.append((
                f"MAGIA: La carta {nombre(senda[j])} en posición {j} retrocede 3",
                mover_a(senda, j, destino)
            ))
        # 2)
        destino = j + 2
        if 0 <= destino < len(senda):
            res.append((
                f"MAGIA: La carta {nombre(senda[j])} en posición {j} adelanta 2",
                mover_a(senda, j, destino)
            ))
    return res

# CUERPO ASTRAL
# Intercambia esta carta de lugar con otra que este exactamente a 4 espacios de distancia de esta
def hab_14_cuerpo_astral(senda: Senda, i: int) -> List[Tuple[str, Senda]]:
    res = []
    for j in (i - 4, i + 4):
        if 0 <= j < len(senda):
            res.append((
                f"CUERPO ASTRAL: INTERCAMBIA las cartas {i} <-> {j}",
                intercambiar(senda, i, j)
            ))
    return res

HABILIDADES_MAESTROS = {
    5:  hab_5_ejercicio,
    7:  hab_7_filosofia,
    8:  hab_8_herbolaria,
    9:  hab_9_meditacion,
    10: hab_10_oracion,
    12: hab_12_peregrino,
    13: hab_13_magia,
    14: hab_14_cuerpo_astral,
}

# HABILIDADES DE LOS FALSOS MAESTROS 

# DUDA
# Intercambia de lugar las 2 cartas adyacentes a esta
# 1) Si está en una orilla recorre esta carta 1 espacio dependiendo de la orilla
# 2) Caso normal: intercambia las dos cartas adyacentes a Duda
def hab_1_duda(senda: Senda, i: int) -> Senda:
    n = len(senda)
    if i == 0:
        # IZQUIERDA: -> SE MUEVE A LA DERECHA
        return mover_a(senda, i, 1)
    if i == n - 1:
        # DERECHA: -> SE MUEVE A LA IZQUIERDA
        return mover_a(senda, i, n - 2)
    return intercambiar(senda, i - 1, i + 1)

# RENCOR 
# Destruye la carta adyacente de menor valor.
def hab_2_rencor(senda: Senda, i: int) -> Senda:
    j = adyacente_min(senda, i)
    if j == -1:
        return senda
    return destruir(senda, j)

# MIEDO
# Mueve la carta adyacente de menor valor al inicio de la senda (posición 0).
def hab_3_miedo(senda: Senda, i: int) -> Senda:
    j = adyacente_min(senda, i)
    if j == -1:
        return senda
    return mover_a_inicio(senda, j)

# PEREZA
# 1) Retrocede la carta adyacente de menor valor 2 espacios
# 2) Si no puede retroceder 2 (está muy cerca del inicio), Pereza misma avanza 1 espacio
def hab_4_pereza(senda: Senda, i: int) -> Senda:
    j = adyacente_min(senda, i)
    if j == -1:
        # 1)
        return mover_a(senda, i, i + 1) if i + 1 < len(senda) else senda
    if j - 2 >= 0:
        return mover_a(senda, j, j - 2)
    # 2)
    return mover_a(senda, i, i + 1) if i + 1 < len(senda) else senda

# CIZAÑOSO
# Manda la carta adyacente de menor valor al espacio inmediatamente ANTERIOR al Rencor en la senda
# 2) Si la carta de valor más bajo es el rencor, mueve el rencor 2 espacios en dirección del aprendiz.
def hab_6_cizanoso(senda: Senda, i: int) -> Senda:
    j = adyacente_min(senda, i)
    if j == -1:
        return senda
    idx_rencor = indice_de(senda, 2)
    # 2)
    if senda[j] == 2:
        # mover rencor 2 espacios hacia el aprendiz
        idx_aprendiz = indice_de(senda, APRENDIZ)
        if idx_aprendiz == -1 or idx_rencor == -1:
            return senda
        direccion = -1 if idx_aprendiz < idx_rencor else +1
        return mover_a(senda, idx_rencor, idx_rencor + 2 * direccion)
    # 1) 
    if idx_rencor == -1:
        # sin Rencor en la senda no hay accion
        return senda

    destino = idx_rencor - 1
    if destino < 0:
        # si rencor está en posición 0 no hay posición anterior posible, no hay accion
        return senda
    return mover_a(senda, j, destino)


# ENVIDIA
# 1) Mueve la carta adyacente de valor más bajo, exactamente 2 espacios en dirección del rencor, aunque esta lo rebase
# 2) Si fuese el rencor, mueve el rencor 2 espacios hacia del aprendiz
def hab_11_envidia(senda: Senda, i: int) -> Senda:

    j = adyacente_min(senda, i)
    if j == -1:
        return senda

    idx_rencor = indice_de(senda, 2)
    idx_aprendiz = indice_de(senda, APRENDIZ)
    # 1)
    if senda[j] == 2:
        if idx_aprendiz == -1 or idx_rencor == -1:
            return senda
        direccion = -1 if idx_aprendiz < idx_rencor else +1
        return mover_a(senda, idx_rencor, idx_rencor + 2 * direccion)
    # 2)
    if idx_rencor == -1:
        # si rencor no esta en la senda no hay accion
        return senda
    
    direccion = +1 if idx_rencor > j else -1
    return mover_a(senda, j, j + 2 * direccion)

# orden para aplicar habilidades de falsos maestros
HABILIDADES_FALSOS = {
    1:  hab_1_duda,
    2:  hab_2_rencor,
    3:  hab_3_miedo,
    4:  hab_4_pereza,
    6:  hab_6_cizanoso,
    11: hab_11_envidia,
}

# TURNO DE LOS FALSOS MAESTROS
def turno_falsos_maestros(senda: Senda) -> Senda:
    actual = senda
    for fm in ORDEN_FALSOS:

        if APRENDIZ not in actual:
            return actual
        idx = indice_de(actual, fm)
        if idx == -1:
            continue
        actual = HABILIDADES_FALSOS[fm](actual, idx)
    return actual

# Versión de debug: registra cada paso del turno
def turno_falsos_maestros_debug(senda: Senda) -> Tuple[Senda, List[dict]]:
    actual = senda
    log = []

    for fm in ORDEN_FALSOS:
        if APRENDIZ not in actual:
            log.append({
                "falso_maestro": nombre(fm),
                "posicion": -1,
                "adyacente_min": "—",
                "senda_antes": actual,
                "senda_despues": actual,
                "cambio": False,
                "nota": "Aprendiz ya destruido — turno interrumpido",
            })
            return actual, log

        idx = indice_de(actual, fm)
        if idx == -1:
            log.append({
                "falso_maestro": nombre(fm),
                "posicion": -1,
                "adyacente_min": "—",
                "senda_antes": actual,
                "senda_despues": actual,
                "cambio": False,
                "nota": "no está en la senda",
            })
            continue

        j_min = adyacente_min(actual, idx)
        carta_min = nombre(actual[j_min]) if j_min != -1 else "—"
        senda_antes = actual
        actual = HABILIDADES_FALSOS[fm](actual, idx)

        log.append({
            "falso_maestro": nombre(fm),
            "posicion": idx,
            "adyacente_min": carta_min,
            "senda_antes": senda_antes,
            "senda_despues": actual,
            "cambio": actual != senda_antes,
            "nota": "",
        })

    return actual, log

# GENERACIÓN DE SUCESORES: esto sirve para construir el grafo de estados para el algoritmo de búsqueda, y también para imprimir el debug de cada ronda completa con activaciones de habilidades
def sucesores(estado: GameState) -> List[Tuple[str, GameState]]:
    salidas = []
    vistos = set()

    if estado.es_derrota():
        return salidas

    for idx, carta in enumerate(estado.senda):
        if carta == APRENDIZ:
            continue
        if not es_maestro(carta):
            continue
        habilidad = HABILIDADES_MAESTROS[carta]
        for desc, senda_tras_jugador in habilidad(estado.senda, idx):
            senda_final = turno_falsos_maestros(senda_tras_jugador)
            nuevo = estado.con_senda(senda_final)
            if nuevo.es_derrota():
                continue
            if nuevo in vistos:
                continue
            vistos.add(nuevo)
            etiqueta = f"Jugar {nombre(carta)}@{idx} → {desc}"
            salidas.append((etiqueta, nuevo))
    return salidas
