"""Name generation using Claude."""
from config.claude_client import send_message


def generate_name(user_context):
    """Generates a single full name based on a user-provided description using Claude."""
    full_prompt = f"Generate a single full name based on this description: {user_context}. Return ONLY the name, nothing else. Use English alphabet."
    message = send_message(full_prompt)
    name = message.content[0].text
    return name