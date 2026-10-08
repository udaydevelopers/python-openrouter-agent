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
7. Conversation memory search
8. Long-term user facts

TOOL USAGE RULES:

Use the calculator when mathematical calculations
are required.

Use the weather tool when the user asks about
current weather.

Use the date/time tool when the user asks for
the current date or time.

Use text analysis when the user asks to analyze
text.

Use search_documents when the question requires
information from the local knowledge base.

Use build_vector_store when documents need to be
indexed into the vector database.

Use memory_search when the user asks about something
from a previous conversation.

Examples:

"What is my name?"

"What did I tell you earlier?"

"What did we discuss about Python?"

"Do you remember my previous question?"

Use stored long-term facts when they are relevant.

IMPORTANT:

Do not invent memories or user facts.

If the requested information is not available in
memory, clearly say that you don't have that
information.

Use RAG information only when it comes from the
retrieved documents.

Use previous conversation context when relevant.

Never pretend that a tool was executed.

After receiving a tool result, use that information
to produce the final answer.

Give natural, human-sounding answers.
"""


def extract_facts(user_input):
    """
    Basic V6 long-term fact extraction.

    This version detects a few common statements
    and stores the complete user message as a fact.
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
    """
    Build the messages sent to the LLM.
    """

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
            "content": (
                "Known user facts:\n"
                f"{fact_text}"
            )
        })

    # Add previous conversation
    messages.extend(memory)

    return messages


def run_agent(user_input):
    """
    Run the AI agent.
    """

    # Store potential long-term facts
    extract_facts(user_input)

    # Build conversation context
    messages = build_messages()

    # Add current user message
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

        # -------------------------------------------------
        # No tool required
        # -------------------------------------------------

        if not message.tool_calls:

            answer = message.content or ""

            save_conversation(
                user_input,
                answer
            )

            return answer

        # -------------------------------------------------
        # Tool call requested
        # -------------------------------------------------

        messages.append(message)

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

            print()
            print(
                f"[Agent → Tool: {tool_name}]"
            )

            print(
                f"[Arguments: {arguments}]"
            )

            # Execute tool
            result = execute_tool(
                tool_name,
                arguments
            )

            print(
                f"[Tool → Agent: {result}]"
            )

            # Add tool result
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
    """
    Save the final user/assistant conversation
    to persistent memory.
    """

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