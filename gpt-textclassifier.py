import time
import os
from openai import OpenAI
from dotenv import load_dotenv


def classify(text:str):
    response = client.responses.create(
        model="gpt-5-nano",
        instructions="""
        You are a text classifier assistant. Your primary function is to classify the given text based on the domains provided below: 

        DOMAINS:
        1. Science
        2. Programming/Technology
        3. English Literature
        4. Mathematics

        CLASSIFICATION RULES:
        1. STRICTLY carefully scan through the given text and take note of the important terminologies that would classify their domain.
        2. If such variety of terminologies exists within the text for different domains, note them and create a mean percentage of how likely it is the domain of the given text.
        3. Don't add information that is not found within the text given, only look for the text given to you.

        OUTPUT FORMAT:
        - Provide only the name of the domain with the highest percentage based on the mean percentage you calculated, without any additional comments or meta-commentary.
        - Provide the number of the domain instead of its full categorical name.
        """,
        input=f"{text}",
    )

    return response.output_text

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

text = input("Text:")

start = time.perf_counter()
output = classify(text)
print(type(output), output)

end = time.perf_counter()
print(f"Time: {end - start:.2f}")