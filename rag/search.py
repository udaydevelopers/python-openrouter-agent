from rag.vector_store import (
    get_database,
    TABLE_NAME
)

from rag.embeddings import embedding_model


def search_documents(
    query,
    top_k=5
):

    db = get_database()

    if TABLE_NAME not in db.table_names():
        return []

    table = db.open_table(TABLE_NAME)

    query_embedding = embedding_model.embed(
        query
    )

    results = (
        table.search(query_embedding)
        .limit(top_k)
        .to_list()
    )

    return results