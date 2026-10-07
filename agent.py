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


# ==================================================
# Environment
# ==================================================

load_dotenv()


# ==================================================
# OpenRouter Client
# ==================================================

client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)


# ==================================================
# Model
# ==================================================

MODEL = "openrouter/free"


# ==================================================
# System Prompt
# ==================================================

SYSTEM_MESSAGE = """
You are an intelligent AI agent.

You have access to several tools.

Available capabilities include:

- Mathematical calculations
- Current date and time
- Text analysis
- Current weather

Use the appropriate tool when needed.

Never pretend that a tool was executed.

Use previous conversation context when it is relevant.

If the user refers to something discussed earlier,
use the conversation history to understand the context.

After receiving a tool result, use that information
to answer the user.

If no tool is required, answer normally.
"""


# ==================================================
# Build Messages
# ==================================================

def build_messages():

    memory = load_memory()


    messages = [

        {
            "role": "system",
            "content": SYSTEM_MESSAGE
        }

    ]


    # Add previous conversation

    messages.extend(
        memory
    )


    return messages


# ==================================================
# Agent
# ==================================================

def run_agent(user_input):

    messages = build_messages()


    # --------------------------------------------------
    # Add user message
    # --------------------------------------------------

    messages.append({

        "role": "user",

        "content": user_input

    })


    # --------------------------------------------------
    # Agent Loop
    # --------------------------------------------------

    while True:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOL_DEFINITIONS

        )


        message = response.choices[0].message


        # ==================================================
        # No Tool Required
        # ==================================================

        if not message.tool_calls:

            # ----------------------------------------------
            # Save user + assistant conversation
            # ----------------------------------------------

            save_conversation(

                user_input,

                message.content

            )


            return message.content


        # ==================================================
        # Add Assistant Tool Request
        # ==================================================

        messages.append(
            message
        )


        # ==================================================
        # Execute Tools
        # ==================================================

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


            # ----------------------------------------------
            # Execute dynamically
            # ----------------------------------------------

            result = execute_tool(

                tool_name,

                arguments

            )


            print(
                f"[Tool → Agent: {result}]"
            )


            # ----------------------------------------------
            # Add tool result
            # ----------------------------------------------

            messages.append({

                "role": "tool",

                "tool_call_id":
                    tool_call.id,

                "content":
                    json.dumps(result)

            })


# ==================================================
# Save Conversation
# ==================================================

def save_conversation(
    user_input,
    assistant_response
):

    memory = load_memory()


    # Add user message

    memory.append({

        "role": "user",

        "content": user_input

    })


    # Add assistant response

    memory.append({

        "role": "assistant",

        "content": assistant_response

    })


    save_memory(
        memory
    )