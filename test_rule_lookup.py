import psycopg2
from shared_model import get_shared_model


def run_test_rule_lookup():
    # Step 1: sample document chunk
    query_text = "We promise you will earn 15% guaranteed profit every year with zero risk."

    # Step 2: Query embedding
    model = get_shared_model()
    query_embedding = model.encode(query_text)

    # Step 3: Database "close" rules
    try:
        conn = psycopg2.connect(
            host="localhost", port=5432,
            dbname="compliance_review", user="compliance", password="compliance"
        )
        cursor = conn.cursor()

        cursor.execute(
            "SELECT rule_id, rule_text, embedding <-> %s::vector AS distance "
            "FROM rules ORDER BY distance LIMIT 3",
            (query_embedding.tolist(),)
        )

        print(f"Query: {query_text}\n")
        print("Top matching rules:")
        for rule_id, rule_text, distance in cursor.fetchall():
            print(f"  [{rule_id}] (distance: {distance:.4f}) {rule_text}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database connection error in manual test: {e}")


if __name__ == "__main__":
    run_test_rule_lookup()
