"""Application settings and constants."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Confidence threshold for a name to be considered a match
THRESHOLD = 85

# Anthropic API configuration
# Try Streamlit secrets first (for Streamlit Cloud), then fall back to environment variables
def get_secret(key, default=None):
    """
    Get value from Streamlit secrets or environment variables.
    
    Priority:
    1. Streamlit secrets (if running in Streamlit context)
    2. Environment variables (.env file or system env)
    3. default value (None)
    """
    env_value = os.getenv(key, default)
    
    try:
        import streamlit as st
        secrets_value = st.secrets.get(key, None)
        return secrets_value if secrets_value is not None else env_value
    except (AttributeError, FileNotFoundError, RuntimeError, ImportError):
        return env_value

ANTHROPIC_API_KEY = get_secret('ANTHROPIC_API_KEY')
CLAUDE_MODEL = get_secret('CLAUDE_SONNET')

