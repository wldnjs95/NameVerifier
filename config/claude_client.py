"""Claude API client initialization and message sending."""
import anthropic
from config.settings import ANTHROPIC_API_KEY, CLAUDE_MODEL

# Validate API key before initializing client
if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY is not set. Please set it in your .env file or environment variables."
    )

if not CLAUDE_MODEL:
    raise ValueError(
        "CLAUDE_MODEL is not set. Please set it in your .env file or environment variables."
    )

# Initialize Anthropic Claude client
client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY
)


def send_message(msg):
    """Sends a message to the Claude API and returns the response."""
    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": msg}]
    )
    return message

