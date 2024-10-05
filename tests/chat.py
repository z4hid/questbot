import logging
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

TELEGRAM_API_KEY=os.getenv('TELEGRAM_API_KEY')
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
SERPER_API_KEY=os.getenv('SERPER_API_KEY')

llm = ChatGroq(
    model='mixtral-8x7b-32768',
    temperature=0.1,
    max_tokens=4096,
    timeout=None,
    max_retries=2,
)

messages = [
    (
        "system",
        "You are a helpful assistant that answers questions based on the given context.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
ai_msg
print(ai_msg.content)