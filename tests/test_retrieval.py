import math

from data import Chunk
from retrieval import BM25Index, HybridIndex, VectorIndex, rrf, tokenize

VOCAB = ["apfel", "birne", "kirsche"]


class FakeEmbed:
    """Vector = how often each VOCAB word occurs. Records every call."""

    def __init__(self):
        self.calls = []

    def __call__(self, texts, task):
        self.calls.append((list(texts), task))
        return [[float(t.lower().split().count(w)) for w in VOCAB] for t in texts]


A = Chunk("apfel apfel birne", "a.md")
B = Chunk("birne", "b.md")
C = Chunk("kirsche und sperrlager sp-02", "c.md")


def test_tokenize():
    assert tokenize("PR-B, 1.200 kg") == ["pr", "b", "1", "200", "kg"]
    assert tokenize("Größe | Übergabe") == ["größe", "übergabe"]


def test_vector_index_embeds_once():
    fake = FakeEmbed()
    VectorIndex([A, B, C], embed=fake)
    assert fake.calls == [([A.text, B.text, C.text], "document")]


def test_vector_search_cosine():
    fake = FakeEmbed()
    index = VectorIndex([A, B, C], embed=fake)
    results = index.search("birne", 2)
    assert fake.calls[-1] == (["birne"], "query")
    assert [c for c, _ in results] == [B, A]
    assert math.isclose(results[0][1], 1.0)
    assert math.isclose(results[1][1], 1 / math.sqrt(5))


def test_bm25_ranking_and_zero_scores():
    index = BM25Index([A, B, C])
    results = index.search("Birne", 5)
    assert [c for c, _ in results] == [B, A]  # shorter chunk wins, C has score 0


def test_bm25_score():
    index = BM25Index([A, B, C])
    (chunk, score), = index.search("sperrlager", 5)
    n, n_t, f, k1, b = 3, 1, 1, 1.5, 0.75
    lens = [3, 1, 5]
    idf = math.log((n - n_t + 0.5) / (n_t + 0.5) + 1)
    expected = idf * f * (k1 + 1) / (f + k1 * (1 - b + b * 5 / (sum(lens) / 3)))
    assert chunk == C and math.isclose(score, expected)


def test_rrf():
    d = Chunk("d", "d.md")
    fused = rrf([[A, B, C], [B, d]])
    assert [c for c, _ in fused] == [B, A, d, C]
    assert math.isclose(fused[0][1], 1 / 62 + 1 / 61)


def test_hybrid_finds_keyword_only_match():
    index = HybridIndex([A, B, C], embed=FakeEmbed(), candidates=3)
    results = index.search("SP-02", 2)
    assert results[0][0] == C
    assert len(results) == 2
