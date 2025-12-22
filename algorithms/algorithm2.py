"""Algorithm 2: Advanced LLM verification with context and rules."""
from config.claude_client import send_message


def verify_name_algorithm2(latest_name, user_input, phonetic_hint=False):
    """
    Algorithm 2: A more sophisticated verification prompt with added context and rules.
    - phonetic_hint: Provides extra context if a risky phonetic match was detected.
    """
    base_prompt = f"""
    You are a financial identity verification expert.
    Analyze if these two names refer to the same person.

    Target Name: "{latest_name}"
    Candidate Name: "{user_input}"
    """

    hint_section = ""
    if phonetic_hint:
        hint_section = f"""

    [IMPORTANT CONTEXT]
    These names have been detected as phonetically similar (Double Metaphone match).
    However, there may be subtle differences that affect identity:
    - Check for suffix variations (e.g., 'Rashid' vs 'Rashidi' - different surname roots)
    - Check for gender differences (e.g., 'Maria' vs 'Mario')
    - Check for cultural/linguistic variations that change meaning
    Focus specifically on these potential differences rather than phonetic similarity.
    """

    rules_section = """
    [Strict Verification Rules]
    1. Nicknames: Accept 'Bob' for 'Robert', but REJECT 'Liam' for 'William' because Liam is an independent name.
    2. Surname Roots: REJECT if the surname root changes, even by one letter (e.g., 'Rashid' vs 'Rashidi').
    3. Order: If the name order is swapped, it is a NO MATCH.
    4. Phonetic variants OK: Steven=Stephen, Johnson=Jonson, -ov=-off
    """

    full_prompt = base_prompt + hint_section + rules_section + """
    Respond ONLY in valid JSON:
    {{
    "match": boolean,
    "confidence": 0-100,
    "explanation": "short reason"
    }}
    """

    message = send_message(full_prompt)
    return message.content[0].text

