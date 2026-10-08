import re

from memory.conversation import (
    load_memory
)


def search_memory(
    query,
    limit=10
):

    memory = load_memory()

    query = query.lower()

    results = []

    for item in reversed(memory):

        text = item.get(
            "content",
            ""
        ).lower()

        if query in text:

            results.append(item)

        if len(results) >= limit:
            break

    return results