"""Algorithm 1: Simple LLM-only verification."""
from config.claude_client import send_message


def verify_name_algorithm1(latest_name, user_input):
    """
    Algorithm 1: A simple LLM-only verification prompt.
    """
    full_prompt = f"""
        Verify whether these two names are considered a match.

        target_name: "{latest_name}"
        search_name: "{user_input}"

        Respond ONLY in valid JSON using the following schema:
        {{
        "match": true or false,
        "confidence": 0-100,
        "explanation": "short explanation"
        }}
        """
    message = send_message(full_prompt)
    return message.content[0].text

