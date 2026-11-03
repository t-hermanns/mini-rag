"""Thin Gemini client.

Embeddings are cached in .cache/embeddings.json, so re-running experiments
costs no API calls for texts that were already embedded.
"""

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Literal

EMBED_MODEL = "gemini-embedding-001"
EMBED_DIM = 768
GENERATE_MODEL = "gemini-3.5-flash"

_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
_CACHE_FILE = Path(__file__).parent / ".cache" / "embeddings.json"
_BATCH = 100
# free tier allows 30,000 embedding tokens per minute; German text is ~2 tokens per word
_BATCH_WORDS = 6000
_cache: dict[str, list[float]] | None = None


def _post(url: str, body: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]},
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except TimeoutError:
            if attempt < 4:
                continue
            raise
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503) and attempt < 4:
                # free tier limits are per minute, so wait for the next minute on 429
                time.sleep(65 if e.code == 429 else 2**attempt * 5)
                continue
            raise RuntimeError(f"{e.code}: {e.read().decode()[:500]}") from e
    raise AssertionError("unreachable")


def _load_cache() -> dict[str, list[float]]:
    global _cache
    if _cache is None:
        _cache = json.loads(_CACHE_FILE.read_text(encoding="utf-8")) if _CACHE_FILE.exists() else {}
    return _cache


def _key(text: str, task: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


def embed(texts: list[str], task: Literal["document", "query"]) -> list[list[float]]:
    """Embed texts. Use task="document" for chunks and task="query" for questions.

    Returns one vector (768 floats) per input text, in the same order.
    """
    cache = _load_cache()
    task_type = "RETRIEVAL_DOCUMENT" if task == "document" else "RETRIEVAL_QUERY"
    missing = [t for t in dict.fromkeys(texts) if _key(t, task) not in cache]
    for batch in _batches(missing):
        resp = _post(
            f"{_BASE}{EMBED_MODEL}:batchEmbedContents",
            {
                "requests": [
                    {
                        "model": f"models/{EMBED_MODEL}",
                        "content": {"parts": [{"text": t}]},
                        "taskType": task_type,
                        "outputDimensionality": EMBED_DIM,
                    }
                    for t in batch
                ]
            },
        )
        for t, e in zip(batch, resp["embeddings"]):
            cache[_key(t, task)] = e["values"]
        # save after every batch, so a rate-limit abort keeps the finished work
        _CACHE_FILE.parent.mkdir(exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(cache), encoding="utf-8")
    return [cache[_key(t, task)] for t in texts]


def _batches(texts: list[str]):
    """Split texts into requests of at most _BATCH texts and roughly _BATCH_WORDS words."""
    batch: list[str] = []
    words = 0
    for t in texts:
        n = len(t.split())
        if batch and (len(batch) == _BATCH or words + n > _BATCH_WORDS):
            yield batch
            batch, words = [], 0
        batch.append(t)
        words += n
    if batch:
        yield batch


def generate(prompt: str) -> str:
    """Send one prompt to the LLM and return its text answer."""
    resp = _post(f"{_BASE}{GENERATE_MODEL}:generateContent", {"contents": [{"parts": [{"text": prompt}]}]})
    return "".join(p.get("text", "") for p in resp["candidates"][0]["content"]["parts"])
