"""Application settings and constants."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Confidence threshold for a name to be considered a match
THRESHOLD = 85

# Anthropic API configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CLAUDE_MODEL = os.getenv('CLAUDE_SONNET')

