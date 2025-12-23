import streamlit as st
import sys
import os
import json
import re

# --- Path Setup ---
# Add the project root to the Python path to allow importing local modules.
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Function Imports ---
try:
    from core.name_generator import generate_name
    from algorithms.algorithm2 import verify_name_algorithm2
except ImportError as e:
    st.error(f"Failed to import necessary functions: {e}")
    st.info("Please ensure the project structure is correct and all required files exist.")
    st.stop()

# --- App State Initialization ---
# 1. The app state is managed by a single variable in the session state.
if 'latest_name' not in st.session_state:
    st.session_state.latest_name = None

# --- UI ---
st.title("Name Generator and Verifier (Jiwon Park)")

# 2. Stored Name Display: Show the currently stored name at the top.
st.header("Lastest Generated Name")
if st.session_state.latest_name:
    st.success(f"**{st.session_state.latest_name}**")
else:
    st.info("No name is currently stored.")
st.divider()


# 3. Name Generation: Provide a prompt to generate and store a single name.
st.header("1. Generate and Store a Name")
st.caption("Example Prompt: Please generate a random Arabic sounding name with an Al and ibn both involved. The name shouldn't be longer than 5 words.")
generation_prompt = st.text_area(
    "Enter a prompt to generate a single name:"
)

if st.button("Generate Name"):
    if generation_prompt:
        with st.spinner("Generating name..."):
            # When a new name is generated, it overwrites the previous one.
            st.session_state.latest_name = generate_name(generation_prompt)
        # Rerun the script to immediately update the "Stored Name" display at the top.
        st.rerun()
    else:
        st.warning("Please enter a prompt to generate a name.")
st.divider()


# 4. Candidate Name Matching: Compare a candidate against the stored name.
st.header("2. Match a Candidate Name")

# The matching section is only usable if a name is stored.
if not st.session_state.latest_name:
    st.warning("A name must be generated and stored before matching can be performed.")
else:
    candidate_name = st.text_input(
        "Enter a candidate name to match against the stored name:",
        placeholder="e.g., John Smyth"
    )

    if st.button("Match Candidate"):
        if candidate_name:
            with st.spinner("Performing match using Algorithm 2..."):
                # Explicitly use Algorithm 2 for matching, as per requirements.
                result_json_str = verify_name_algorithm2(
                    st.session_state.latest_name,
                    candidate_name
                )

                # Display the match result clearly.
                st.subheader("Match Result (Algorithm 2)")
                try:
                    # Pre-process the string to remove markdown fences before parsing.
                    cleaned_str = result_json_str.strip()
                    if cleaned_str.startswith("```"):
                        # Use regex to remove the ```json ... ``` wrapper.
                        cleaned_str = re.sub(r'^```(?:json)?\s*', '', cleaned_str, flags=re.MULTILINE)
                        cleaned_str = re.sub(r'\s*```$', '', cleaned_str, flags=re.MULTILINE)

                    # Attempt to parse the cleaned string.
                    result_data = json.loads(cleaned_str)
                    st.json(result_data)

                    # Also provide a simple, human-readable result.
                    if result_data.get("match"):
                        st.success("✅ The names are considered a match.")
                    else:
                        st.error("❌ The names are not considered a match.")

                except (json.JSONDecodeError, TypeError):
                    # If parsing still fails, show the raw string response.
                    st.warning("Could not parse the result as JSON. Displaying raw response:")
                    st.text(result_json_str)
        else:
            st.warning("Please enter a candidate name.")
