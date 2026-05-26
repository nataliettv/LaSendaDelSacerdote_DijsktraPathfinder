from typing import Tuple, List
from cards import APRENDIZ

Senda = Tuple[int, ...]

def indice_de(senda: Senda, carta: int) -> int:
    try:
        return senda.index(carta)
    except ValueError:
        return -1

def vecinos_validos(senda: Senda, i: int) -> List[int]:
    res = []
    if i - 1 >= 0:
        res.append(i - 1)
    if i + 1 < len(senda):
        res.append(i + 1)
    return res

def adyacente_min(senda: Senda, i: int) -> int:
    candidatos = []
    for j in vecinos_validos(senda, i):
        candidatos.append((senda[j], j))
    if not candidatos:
        return -1
    candidatos.sort(key=lambda t: (t[0], t[1]))
    return candidatos[0][1]

def intercambiar(senda: Senda, i: int, j: int) -> Senda:
    if i == j:
        return senda
    lst = list(senda)
    lst[i], lst[j] = lst[j], lst[i]
    return tuple(lst)

def destruir(senda: Senda, i: int) -> Senda:
    lst = list(senda)
    del lst[i]
    return tuple(lst)

def mover_a(senda: Senda, origen: int, destino: int) -> Senda:
    n = len(senda)
    if destino < 0:
        destino = 0
    elif destino >= n:
        destino = n - 1
    if origen == destino:
        return senda

    lst = list(senda)
    carta = lst.pop(origen)
    lst.insert(destino, carta)
    return tuple(lst)

def mover_a_inicio(senda: Senda, origen: int) -> Senda:
    return mover_a(senda, origen, 0)

def puede_retroceder(senda: Senda, i: int, pasos: int) -> bool:
    return i - pasos >= 0
