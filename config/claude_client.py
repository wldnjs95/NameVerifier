"""Claude API client initialization and message sending."""
import anthropic
from config.settings import ANTHROPIC_API_KEY, CLAUDE_MODEL

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

