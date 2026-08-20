#
#
#
#
#
#




from flask import Flask, jsonify, request

app = Flask(__name__)

posts = []
next_id = 1


@app.get("/")
def home():
    return """
    <h1>미니 게시판 서버</h1>
    <p>GET /posts : 게시글 목록</p>
    <p>POST /posts : 게시글 작성</p>
    <p>GET /health : 서버 상태 확인</p>
    """


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/posts")
def get_posts():
    return jsonify(posts)


@app.get("/posts/<int:post_id>")
def get_post(post_id):
    post = next((item for item in posts if item["id"] == post_id), None)

    if post is None:
        return {"error": "게시글을 찾을 수 없습니다."}, 404

    return jsonify(post)

#

@app.post("/posts")
def create_post():
    global next_id

    data = request.get_json(silent=True) or {}

    if not data.get("title") or not data.get("content"):
        return {"error": "title과 content가 필요합니다."}, 400

    post = {
        "id": next_id,
        "title": data["title"],
        "content": data["content"],
    }

    posts.append(post)
    next_id += 1

    return jsonify(post), 201


@app.put("/posts/<int:post_id>")
def update_post(post_id):
    post = next((item for item in posts if item["id"] == post_id), None)

    if post is None:
        return {"error": "게시글을 찾을 수 없습니다."}, 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        post["title"] = data["title"]

    if "content" in data:
        post["content"] = data["content"]

    return jsonify(post)


@app.delete("/posts/<int:post_id>")
def delete_post(post_id):
    post = next((item for item in posts if item["id"] == post_id), None)

    if post is None:
        return {"error": "게시글을 찾을 수 없습니다."}, 404

    posts.remove(post)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
