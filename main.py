import argparse
import os
import sys

from call_functions import available_functions, call_function
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)

    #generate_content handle model text responses and execute requested tool calls
def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:

    final_response_found = False
    for _ in range(20):
    # call the model, handle responses, etc.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)

        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            print("Response:")
            print(message.content)
            final_response_found = True
            break

        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            result_message = call_function(tool_call, verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")
            if verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    if not final_response_found:
        print("Error: Maximum iteration limit reached without a final response.")
        sys.exit(1)
           



            


if __name__ == "__main__":
    main()
