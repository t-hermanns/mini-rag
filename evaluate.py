"""Measure retrieval quality against testset.json.

Run: python evaluate.py
"""

from pathlib import Path

from chunking import chunk_fixed, chunk_structured
from data import is_hit, load_documents, load_testset
from retrieval import BM25Index, HybridIndex, VectorIndex

def recall_at_k(hits: list[list[bool]], k: int) -> float:
    """Share of questions with at least one hit among the first k results.

    hits has one list per question: hits[q][i] is True if the result at
    position i (0 = best) answers question q (see data.is_hit).
    An empty hits list gives 0.0.
    """
    return [any(q[:k]) for q in hits].count(True)/len(hits) if len(hits) > 0 else 0.0


def mrr(hits: list[list[bool]]) -> float:
    """Mean reciprocal rank: per question 1 / (position of the first hit,
    counting from 1), or 0 without any hit; averaged over all questions.
    An empty hits list gives 0.0."""
    return sum(1/(q.index(True)+1.0) for q in hits if any(q))/len(hits) if len(hits) > 0 else 0.0


def main() -> None:
    """Compare all chunking and search setups."""
    docs = load_documents()
    testset = load_testset()

    print_results = []

    for fun,extra_args in [(chunk_fixed,[60,10]),(chunk_fixed,[200,30]),
                           (chunk_structured,[120,False]),(chunk_structured,[120,True])
                           ]:
        for index_class in [VectorIndex, BM25Index, HybridIndex]:
            chunks = []
            for doc in docs:
                chunks.extend(fun(doc[1], doc[0], *extra_args))
            index = index_class(chunks)
            hits = []
            for test in testset:
                top10 = index.search(test["question"], 10)
                hits.append([is_hit(c, test) for c,_ in top10])

            r_1 = recall_at_k(hits,1)
            r_3 = recall_at_k(hits,3)
            r_5 = recall_at_k(hits,5)
            mr = mrr(hits)
            questions = [test["question"] for test,hit in zip(testset,hits) if not any(hit[:5])]
            args = " ".join(("mit" if x else "ohne") + " Überschriften" if isinstance(x, bool) else str(x)
                            for x in extra_args)
            print_results.append(f"{fun.__name__} {args} {index_class.__name__} chunks={len(chunks)} "
                                 f"R@1={r_1:.2f} R@3={r_3:.2f} R@5={r_5:.2f} MRR={mr:.3f}")
            print(print_results[-1])
            print()
            for question in questions:
                print(question)
            print()
    for p in print_results:
        print(p)

if __name__ == "__main__":
    main()
