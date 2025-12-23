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
    """Get value from Streamlit secrets or environment variables."""
    try:
        import streamlit as st
        return st.secrets.get(key) or os.getenv(key, default)
    except (AttributeError, FileNotFoundError, RuntimeError):
        # If st.secrets is not available, use environment variables
        return os.getenv(key, default)

ANTHROPIC_API_KEY = get_secret('ANTHROPIC_API_KEY')
CLAUDE_MODEL = get_secret('CLAUDE_SONNET')

