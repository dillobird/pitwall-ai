from agent import run_agent_step, new_conversation

def run_terminal_agent():
    messages = new_conversation()
    print("F1 Agent ready. Type 'exit' to quit.")

    while True:
        user_input = input("\n>>> ").strip()
        if user_input.lower() == "exit":
            print("Goodbye.")
            break
        elif user_input.lower() == "test":
            test_prompt = "Give me the results of the 2025 Chinese GP."
            print("Testing with prompt: ", test_prompt)
            messages.append({"role": "user", "content": test_prompt})
        else:
            messages.append({"role": "user", "content": user_input})
        reply = run_agent_step(messages)
        print(f"PitwallAI: {reply}")


if __name__ == "__main__":
    run_terminal_agent()
