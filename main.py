from agent import run_agent


print("=" * 50)
print("Python OpenRouter AI Agent")
print("=" * 50)

print("Type 'exit' to stop.\n")


while True:

    user_input = input("You: ")


    if user_input.lower() == "exit":
        print("Goodbye!")
        break


    try:

        answer = run_agent(user_input)

        print("\nAgent:")
        print(answer)
        print()

    except Exception as error:

        print("\nError:")
        print(error)
        print()