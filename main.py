from agent import run_agent

from memory.conversation import clear_memory
from memory.facts import get_facts
from rag.vector_store import build_vector_store


print("=" * 65)
print("Python OpenRouter AI Agent - V6")
print("=" * 65)

print()
print("Features:")
print("✓ Multiple Tools")
print("✓ Dynamic Tool Registry")
print("✓ Persistent Conversation Memory")
print("✓ Long-Term Facts")
print("✓ Memory Search")
print("✓ Local RAG")
print("✓ LanceDB Vector Search")
print("✓ Local Embeddings")
print("✓ Weather API")
print()

print("Commands:")
print("/build  - Build RAG vector database")
print("/facts  - Show stored user facts")
print("/clear  - Clear conversation memory")
print("/exit   - Exit application")
print()


while True:

    try:
        user_input = input("You: ").strip()

    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        break

    if not user_input:
        continue

    command = user_input.lower()

    # Exit
    if command == "/exit":
        print("Goodbye!")
        break

    # Clear conversation memory
    if command == "/clear":
        clear_memory()

        print()
        print("Conversation memory cleared.")
        print()

        continue

    # Build RAG vector database
    if command == "/build":

        print()
        print("Building RAG vector database...")
        print()

        try:
            result = build_vector_store()

            print("RAG Result:")

            if result.get("success"):
                print(
                    f"✓ Documents: "
                    f"{result.get('documents', 0)}"
                )

                print(
                    f"✓ Chunks: "
                    f"{result.get('chunks', 0)}"
                )

                print(
                    "✓ Vector database built successfully."
                )

            else:
                print(
                    f"✗ {result.get('message', 'Unknown error')}"
                )

        except Exception as error:

            print()
            print("RAG Error:")
            print(error)

        print()

        continue

    # Show stored facts
    if command == "/facts":

        print()
        print("Stored User Facts:")
        print("-" * 40)

        try:
            facts = get_facts()

            if not facts:
                print("No facts stored yet.")

            else:
                for index, fact in enumerate(
                    facts,
                    start=1
                ):
                    print(
                        f"{index}. {fact}"
                    )

        except Exception as error:

            print("Memory Error:")
            print(error)

        print()

        continue

    # Normal AI agent request
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