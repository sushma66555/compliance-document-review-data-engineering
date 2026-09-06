from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer('all-MiniLM-L6-v2')

def check_disclosure(document_chunks, disclosure_id, disclosure_text, threshold=0.5):
    """
    Given a list of chunk texts from ONE document, check whether a required
    disclosure is present or missing based on similarity.
    Returns a dict matching the shape agreed with the team.
    """
    # Step 1: Embed the required disclosure text
    disclosure_embedding = model.encode(disclosure_text)

    # Step 2: Embed all the document's chunks and find the closest one
    chunk_embeddings = model.encode(document_chunks)

    best_score = -1
    best_chunk_index = None

    for i, chunk_embedding in enumerate(chunk_embeddings):
        # cosine similarity: closer to 1 means more similar
        similarity = _cosine_similarity(disclosure_embedding, chunk_embedding)
        if similarity > best_score:
            best_score = similarity
            best_chunk_index = i

    # Step 3: Decide present vs missing using the threshold
    found = best_score >= threshold

    return {
        "disclosure_id": disclosure_id,
        "disclosure_type": disclosure_text,
        "present": found,
        "similarity_score": round(float(best_score), 4),
        "matched_chunk_id": f"CHUNK-{best_chunk_index}" if found else None
    }


def _cosine_similarity(a, b):
    import numpy as np
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# Quick test when running this file directly
if __name__ == "__main__":
    # Test 1: Document with NO disclaimer (should be missing)
    test_chunks_missing = [
        "We promise you will earn 15% guaranteed profit every year with zero risk.",
        "Fees are 2% annually, billed quarterly.",
    ]

    # Test 2: Document that DOES include the disclaimer (should be present)
    test_chunks_present = [
        "We promise you will earn 15% guaranteed profit every year with zero risk.",
        "Please note that past performance does not guarantee future results.",
    ]

    required_disclosure = "Past performance does not guarantee future results."

    print("Test 1 (disclaimer missing):")
    result1 = check_disclosure(test_chunks_missing, "DISC-001", required_disclosure)
    print(result1)

    print("\nTest 2 (disclaimer present):")
    result2 = check_disclosure(test_chunks_present, "DISC-001", required_disclosure)
    print(result2)