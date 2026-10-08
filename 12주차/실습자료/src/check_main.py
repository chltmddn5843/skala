"""실행: python src/check_main.py (외부 서버·임베딩 모델 없이 검증)."""
from pathlib import Path
from contextlib import closing
from tempfile import TemporaryDirectory

from main import (QdrantClient, build_faiss, load_chunks, np, pymupdf,
                  search_faiss, search_qdrant, upload)


with TemporaryDirectory() as directory:
    with pymupdf.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), "Alpha semiconductor. " * 12)
        pdf.new_page()  # 빈 페이지는 제외되어야 함
        pdf.save(Path(directory) / "sample.pdf")
    chunks = load_chunks(Path(directory), 60, 10)
    assert len(chunks) > 1
    assert all(0 < len(c["text"]) <= 60 and c["page"] == 1 for c in chunks)
    try:
        load_chunks(Path(directory), 10, 10)
    except ValueError:
        pass
    else:
        raise AssertionError("잘못된 overlap을 거부해야 합니다.")

chunks = [{"text": "alpha", "source": "a.pdf", "page": 1},
          {"text": "beta", "source": "b.pdf", "page": 5},
          {"text": "gamma", "source": "a.pdf", "page": 6}]
vectors = np.array([[1, 0], [0, 1], [-1, 0]], dtype="float32")
query = vectors[:1]
index = build_faiss(vectors)
with closing(QdrantClient(":memory:")) as client:
    upload(client, "check", chunks, vectors)
    for source, page, expected in [(None, 1, [0, 1, 2]), ("a.pdf", 5, [2]),
                                    ("missing.pdf", 1, []), (None, 99, [])]:
        left = search_faiss(index, query, chunks, 10, source, page)
        right = search_qdrant(client, "check", query, 10, source, page)
        assert [h[0] for h in left] == [h[0] for h in right] == expected
        assert np.allclose([h[1] for h in left], [h[1] for h in right], atol=1e-6)
print("PASS: PDF·청킹·빈 페이지·잘못된 overlap·검색 순위·필터·빈 결과·점수 일치")
