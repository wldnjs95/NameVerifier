"""Main entry point for the name verification application."""
from core.verification import verify_flow
from core.name_generator import generate_name


if __name__ == '__main__':
    # Example usage when the script is run directly.
    # 1. Generate a name
    user_msg = input('Enter a prompt to generate a name: ')
    # latest_name = generate_name(user_msg)  # This is the intended use
    latest_name = user_msg  # For easier testing, use the input directly
    print(f"Target Name: {latest_name}")

    # 2. Verify a name against the generated one
    while True:
        user_verification_input = input("Enter a name to verify (or -1 to exit): ")
        if user_verification_input == '-1':
            break
        result, source = verify_flow(latest_name, user_verification_input)
        print(f"[{source.upper()}] {result}")
