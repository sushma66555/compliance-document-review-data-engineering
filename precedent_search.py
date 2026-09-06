from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_precedents(query_text, top_n=3):
    """
    Given a chunk of text from a new document, find the most similar
    previously-reviewed chunks (precedents) from document_chunks.
    Returns a list of dicts matching the shape agreed with the team.
    """
    query_embedding = model.encode(query_text)

    conn = psycopg2.connect(
        host="localhost", port=5432,
        dbname="compliance_review", user="compliance", password="compliance"
    )
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, chunk_text, embedding <-> %s::vector AS distance "
        "FROM document_chunks ORDER BY distance LIMIT %s",
        (query_embedding.tolist(), top_n)
    )
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    precedents = []
    for chunk_id, chunk_text, distance in results:
        similarity_score = 1 / (1 + distance)
        precedents.append({
            "document_id": "DOC-EXISTING",  # placeholder until Backend provides real document IDs
            "chunk_id": f"CHUNK-{chunk_id}",
            "similarity_score": round(similarity_score, 4),
            "chunk_text": chunk_text
        })
    return precedents


if __name__ == "__main__":
    test_query = "Experience building data pipelines with Python and SQL."
    results = find_precedents(test_query)
    print(f"Query: {test_query}\n")
    for r in results:
        print(r)