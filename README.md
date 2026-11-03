# mini-rag

A small RAG pipeline in plain Python that measures how chunking and search method affect retrieval, on a fictional knowledge base of 40 German work instructions from a contract logistics company. All data is made up and nothing here runs in production.

## Results

Retrieval over 88 test questions, each with a source document and the passage that contains the answer. A chunk counts as a hit if it comes from the right document and contains that passage.

| Chunking | Search | Chunks | Recall@1 | Recall@3 | Recall@5 | MRR |
|---|---|---:|---:|---:|---:|---:|
| Fixed, 60 words, 10 overlap | Vector | 576 | 0.51 | 0.74 | 0.88 | 0.646 |
| | BM25 | 576 | 0.39 | 0.55 | 0.62 | 0.498 |
| | Hybrid | 576 | 0.48 | 0.72 | 0.81 | 0.618 |
| Fixed, 200 words, 30 overlap | Vector | 180 | 0.64 | 0.88 | 0.94 | 0.769 |
| | BM25 | 180 | 0.56 | 0.69 | 0.76 | 0.640 |
| | Hybrid | 180 | 0.62 | 0.84 | 0.91 | 0.737 |
| Structured, max. 120 words, no headings | Vector | 511 | 0.57 | 0.88 | 0.94 | 0.725 |
| | BM25 | 511 | 0.43 | 0.60 | 0.68 | 0.535 |
| | Hybrid | 511 | 0.53 | 0.80 | 0.84 | 0.678 |
| Structured, max. 120 words, with headings | Vector | 511 | **0.77** | **0.98** | **0.98** | **0.865** |
| | BM25 | 511 | 0.48 | 0.69 | 0.75 | 0.601 |
| | Hybrid | 511 | 0.69 | 0.88 | 0.91 | 0.793 |

- Putting the heading path into each chunk made the biggest difference: with the same chunks, vector Recall@1 rose from 0.57 to 0.77.
- Hybrid search (reciprocal rank fusion of vector and BM25) was worse than vector search alone in all four setups.
- With 88 questions, one question is worth about 1.1 points, so small differences between setups mean little. The results apply to this data set only.

## Run it

Standard library only, nothing to install. Embeddings and answers use the Gemini API (`gemini-embedding-001`, `gemini-3.5-flash`), so set `GEMINI_API_KEY` first.

```bash
python run_tests.py
python evaluate.py
python answer.py "Was mache ich, wenn bei Altmann der DESADV fehlt?"
```

The tests run offline. `evaluate.py` prints the table above plus the questions each setup missed in its top 5. Embeddings are cached in `.cache/`, so only the first run calls the embedding API; on the free tier it takes a few minutes because `llm.py` waits for the rate limit.

`answer.py` uses the best setup from the table (structured chunks with headings, vector search). It answers only from the retrieved chunks, names its sources and says so when the documents do not contain the answer.

## Layout

| Path | Content |
|---|---|
| `chunking.py` | Fixed-size and structure-aware chunking |
| `retrieval.py` | Vector search, BM25, reciprocal rank fusion, hybrid index |
| `evaluate.py` | Recall@k, MRR and the comparison of all setups |
| `answer.py` | Answers with sources from the retrieved chunks |
| `llm.py` | Thin Gemini client with embedding cache |
| `data.py` | Document and test set loading, hit definition |
| `docs/` | The 40 fictional documents (about 28,000 words), including tables and scanned sheets |
| `testset.json` | The 88 test questions |
| `tests/`, `run_tests.py` | Tests and a standard-library test runner |
