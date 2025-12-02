"""
Script placeholder para dataset de Tweets.
El archivo Tweets.csv ya debe estar presente en el directorio raíz.
Se muestra su ruta absoluta para usarlo con build_docs.py.
Ejecutar: python download_dataset.py
"""

from pathlib import Path


def main() -> None:
    csv_path = Path("Tweets.csv").resolve()
    if not csv_path.exists():
        raise FileNotFoundError("No se encontró Tweets.csv en el directorio actual.")
    print(f"Ruta del dataset: {csv_path}")
    print("Usa esta ruta con: python build_docs.py --dataset-path . --csv Tweets.csv")


if __name__ == "__main__":
    main()
