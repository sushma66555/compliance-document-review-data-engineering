import requests

BACKEND_URL = "http://127.0.0.1:8000"  # placeholder, confirm with Petros
INTERNAL_SERVICE_TOKEN = "placeholder-token"  # get real value from Petros

def retrieve_document_file(document_id):
    """
    Fetches the original uploaded file from Backend using the internal service endpoint.
    """
    url = f"{BACKEND_URL}/api/v1/documents/{document_id}/file"
    headers = {"Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raises an error if the request failed
    return response.content  # the raw file bytes


if __name__ == "__main__":
    file_bytes = retrieve_document_file(7)  # test with document_id 7
    print(f"Retrieved {len(file_bytes)} bytes")