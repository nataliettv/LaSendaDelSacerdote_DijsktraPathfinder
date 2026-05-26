# implementación de Dijkstra sobre el grafo IMPLÍCITO de estados del juego.

import heapq
from typing import Dict, List, Optional, Tuple
from state import GameState
from game import sucesores

def costo_movimiento(estado_anterior: GameState, estado_nuevo: GameState) -> int:
    return 1

def dijkstra(
    inicio: GameState,
    limite_profundidad: Optional[int] = None,
) -> Tuple[Optional[GameState], Dict[GameState, int],
           Dict[GameState, Tuple[GameState, str]]]:
    dist: Dict[GameState, int] = {inicio: 0}
    padre: Dict[GameState, Tuple[GameState, str]] = {}

    contador = 0
    heap: List[Tuple[int, int, GameState]] = [(0, contador, inicio)]
    cerrados = set()

    while heap:
        costo_actual, _, actual = heapq.heappop(heap)

        if actual in cerrados:
            continue
        cerrados.add(actual)

        if actual.es_victoria():
            return actual, dist, padre

        if limite_profundidad is not None and costo_actual >= limite_profundidad:
            continue

        for descripcion, vecino in sucesores(actual):
            nuevo_costo = costo_actual + costo_movimiento(actual, vecino)
            if nuevo_costo < dist.get(vecino, float("inf")):
                dist[vecino] = nuevo_costo
                padre[vecino] = (actual, descripcion)
                contador += 1
                heapq.heappush(heap, (nuevo_costo, contador, vecino))

    return None, dist, padre

def reconstruir_camino(
    meta: GameState,
    padre: Dict[GameState, Tuple[GameState, str]],
) -> List[Tuple[str, GameState]]:
    camino = []
    actual = meta

    while actual in padre:
        anterior, descripcion = padre[actual]
        camino.append((descripcion, actual))
        actual = anterior
    camino.reverse()
    return camino
