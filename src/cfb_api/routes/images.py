from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from src.cfb_api.services.s3_service import get_image
from botocore.exceptions import ClientError

bp = Blueprint('images', __name__)

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
    bucket = request.args.get('bucket')
    path = request.args.get('path')
    
    # Validate required parameters
    if not bucket or not path:
        return jsonify({
            "error": "Missing parameters",
            "description": "Both 'bucket' and 'path' parameters are required",
            "code": 400
        }), 400
    
    try:
        image_data, content_type = get_image(bucket, path)
        return send_file(
            BytesIO(image_data),
            mimetype=content_type,
            download_name=path.split('/')[-1]
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
