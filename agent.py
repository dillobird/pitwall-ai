import json
from openai_client import client
from tool_registry import TOOLS, call_tool
from prompts import SYSTEM_PROMPT

def run_agent_step(messages):
    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
        tools=TOOLS,
    )

    msg = response.choices[0].message
    messages.append(msg)

    if not msg.tool_calls:
        return msg.content

    for tool_call in msg.tool_calls:
        result = call_tool(
            tool_call.function.name,
            tool_call.function.arguments,
        )

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result),
        })

    followup = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
    )

    final_msg = followup.choices[0].message
    messages.append(final_msg)

    return final_msg.content


def new_conversation():
    return [{"role": "system", "content": SYSTEM_PROMPT}]
