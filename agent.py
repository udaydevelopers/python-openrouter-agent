import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.registry import (
    TOOL_DEFINITIONS,
    execute_tool
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
# Agent
# ==================================================

def run_agent(user_input):

    messages = [

        {
            "role": "system",

            "content": """
You are an intelligent AI agent.

You have access to tools.

Use tools whenever they are useful.

Never pretend that a tool was executed.

After receiving the tool result, use that
information to answer the user.

If no tool is required, answer normally.
"""
        },

        {
            "role": "user",

            "content": user_input
        }

    ]


    # ==================================================
    # Agent Loop
    # ==================================================

    while True:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOL_DEFINITIONS

        )


        message = response.choices[0].message


        # ==================================================
        # Final Answer
        # ==================================================

        if not message.tool_calls:

            return message.content


        # ==================================================
        # Add assistant message
        # ==================================================

        messages.append(message)


        # ==================================================
        # Process Tool Calls
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


            # ------------------------------------------
            # Dynamic Tool Registry
            # ------------------------------------------

            result = execute_tool(

                tool_name,

                arguments

            )


            print(
                f"[Tool → Agent: {result}]"
            )


            # ------------------------------------------
            # Send result back to LLM
            # ------------------------------------------

            messages.append({

                "role": "tool",

                "tool_call_id":
                    tool_call.id,

                "content":
                    json.dumps(result)

            })