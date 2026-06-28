from groq import Groq
from dotenv import load_dotenv
import os

#Load API Key from Groq
load_dotenv()

#Connect to Groq
client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

#Making my first LLM API call
response=client.chat.completions.create(
    model="llama-3.1-8b-instant", #Meta's LLama 3 model!
    messages=[
        {
            "role":"user",
            "content":"Hello! I am Varun an aspiring GenAI engineer. Tell me in 2 lines why python is important for API"
        }
    ] 
)
#Print the response
print(response.choices[0].message.content)

#Lets have a conversation!
messages=[
    {
        "role":"system",
        "content":"You are a senior Meta engineer helping Varun transition into GenAI engineering. Keep answers concise and practical."
    },
    {
        "role":"user",
        "content":"What is the single most important skill I need to land a job at Meta in GenAI?"
    }
]
response=client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=messages
)

print(response.choices[0].message.content)