import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://compliance:compliance@localhost:5432/compliance_review"
)

def get_connection():
    return psycopg2.connect(DATABASE_URL)