"""Answer a question from the retrieved chunks.

Run: python answer.py "Was mache ich, wenn bei Altmann der DESADV fehlt?"
"""

import json
import sys

from chunking import chunk_structured
from data import load_documents
import llm
from retrieval import VectorIndex


def answer(question: str, index : VectorIndex, k: int = 5) -> str:
    """Answer the question using only the top k chunks from index.search().

    - The answer names its sources (document file name and heading path).
    - If the chunks do not contain the answer, it says so instead of guessing:
      "Dazu habe ich in den Dokumenten nichts gefunden."
    - Uses llm.generate(prompt: str) -> str.
    """
    chunks = [res[0] for res in index.search(question, k)]
    systemprompt ="""
    You are an AI at a logistics company, helping the workers to find answers to their questions.
    For this you are also provided with excerpts from Company Documents, that were found using Retrieval-Augmented Generation.
    Only answer on the basis of the documents, even if you believe you know it better. If you don't find anything in the documents say: "Dazu habe ich in den Dokumenten nichts gefunden.".
    If you find the answer through the sources, please provide the sources in the answers in this format: [1] Quelle: kunde_altmann_automotive.md.
    Answer in German.
    """
    print(*(c.source for c in chunks))
    return llm.generate(systemprompt + "\n" + "Question: " + question + "\n" + "Document chunks: " + "\n".join(f"[{i}] Quelle: " + c.source + "\n" + "Inhalt: " + c.text for i,c in enumerate(chunks,start=1)))


if __name__ == "__main__":
    docs = load_documents()
    chunks = []
    for doc in docs:
        chunks.extend(chunk_structured(doc[1], doc[0], 120, True))
    index = VectorIndex(chunks)
    print(answer(sys.argv[1], index))
