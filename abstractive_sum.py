from ollama import chat
from ollama import ChatResponse
import time
import os
from openai import OpenAI
from dotenv import load_dotenv


# Streaming chat (slow in low specs devices) using OLLAMA
def stream_text(text, length):
    stream = chat(
        model='gptsum:latest',
        messages=[{'role': 'user', 'content': f'{text}{length}'}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

# Summarize normally using OLLAMA
def oll_summarize(text, length):
    response: ChatResponse = chat(model='gptsum:latest', messages=[
        {
            'role': 'user',
            'content': f'{text}{length}',
        },
    ])
    print(response['message']['content'])

def openai_summarize(text, length, client):
    response = client.responses.create(
        model="gpt-5-mini",
        instructions="""
        You are a text summarization assistant. Your primary function is to create accurate summaries that preserve the main context and key information of the input text.

        SUMMARIZATION RULES:
        1. Carefully read and understand the entire input text before summarizing
        2. Identify and preserve all main ideas, key points, and critical context
        3. Maintain the logical flow and structure of the original content
        4. Do not add information that wasn't in the original text
        5. Do not lose important details or change the meaning

        LENGTH CONTROL:
        The desired summary length is indicated by a number in curly braces at the end of the input:
        - {1} = Produce a summary that is 20% of the original text length
        - {2} = Produce a summary that is 40% of the original text length  
        - {3} = Produce a summary that is 65% of the original text length

        If no length indicator is provided, default to {2} (40% length).

        OUTPUT FORMAT:
        - Provide only the summary without any preamble or meta-commentary
        - Use clear, concise language
        - Maintain the same tone and style as the original text when possible
        """,
        input=f"{text}{length}",
    )
    
    return response.output_text

if __name__ == "__main__":
    # Initialize openai api
    load_dotenv()
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    text = input("Text:")
    length = int(input("Length:"))

    match length:
        case 1:
            length = "{1}"
        case 2:
            length = "{2}"
        case 3:
            length = "{3}"
        case _:
            length = "{2}"

    start = time.perf_counter()

    # oll_summarize(text, length)     # Local summarization using OLLAMA gptsum model

    openai_summarize(text, length, client)  # OpenAI summarization using gpt-5-mini

    end = time.perf_counter()
    print(f"Time: {end - start:.2f}")