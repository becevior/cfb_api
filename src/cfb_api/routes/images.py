from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from src.cfb_api.services.s3_service import get_image
from botocore.exceptions import ClientError
from pydantic import BaseModel, Field, ValidationError

bp = Blueprint('images', __name__)

class ImageRequest(BaseModel):
    bucket: str = Field(..., description="S3 bucket name")
    path: str = Field(..., description="Object key/path in the bucket")

@bp.route('/images', methods=['GET'])
def get_image_from_s3():
    """
    Retrieve an image from S3 bucket based on query parameters.
    
    Query Parameters:
        bucket (str): Name of the S3 bucket
        path (str): Object key/path in the bucket
        
    Returns:
        flask.Response: Image file response or error JSON
        
    Example:
        GET /images?bucket=my-bucket&path=images/photo.jpg
    """
    try:
        image_request = ImageRequest(
            bucket=request.args.get('bucket'),
            path=request.args.get('path')
        )
    except ValidationError as e:
        return jsonify({
            "error": "Validation Error",
            "description": str(e),
            "code": 400
        }), 400
    
    try:
        image_data, content_type = get_image(image_request.bucket, image_request.path)
        return send_file(
            BytesIO(image_data),
            mimetype=content_type,
            download_name=image_request.path.split('/')[-1]
        )
    except FileNotFoundError as e:
        return jsonify({
            "error": "Not Found",
            "description": str(e),
            "code": 404
        }), 404
    except PermissionError as e:
        return jsonify({
            "error": "Access Denied",
            "description": str(e),
            "code": 403
        }), 403
    except ClientError as e:
        return jsonify({
            "error": "S3 Error",
            "description": str(e),
            "code": 500
        }), 500
