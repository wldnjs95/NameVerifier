"""Phonetic matching utilities."""
from metaphone import doublemetaphone
from utils.normalization import normalize
from rules.gender import is_gender_swap


def check_phonetic_with_risk_assessment(t_norm, c_norm):
    """
    Checks for phonetic similarity using Double Metaphone and assesses risk factors.

    Returns:
    - A high-confidence match result if names are phonetically similar and low-risk.
    - None if names are not phonetically similar or are high-risk, deferring to the LLM.
    """
    t_tokens = t_norm.split()
    c_tokens = c_norm.split()

    if len(t_tokens) != len(c_tokens):
        return None

    # 1. First, check for phonetic similarity as a baseline.
    phonetic_match = True
    for t1, t2 in zip(t_tokens, c_tokens):
        code1 = doublemetaphone(t1)
        code2 = doublemetaphone(t2)
        # Check for any intersection between the two sets of phonetic codes
        if not (set(code1) & set(code2) - {''}):
            phonetic_match = False
            break

    if not phonetic_match:
        return None

    # 2. [Core Logic] If phonetically similar, check for 'risky' differences.
    for t_token, c_token in zip(t_tokens, c_tokens):
        if t_token == c_token:
            continue

        # Risk A: Gendered endings (Maria/Mario, Michael/Michelle)
        if is_gender_swap(t_token, c_token) or \
           (t_token.endswith('el') and c_token.endswith('elle')) or \
           (t_token.endswith('elle') and c_token.endswith('el')):
            return None  # Risky -> Defer to LLM

        # Risk B: Suffixes indicating different family roots (Rashid/Rashidi)
        if (t_token.endswith('i') ^ c_token.endswith('i')):
            return None  # Risky -> Defer to LLM

        # Risk C: Differences in very short names are more significant (e.g., Ali/Alin)
        if len(t_token) <= 4:
            return None

    # 3. If no risk factors are found, approve as a safe phonetic variation.
    # Import here to avoid circular dependency
    from rules.hard_rules import create_match_result
    return create_match_result(95, "Safe phonetic match detected (Double Metaphone).")

