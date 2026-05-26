from dataclasses import dataclass
from typing import Tuple
from cards import APRENDIZ, nombre

@dataclass(frozen=True)
class GameState:
    senda: Tuple[int, ...] 
    aprendiz: int      

    def carta_en(self, i: int) -> int:
        if 0 <= i < len(self.senda):
            return self.senda[i]
        return -1

    def es_derrota(self) -> bool:
        return self.aprendiz == -1

    def es_victoria(self) -> bool:
        if self.es_derrota():
            return False
        return self.aprendiz == len(self.senda) - 1

    def con_senda(self, nueva_senda: Tuple[int, ...]) -> "GameState":
        try:
            nuevo_apr = nueva_senda.index(APRENDIZ)
        except ValueError:
            return GameState(senda=nueva_senda, aprendiz=-1)
        return GameState(senda=nueva_senda, aprendiz=nuevo_apr)

    def __str__(self) -> str:
        partes = []
        for pos, c in enumerate(self.senda):
            marca = "★" if pos == self.aprendiz else " "
            partes.append(f"[{marca}{nombre(c)}]")
        sufijo = " ⏢ (Deidad)"
        if self.es_derrota():
            sufijo += "  ✗ (Aprendiz destruido)"
        elif self.es_victoria():
            sufijo = " ← ✓ VICTORIA" + sufijo
        return " ".join(partes) + sufijo

def estado_inicial(orden_cartas, posicion_aprendiz: int = 0) -> GameState:
    if not orden_cartas:
        raise ValueError("La senda no puede estar vacía.")
    senda = [APRENDIZ] + list(orden_cartas)
    if posicion_aprendiz != 0:
        senda.remove(APRENDIZ)
        senda.insert(posicion_aprendiz, APRENDIZ)
    return GameState(senda=tuple(senda), aprendiz=posicion_aprendiz)