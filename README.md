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
- [ ] Disclosure-by-absence job
- [ ] Precedent search job
- [ ] Retrieval tuning

## Files
- `extract_text.py` — extracts text from DOCX files
- `extract_pdf.py` — extracts text from PDF files
- `extract_xlsx.py` — extracts text from XLSX files
- `chunk_text.py` — splits extracted text into overlapping chunks
- `embed_text.py` — quick test script for generating embeddings
- `store_embeddings.py` — full pipeline: extract, chunk, embed, and insert into Postgres (document_chunks table)
- `seed_rules.py` — seeds the rules table with sample compliance rules and their embeddings
- `rule_lookup.py` — reusable function that finds the top matching rules for a given document chunk
- `test_rule_lookup.py` — standalone test for the similarity search query

## How to run
```
pip install python-docx pdfplumber openpyxl sentence-transformers psycopg2-binary
python store_embeddings.py
python seed_rules.py
python rule_lookup.py
```
Requires the platform repo's Postgres + pgvector database running (see compliance-document-review-platform).

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

## Dependencies (waiting on)
- AI team: confirmed masked-text format (document_id, chunk_id, masked_text); embedding model still being finalized
- Backend: file-storage/access contract in progress (Data Engineering will retrieve stored files and run its own extraction pipeline)
- DevOps: pgvector/Postgres access confirmed and working

## Notes
This pipeline is designed to be invoked as a script/job when a document is submitted, not run as a long-lived service.