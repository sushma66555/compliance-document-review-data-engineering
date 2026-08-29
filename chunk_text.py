from docx import Document

# Step 1: Extract text 
doc = Document("Sushma_Yadav_Data_Engineer_Resume.docx")
text_parts = []
for para in doc.paragraphs:
    if para.text.strip():
        text_parts.append(para.text)
full_text = "\n".join(text_parts)

# Step 2: Chunking function
def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# Step 3: Test it
chunks = chunk_text(full_text)
print("Total chunks created:", len(chunks))
print()
print("Chunk 1:")
print(chunks[0])
print()
print("Chunk 2:")
print(chunks[1])