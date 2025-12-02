"""
Elimina stopwords del índice invertido.
Ejecutar: python clean_stopwords.py
"""

from pathlib import Path

SRC_DIR = Path("inverted_index")
DEST_DIR = Path("inverted_index_clean")

# Lista estándar en inglés (puede ampliarse si se requiere).
STOPWORDS = {
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "could",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "ours",
    "ourselves",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "so",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "with",
    "would",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
}


def process_files(files: list[Path]) -> None:
    """Procesa recursivamente dividiendo la lista para evitar desbordar el stack."""
    if not files:
        return
    if len(files) == 1:
        file_path = files[0]
        word = file_path.stem.lower()
        if word in STOPWORDS:
            print(f"Eliminando stopword: {word}")
        else:
            DEST_DIR.mkdir(parents=True, exist_ok=True)
            content = file_path.read_text(encoding="utf-8")
            (DEST_DIR / file_path.name).write_text(content, encoding="utf-8")
        return
    mid = len(files) // 2
    process_files(files[:mid])
    process_files(files[mid:])


def main() -> None:
    if not SRC_DIR.exists():
        raise FileNotFoundError("No se encontró inverted_index/. Ejecuta primero build_index.awk.")
    files = sorted(SRC_DIR.glob("*.txt"))
    process_files(files)
    print(f"Índice filtrado en {DEST_DIR.resolve()}")


if __name__ == "__main__":
    main()
