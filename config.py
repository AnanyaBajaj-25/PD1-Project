import os
from dotenv import load_dotenv
import dspy

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found")

lm = dspy.LM(
    model="gpt-4o-mini",
    model_type="chat",
    api_key=OPENAI_API_KEY,
    max_tokens=300,
    temperature=0.5,
    cache=False
)