from agent import run_agent

from memory.conversation import (
    clear_memory
)

from memory.facts import (
    get_facts,
    clear_facts
)

from rag.vector_store import (
    build_vector_store
)


print("=" * 65)
print("Python OpenRouter AI Agent - V7")
print("=" * 65)

print()
print("Features:")
print("✓ Tool Calling")
print("✓ Dynamic Tool Registry")
print("✓ Persistent Memory")
print("✓ Long-Term Facts")
print("✓ Memory Search")
print("✓ Local RAG")
print("✓ LanceDB")
print("✓ Weather")
print("✓ Simple Agent Planner")
print()

print("Commands:")
print("/build       - Build RAG database")
print("/facts       - Show stored facts")
print("/clear       - Clear conversation")
print("/clearfacts  - Clear stored facts")
print("/exit        - Exit")
print()


while True:

    try:

        user_input = input(
            "You: "
        ).strip()

    except (
        KeyboardInterrupt,
        EOFError
    ):

        print()
        print("Goodbye!")
        break

    if not user_input:
        continue

    command = user_input.lower()

    # -------------------------
    # EXIT
    # -------------------------

    if command == "/exit":

        print("Goodbye!")

        break

    # -------------------------
    # CLEAR CONVERSATION
    # -------------------------

    if command == "/clear":

        clear_memory()

        print()
        print(
            "Conversation memory cleared."
        )
        print()

        continue

    # -------------------------
    # SHOW FACTS
    # -------------------------

    if command == "/facts":

        print()
        print("Stored User Facts:")
        print("-" * 40)

        try:

            facts = get_facts()

            if not facts:

                print(
                    "No facts stored yet."
                )

            else:

                for index, fact in enumerate(
                    facts,
                    start=1
                ):

                    print(
                        f"{index}. {fact}"
                    )

        except Exception as error:

            print(
                "Memory Error:"
            )

            print(error)

        print()

        continue

    # -------------------------
    # CLEAR FACTS
    # -------------------------

    if command == "/clearfacts":

        clear_facts()

        print()
        print(
            "Stored facts cleared."
        )
        print()

        continue

    # -------------------------
    # BUILD RAG
    # -------------------------

    if command == "/build":

        print()
        print(
            "Building vector database..."
        )

        try:

            result = build_vector_store()

            if result.get("success"):

                print(
                    "✓ Vector database built."
                )

                print(
                    "Documents:",
                    result.get(
                        "documents",
                        0
                    )
                )

                print(
                    "Chunks:",
                    result.get(
                        "chunks",
                        0
                    )
                )

            else:

                print(
                    "RAG Error:"
                )

                print(
                    result.get(
                        "message",
                        "Unknown error"
                    )
                )

        except Exception as error:

            print(
                "RAG Error:"
            )

            print(error)

        print()

        continue

    # -------------------------
    # NORMAL AGENT
    # -------------------------

    try:

        answer = run_agent(
            user_input
        )

        print()
        print("Agent:")
        print(answer)
        print()

    except Exception as error:

        print()
        print("Agent Error:")
        print(error)

        print()