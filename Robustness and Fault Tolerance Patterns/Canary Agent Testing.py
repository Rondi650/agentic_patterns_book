import time
import threading

# Simulate a logging mechanism


def log_comparison(request_id, stable_output, canary_output):
    print(f"LOG (Request ID: {request_id}):")
    print(f"  - Stable Output: '{stable_output}'")
    print(f"  - Canary Output: '{canary_output}'")
    # In a real system, this would write to a database or logging service.


def log_error(message):
    print(f"ERROR: {message}")


class CanaryOrchestrator:

    def _call_stable_summary_agent(self, document):
        # Simulate calling the existing, reliable v1 agent
        return f"Stable summary for: {document}"

    def _call_canary_summary_agent(self, document):
        # Simulate calling the new v2 agent, which might be different or fail
        if "fail" in document:
            raise ValueError("Canary agent encountered a bug")
        return f"NEW canary summary for: {document}"

    def get_summary(self, document, request_id):
        # The stable agent handles the user-facing request
        stable_summary = self._call_stable_summary_agent(document)

        # The canary agent processes the same request in a background thread
        def canary_task():
            try:
                canary_summary = self._call_canary_summary_agent(document)
                # Log both summaries for offline comparison and evaluation
                log_comparison(request_id, stable_summary, canary_summary)
            except Exception as e:
                log_error(f"Canary agent failed for request {request_id}: {e}")

        # Run the canary test in the background so it doesn't delay the user response
        threading.Thread(target=canary_task).start()

        # Return the stable result to the user immediately
        return stable_summary

# --- Simulation ---


orchestrator = CanaryOrchestrator()

print("--- Processing a standard request ---")
user_response = orchestrator.get_summary("Annual Report Q3", "req-001")
print(f"User receives: '{user_response}'")

print("\n--- Processing a request that makes the canary fail ---")
user_response_2 = orchestrator.get_summary("Urgent memo fail test", "req-002")
print(f"User receives: '{user_response_2}' (user experience is unaffected)")

# Give the background threads a moment to finish for the demo output
time.sleep(0.1)
