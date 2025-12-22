"""Core name verification orchestration."""
from metaphone import doublemetaphone
from utils.normalization import normalize
from rules.hard_rules import check_hard_rules
from algorithms.algorithm1 import verify_name_algorithm1
from algorithms.algorithm2 import verify_name_algorithm2


def verify_name(latest_name, user_input, algorithm=2):
    """
    Main name verification function that orchestrates the process.

    - algorithm: 1 (LLM only) or 2 (Hard Rules + LLM).
    Returns a tuple: (result_json_string, source_of_decision)
    """
    if algorithm == 1:
        # Algorithm 1: Use LLM directly without pre-checks.
        llm_result = verify_name_algorithm1(latest_name, user_input)
        return llm_result, 'llm'

    elif algorithm == 2:
        # Algorithm 2: Apply hard rules first, then use LLM if necessary.
        hard_result = check_hard_rules(latest_name, user_input)
        if hard_result:
            return hard_result, 'hard_rule'

        # If hard rules didn't yield a result, check if a phonetic hint is needed for the LLM.
        t_norm = normalize(latest_name)
        c_norm = normalize(user_input)
        from utils.phonetic import check_phonetic_with_risk_assessment
        phonetic_result = check_phonetic_with_risk_assessment(t_norm, c_norm)

        # Determine if a risky phonetic match occurred.
        t_tokens = t_norm.split()
        c_tokens = c_norm.split()
        is_phonetically_matched = False
        if len(t_tokens) == len(c_tokens):
            is_phonetically_matched = all(
                set(doublemetaphone(t1)) & set(doublemetaphone(t2)) - {''}
                for t1, t2 in zip(t_tokens, c_tokens)
            )
        # Provide a hint if names are phonetically similar but were flagged as risky.
        phonetic_hint = is_phonetically_matched and phonetic_result is None

        # Call the advanced LLM verification with the hint if applicable.
        llm_result = verify_name_algorithm2(latest_name, user_input, phonetic_hint=phonetic_hint)
        return llm_result, 'llm'
    else:
        raise ValueError("Algorithm must be 1 or 2.")


def verify_flow(latest_name, user_input):
    """
    Alias for the default verification flow, which uses Algorithm 2.
    Returns a tuple: (result_json_string, source_of_decision)
    """
    return verify_name(latest_name, user_input, algorithm=2)

