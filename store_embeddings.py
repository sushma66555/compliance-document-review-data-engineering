from docx import Document
from sentence_transformers import SentenceTransformer
import psycopg2

# Step 1: Extract text
doc = Document("Sushma_Yadav_Data_Engineer_Resume.docx")
text_parts = []
for para in doc.paragraphs:
    if para.text.strip():
        text_parts.append(para.text)
full_text = "\n".join(text_parts)

# Step 2: Chunk it
def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(full_text)

# Step 3: Embed all chunks
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)

# Step 4: Connect to Postgres and insert
conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="compliance_review", user="compliance", password="compliance"
)
cursor = conn.cursor()

for chunk, embedding in zip(chunks, embeddings):
    cursor.execute(
        "INSERT INTO document_chunks (chunk_text, embedding) VALUES (%s, %s)",
        (chunk, embedding.tolist())
    )

conn.commit()
cursor.close()
conn.close()
print(f"Inserted {len(chunks)} chunks into the database!")