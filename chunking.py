"""Split documents into chunks.

Sizes are measured in words (text.split()) as a stand-in for tokens.
"""

import re

from data import Chunk


def chunk_fixed(text: str, source: str, size: int, overlap: int) -> list[Chunk]:
    """Split text into windows of `size` words, ignoring any structure.

    - text: full document text
    - source: document file name, copied into every chunk
    - size: words per chunk (> 0)
    - overlap: words shared by two consecutive chunks (0 <= overlap < size)

    Chunk text is the words joined by single spaces. The last chunk may be
    shorter. Stop once the last word is covered, so no chunk consists only of
    words the previous chunk already had. heading_path stays empty.
    Empty text gives [].
    """
    words = text.split()
    return [Chunk(" ".join(words[start:start+size]),source) for start in range(0,len(words)-overlap, size-overlap)]


def chunk_structured(text: str, source: str, max_words: int, with_headings: bool = True) -> list[Chunk]:
    """Split a Markdown document along its structure.

    - text: full document text (Markdown, or plain text without headings)
    - source: document file name, copied into every chunk
    - max_words: upper limit of content words per chunk
    - with_headings: if True, each chunk's text starts with its heading path

    Rules:
    - A heading is a line starting with one or more "#" followed by a space;
      the number of "#" is its level. heading_path is the chain of headings
      above the content, from level 1 down, e.g.
      ("Inventur", "Zählregeln"). Heading lines are not content.
    - Content is split into blocks at blank lines. Consecutive lines starting
      with "|" form a table, which is one block.
    - Consecutive blocks under the same heading are joined (separated by a
      blank line) into one chunk as long as the chunk stays within max_words.
      A chunk never spans two different headings.
    - A single block longer than max_words is split into pieces, and each
      piece becomes a chunk of its own. A paragraph is cut into pieces of
      exactly max_words words (the last may be shorter), joined by spaces.
      A table is cut between rows: each piece takes as many whole rows as fit
      (at least one row, even if that alone exceeds max_words),
      and every piece after the first starts with the table's first two lines
      (header row and separator row) again; those repeated lines do not count
      toward max_words. Lines inside a table piece stay separated by newlines.
    - With with_headings=True the chunk text is the heading path joined with
      " > ", a newline, then the content. The heading line does not count
      toward max_words. Without headings (or with_headings=False) the chunk
      text is just the content.
    - Headings without content produce no chunk. Text without any heading
      gets heading_path ().
    """
    sections: list[tuple[tuple[str, ...], list[str]]] = []
    path: list[str] = []
    lines: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^(#+) (.*)$", line)
        if m:
            sections.append((tuple(path), lines))
            lines = []
            path = path[: len(m.group(1)) - 1] + [m.group(2).strip()]
        else:
            lines.append(line)
    sections.append((tuple(path), lines))

    chunks: list[Chunk] = []

    def emit(heading_path: tuple[str, ...], content: str) -> None:
        if with_headings and heading_path:
            content = " > ".join(heading_path) + "\n" + content
        chunks.append(Chunk(content, source, heading_path))

    for heading_path, section_lines in sections:
        pending: list[str] = []
        for block in _blocks(section_lines):
            block_text = "\n".join(block)
            if _words(block_text) > max_words:
                if pending:
                    emit(heading_path, "\n\n".join(pending))
                    pending = []
                for piece in _split_block(block, max_words):
                    emit(heading_path, piece)
                continue
            if pending and _words("\n\n".join(pending + [block_text])) > max_words:
                emit(heading_path, "\n\n".join(pending))
                pending = []
            pending.append(block_text)
        if pending:
            emit(heading_path, "\n\n".join(pending))
    return chunks


def _words(text: str) -> int:
    return len(text.split())


def _is_table_line(line: str) -> bool:
    return line.lstrip().startswith("|")


def _blocks(lines: list[str]) -> list[list[str]]:
    """Group lines into blocks: split at blank lines and at table borders."""
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if not line.strip() or (current and _is_table_line(current[0]) != _is_table_line(line)):
            if current:
                blocks.append(current)
            current = []
        if line.strip():
            current.append(line.rstrip())
    if current:
        blocks.append(current)
    return blocks


def _split_block(block: list[str], max_words: int) -> list[str]:
    """Cut an oversized block: tables between rows (header repeated), paragraphs by word count."""
    if not _is_table_line(block[0]):
        words = " ".join(block).split()
        return [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]
    header, rows = block[:2], block[2:]
    pieces: list[str] = []
    piece, count = list(header), _words("\n".join(header))
    for row in rows:
        if count + _words(row) > max_words and len(piece) > len(header):
            pieces.append("\n".join(piece))
            piece, count = list(header), 0
        piece.append(row)
        count += _words(row)
    pieces.append("\n".join(piece))
    return pieces
