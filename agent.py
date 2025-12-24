import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
from tool_registry import TOOLS, call_tool

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent_step(messages):
    """
    Sends messages to the OpenAI Responses API and returns the assistant's reply.
    Handles function calls by executing them and continuing the conversation using previous_response_id.
    """
    max_iterations = 10
    iteration = 0
    previous_response_id = None
    tool_results = None

    while iteration < max_iterations:
        iteration += 1
        logging.info(f"Sending messages to OpenAI Responses API (iteration {iteration})...")
        if previous_response_id:
            logging.debug(f"Continuing with previous_response_id: {previous_response_id}")
        if tool_results:
            logging.debug(f"Tool results: {json.dumps(tool_results, indent=2)}")
        logging.debug(f"Messages: {json.dumps(messages, indent=2)}")

        try:
            # Build request parameters
            request_params = {
                "model": "gpt-5",
                "tools": TOOLS,
                "metadata": {"succinct": "true"}
            }

            if previous_response_id:
                request_params["previous_response_id"] = previous_response_id
                if tool_results:
                    request_params["input"] = tool_results
            else:
                # First request - send the input messages
                request_params["input"] = messages

            response = client.responses.create(**request_params)
            logging.debug(f"Raw response object: {response}")

            # Check if we have a text response
            if response.output_text:
                messages.append({
                    "role": "assistant",
                    "content": response.output_text
                })
                previous_response_id = None
                tool_results = None
                return response.output_text

            # Check for function calls in the output
            function_calls = []
            if response.output:
                for item in response.output:
                    item_type = getattr(item, "type", None)
                    if item_type == "function_call":
                        function_calls.append(item)
                    elif hasattr(item, "__class__"):
                        class_name = item.__class__.__name__
                        if "FunctionToolCall" in class_name:
                            function_calls.append(item)

            if function_calls:
                previous_response_id = response.id
                tool_results = []

                for func_call in function_calls:
                    call_id = getattr(func_call, "call_id", None)
                    func_name = getattr(func_call, "name", None)
                    func_args = getattr(func_call, "arguments", None)

                    if not all([call_id, func_name, func_args]):
                        logging.warning(f"Incomplete function call: call_id={call_id}, name={func_name}, args={func_args}")
                        continue

                    logging.info(f"Executing function call: {func_name} with args: {func_args}")

                    try:
                        result = call_tool(func_name, func_args)
                        result_json = json.dumps(result) if not isinstance(result, str) else result

                        tool_results.append({
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": result_json
                        })

                        logging.debug(f"Function {func_name} returned: {result_json}")
                    except Exception as e:
                        logging.error(f"Error executing function {func_name}: {e}", exc_info=True)
                        tool_results.append({
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": json.dumps({"error": str(e)})
                        })

                if tool_results:
                    continue
                else:
                    logging.warning("No tool results generated from function calls")
                    return None

            logging.warning("No text response and no function calls found")
            return None

        except Exception as e:
            logging.error(f"Error in run_agent_step: {e}", exc_info=True)
            raise

    logging.error(f"Reached max iterations ({max_iterations}) without getting a text response")
    return None

def new_conversation(system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    return messages

if __name__ == "__main__":
    messages = new_conversation(SYSTEM_PROMPT)

    logging.info("Running terminal agent test...")
    reply = run_agent_step(messages)
    print("\nAssistant reply:\n", reply)