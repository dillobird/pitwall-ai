import json
import os
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --------------------------------------------------------------
# Tool definition
# --------------------------------------------------------------

VALID_PARAMS = {"location", "session_name", "year", "meeting_key", "circuit_key", "country_name"}

def get_sessions(**params):
    base_url = "https://api.openf1.org/v1/sessions"
    query = {k: v for k, v in params.items() if k in VALID_PARAMS and v is not None}
    resp = requests.get(base_url, params=query)
    resp.raise_for_status()
    return resp.json()


def call_tool(name, args):
    if name == "get_sessions":
        return get_sessions(**args)
    return {"error": f"Unknown tool {name}"}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_sessions",
            "description": "Get F1 sessions from OpenF1 API using any combination of parameters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "session_name": {"type": "string"},
                    "year": {"type": "integer"},
                    "meeting_key": {"type": "integer"},
                    "circuit_key": {"type": "integer"},
                    "country_name": {"type": "string"}
                },
                "additionalProperties": False
            },
            "strict": False,
        },
    }
]

SYSTEM_PROMPT = "You are a helpful Formula 1 statistics assistant. Use the get_sessions tool only when relevant."


# --------------------------------------------------------------
# Terminal loop agent
# --------------------------------------------------------------

def run_terminal_agent():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("F1 Agent ready. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        # Step 1: append user message
        messages.append({"role": "user", "content": user_input})

        # Step 2: model response (may include tool call)
        first = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            tools=tools,
        )

        msg = first.choices[0].message
        messages.append(msg)

        # Step 3: handle tool calls if present
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"[Tool call → {tool_name}({args})]")

                result = call_tool(tool_name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

            # Step 4: second pass after tool results
            followup = client.chat.completions.create(
                model="gpt-5",
                messages=messages,
            )
            final_msg = followup.choices[0].message
            print(f"Agent: {final_msg.content}")
            messages.append(final_msg)

        else:
            # No tool call; just reply
            print(f"Agent: {msg.content}")


if __name__ == "__main__":
    run_terminal_agent()