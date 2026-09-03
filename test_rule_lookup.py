from sentence_transformers import SentenceTransformer
import psycopg2

# Step 1:sample document chunk
query_text = "We promise you will earn 15% guaranteed profit every year with zero risk."

# Step 2: Query embedding 
model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode(query_text)

# Step 3: Database "close" rules 
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
