import os
import lancedb

from rag.embeddings import embedding_model
from rag.document_loader import (
    load_documents,
    chunk_text
)


DB_PATH = "db"
TABLE_NAME = "documents"


def get_database():

    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)

    return lancedb.connect(DB_PATH)


def build_vector_store():

    documents = load_documents()

    if not documents:
        return {
            "success": False,
            "message": "No documents found."
        }

    rows = []

    for document in documents:

        chunks = chunk_text(
            document["content"]
        )

        for index, chunk in enumerate(chunks):

            embedding = embedding_model.embed(
                chunk
            )

            rows.append({
                "vector": embedding,
                "text": chunk,
                "source": document["filename"],
                "chunk_id": index
            })

    if not rows:
        return {
            "success": False,
            "message": "No text chunks found."
        }

    db = get_database()

    existing_tables = db.table_names()

    if TABLE_NAME in existing_tables:
        db.drop_table(TABLE_NAME)

    db.create_table(
        TABLE_NAME,
        data=rows
    )

    return {
        "success": True,
        "documents": len(documents),
        "chunks": len(rows)
    }