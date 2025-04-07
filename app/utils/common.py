import logging.config
import os
import base64
from typing import List
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta
from app.config import ADMIN_PASSWORD, ADMIN_USER, ALGORITHM, SECRET_KEY
import validators
from urllib.parse import urlparse, urlunparse

# Load environment variables from .env file for security and configuration.
load_dotenv()

# Set up logging configuration.
def setup_logging():
    logging_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'logging.conf')
    normalized_path = os.path.normpath(logging_config_path)
    logging.config.fileConfig(normalized_path, disable_existing_loggers=False)

# Authenticate the user with a simple check for the admin credentials.
def authenticate_user(username: str, password: str):
    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        return {"username": username}
    logging.warning(f"Authentication failed for user: {username}")
    return None

# Generate an access token using JWT.
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Validate and sanitize URL.
def validate_and_sanitize_url(url_str):
    if validators.url(url_str):
        parsed_url = urlparse(url_str)
        sanitized_url = urlunparse(parsed_url)
        return sanitized_url
    else:
        logging.error(f"Invalid URL provided: {url_str}")
        return None

# Encode URL to a safe filename.
def encode_url_to_filename(url):
    sanitized_url = validate_and_sanitize_url(str(url))
    if sanitized_url is None:
        raise ValueError("Provided URL is invalid and cannot be encoded.")
    encoded_bytes = base64.urlsafe_b64encode(sanitized_url.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8').rstrip('=')
    return encoded_str

# Decode a filename back to a URL.
def decode_filename_to_url(encoded_str: str) -> str:
    padding_needed = 4 - (len(encoded_str) % 4)
    if padding_needed:
        encoded_str += "=" * padding_needed
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    return decoded_bytes.decode('utf-8')

# Generate HATEOAS links for QR code resources.
def generate_links(action: str, qr_filename: str, base_api_url: str, download_url: str) -> List[dict]:
    links = []
    if action in ["list", "create"]:
        original_url = decode_filename_to_url(qr_filename[:-4])
        links.append({"rel": "view", "href": download_url, "action": "GET", "type": "image/png"})
    if action in ["list", "create", "delete"]:
        delete_url = f"{base_api_url}/qr-codes/{qr_filename}"
        links.append({"rel": "delete", "href": delete_url, "action": "DELETE", "type": "application/json"})
    return links

# Create the directory if it doesn't exist for storing QR codes.
def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

# Directory for saving QR codes
QR_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', 'qr_codes')
QR_DIRECTORY = os.path.normpath(QR_DIRECTORY)
