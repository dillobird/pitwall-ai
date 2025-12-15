import json
import logging
from datetime import datetime
from openai_client import client
from tool_registry import TOOLS, call_tool
from prompts import SYSTEM_PROMPT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def run_agent_step(messages):
    logging.info("Sending message to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages,
        tools=TOOLS,
    )
    logging.info("Received response from GPT.")

    msg = response.choices[0].message
    messages.append(msg)

    if not msg.tool_calls:
        return msg.content

    for tool_call in msg.tool_calls:
        logging.info(
            "Tool call detected: %s(%s)",
            tool_call.function.name,
            tool_call.function.arguments,
        )

        result = call_tool(tool_call.function.name, tool_call.function.arguments)
        logging.info("Tool result: %s", str(result)[:200])  # truncate if large

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
