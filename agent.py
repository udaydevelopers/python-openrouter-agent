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

You have access to these capabilities:

- Calculator
- Date and time
- Text analysis
- Weather
- Local document search
- Vector database
- Conversation memory
- Long-term user facts

Follow the plan provided by the application.

Use tools when required.

Do not invent tool results.

Do not invent memories.

For document questions, use the RAG search tool.

For previous conversation questions, use memory.

Use known user facts when relevant.

After tools return results, give a clear,
natural and concise answer.

Do not mention internal tool names unless useful.
"""


def extract_facts(user_input):
    """
    Store simple user facts.
    """

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

            add_fact(user_input)

            break


def build_messages():

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }
    ]

    # Add long-term facts
    facts = get_facts()

    if facts:

        fact_text = "\n".join(
            f"- {fact}"
            for fact in facts
        )

        messages.append({
            "role": "system",
            "content":
                "Known user facts:\n"
                + fact_text
        })

    # Add conversation memory
    messages.extend(memory)

    return messages


def run_agent(user_input):

    # Save possible user fact
    extract_facts(user_input)

    # Create plan
    plan = create_plan(user_input)

    print()
    print(
        f"[Plan: {' → '.join(plan)}]"
    )

    messages = build_messages()

    messages.append({
        "role": "user",
        "content": user_input
    })

    # Tell the LLM about the plan
    messages.append({
        "role": "system",
        "content": (
            "Execution plan:\n"
            + "\n".join(
                f"{index + 1}. {step}"
                for index, step in enumerate(plan)
            )
        )
    })

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS
        )

        message = response.choices[0].message

        # Final answer
        if not message.tool_calls:

            answer = message.content or ""

            save_conversation(
                user_input,
                answer
            )

            return answer

        # Add assistant tool request
        messages.append(message)

        # Execute tools
        for tool_call in message.tool_calls:

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