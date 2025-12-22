# AI Name Generator and Verifier

A simple command-line application that uses the Anthropic Claude API to generate and verify names.

## Installation

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv abode_env
    source abode_env/bin/activate  # On Windows, use: abode_env\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**

    Create a file named `.env` in the project root and add your Anthropic API key:
    ```
    ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
    CLAUDE_SONNET=claude-3-sonnet-20240229
    ```

## How to Run

Execute the main application script:
```bash
python app.py
```

## How to Use

The application runs in two phases:

1.  **Name Generation:**
    *   You will first be prompted to enter a description for a name you want to generate.
    *   The AI will then generate a name based on your input. For testing purposes, the script currently uses your input directly as the "target name".

2.  **Name Verification:**
    *   After a target name is established, you will be prompted to enter a name to verify against it.
    *   The application will output a JSON result indicating if the names are a `match`, a `confidence` score, and an `explanation`.
    *   The source of the decision (`HARD_RULE` or `LLM`) will also be displayed.
    *   Enter `-1` to exit the verification loop.

## Important Notes

*   An **Anthropic API key** is required. You can get one from the [Anthropic Console](https://console.anthropic.com/).
*   API usage may incur costs.