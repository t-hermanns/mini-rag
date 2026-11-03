"""Find the chunks that best match a question."""

from collections import defaultdict
import math
import re
from typing import Callable, Literal

import llm
from data import Chunk

EmbedFn = Callable[[list[str], Literal["document", "query"]], list[list[float]]]


class VectorIndex:
    def __init__(self, chunks: list[Chunk], embed: EmbedFn = llm.embed) -> None:
        """Embed all chunk texts (task "document") when the index is built.

        embed is a synchronous function with the same signature as llm.embed;
        tests pass a fake one. Call it once for all chunks, not once per chunk.
        """
        self.embedfn = embed
        self.embeds = [x for x in zip(self.embedfn([c.text for c in chunks], "document"), chunks)]

    def search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        """Return the k chunks most similar to the query, best first.

        The query is embedded with task "query". Similarity is cosine
        similarity; a zero vector has similarity 0 to everything. If several
        chunks have the same similarity, keep their original order.
        Returns (chunk, similarity) pairs.
        """
        query_embed = self.embedfn([query], "query")
        similarities = []
        for ground_embed in self.embeds:
            length = math.prod(sum([(x**2) for x in embed])**0.5 for embed in [query_embed[0], ground_embed[0]])
            if length == 0:
                similarities.append((ground_embed[1],0))
                continue
            scalar_prod = sum(a*b for a,b in zip(query_embed[0], ground_embed[0]))
            similarities.append((ground_embed[1], scalar_prod/length))
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:k]



def tokenize(text: str) -> list[str]:
    """Lowercase the text and split it into tokens of letters and digits.

    Everything else (spaces, punctuation, "|", "-", ...) separates tokens.
    Umlauts and ß count as letters. "PR-B, 1.200 kg" -> ["pr", "b", "1", "200", "kg"].
    """
    text = text.lower()
    return re.findall(r'[^\W_]+', text)



class BM25Index:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75) -> None:
        """Keyword index over the chunk texts, using tokenize()."""
        self.chunks = chunks
        tokenized_texts = [tokenize(c.text) for c in chunks]
        self.t_index = {}
        for c,c_t in zip(chunks,tokenized_texts):
            for t in c_t:
                counts = self.t_index.setdefault(t, {})
                counts[c] = counts.get(c, 0) + 1
        self.k1 = k1
        self.b = b
        self.N = len(self.chunks)
        self.avg_len = sum(len(c) for c in tokenized_texts)/len(self.chunks)
        self.len_d = {c:len(c_t) for c,c_t in zip(chunks,tokenized_texts)}

    def search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        """Return up to k chunks by Okapi BM25 score, best first.

        For each query token t (repeated tokens count repeatedly) and chunk d:
            idf(t)      = ln((N - n_t + 0.5) / (n_t + 0.5) + 1)
            score(t, d) = idf(t) * f * (k1 + 1) / (f + k1 * (1 - b + b * len_d / avg_len))
        N = number of chunks, n_t = chunks containing t, f = count of t in d,
        len_d = number of tokens in d, avg_len = average over all chunks.
        A chunk's score is the sum over the query tokens. Chunks with score 0
        are left out. Returns (chunk, score) pairs.
        """
        res_dict = {}
        for t in tokenize(query):
            if t not in self.t_index:
                continue
            n_t = len(self.t_index[t])
            idf = math.log((self.N - n_t + 0.5) / (n_t + 0.5) + 1)
            for c,count in self.t_index[t].items():
                f = count
                len_d = self.len_d[c]
                score = idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len_d / self.avg_len))
                res_dict[c] = res_dict.get(c,0.0) + score
        return sorted(res_dict.items(),key=lambda x: x[1],reverse=True)[:k]




def rrf(rankings: list[list[Chunk]], c: int = 60) -> list[tuple[Chunk, float]]:
    """Reciprocal Rank Fusion of several rankings (each best first).

    A chunk at rank r (starting at 1) in a ranking gets 1 / (c + r) from that
    ranking; its fused score is the sum over all rankings it appears in.
    Returns every chunk that appears anywhere, as (chunk, fused score),
    best first.
    """
    res = defaultdict(float)
    for ranking in rankings:
        for r,chunk in enumerate(ranking,1):
            res[chunk] += 1 / (c + r)
    return sorted(res.items(), key=lambda x: x[1],reverse=True)


class HybridIndex:
    def __init__(self, chunks: list[Chunk], embed: EmbedFn = llm.embed, candidates: int = 20) -> None:
        """Holds a VectorIndex and a BM25Index over the same chunks."""
        self.vectorindex = VectorIndex(chunks, embed)
        self.bm25index = BM25Index(chunks)
        self.candidates = candidates

    def search(self, query: str, k: int) -> list[tuple[Chunk, float]]:
        """Take the top `candidates` from both indexes, fuse them with rrf(),
        and return the best k as (chunk, fused score)."""
        vector = [chunk for chunk, _ in self.vectorindex.search(query, self.candidates)]
        keyword = [chunk for chunk, _ in self.bm25index.search(query, self.candidates)]
        return rrf([vector, keyword])[:k]   
