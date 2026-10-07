import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.calculator import calculate
from tools.datetime_tool import get_current_datetime
from tools.text_analyzer import analyze_text


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# OpenRouter client
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


# --------------------------------------------------
# Model
# --------------------------------------------------

MODEL = "openrouter/free"


# --------------------------------------------------
# Tool Registry
# --------------------------------------------------

TOOL_FUNCTIONS = {

    "calculate": calculate,

    "get_current_datetime": get_current_datetime,

    "analyze_text": analyze_text

}


# --------------------------------------------------
# Tool Definitions
# --------------------------------------------------

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "calculate",

            "description":
                "Perform mathematical calculations such as "
                "addition, subtraction, multiplication and division.",

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

                        "description":
                            "Mathematical operation to perform"
                    }

                },

                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    },


    {
        "type": "function",

        "function": {

            "name": "get_current_datetime",

            "description":
                "Get the current date, time and day.",

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []
            }
        }
    },


    {
        "type": "function",

        "function": {

            "name": "analyze_text",

            "description":
                "Analyze text and return word count, "
                "character count and line count.",

            "parameters": {

                "type": "object",

                "properties": {

                    "text": {

                        "type": "string",

                        "description":
                            "Text that should be analyzed"
                    }

                },

                "required": [
                    "text"
                ]
            }
        }
    }

]


# --------------------------------------------------
# Execute Tool
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    print(
        f"\n[Tool requested: {tool_name}]"
    )

    print(
        f"[Arguments: {arguments}]"
    )


    # Find function in registry

    tool_function = TOOL_FUNCTIONS.get(
        tool_name
    )


    if not tool_function:

        return {
            "error": f"Tool '{tool_name}' not found"
        }


    try:

        result = tool_function(
            **arguments
        )

        print(
            f"[Tool result: {result}]"
        )

        return result


    except Exception as error:

        return {
            "error": str(error)
        }


# --------------------------------------------------
# Agent
# --------------------------------------------------

def run_agent(user_input):

    messages = [

        {
            "role": "system",

            "content": """
You are an intelligent AI agent.

You have access to several tools.

Available tools include:

1. Calculator
2. Current date/time
3. Text analyzer

Use a tool whenever it is appropriate.

Do not pretend that you executed a tool.

After receiving tool results, use those results
to produce the final answer.

Be concise and helpful.
"""
        },

        {
            "role": "user",

            "content": user_input
        }

    ]


    # --------------------------------------------------
    # Agent loop
    # --------------------------------------------------

    while True:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS

        )


        message = response.choices[0].message


        # --------------------------------------------------
        # No more tools required
        # --------------------------------------------------

        if not message.tool_calls:

            return message.content


        # --------------------------------------------------
        # Add assistant message
        # --------------------------------------------------

        messages.append(message)


        # --------------------------------------------------
        # Execute every requested tool
        # --------------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )


            arguments = json.loads(
                tool_call.function.arguments
            )


            result = execute_tool(
                tool_name,
                arguments
            )


            # --------------------------------------------------
            # Send tool result back to model
            # --------------------------------------------------

            messages.append({

                "role": "tool",

                "tool_call_id":
                    tool_call.id,

                "content":
                    json.dumps(result)

            })