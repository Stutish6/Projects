import os
import tiktoken

#Read the secret info from .env file
from dotenv import load_dotenv
#from xai_sdk import Client

#let you talk to an AI model
from openai import OpenAI
#

# Load environment variables from the .env file
load_dotenv()

#Get the API key from the .env file i.e. read the .env file
api_key = os.getenv("GROQ_API_KEY")


client = OpenAI(
    api_key=api_key, # Use the AI key
    base_url="https://api.groq.com/openai/v1", # tlak to Groq server.
    timeout=60.0
)
MODEL = "openai/gpt-oss-20b"
MAX_TOKENS = 1000 # Max size of words for the answer
TOKEN_BUDGET = 4000

#Give job to a AI
SYSTEM_PROMPT = "You are a diet planning assistant that provides accurate, evidence-based nutrition information and helps users stay disciplined with their health, fitness, and dietary goals. Create practical meal plans, suggest healthy food choices, track progress when requested, and offer motivation and accountability. Tailor recommendations to the user's goals, preferences, dietary restrictions, and lifestyle. Maintain a supportive, encouraging, and professional tone. Do not provide medical diagnoses or replace professional healthcare advice. Prioritize safe, balanced, and sustainable nutrition practices."


#Create Memory, i.e. AI's Memory
messages = [{'role': "system", "content": SYSTEM_PROMPT}]


'''
Chat funcation
1. Receives your message.
2. Sends it to AI.
3. Gets a reply.
4. Return the reply.
'''
def chat(user_input):
    #Save your memory.
    messages.append({'role':"user", "content": user_input})

    #This send conversation to the AI
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_completion_tokens=MAX_TOKENS
    )

    #AI sends back big response object, taking only text.
    reply = response.choices[0].message.content

    #Here the AI will remember what it said.
    messages.append({"role":"assistant", "content":reply})

    return reply

'''
This code is for terminal code.
while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    reply = chat(user_input)
    print(f"Assistant: {reply}")
'''


