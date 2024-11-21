# cfb_api

A Flask-based API for college football data, containerized with Docker and deployable to AWS App Runner.

## Prerequisites

- Docker installed locally
- AWS CLI configured with appropriate credentials
- AWS App Runner access configured

## Local Development

1. Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Run the application locally:
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
   - No additional environment variables are required
   - The service will automatically scale based on traffic

4. Deploy the service:
   - Click "Create service" to start the deployment
   - AWS App Runner will build and deploy your application
   - Once complete, you'll receive a service URL where your API is accessible

## Environment Variables

No environment variables are required for basic operation. The application uses default configurations suitable for both development and production environments.

## API Endpoints

- GET /items - Returns list of all items
- GET /items/<id> - Returns specific item by ID
- POST /items - Creates a new item

## Production Notes

The application runs using Gunicorn in production, configured for optimal performance on AWS App Runner. The service will automatically scale based on traffic, including scaling to near-zero during periods of inactivity.
