from retrieve_document import retrieve_document_file
from extract_from_bytes import extract_text_from_bytes

from fastapi import FastAPI
from pydantic import BaseModel

from rule_lookup import find_matching_rules
from disclosure_check import check_disclosure
from precedent_search import find_precedents

app = FastAPI()


# Request format for rule lookup and precedent search
class TextQuery(BaseModel):
    text: str


# Request format for disclosure check
class DisclosureQuery(BaseModel):
    document_chunks: list[str]
    disclosure_id: str
    disclosure_text: str


@app.post("/rule-lookup")
def rule_lookup_endpoint(query: TextQuery):
    return find_matching_rules(query.text)


@app.post("/disclosure-check")
def disclosure_check_endpoint(query: DisclosureQuery):
    return check_disclosure(query.document_chunks, query.disclosure_id, query.disclosure_text)


@app.post("/precedent-search")
def precedent_search_endpoint(query: TextQuery):
    return find_precedents(query.text)

@app.get("/documents/{document_id}/extracted-text")
def get_extracted_text(document_id: int):
    file_bytes, content_type = retrieve_document_file(document_id)
    text = extract_text_from_bytes(file_bytes, content_type)
    return {"document_id": document_id, "extracted_text": text}