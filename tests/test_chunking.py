from chunking import chunk_fixed, chunk_structured

WORDS = " ".join(f"w{i}" for i in range(1, 11))  # w1 .. w10

DOC = """# Titel

Intro eins zwei drei.

## A

Absatz eins hat fünf Wörter.

Absatz zwei hat auch fünf.

## B

### B1

Text in B1.

## Leer

## C

| Spalte | Wert |
|---|---|
| a | 1 |
| b | 2 |
| c | 3 |
"""


def texts(chunks):
    return [c.text for c in chunks]


def test_fixed_overlap():
    assert texts(chunk_fixed(WORDS, "x.md", 4, 1)) == ["w1 w2 w3 w4", "w4 w5 w6 w7", "w7 w8 w9 w10"]


def test_fixed_no_overlap_short_last():
    assert texts(chunk_fixed(WORDS, "x.md", 4, 0)) == ["w1 w2 w3 w4", "w5 w6 w7 w8", "w9 w10"]


def test_fixed_stops_when_covered():
    text = " ".join(f"w{i}" for i in range(1, 9))
    assert texts(chunk_fixed(text, "x.md", 5, 2)) == ["w1 w2 w3 w4 w5", "w4 w5 w6 w7 w8"]


def test_fixed_short_and_empty():
    chunks = chunk_fixed("ein  kurzer\nText", "x.md", 5, 1)
    assert texts(chunks) == ["ein kurzer Text"]
    assert chunks[0].source == "x.md" and chunks[0].heading_path == ()
    assert chunk_fixed("", "x.md", 5, 1) == []


def test_structured_paths_and_joining():
    chunks = chunk_structured(DOC, "d.md", 10, with_headings=False)
    assert list(dict.fromkeys(c.heading_path for c in chunks)) == [
        ("Titel",),
        ("Titel", "A"),
        ("Titel", "B", "B1"),
        ("Titel", "C"),
    ]
    assert chunks[1].text == "Absatz eins hat fünf Wörter.\n\nAbsatz zwei hat auch fünf."
    assert chunks[2].text == "Text in B1."
    assert all(c.source == "d.md" for c in chunks)


def test_structured_respects_limit():
    chunks = chunk_structured(DOC, "d.md", 9, with_headings=False)
    a = [c.text for c in chunks if c.heading_path == ("Titel", "A")]
    assert a == ["Absatz eins hat fünf Wörter.", "Absatz zwei hat auch fünf."]


def test_structured_with_headings():
    chunks = chunk_structured(DOC, "d.md", 10)
    assert chunks[1].text == "Titel > A\nAbsatz eins hat fünf Wörter.\n\nAbsatz zwei hat auch fünf."


def test_structured_table_kept_whole_when_it_fits():
    chunks = chunk_structured(DOC, "d.md", 30, with_headings=False)
    assert chunks[-1].text == "| Spalte | Wert |\n|---|---|\n| a | 1 |\n| b | 2 |\n| c | 3 |"


def test_structured_table_split_repeats_header():
    chunks = chunk_structured(DOC, "d.md", 12, with_headings=False)
    table = [c.text for c in chunks if c.heading_path == ("Titel", "C")]
    assert table == [
        "| Spalte | Wert |\n|---|---|\n| a | 1 |",
        "| Spalte | Wert |\n|---|---|\n| b | 2 |\n| c | 3 |",
    ]


def test_structured_long_paragraph():
    para = " ".join(f"p{i}" for i in range(1, 26))
    chunks = chunk_structured(f"# T\n\nkurz\n\n{para}\n\nauch kurz", "d.md", 10, with_headings=False)
    assert [len(c.text.split()) for c in chunks] == [1, 10, 10, 5, 2]


def test_structured_plain_text():
    chunks = chunk_structured("nur ein Absatz ohne Überschrift", "s.txt", 50)
    assert len(chunks) == 1
    assert chunks[0].heading_path == () and chunks[0].text == "nur ein Absatz ohne Überschrift"
