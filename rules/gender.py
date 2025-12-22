"""Gender-related name checking utilities."""


def is_gender_swap(name1, name2):
    """
    Detects potential gender-swapped names by checking for common suffixes.
    Example: "Maria" vs. "Mario"
    """
    n1, n2 = name1.lower(), name2.lower()
    # Block cases like Maria vs Mario if the root is the same
    if (n1.endswith('a') and n2.endswith('o')) or (n1.endswith('o') and n2.endswith('a')):
        if n1[:-1] == n2[:-1]:
            return True
    return False

