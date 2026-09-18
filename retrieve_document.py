import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN")

def retrieve_document_file(document_id):
    """
    Fetches the original uploaded file from Backend.
    Returns (file_bytes, content_type).
    """
    url = f"{BACKEND_URL}/api/v1/documents/{document_id}/file"
    headers = {"Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    return response.content, content_type


if __name__ == "__main__":
    file_bytes, content_type = retrieve_document_file(7)
    print(f"Retrieved {len(file_bytes)} bytes, type: {content_type}")