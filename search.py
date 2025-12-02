"""
Buscador textual sobre el índice invertido limpio.
Ejecutar: python search.py "russian mbt armor"
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

INDEX_DIR = Path("inverted_index_clean")
DOCS_DIR = Path("docs")
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


def normalize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return [token for token in re.split(r"\s+", text) if token]


def load_index(index_path: Path) -> Dict[str, Set[str]]:
    if not index_path.exists():
        raise FileNotFoundError("No se encontró inverted_index_clean/. Ejecuta clean_stopwords.py.")
    word_files = sorted(index_path.glob("*.txt"))
    index: Dict[str, Set[str]] = {}
    for file in word_files:
        docs = {line.strip() for line in file.read_text(encoding="utf-8").splitlines() if line.strip()}
        index[file.stem] = docs
    return index


def recursive_intersect(
    words: List[str],
    index: Dict[str, Set[str]],
    pos: int = 0,
    acc: Optional[Set[str]] = None,
    trace: Optional[List[Tuple[str, List[str], List[str]]]] = None,
) -> Tuple[Set[str], List[Tuple[str, List[str], List[str]]]]:
    """Calcula la intersección recursiva y guarda el trazo de cada paso."""
    if trace is None:
        trace = []
    if pos >= len(words):
        return (acc or set(), trace)
    current_docs = index.get(words[pos], set())
    acc = current_docs if acc is None else acc & current_docs
    trace.append((words[pos], sorted(current_docs), sorted(acc)))
    return recursive_intersect(words, index, pos + 1, acc, trace)


def print_posting_lists(words: List[str], index: Dict[str, Set[str]]) -> None:
    print("Listas de posteo:")
    for w in words:
        docs = sorted(index.get(w, set()))
        docs_str = ", ".join(docs) if docs else "(vacío)"
        print(f"- {w}: {docs_str}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", help="Consulta de texto (ej: \"russian armor composite\")")
    args = parser.parse_args()

    query = args.query or input("Consulta: ")
    words = [w for w in normalize(query) if w not in STOPWORDS]
    if not words:
        print("No se ingresaron palabras válidas (solo stopwords).")
        return

    index = load_index(INDEX_DIR)
    print_posting_lists(words, index)
    results, trace = recursive_intersect(words, index)
    print("\nIntersección paso a paso:")
    for word, docs_before, acc_after in trace:
        docs_before_str = ", ".join(docs_before) if docs_before else "(vacío)"
        acc_after_str = ", ".join(acc_after) if acc_after else "(vacío)"
        print(f"- Palabra '{word}': docs={docs_before_str} -> acumulado={acc_after_str}")
    if results:
        print("\nResultados:")
        for doc in sorted(results):
            tweet_path = DOCS_DIR / f"{doc}.txt"
            if tweet_path.exists():
                lines = tweet_path.read_text(encoding="utf-8").splitlines()
                tweet_text = lines[2] if len(lines) >= 3 else " ".join(lines)
                print(f"{doc}: {tweet_text}")
            else:
                print(doc)
    else:
        print("Sin resultados para la consulta dada.")


if __name__ == "__main__":
    main()
