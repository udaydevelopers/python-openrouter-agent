from memory.search import (
    search_memory
)


def memory_search(
    query,
    limit=5
):

    results = search_memory(
        query,
        limit
    )

    return {
        "results": results
    }