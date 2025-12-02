"""
Genera un archivo de texto por tweet a partir de Tweets.csv.
Ejecutar: python build_docs.py --dataset-path <ruta_directorio> [--csv Tweets.csv]
"""

import argparse
import re
from pathlib import Path
from typing import Optional

import pandas as pd

DOCS_DIR = Path("docs")


def slugify(name: str) -> str:
    """Convierte el identificador en un nombre de archivo seguro."""
    cleaned = re.sub(r"[^\w\-]+", "_", name.strip())
    return re.sub(r"_+", "_", cleaned).strip("_") or "tweet"


def find_csv(dataset_path: Path, csv_name: Optional[str]) -> Path:
    if csv_name:
        return (dataset_path / csv_name).resolve()
    csv_files = list(dataset_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No se encontró un CSV en la ruta indicada.")
    if len(csv_files) > 1:
        print("Se encontraron múltiples CSV; usando el primero:", csv_files[0].name)
    return csv_files[0].resolve()


def write_docs(df: pd.DataFrame) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    required = {"tweet_id", "airline", "text"}
    missing = required - set(df.columns)
    if missing:
        raise KeyError(f"Columnas faltantes en CSV: {missing}")

    for _, row in df.iterrows():
        tweet_id = str(row["tweet_id"]).strip()
        airline = str(row["airline"]).strip()
        text = str(row["text"]).strip()
        if not tweet_id or not text:
            continue
        filename = slugify(tweet_id) + ".txt"
        sentiment = str(row.get("airline_sentiment", "")).strip()
        neg_reason = str(row.get("negativereason", "")).strip()
        created = str(row.get("tweet_created", "")).strip()
        location = str(row.get("tweet_location", "")).strip()
        parts = [
            tweet_id,
            airline,
            text,
            f"sentiment: {sentiment}" if sentiment else "",
            f"negativereason: {neg_reason}" if neg_reason else "",
            f"created: {created}" if created else "",
            f"location: {location}" if location else "",
        ]
        content = "\n".join(p for p in parts if p)
        (DOCS_DIR / filename).write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-path", required=True, type=Path, help="Ruta donde está Tweets.csv")
    parser.add_argument("--csv", type=str, default="Tweets.csv", help="Nombre del CSV dentro de la ruta")
    args = parser.parse_args()

    csv_path = find_csv(args.dataset_path, args.csv)
    df = pd.read_csv(csv_path)
    write_docs(df)
    print(f"Archivos creados en {DOCS_DIR.resolve()}")


if __name__ == "__main__":
    main()
