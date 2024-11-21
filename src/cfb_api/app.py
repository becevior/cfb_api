from flask import Flask
from werkzeug.exceptions import HTTPException
from flask import jsonify

app = Flask(__name__)

# Import routes after app initialization to avoid circular imports
from src.cfb_api.routes import items, images

# Register blueprints
app.register_blueprint(items.bp)
app.register_blueprint(images.bp)

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
