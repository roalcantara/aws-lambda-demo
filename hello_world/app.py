import json
import logging
import os
import urllib.request
from typing import Any, Dict

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Default CORS headers for API Gateway responses
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",  # Use specific origin in production
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,OPTIONS",
}

# External service URL - configurable via environment variable
CHECKIP_URL = os.environ.get("CHECKIP_URL", "http://checkip.amazonaws.com/")


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Sample pure Lambda function

    This function demonstrates a basic AWS Lambda handler that:
    - Fetches the caller's IP address from an external service
    - Returns a JSON response with a greeting and location
    - Handles errors gracefully with proper HTTP responses
    - Supports CORS for browser-based testing

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html

    Examples
    --------
    Successful response:
        {
            "statusCode": 200,
            "headers": {...},
            "body": '{"message": "hello world", "location": "1.2.3.4"}'
        }

    Error response:
        {
            "statusCode": 500,
            "headers": {...},
            "body": '{"message": "Internal server error", "error": "Failed to fetch location"}'
        }
    """

    # Handle OPTIONS request for CORS preflight
    if event.get("httpMethod") == "OPTIONS":
        logger.info("Handling CORS preflight request")
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "OK"}),
        }

    try:
        logger.info(f"Fetching IP address from {CHECKIP_URL}")
        with urllib.request.urlopen(CHECKIP_URL, timeout=5) as resp:
            ip_text = resp.read().decode("utf-8").strip()

        logger.info(f"Successfully fetched IP: {ip_text}")

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "message": "hello world",
                "location": ip_text,
            }),
        }

    except urllib.error.URLError as e:
        logger.error(f"Network error fetching IP: {str(e)}", exc_info=True)
        return {
            "statusCode": 503,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "message": "Service unavailable",
                "error": "Failed to fetch location information",
            }),
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "message": "Internal server error",
                "error": "An unexpected error occurred",
            }),
        }
