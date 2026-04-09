import os
from dotenv import load_dotenv
import dspy
import warnings

# Suppress noisy Pydantic serialization warnings emitted by the OpenAI client.
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Set it in your environment or .env file.")

lm = dspy.LM(
    model="gpt-4o-mini",
    model_type="chat",
    api_key=OPENAI_API_KEY,
    max_tokens=700,
    temperature=0.5,
    cache=False,
)

dspy.configure(lm=lm)
