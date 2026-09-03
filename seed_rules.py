from sentence_transformers import SentenceTransformer
import psycopg2

# Step 1: dummy compliance rules (test data)
rules = [
    ("RULE-001", "Advisors must not guarantee investment returns or promise specific profit outcomes."),
    ("RULE-002", "Any mention of risk must be accompanied by a clear disclosure of potential losses."),
    ("RULE-003", "Client testimonials require a disclaimer that past performance does not indicate future results."),
    ("RULE-004", "Fees and commissions must be disclosed clearly before any transaction is finalized."),
]

# Step 2: Embed each rule's text
model = SentenceTransformer('all-MiniLM-L6-v2')
rule_texts = [r[1] for r in rules]
embeddings = model.encode(rule_texts)

# Step 3: Insert into the rules table
conn = psycopg2.connect(
    host="localhost", port=5432,
    dbname="compliance_review", user="compliance", password="compliance"
)
cursor = conn.cursor()

for (rule_id, rule_text), embedding in zip(rules, embeddings):
    cursor.execute(
        "INSERT INTO rules (rule_id, rule_text, embedding) VALUES (%s, %s, %s)",
        (rule_id, rule_text, embedding.tolist())
    )

conn.commit()
cursor.close()
conn.close()
print(f"Inserted {len(rules)} rules into the database!")