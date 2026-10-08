import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.registry import (
    TOOL_DEFINITIONS,
    execute_tool
)

from memory.conversation import (
    load_memory,
    save_memory
)


load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)


MODEL = "openrouter/free"


SYSTEM_MESSAGE = """
You are an intelligent AI agent.

You have access to several tools.

Available capabilities:

1. Calculator
2. Current date and time
3. Text analysis
4. Current weather
5. Local document search
6. Local vector database creation

IMPORTANT TOOL RULES:

Use the calculator when mathematical calculations
are required.

Use the weather tool when the user asks about
current weather.

Use the date/time tool when the user asks for
the current date or time.

Use text analysis when the user asks to analyze
text.

Use search_documents when the user asks a question
that may require information from the local
knowledge base.

Use build_vector_store when the local document
database needs to be created or rebuilt.

For knowledge-base questions:

1. Search the documents.
2. Read the retrieved information.
3. Answer using the retrieved information.
4. Do not invent information.
5. If the documents do not contain the answer,
   clearly say that the information was not found.

Use previous conversation context when relevant.

Never pretend that a tool was executed.

After receiving a tool result, use that information
to produce the final answer.

Give natural, human-sounding answers.
"""


def build_messages():

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    messages.extend(memory)

    return messages


def run_agent(user_input):

    messages = build_messages()

    messages.append({
        "role": "user",
        "content": user_input
    })

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        message = response.choices[0].message

        if not message.tool_calls:

            answer = message.content or ""

            save_conversation(
                user_input,
                answer
            )

            return answer

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            print()
            print(
                f"[Agent → Tool: {tool_name}]"
            )

            print(
                f"[Arguments: {arguments}]"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"[Tool → Agent: {result}]"
            )

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False
                )
            })


def save_conversation(
    user_input,
    assistant_response
):

    memory = load_memory()

    memory.append({
        "role": "user",
        "content": user_input
    })

    memory.append({
        "role": "assistant",
        "content": assistant_response
    })

    save_memory(memory)