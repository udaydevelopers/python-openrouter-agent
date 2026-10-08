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

from memory.facts import (
    get_facts,
    add_fact
)

from planner import create_plan


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

You can use:

- Calculator
- Date and time
- Text analysis
- Weather
- Local document search
- LanceDB vector database
- Conversation memory
- Long-term user facts
- Web search

TOOL RULES:

Use calculator for mathematical calculations.

Use weather for current weather.

Use date/time for current date or time.

Use memory_search when the user asks about
previous conversations or remembered information.

Use search_documents when the answer may exist
in the local knowledge base.

Use build_vector_store to create or rebuild
the local vector database.

Use web_search for current, recent, online,
external or live information.

Do not invent search results.

Do not invent memories.

Do not invent information from documents.

If a tool returns no useful information,
say so clearly.

Use the execution plan as guidance.

You may use more than one tool when necessary.

After receiving tool results, combine the
information and provide a clear final answer.

Keep answers natural and easy to understand.
"""


def extract_facts(user_input):

    patterns = [
        "my name is",
        "i live in",
        "my favorite",
        "i work as",
        "i am"
    ]

    text = user_input.lower()

    for pattern in patterns:

        if pattern in text:

            add_fact(
                user_input
            )

            break


def build_messages():

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    facts = get_facts()

    if facts:

        fact_text = "\n".join(
            f"- {fact}"
            for fact in facts
        )

        messages.append({
            "role": "system",
            "content": (
                "Known user facts:\n"
                + fact_text
            )
        })

    messages.extend(
        memory
    )

    return messages


def run_agent(user_input):

    extract_facts(
        user_input
    )

    plan = create_plan(
        user_input
    )

    print()

    print(
        "[Plan: "
        + " → ".join(plan)
        + "]"
    )

    messages = build_messages()

    messages.append({
        "role": "user",
        "content": user_input
    })

    messages.append({
        "role": "system",
        "content": (
            "Execution plan:\n"
            + "\n".join(
                f"{index + 1}. {step}"
                for index, step
                in enumerate(plan)
            )
        )
    })

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        message = (
            response.choices[0].message
        )

        # Final answer
        if not message.tool_calls:

            answer = (
                message.content
                or ""
            )

            save_conversation(
                user_input,
                answer
            )

            return answer

        # Add tool request
        messages.append(
            message
        )

        # Execute tools
        for tool_call in (
            message.tool_calls
        ):

            tool_name = (
                tool_call.function.name
            )

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                arguments = {}

            print(
                f"[Agent → Tool: "
                f"{tool_name}]"
            )

            print(
                f"[Arguments: "
                f"{arguments}]"
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"[Tool → Agent: "
                f"{result}]"
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

    save_memory(
        memory
    )