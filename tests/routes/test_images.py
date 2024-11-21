import pytest
from io import BytesIO
from unittest.mock import patch, MagicMock
from src.cfb_api.app import app
from botocore.exceptions import ClientError

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_image_missing_parameters(client):
    """Test that the endpoint returns 400 when parameters are missing."""
    # Test missing both parameters
    response = client.get('/images')
    assert response.status_code == 400
    assert b'Missing parameters' in response.data
    
    # Test missing path parameter
    response = client.get('/images?bucket=test-bucket')
    assert response.status_code == 400
    
    # Test missing bucket parameter
    response = client.get('/images?path=test.jpg')
    assert response.status_code == 400

@patch('src.cfb_api.routes.images.get_image')
def test_get_image_success(mock_get_image, client):
    """Test successful image retrieval."""
    # Mock successful image retrieval
    mock_image_data = b'fake-image-data'
    mock_get_image.return_value = (mock_image_data, 'image/jpeg')
    
    response = client.get('/images?bucket=test-bucket&path=test.jpg')
    
    assert response.status_code == 200
    assert response.mimetype == 'image/jpeg'
    assert response.data == mock_image_data

@patch('src.cfb_api.routes.images.get_image')
def test_get_image_not_found(mock_get_image, client):
    """Test image not found scenario."""
    mock_get_image.side_effect = FileNotFoundError("Image not found")
    
    response = client.get('/images?bucket=test-bucket&path=nonexistent.jpg')
    
    assert response.status_code == 404
    assert b'Not Found' in response.data

@patch('src.cfb_api.routes.images.get_image')
def test_get_image_permission_denied(mock_get_image, client):
    """Test permission denied scenario."""
    mock_get_image.side_effect = PermissionError("Access denied")
    
    response = client.get('/images?bucket=test-bucket&path=test.jpg')
    
    assert response.status_code == 403
    assert b'Access Denied' in response.data

@patch('src.cfb_api.routes.images.get_image')
def test_get_image_s3_error(mock_get_image, client):
    """Test S3 client error scenario."""
    mock_error = ClientError(
        operation_name='GetObject',
        error_response={'Error': {'Code': 'InternalError', 'Message': 'S3 Error'}}
    )
    mock_get_image.side_effect = mock_error
    
    response = client.get('/images?bucket=test-bucket&path=test.jpg')
    
    assert response.status_code == 500
    assert b'S3 Error' in response.data