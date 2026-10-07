import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.calculator import calculate


# Load environment variables
load_dotenv()


# Create OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# Model
MODEL = "openrouter/free"


# --------------------------------------------------
# Tool definitions
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    }
]


# --------------------------------------------------
# Execute tool
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "calculate":

        return calculate(
            a=arguments["a"],
            b=arguments["b"],
            operation=arguments["operation"]
        )

    return f"Unknown tool: {tool_name}"


# --------------------------------------------------
# Agent
# --------------------------------------------------

def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": """
You are a helpful AI agent.

You have access to tools.

When a tool is useful, use the tool instead of trying
to perform the operation yourself.

After receiving the tool result, give a clear answer
to the user.
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]


    # Agent loop
    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )


        message = response.choices[0].message


        # ------------------------------------------
        # No tool required
        # ------------------------------------------

        if not message.tool_calls:

            return message.content


        # ------------------------------------------
        # Add assistant message
        # ------------------------------------------

        messages.append(message)


        # ------------------------------------------
        # Execute requested tools
        # ------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )


            print(
                f"\n[Agent calling tool: {tool_name}]"
            )

            print(
                f"[Arguments: {arguments}]"
            )


            result = execute_tool(
                tool_name,
                arguments
            )


            print(
                f"[Tool result: {result}]"
            )


            # Send result back to AI
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )