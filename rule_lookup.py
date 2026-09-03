from sentence_transformers import SentenceTransformer
import psycopg2

# Load the embedding model once (reused across calls)
model = SentenceTransformer('all-MiniLM-L6-v2')

def find_matching_rules(chunk_text, top_n=3):
    """
    Given a document chunk, find the most relevant compliance rules.
    Returns a list of (rule_id, rule_text, similarity_score).
    """
    # Step 1: Embed the input chunk
    chunk_embedding = model.encode(chunk_text)

    # Step 2: Connect to the database
    conn = psycopg2.connect(
        host="localhost", port=5432,
        dbname="compliance_review", user="compliance", password="compliance"
    )
    cursor = conn.cursor()

    # Step 3: Find the closest matching rules using vector distance
    cursor.execute(
        "SELECT rule_id, rule_text, embedding <-> %s::vector AS distance "
        "FROM rules ORDER BY distance LIMIT %s",
        (chunk_embedding.tolist(), top_n)
    )
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # Step 4: Format results as a list of dictionaries (matches the response shape we proposed to the team)
    matches = []
    for rule_id, rule_text, distance in results:
        similarity_score = 1 / (1 + distance)  # convert distance to a 0-1 similarity score
        matches.append({
            "rule_id": rule_id,
            "rule_text": rule_text,
            "similarity_score": round(similarity_score, 4)
        })
    return matches


# Quick test when running this file directly
if __name__ == "__main__":
    test_chunk = "We promise you will earn 15% guaranteed profit every year with zero risk."
    matches = find_matching_rules(test_chunk)
    print(f"Chunk: {test_chunk}\n")
    for m in matches:
        print(m)