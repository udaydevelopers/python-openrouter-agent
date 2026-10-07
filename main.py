from agent import run_agent

from memory.conversation import (
    clear_memory
)


# ==================================================
# Header
# ==================================================

print("=" * 60)

print(
    "Python OpenRouter AI Agent - V4"
)

print("=" * 60)

print()

print(
    "Features:"
)

print(
    "✓ Multiple Tools"
)

print(
    "✓ Dynamic Tool Registry"
)

print(
    "✓ Persistent Conversation Memory"
)

print()

print(
    "Commands:"
)

print(
    "/clear  - Clear conversation memory"
)

print(
    "/exit   - Exit application"
)

print()


# ==================================================
# Chat Loop
# ==================================================

while True:

    user_input = input(
        "You: "
    )


    # --------------------------------------------------
    # Exit
    # --------------------------------------------------

    if user_input.lower() == "/exit":

        print(
            "Goodbye!"
        )

        break


    # --------------------------------------------------
    # Clear memory
    # --------------------------------------------------

    if user_input.lower() == "/clear":

        clear_memory()

        print(
            "\nConversation memory cleared.\n"
        )

        continue


    # --------------------------------------------------
    # Empty input
    # --------------------------------------------------

    if not user_input.strip():

        continue


    # --------------------------------------------------
    # Run Agent
    # --------------------------------------------------

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
            "Error:"
        )

        print(
            error
        )

        print()