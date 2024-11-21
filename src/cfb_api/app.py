from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Sample data (replace with your database or other data source)
data = {
    "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
    ]
}

# Error handler for HTTPExceptions
@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({
        "error": e.name,
        "description": e.description,
        "code": e.code,
    }).data
    response.content_type = "application/json"
    return response

# Error handler for other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for other errors."""
    return jsonify({
        "error": "Internal Server Error",
        "description": str(e),
        "code": 500
    }), 500


@app.route('/items', methods=['GET'])
def get_items():
    """Returns a list of items."""
    return jsonify(data['items'])


@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Returns a single item by ID."""
    for item in data['items']:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404


@app.route('/items', methods=['POST'])
def create_item():
    """Creates a new item."""
    try:
        new_item = request.get_json()
        new_item['id'] = len(data['items']) + 1  # Assign a new ID
        data['items'].append(new_item)
        return jsonify(new_item), 201 # 201 Created
    except Exception as e:
        return jsonify({"error": "Invalid request data", "description": str(e)}), 400

