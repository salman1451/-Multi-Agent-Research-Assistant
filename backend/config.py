import os
import sys
import logging
from dotenv import load_dotenv

# Step 2: Settings & Security (Config)
# This file reads the API keys from your .env file so we can use them safely.
# 1. Load the .env file
load_dotenv()

# 2. Set up "Logging" 
# This is better than 'print' because it adds timestamps and info levels.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("research_assistant")

class Config:
    # Get the keys from the environment
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Choose which AI to use (OpenAI is default)
    DEFAULT_LLM = os.getenv("DEFAULT_LLM", "openai").lower()

    # How many times can we loop back for more research?
    MAX_RETRIES = 2

# 3. Simple Check
# This runs when we start the app to make sure you didn't forget your keys!
def validate_env():
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("GROQ_API_KEY"):
        logger.error("❌ No AI API Key found! Please check your .env file.")
        # sys.exit(1) # We would normally stop the app here
    
    if not os.getenv("TAVILY_API_KEY"):
        logger.warning("⚠️ No Tavily Search Key found. Search won't work!")
