"""실습 1: PDF → 청킹 → 임베딩 → FAISS / Qdrant → 검색·필터 비교.

실습자료에서 실행:
    python src/main.py --query "HBM 반도체 전망"
    python src/main.py --max-chunks 30 --min-page 5
    python src/main.py --model bge-m3  # 먼저 ollama pull bge-m3

기본 모델은 설치된 embeddinggemma이며 교재 BGE-M3와 결과·차원이 다릅니다.
Qdrant와 Ollama 서버가 실행 중이어야 합니다. PDF OCR은 포함하지 않습니다.
"""

import argparse
from contextlib import closing
import json
from pathlib import Path
from time import perf_counter
from urllib.request import Request, urlopen
from uuid import uuid4

import faiss
import numpy as np
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models


def load_chunks(data_dir, chunk_size=500, overlap=50):
    if not 0 <= overlap < chunk_size:
        raise ValueError("0 <= overlap < chunk_size 조건이 필요합니다.")
    files = sorted(path for path in data_dir.rglob("*") if path.suffix.lower() == ".pdf")
    if not files:
        raise ValueError(f"PDF 파일이 없습니다: {data_dir}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = []
    for path in files:
        with pymupdf.open(path) as pdf:
            for page_num, page in enumerate(pdf, 1):
                text = page.get_text().strip()
                if not text:
                    print(f"텍스트 없는 페이지 건너뜀(OCR 미지원): {path.name} p.{page_num}")
                for part in splitter.split_text(text):
                    chunks.append({"text": part, "source": path.name, "page": page_num})
    if not chunks:
        raise ValueError("추출된 텍스트가 없습니다. 스캔 PDF는 OCR이 필요합니다.")
    print(f"① PDF {len(files)}개 로딩  ② {len(chunks)}개 청크 ({chunk_size}문자, overlap={overlap})")
    return chunks


def embed(texts, model, ollama_url):
    vectors = []
    for start in range(0, len(texts), 32):
        body = {"model": model, "input": texts[start:start + 32], "truncate": False}
        request = Request(ollama_url.rstrip("/") + "/api/embed",
                          data=json.dumps(body).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=180) as response:
            vectors.extend(json.load(response)["embeddings"])
        print(f"  임베딩 {min(start + 32, len(texts))}/{len(texts)}", flush=True)
    result = np.asarray(vectors, dtype="float32")
    if (result.ndim != 2 or result.shape[0] != len(texts)
            or not np.isfinite(result).all() or np.any(np.linalg.norm(result, axis=1) == 0)):
        raise ValueError("임베딩 응답의 개수·차원·값이 유효하지 않습니다.")
    faiss.normalize_L2(result)
    return result


def build_faiss(vectors):
    # 정규화 벡터의 내적 = 코사인 유사도. 양쪽 모두 높을수록 유사합니다.
    index = faiss.IndexHNSWFlat(vectors.shape[1], 32, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = 128
    index.hnsw.efSearch = 128
    index.add(vectors)
    return index


def upload(client, collection, chunks, vectors):
    # 기존 컬렉션을 삭제하지 않고, 실행마다 새 이름으로 저장합니다.
    client.create_collection(collection, vectors_config=models.VectorParams(
        size=vectors.shape[1], distance=models.Distance.COSINE))
    for start in range(0, len(chunks), 64):
        client.upsert(collection, points=[
            models.PointStruct(id=i, vector=vectors[i].tolist(), payload=chunks[i])
            for i in range(start, min(start + 64, len(chunks)))
        ], wait=True)


def search_faiss(index, query, chunks, k, source=None, min_page=1):
    # ponytail: 필터 시 전체 후보 O(N) 조회. 대규모 조건 검색은 Qdrant 사용.
    filtered = source is not None or min_page > 1
    scores, ids = index.search(query, len(chunks) if filtered else min(k, len(chunks)))
    return [(int(i), float(score), chunks[i]) for i, score in zip(ids[0], scores[0])
            if i >= 0 and chunks[i]["page"] >= min_page
            and (source is None or chunks[i]["source"] == source)][:k]


def search_qdrant(client, collection, query, k, source=None, min_page=1):
    conditions = [models.FieldCondition(key="page", range=models.Range(gte=min_page))]
    if source is not None:
        conditions.append(models.FieldCondition(key="source", match=models.MatchValue(value=source)))
    hits = client.query_points(collection, query=query[0].tolist(), limit=k,
                               query_filter=models.Filter(must=conditions), with_payload=True).points
    return [(hit.id, hit.score, hit.payload) for hit in hits]


def compare(index, client, collection, query, chunks, k, source=None, min_page=1):
    results = []
    for name, search in [
        ("FAISS", lambda: search_faiss(index, query, chunks, k, source, min_page)),
        ("Qdrant", lambda: search_qdrant(client, collection, query, k, source, min_page)),
    ]:
        start = perf_counter()
        hits = search()
        elapsed = (perf_counter() - start) * 1000
        print(f"\n{name}: {len(hits)}건, {elapsed:.2f}ms (검색 호출 1회, 임베딩 제외)")
        for rank, (chunk_id, score, payload) in enumerate(hits, 1):
            print(f"{rank}. [{score:.4f}] {payload['source']} p.{payload['page']} / chunk={chunk_id}")
            print("   " + " ".join(payload["text"].split())[:180])
        if not hits:
            print("조건에 맞는 결과가 없습니다.")
        results.append({hit[0] for hit in hits})
    print(f"공통 청크: {len(results[0] & results[1])}개 (정답 정확도 지표가 아닙니다)")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--query", default="HBM 반도체 산업의 전망은?")
    parser.add_argument("--model", default="embeddinggemma")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--qdrant-url", default="http://localhost:6333")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=50)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-chunks", type=int, help="빠른 동작 확인용 청크 수 제한")
    parser.add_argument("--source", help="필터 검색 대상 PDF 파일명(완전 일치)")
    parser.add_argument("--min-page", type=int, default=5)
    args = parser.parse_args()
    if (not args.query.strip() or args.top_k < 1 or args.min_page < 1
            or (args.max_chunks is not None and args.max_chunks < 1)
            or not 0 <= args.overlap < args.chunk_size):
        parser.error("질문은 비어 있으면 안 되며 개수·페이지는 양수, 0 <= overlap < chunk-size여야 합니다.")
    with closing(QdrantClient(url=args.qdrant_url, timeout=60)) as client:
        client.get_collections()  # 임베딩 전에 서버 연결을 확인합니다.
        chunks = load_chunks(args.data_dir, args.chunk_size, args.overlap)
        if args.max_chunks:
            chunks = chunks[:args.max_chunks]
            print(f"동작 확인용: 앞 {len(chunks)}개 청크만 사용")
        print(f"③ 임베딩: {args.model}", flush=True)
        vectors = embed([chunk["text"] for chunk in chunks], args.model, args.ollama_url)
        query = embed([args.query], args.model, args.ollama_url)
        print(f"벡터 shape={vectors.shape}")
        index = build_faiss(vectors)
        print(f"④ FAISS HNSW: {index.ntotal}개 저장")
        collection = "skala_pdf_" + uuid4().hex
        print(f"⑤ Qdrant 컬렉션: {collection}", flush=True)
        upload(client, collection, chunks, vectors)
        print(f"⑥ 검색 비교: {args.query}")
        compare(index, client, collection, query, chunks, args.top_k)
        source = args.source or chunks[0]["source"]
        print(f"\n필터: source={source}, page >= {args.min_page}")
        compare(index, client, collection, query, chunks, args.top_k, source, args.min_page)
        print("\nQdrant 데이터는 서버에 남습니다. FAISS는 이번 실행 메모리에만 유지됩니다.")


if __name__ == "__main__":
    main()
