from agent import run_agent

from memory.conversation import (
    clear_memory
)

from rag.vector_store import (
    build_vector_store
)


print("=" * 65)
print(
    "Python OpenRouter AI Agent - V5"
)
print("=" * 65)

print()
print("Features:")
print("✓ Multiple Tools")
print("✓ Dynamic Tool Registry")
print("✓ Persistent Conversation Memory")
print("✓ Local RAG")
print("✓ LanceDB Vector Search")
print("✓ Local Embeddings")
print("✓ Weather API")
print()

print("Commands:")
print("/build  - Build RAG vector database")
print("/clear  - Clear conversation memory")
print("/exit   - Exit application")
print()


while True:

    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "/exit":

        print("Goodbye!")

        break

    if user_input.lower() == "/clear":

        clear_memory()

        print()
        print(
            "Conversation memory cleared."
        )
        print()

        continue

    if user_input.lower() == "/build":

        print()
        print(
            "Building vector database..."
        )

        try:

            result = build_vector_store()

            print()
            print(
                "RAG:"
            )
            print(result)
            print()

        except Exception as error:

            print()
            print(
                "RAG Error:"
            )
            print(error)
            print()

        continue

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
        print("Error:")
        print(error)
        print()