import json
import re
import time
from test_cases import TEST_CASES
from core.verification import verify_flow

def parse_claude_response(response_text):
    """Extracts and parses JSON from the Claude response."""
    try:
        # Strip leading/trailing whitespace
        response_text = response_text.strip()

        # Remove markdown JSON code blocks if present
        if response_text.startswith('```'):
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text, flags=re.MULTILINE)
            response_text = re.sub(r'\s*```$', '', response_text, flags=re.MULTILINE)

        # Parse the JSON string
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError as e:
        # If JSON parsing fails, try to extract the 'match' value directly from the text
        match_found = None
        if '"match":' in response_text or "'match':" in response_text:
            match_pattern = r'"match":\s*(true|false)'
            match = re.search(match_pattern, response_text, re.IGNORECASE)
            if match:
                match_found = match.group(1).lower() == 'true'

        return {
            'match': match_found,
            'confidence': None,
            'explanation': f'JSON parsing failed: {str(e)}',
            'raw_response': response_text
        }

def run_tests():
    """Runs all test cases and analyzes the results."""
    results = []
    total = len(TEST_CASES)
    correct = 0
    incorrect = 0
    parse_errors = 0

    true_cases_correct = 0
    true_cases_total = 0
    false_cases_correct = 0
    false_cases_total = 0

    # Timing variables
    total_start_time = time.time()
    test_times = []

    print("=" * 80)
    print("Starting Claude Name Verification Tests")
    print("=" * 80)
    print()

    for idx, (target_name, candidate_name, expected_match, reason) in enumerate(TEST_CASES, 1):
        print(f"[{idx}/{total}] Running test...")
        print(f"  Target: {target_name}")
        print(f"  Candidate: {candidate_name}")
        print(f"  Expected: {expected_match}")

        # Start timing the test
        test_start_time = time.time()

        try:
            # Call the verification flow (Hard rules + Algorithm 2)
            claude_response, source = verify_flow(target_name, candidate_name)

            # Stop timing the test
            test_elapsed_time = time.time() - test_start_time
            test_times.append(test_elapsed_time)
            parsed_result = parse_claude_response(claude_response)

            claude_match = parsed_result.get('match')
            confidence = parsed_result.get('confidence')
            result_reason = parsed_result.get('explanation', parsed_result.get('reason', ''))

            # Compare results
            is_correct = (claude_match == expected_match)

            if is_correct:
                correct += 1
            else:
                incorrect += 1

            # Statistics by category
            if expected_match:
                true_cases_total += 1
                if is_correct:
                    true_cases_correct += 1
            else:
                false_cases_total += 1
                if is_correct:
                    false_cases_correct += 1

            # Check for parsing errors
            if claude_match is None:
                parse_errors += 1

            result_entry = {
                'test_num': idx,
                'target_name': target_name,
                'candidate_name': candidate_name,
                'expected_match': expected_match,
                'claude_match': claude_match,
                'is_correct': is_correct,
                'confidence': confidence,
                'result_reason': result_reason,
                'expected_reason': reason,
                'source': source,
                'elapsed_time': test_elapsed_time,
                'raw_response': claude_response
            }
            results.append(result_entry)

            status = "✓" if is_correct else "✗"
            source_label = "Hard Rule" if source == 'hard_rule' else "LLM"
            print(f"  [{source_label}] Claude Result: {claude_match} (Confidence: {confidence})")
            print(f"  Result: {status} {'Correct' if is_correct else 'Incorrect'}")
            print(f"  Time Taken: {test_elapsed_time:.2f}s")
            print()

        except Exception as e:
            # Also record time if an error occurs
            test_elapsed_time = time.time() - test_start_time
            test_times.append(test_elapsed_time)

            print(f"  Error occurred: {str(e)}")
            print(f"  Time Taken: {test_elapsed_time:.2f}s")
            print()
            results.append({
                'test_num': idx,
                'target_name': target_name,
                'candidate_name': candidate_name,
                'expected_match': expected_match,
                'error': str(e),
                'elapsed_time': test_elapsed_time
            })
            incorrect += 1

    # Calculate total execution time
    total_elapsed_time = time.time() - total_start_time

    # Print final statistics
    print("=" * 80)
    print("Test Result Summary")
    print("=" * 80)
    print()
    print(f"Total Tests: {total}")
    print(f"Correct: {correct} ({correct/total*100:.1f}%)")
    print(f"Incorrect: {incorrect} ({incorrect/total*100:.1f}%)")
    print()
    print(f"Expected Match (True) Cases:")
    print(f"  Accuracy: {true_cases_correct}/{true_cases_total} ({true_cases_correct/true_cases_total*100:.1f}%)" if true_cases_total > 0 else "  No cases")
    print()
    print(f"Expected Non-Match (False) Cases:")
    print(f"  Accuracy: {false_cases_correct}/{false_cases_total} ({false_cases_correct/false_cases_total*100:.1f}%)" if false_cases_total > 0 else "  No cases")
    print()
    print("=" * 80)
    print("Execution Time Statistics")
    print("=" * 80)
    print()
    if test_times:
        avg_time = sum(test_times) / len(test_times)
        min_time = min(test_times)
        max_time = max(test_times)
        print(f"Total Execution Time: {total_elapsed_time:.2f}s")
        print(f"Average Test Time: {avg_time:.2f}s")
        print(f"Minimum Test Time: {min_time:.2f}s")
        print(f"Maximum Test Time: {max_time:.2f}s")
        print()

    if parse_errors > 0:
        print(f"⚠️  JSON Parsing Failed: {parse_errors} cases")
        print()

    # Detailed report for incorrect cases
    incorrect_cases = [r for r in results if not r.get('is_correct', True)]
    if incorrect_cases:
        print("=" * 80)
        print("Details of Incorrect Cases")
        print("=" * 80)
        print()
        for case in incorrect_cases:
            print(f"Test #{case['test_num']}")
            print(f"  Target: {case['target_name']}")
            print(f"  Candidate: {case['candidate_name']}")
            print(f"  Expected: {case['expected_match']}")
            print(f"  Actual: {case.get('claude_match', 'N/A')}")
            source = case.get('source', 'N/A')
            source_label = "Hard Rule" if source == 'hard_rule' else "LLM" if source == 'llm' else source
            print(f"  Source: {source_label}")
            print(f"  Expected Reason: {case.get('expected_reason', 'N/A')}")
            reason_label = f"  {source_label} Reason:" if source in ['hard_rule', 'llm'] else "  Reason:"
            print(f"{reason_label} {case.get('result_reason', 'N/A')}")
            if 'raw_response' in case:
                print(f"  Raw Response: {case['raw_response'][:200]}...")
            print()

    return results

def analyze_sources(results):
    """Analyzes the accuracy of each decision source (Hard Rule vs. LLM)."""
    hard_rule_correct = 0
    hard_rule_total = 0
    llm_correct = 0
    llm_total = 0

    for r in results:
        if 'source' in r:
            if r['source'] == 'hard_rule':
                hard_rule_total += 1
                if r['is_correct']:
                    hard_rule_correct += 1
            elif r['source'] == 'llm':
                llm_total += 1
                if r['is_correct']:
                    llm_correct += 1

    print("=" * 80)
    print("Accuracy by Decision Source")
    print("=" * 80)
    print()
    if hard_rule_total > 0:
        print(f"Hard Rule Accuracy: {hard_rule_correct}/{hard_rule_total} ({hard_rule_correct/hard_rule_total*100:.1f}%)")
    if llm_total > 0:
        print(f"LLM Accuracy: {llm_correct}/{llm_total} ({llm_correct/llm_total*100:.1f}%)")
    print()

if __name__ == '__main__':
    # Run the tests and get the results
    test_results = run_tests()
    # Analyze the results by source
    analyze_sources(test_results)

    # Exit with a non-zero status code if any tests failed (for CI/CD)
    if any(not r.get('is_correct', True) for r in test_results):
        exit(1)
    else:
        exit(0)