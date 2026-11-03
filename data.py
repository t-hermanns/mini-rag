"""Documents, test set and the hit definition."""

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str  # file name of the document, e.g. "retouren.md"
    heading_path: tuple[str, ...] = ()  # e.g. ("Retourenabwicklung", "Fristen")


def load_documents() -> list[tuple[str, str]]:
    """All documents as (file name, full text), sorted by file name."""
    return [(p.name, p.read_text(encoding="utf-8")) for p in sorted((ROOT / "docs").iterdir())]


def load_testset() -> list[dict]:
    """Test cases: {"question": str, "source": str, "evidence": str}."""
    return json.loads((ROOT / "testset.json").read_text(encoding="utf-8"))


def _norm(s: str) -> str:
    return " ".join(s.split()).lower()


def is_hit(chunk: Chunk, case: dict) -> bool:
    """A chunk answers a test case if it comes from the right document and contains the evidence."""
    return chunk.source == case["source"] and _norm(case["evidence"]) in _norm(chunk.text)
