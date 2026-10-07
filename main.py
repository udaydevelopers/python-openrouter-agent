from agent import run_agent


print("=" * 60)

print(
    "Python OpenRouter AI Agent - V3"
)

print("=" * 60)

print()
print("Dynamic Tool Registry")
print()

print("Available tools:")

print("1. Calculator")
print("2. Date/Time")
print("3. Text Analyzer")
print("4. Weather")

print()
print("Type 'exit' to stop.")
print()


while True:

    user_input = input("You: ")


    if user_input.lower() == "exit":

        print(
            "Goodbye!"
        )

        break


    if not user_input.strip():

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