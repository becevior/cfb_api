# cfb_api

A Flask-based API for college football data, containerized with Docker and deployable to AWS App Runner.

## Prerequisites

- Docker installed locally
- AWS CLI configured with appropriate credentials
- AWS App Runner access configured
- AWS S3 bucket access configured with appropriate IAM roles/permissions

## Local Development

1. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Configure AWS credentials:
- Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
- Or configure AWS CLI credentials file (~/.aws/credentials)

4. Run the application locally:
python -m src.cfb_api.app

## Docker Build and Run

1. Build the Docker image:
docker build -t cfb_api .

2. Run the container locally:
docker run -p 8000:8000 cfb_api

The API will be available at http://localhost:8000

## AWS App Runner Deployment

1. Ensure your AWS CLI is configured with appropriate credentials

2. Create a new App Runner service:
   - Select "Source code repository" as the source
   - Choose your repository containing the cfb_api code
   - Select the branch you want to deploy
   - AWS App Runner will automatically detect the apprunner.yaml configuration

3. Configure the service:
   - The service will use the configuration from apprunner.yaml
   - Set required AWS credentials as environment variables
   - The service will automatically scale based on traffic

4. Deploy the service:
   - Click "Create service" to start the deployment
   - AWS App Runner will build and deploy your application
   - Once complete, you'll receive a service URL where your API is accessible

## Environment Variables

Required environment variables:
- AWS_ACCESS_KEY_ID: AWS access key for S3 bucket access
- AWS_SECRET_ACCESS_KEY: AWS secret key for S3 bucket access
- AWS_DEFAULT_REGION: AWS region (e.g., us-east-1)

## Project Structure

src/cfb_api/
├── app.py              # Main application file
├── services/
│   └── s3_service.py   # AWS S3 interaction service
└── routes/
    ├── images.py       # Image retrieval routes
    └── items.py        # Item management routes

## API Endpoints

### Items API
- GET /items - Returns list of all items
- GET /items/<id> - Returns specific item by ID
- POST /items - Creates a new item

### Images API
- GET /images - Retrieves an image from S3 bucket
  - Query Parameters:
    - bucket (required): S3 bucket name (e.g., connerbeckwith-images)
    - path (required): Object key/path in bucket (e.g., headshot.jpg)
  - Example: GET /images?bucket=connerbeckwith-images&path=headshot.jpg

## Production Notes

The application runs using Gunicorn in production, configured for optimal performance on AWS App Runner. The service will automatically scale based on traffic, including scaling to near-zero during periods of inactivity.
