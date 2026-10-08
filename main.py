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


print("=" * 70)
print("Python OpenRouter AI Agent - V8")
print("=" * 70)

print()
print("Features:")
print("✓ Tool Calling")
print("✓ Dynamic Tool Registry")
print("✓ Persistent Memory")
print("✓ Long-Term Facts")
print("✓ Memory Search")
print("✓ Local RAG")
print("✓ LanceDB")
print("✓ Local Embeddings")
print("✓ Weather")
print("✓ Agent Planner")
print("✓ Web Search")
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

    # Exit
    if command == "/exit":

        print(
            "Goodbye!"
        )

        break

    # Clear conversation
    if command == "/clear":

        clear_memory()

        print()
        print(
            "Conversation memory cleared."
        )
        print()

        continue

    # Show facts
    if command == "/facts":

        print()
        print(
            "Stored User Facts:"
        )

        print(
            "-" * 40
        )

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

            print(
                error
            )

        print()

        continue

    # Clear facts
    if command == "/clearfacts":

        clear_facts()

        print()
        print(
            "Stored facts cleared."
        )
        print()

        continue

    # Build RAG
    if command == "/build":

        print()
        print(
            "Building vector database..."
        )

        try:

            result = (
                build_vector_store()
            )

            if result.get(
                "success"
            ):

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

            print(
                error
            )

        print()

        continue

    # Normal agent
    try:

        answer = run_agent(
            user_input
        )

        print()
        print(
            "Agent:"
        )

        print(
            answer
        )

        print()

    except Exception as error:

        print()
        print(
            "Agent Error:"
        )

        print(
            error
        )

        print()