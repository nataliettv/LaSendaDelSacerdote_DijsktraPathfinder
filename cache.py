import shutil
from pathlib import Path
 
 
def limpiar_cache():
    raiz = Path(__file__).parent
    borrados = 0
    for carpeta in raiz.rglob("__pycache__"):
        shutil.rmtree(carpeta)
        borrados += 1
    if borrados:
        print(f"✓ {borrados} carpeta(s) __pycache__ eliminada(s).")
    else:
        print("· No había caché que limpiar.")
 
 
if __name__ == "__main__":
    limpiar_cache()
 