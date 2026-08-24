
# -----------------------------------
# 작성일자 : 2026-08-20
# 작성자 : 최승우
# 설명 : 게시판 API 서버
# 내용 : Flask + PostgreSQL 기반 게시판 API 서버
# 수정 사항
# 1. 2026-08-20 : 최초 작성
# 
#
# -----------------------------------



import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)


# DB 연결: 환경변수로 컨테이너 간 접속 정보를 받는다.
def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "board-db"),
        dbname=os.getenv("DB_NAME", "board"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.environ["DB_PASSWORD"],
    )


# DB 초기화: 최초 실행 시 테이블을 만들고 기존 테이블에는 작성일 컬럼을 보완한다.
def init_db():
    with connect() as conn, conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("ALTER TABLE posts ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP")


# 상태 확인 API
@app.get("/health")
def health():
    return {"status": "ok"}


# 게시글 목록: 최신 글부터 반환한다.
@app.get("/posts")
def get_posts():
    with connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT id, title, content, created_at FROM posts ORDER BY id DESC")
        return jsonify(cursor.fetchall())


# 게시글 작성: 입력값을 검사하고 DB가 작성 시각을 자동 기록한다.
@app.post("/posts")
def create_post():
    data = request.get_json(silent=True) or {}
    if not data.get("title", "").strip() or not data.get("content", "").strip():
        return {"error": "제목과 내용을 입력하세요."}, 400

    with connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id, title, content, created_at",
            (data["title"].strip(), data["content"].strip()),
        )
        return jsonify(cursor.fetchone()), 201


# 게시글 수정: 제목과 내용만 바꾸며 최초 작성 시각은 유지한다.
@app.put("/posts/<int:post_id>")
def update_post(post_id):
    data = request.get_json(silent=True) or {}
    if not data.get("title", "").strip() or not data.get("content", "").strip():
        return {"error": "제목과 내용을 입력하세요."}, 400

    with connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING id, title, content, created_at",
            (data["title"].strip(), data["content"].strip(), post_id),
        )
        post = cursor.fetchone()
        return (jsonify(post), 200) if post else ({"error": "게시글을 찾을 수 없습니다."}, 404)


# 게시글 삭제: 없는 글은 404, 삭제 성공은 본문 없이 204를 반환한다.
@app.delete("/posts/<int:post_id>")
def delete_post(post_id):
    with connect() as conn, conn.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id=%s", (post_id,))
        return ("", 204) if cursor.rowcount else ({"error": "게시글을 찾을 수 없습니다."}, 404)


# 컨테이너 외부 요청을 받을 수 있도록 모든 인터페이스에서 실행한다.
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
