# Compliance Document Review — Data Engineering

Data ingestion and retrieval pipeline for the Compliance Document Review App.

## Role in the project
This repo handles the Data Engineering side of the app:
- Extracting clean text from PDF / DOCX / XLSX documents
- Chunking extracted text for embedding
- Generating embeddings and storing them as vectors (pgvector)
- Powering three retrieval jobs: rule lookup, disclosure-by-absence, and precedent search

## Current status
- [x] Text extraction (PDF, DOCX, XLSX)
- [x] Chunking with overlap
- [x] Embedding pipeline (sentence-transformers, 384 dimensions)
- [x] Vector storage working end-to-end (extraction -> chunking -> embedding -> Postgres/pgvector)
- [x] Rule lookup job (working, tested)
- [x] Disclosure-by-absence job
- [x] Precedent search job
- [ ] Retrieval tuning

## Files
- `extract_text.py` — extracts text from DOCX files
- `extract_pdf.py` — extracts text from PDF files
- `extract_xlsx.py` — extracts text from XLSX files
- `chunk_text.py` — splits extracted text into
 overlapping chunks
- `embed_text.py` — quick test script for generating embeddings
- `store_embeddings.py` — full pipeline: extract, chunk, embed, and insert into Postgres (document_chunks table)
- `seed_rules.py` — seeds the rules table with sample compliance rules and their embeddings
- `rule_lookup.py` — reusable function that finds the top matching rules for a given document chunk
- `test_rule_lookup.py` — standalone test for the similarity search query
- `disclosure_check.py` — checks whether a required disclosure is present or missing in a document's chunks
- `precedent_search.py` — finds the most similar previously-reviewed chunks for a given query
- `api_server.py` — FastAPI wrapper exposing rule lookup, disclosure check, and precedent search as HTTP endpoints
- `db.py` — shared database connection helper, reads from DATABASE_URL env var
- `seed_document_chunks.py` — seeds document_chunks with generic sample data (no personal files needed)
- `retrieve_document.py` — retrieves the original uploaded file from Backend's internal endpoint (GET /api/v1/documents/{document_id}/file)

## How to run
pip install python-docx pdfplumber openpyxl sentence-transformers psycopg2-binary fastapi uvicorn
python store_embeddings.py
python seed_rules.py
python api_server.py
Or run the API server directly:
python -m uvicorn api_server:app --reload --port 5000
Then visit http://localhost:5000/docs for interactive API testing.

## API Endpoints

POST /rule-lookup
- Request: `{ "text": "..." }`
- Response: `[{ rule_id, rule_text, similarity_score }, ...]`

POST /disclosure-check
- Request: `{ "document_chunks": ["..."], "disclosure_id": "...", "disclosure_text": "..." }`
- Response: `{ disclosure_id, disclosure_type, present, similarity_score, matched_chunk_id }`

POST /precedent-search
- Request: `{ "text": "..." }`
- Response: `[{ document_id, chunk_id, similarity_score, chunk_text }, ...]`

## Database schema
`document_chunks` table:
- `id` SERIAL PRIMARY KEY
- `chunk_text` TEXT
- `embedding` vector(384)

`rules` table:
- `id` SERIAL PRIMARY KEY
- `rule_id` TEXT
- `rule_text` TEXT
- `embedding` vector(384)

## Retrieval response format
Rule lookup: `{ rule_id: string, rule_text: string, similarity_score: float }`
Disclosure-by-absence: `{ disclosure_id: string, disclosure_type: string, present: boolean, similarity_score: float, matched_chunk_id: string | null }`
Precedent match: `{ document_id: string, chunk_id: string, similarity_score: float, chunk_text: string }`

## Dependencies (waiting on)
- AI team: embedding model confirmed (sentence-transformers, all-MiniLM-L6-v2, 384 dims) — AI integrating against my API endpoints
- Backend: endpoint confirmed (GET /api/v1/documents/{document_id}/file, auth via INTERNAL_SERVICE_TOKEN) — have real token and test document_id, but need a reachable URL (Backend currently only runs on Petros's local machine)
- DevOps: pgvector/Postgres access confirmed and working

## Notes
This pipeline is designed to be invoked as a script/job when a document is submitted, not run as a long-lived service.

The `document_id` field in precedent search is currently a placeholder — will be updated once Backend's document metadata format is available.

Database connection now reads from DATABASE_URL env var (see .env.example) instead of hardcoded credentials.