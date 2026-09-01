from sentence_transformers import SentenceTransformer

# Step 1: Load the embedding model (downloads once, then cached)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Some example sentences to test
sentences = [
    "The task is complete",
    "The task is done",
    "The weather is sunny today"
]

# Step 3: Generate embeddings
embeddings = model.encode(sentences)

# Step 4: Show the results
for i, sentence in enumerate(sentences):
    print(f"Sentence: {sentence}")
    print(f"Embedding size: {len(embeddings[i])}")
    print(f"First 5 numbers: {embeddings[i][:5]}")
    print()