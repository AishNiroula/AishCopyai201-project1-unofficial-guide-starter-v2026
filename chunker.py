"""
Stage 2 of the pipeline: splitting documents into chunks.

Milestone 3: replaced with whole-document chunking. campus_life posts are
short (3-9 lines) and each stays on a single topic, even the longest ones -
housing_aldridge_hall.txt mixes room details, pros/cons, laundry cost, and
noise policy, but all of it is still "what it's like to live in Aldridge
Hall." The starter's fixed 800-char window already produced 88 chunks from
88 documents, meaning it never actually split anything - one-post-per-chunk
was already happening by accident. This makes it explicit and intentional.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str
    index: int
    produced_by: str

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """The starter's original chunker. Kept for comparison."""
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Whole-document chunking. Each campus_life post becomes one chunk."""
    chunks: list[Chunk] = []
    for doc in documents:
        text = doc.text.strip()
        if text:
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=0,
                    produced_by="chunker.py::split_documents",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))


