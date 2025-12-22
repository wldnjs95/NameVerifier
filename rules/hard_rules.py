"""Hard rules for deterministic name matching."""
import json
from config.settings import THRESHOLD
from utils.normalization import normalize, normalize_no_space
from utils.phonetic import check_phonetic_with_risk_assessment
from rules.gender import is_gender_swap


def create_match_result(confidence, reasoning):
    """
    Formats the verification result into a JSON string.
    """
    is_match = confidence >= THRESHOLD

    result = {
        "match": is_match,
        "confidence": confidence,
        "explanation": reasoning
    }
    return json.dumps(result, ensure_ascii=False)


def check_hard_rules(target, candidate):
    """
    Applies a set of deterministic rules to quickly filter out non-matches
    or identify clear matches before calling the LLM.
    """
    t_norm = normalize(target)
    c_norm = normalize(candidate)
    t_tokens = t_norm.split()
    c_tokens = c_norm.split()

    # Rule 0: Check for gender swaps first (e.g., Maria Gonzalez vs. Mario Gonzalez)
    if len(t_tokens) == len(c_tokens):
        for t_token, c_token in zip(t_tokens, c_tokens):
            if is_gender_swap(t_token, c_token):
                return create_match_result(20, "Gendered name difference detected. This is a non-match in financial contexts.")

    # Rule 1: Exact match after full normalization (case, punctuation, space insensitive)
    if normalize_no_space(target) == normalize_no_space(candidate):
        return create_match_result(100, "Exact match after case and punctuation normalization.")

    # Rule 2: Check for swapped token order (e.g., Ali Hassan vs. Hassan Ali)
    if set(t_tokens) == set(c_tokens) and t_tokens != c_tokens:
        return create_match_result(30, "Token order swap changes identity. This is a non-match in financial contexts.")

    # Rule 3: Check for safe phonetic matches (e.g., Steven/Stephen)
    phonetic_result = check_phonetic_with_risk_assessment(t_norm, c_norm)
    if phonetic_result is not None:
        return phonetic_result

    # If no hard rules apply, proceed to the LLM stage
    return None

