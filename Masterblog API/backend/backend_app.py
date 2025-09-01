from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Second post", "content": "This is the second post about Flask."},
    {"id": 2, "title": "First post", "content": "This is the first post about Python."},
    {"id": 3, "title": "A Third Post", "content": "This post discusses both Python and Flask."}
]


@app.route('/', methods=['GET'])
def home():
    """A simple welcome message for the root URL."""
    return "<h1>Welcome to the Flask API!</h1><p>Navigate to /api/posts to see the data.</p>"


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Searches for posts by title or content."""
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    if not title_query and not content_query:
        return jsonify(POSTS)

    results = []
    for post in POSTS:
        post_title_lower = post['title'].lower()
        post_content_lower = post['content'].lower()
        if title_query and title_query.lower() in post_title_lower:
            if post not in results:
                results.append(post)
        if content_query and content_query.lower() in post_content_lower:
            if post not in results:
                results.append(post)
    return jsonify(results)


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """
    Handles GET and POST requests for the /api/posts endpoint.
    GET: Returns a list of all posts, with optional sorting.
    POST: Creates a new post.
    """
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        data = request.get_json()
        new_post = {"id": len(POSTS) + 1, "title": data.get('title'), "content": data.get('content')}
        POSTS.append(new_post)
        return jsonify(new_post), 201
    else:
        # --- START of new sorting logic for GET requests ---
        sort_by = request.args.get('sort')
        direction = request.args.get('direction')

        # Make a copy to avoid modifying the original list
        sorted_posts = list(POSTS)

        # Check if a valid sort key is provided
        if sort_by in ['title', 'content']:
            # Determine the sorting direction
            is_reverse = direction == 'desc'

            # Sort the list using a lambda function as the key
            sorted_posts = sorted(sorted_posts, key=lambda x: x[sort_by].lower(), reverse=is_reverse)

        return jsonify(sorted_posts)
        # --- END of new sorting logic ---


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """Updates a post by its ID."""
    post_to_update = next((p for p in POSTS if p["id"] == id), None)
    if not post_to_update:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()
    post_to_update['title'] = data.get('title', post_to_update['title'])
    post_to_update['content'] = data.get('content', post_to_update['content'])
    return jsonify(post_to_update), 200


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Deletes a post by its ID."""
    global POSTS
    post_to_delete = next((p for p in POSTS if p["id"] == id), None)
    if post_to_delete:
        POSTS.remove(post_to_delete)
        return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": f"Post with id {id} not found."}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

