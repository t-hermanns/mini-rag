import math

from evaluate import mrr, recall_at_k

HITS = [
    [True, False, False],
    [False, False, True],
    [False, False, False],
    [False, True, True],
]


def test_recall_at_k():
    assert recall_at_k(HITS, 1) == 0.25
    assert recall_at_k(HITS, 2) == 0.5
    assert recall_at_k(HITS, 3) == 0.75
    assert recall_at_k([], 3) == 0.0


def test_mrr():
    assert math.isclose(mrr(HITS), (1 + 1 / 3 + 0 + 1 / 2) / 4)
    assert mrr([]) == 0.0
