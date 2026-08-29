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
- [ ] Embedding pipeline
- [ ] Vector storage schema
- [ ] Rule retrieval job
- [ ] Disclosure-by-absence job
- [ ] Precedent search job
- [ ] Retrieval tuning

## Files
- `extract_text.py` — extracts text from DOCX files
- `extract_pdf.py` — extracts text from PDF files
- `extract_xlsx.py` — extracts text from XLSX files
- `chunk_text.py` — splits extracted text into overlapping chunks

## How to run
pip install python-docx pdfplumber openpyxl
python extract_text.py


## Notes
This pipeline is designed to be invoked as a script/job when a document is submitted, not run as a long-lived service.

## Dependencies (waiting on)
- AI team: embedding model/API choice + format for masked text handoff
- Backend: document storage location + access method
- DevOps: pgvector/Postgres connection details