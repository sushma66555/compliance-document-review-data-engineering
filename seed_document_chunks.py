from sentence_transformers import SentenceTransformer
import psycopg2

model = SentenceTransformer('all-MiniLM-L6-v2')

# Generic sample document text (no personal data) for testing precedent search
sample_chunks = [
    "The advisor recommended a diversified portfolio with a mix of equities and bonds based on the client's risk tolerance.",
    "Please note that past performance does not guarantee future results, and all investments carry risk of loss.",
    "Management fees are charged quarterly at 1.5% of assets under management, as disclosed in the client agreement.",
    "The client testimonial reflects individual experience and may not be representative of all client outcomes.",
]

model_embeddings = model.encode(sample_chunks)

conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="compliance_review", user="compliance", password="compliance"
)
cursor = conn.cursor()

for chunk_text, embedding in zip(sample_chunks, model_embeddings):
    cursor.execute(
        "INSERT INTO document_chunks (chunk_text, embedding) VALUES (%s, %s)",
        (chunk_text, embedding.tolist())
    )

conn.commit()
cursor.close()
conn.close()
print(f"Inserted {len(sample_chunks)} sample chunks into document_chunks!")