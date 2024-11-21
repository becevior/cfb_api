from flask import Blueprint, jsonify, request

bp = Blueprint('items', __name__)

# Sample data (replace with your database or other data source)
data = {
    "items": [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
    ]
}

@bp.route('/items', methods=['GET'])
def get_items():
    """Returns a list of items."""
    return jsonify(data['items'])

@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Returns a single item by ID."""
    for item in data['items']:
        if item['id'] == item_id:
            return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@bp.route('/items', methods=['POST'])
def create_item():
    """Creates a new item."""
    try:
        new_item = request.get_json()
        new_item['id'] = len(data['items']) + 1  # Assign a new ID
        data['items'].append(new_item)
        return jsonify(new_item), 201 # 201 Created
    except Exception as e:
        return jsonify({"error": "Invalid request data", "description": str(e)}), 400
