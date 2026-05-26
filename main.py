import json
import re
import sys
import time
import random
from typing import Dict, Any
from pathlib import Path
from cache import limpiar_cache

from cards import nombre
from state import GameState, estado_inicial
from dijkstra import dijkstra, reconstruir_camino
from game import turno_falsos_maestros_debug, HABILIDADES_MAESTROS


def cargar_configuracion() -> Dict[str, Any]:
    ruta = Path(__file__).parent / "data.json"
    with open(ruta, encoding="utf-8") as f:
        raw = f.read()
    clean = re.sub(r"//.*", "", raw)
    return json.loads(clean)


def imprimir_separador(titulo: str = ""):
    print("\n" + "═" * 70)
    if titulo:
        print(f"  {titulo}")
        print("═" * 70)


def _fmt_senda(senda) -> str:
    cartas = "  ".join(f"[{nombre(c)}]" for c in senda)
    return cartas + f"  → [{nombre(15)}]"


def _aplicar_jugada_jugador(estado: GameState, desc_jugada: str):
    try:
        parte_maestro = desc_jugada.split(" → ")[0]
        token = parte_maestro.split("@")
        idx = int(token[1])
        carta = estado.senda[idx]

        if carta not in HABILIDADES_MAESTROS:
            return None

        desc_interna = desc_jugada.split(" → ", 1)[1]
        opciones = HABILIDADES_MAESTROS[carta](estado.senda, idx)

        for desc, senda in opciones:
            if desc == desc_interna:
                return senda

        return None

    except Exception:
        return None

def imprimir_ronda_debug(
    num_ronda: int,
    desc_jugada: str,
    estado_antes: GameState,
    estado_despues: GameState,
):
    SEP = "─" * 68

    print(f"\n  RONDA #{num_ronda}")
    print(f"  {SEP}")

    partes = desc_jugada.split(" → ", 1)
    print(f"  ► JUGADOR: {partes[1] if len(partes) > 1 else desc_jugada}")

    print(f"    Antes: {_fmt_senda(estado_antes.senda)}")

    senda_tras_jugador = _aplicar_jugada_jugador(estado_antes, desc_jugada)

    if senda_tras_jugador is None:
        print("    (No se pudo reconstruir la jugada)")
        print(f"    Después: {_fmt_senda(estado_despues.senda)}")
        return

    print(f"    Después jugador: {_fmt_senda(senda_tras_jugador)}")

    print(f"  {SEP}")
    print(f"  ► FALSOS MAESTROS:")

    _, log = turno_falsos_maestros_debug(senda_tras_jugador)

    for paso in log:
        fm = paso["falso_maestro"]

        if paso["posicion"] == -1:
            print(f"    {fm:14s}: {paso.get('nota', '')}")
            continue

        adj = paso["adyacente_min"]

        if paso["cambio"]:
            print(
                f"    {fm:14s} "
                f"(afecta: {adj:14s}) "
                f"→ "
                f"{_fmt_senda(paso['senda_despues'])}"
            )
        else:
            print(
                f"    {fm:14s} "
                f"(afecta: {adj:14s}) "
                f"· sin cambio"
            )

    print(f"  {SEP}")
    print(f"  ► ESTADO FINAL DE LA RONDA {num_ronda}:")
    print(f"    {_fmt_senda(estado_despues.senda)}")


def mostrar_bienvenida():
    print("\n" + "═" * 50)
    print("    LA SENDA DEL SACERDOTE")
    print("═" * 50)
    print("""
    Tienes 14 cartas en la senda, incluyendo el Aprendiz (★) y la Deidad (⏢):

    1.- Duda
    2.- Rencor
    3.- Miedo
    4.- Pereza
    5.- Ejercicio
    6.- Cizañoso
    7.- Filosofía
    8.- Herbolaria
    9.- Meditación
    10.- Oración
    11.- Envidia
    12.- Peregrino
    13.- Magia
    14.- Cuerpo Astral
    """)

def menu_principal(config) -> bool:
    print("\n┌─────────────────────────────────┐")
    print("│           MENÚ PRINCIPAL        │")
    print("├─────────────────────────────────┤")
    print("│  A) TECLEAR SENDA MANUALMENTE   │")
    print("│  B) SENDA ALEATORIA             │")
    print("│  C) LIMPIAR CACHÉ               │")
    print("│  D) Salir                       │")
    print("└─────────────────────────────────┘")

    opcion = input("\nOPCIÓN: ").strip().lower()

    if opcion == "d":
        return False

    elif opcion == "a":
        print("\nEscribe las cartas separadas por comas (1 ► 14).")
        print("Ej: 14,7,6")

        while True:
            entrada = input("\nSenda: ").strip()
            try:
                senda = [int(x.strip()) for x in entrada.split(",")]
                if not senda:
                    raise ValueError
                config["senda_inicial"] = senda
                config["randomizar"] = False
                break
            except ValueError:
                print("✗ Entrada inválida. Usa números separados por comas.")

    elif opcion == "b":
        config["randomizar"] = True
        config["usar_semilla"] = False
    
    elif opcion == "c":
        limpiar_cache()
        return menu_principal(config)

    else:
        print("✗ Opción inválida.")
        return menu_principal(config)

    return True


def elegir_senda(config):
    senda = list(config["senda_inicial"])
    if config.get("randomizar", False):
        if config.get("usar_semilla", False):
            random.seed(config.get("semilla", 42))
        random.shuffle(senda)
        print("► Senda randomizada")
    return senda


def ejecutar_partida(config):
    senda = elegir_senda(config)
    limite = config.get("limite_profundidad", 20)

    print(f"\nLímite de profundidad: {limite} rondas")

    inicial = estado_inicial(senda)
    print(f"\nEstado inicial:")
    print(f"  {_fmt_senda(inicial.senda)}")

    imprimir_separador("Ejecutando Dijkstra…")

    t0 = time.perf_counter()
    meta, dist, padre = dijkstra(inicial, limite_profundidad=limite)
    t1 = time.perf_counter()

    print(f"  Estados explorados: {len(dist):,}")
    print(f"  Tiempo: {t1 - t0:.3f} s")

    if meta is None:
        print("\n✗ No se encontró solución dentro del límite de profundidad.")
        print("  Intenta aumentar 'limite_profundidad' en data.json")
        print("  o probar con una senda distinta.")
        return

    camino = reconstruir_camino(meta, padre)

    imprimir_separador(f"✓ Solución encontrada en {len(camino)} ronda(s)")

    estados = [inicial] + [est for _, est in camino]

    for i, (desc, est_fin) in enumerate(camino, start=1):
        imprimir_ronda_debug(i, desc, estados[i - 1], est_fin)

    imprimir_separador("Resumen")
    print(f"  Rondas mínimas   : {len(camino)}")
    print(f"  Estados visitados: {len(dist):,}")
    print(f"  Tiempo total     : {t1 - t0:.3f} s")
    print()


def main():
    mostrar_bienvenida()

    while True:
        config = cargar_configuracion()

        if not menu_principal(config):
            print("\nGracias por jugar La Senda del Sacerdote \n")
            break

        ejecutar_partida(config)

        print("\n¿Deseas jugar otra vez?")
        print("  1) Sí  –  volver al menú")
        print("  2) No  –  salir")

        if input("\nOpción: ").strip() == "2":
            print("\nGracias por jugar La Senda del Sacerdote \n")
            break


if __name__ == "__main__":
    main()