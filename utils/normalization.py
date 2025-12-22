"""Name normalization utilities."""
import re
import unicodedata


def normalize(name):
    """
    Normalizes a name for consistent comparison.
    - Converts to lowercase
    - Removes accents and diacritics
    - Replaces hyphens with spaces
    - Removes apostrophes and periods
    - Collapses multiple spaces into one
    - Strips leading/trailing whitespace
    """
    if not name:
        return ""

    clean = name.lower()
    # Normalize unicode characters to remove accents (e.g., "José" -> "Jose")
    clean = unicodedata.normalize('NFKD', clean)
    clean = ''.join([c for c in clean if not unicodedata.combining(c)])
    # Handle special characters
    clean = clean.replace("-", " ")
    clean = clean.replace("'", "")
    clean = clean.replace("'", "")  # Smart quote
    clean = clean.replace(".", "")
    # Standardize whitespace
    clean = re.sub(r'\s+', ' ', clean)
    clean = clean.strip()
    return clean


def normalize_no_space(name):
    """
    Performs normalization and also removes all spaces for a more lenient match.
    """
    clean = normalize(name)
    return clean.replace(" ", "")

