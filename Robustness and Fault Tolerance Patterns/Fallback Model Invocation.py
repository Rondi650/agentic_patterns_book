import random


class FallbackModelAgent:

    def _call_primary_llm(self, prompt: str):
        """Simulates calling the primary, powerful, but sometimes flaky model."""
        print("AGENT: Attempting to call Primary LLM...")

        if random.random() < 0.5:  # 50% chance of failure
            raise ConnectionError("API Service Unavailable")

        # Simulate a valid, structured response
        return {"response": "This is a highly detailed answer from the primary model."}

    def _call_backup_llm(self, prompt: str):
        """Simulates calling the stable, reliable backup model."""
        print("AGENT: Calling Backup LLM...")
        return {"response": "This is a solid, reliable answer from the backup model."}

    def _is_valid(self, result: dict) -> bool:
        """A simple check to see if the response is in the expected format."""
        return isinstance(result, dict) and "response" in result

    def get_analysis(self, user_prompt: str):
        primary_result = None

        try:
            # 1. Attempt to use the primary, most powerful model
            primary_result = self._call_primary_llm(user_prompt)

            if self._is_valid(primary_result):
                print("SUCCESS: Primary LLM returned a valid result.")
                return primary_result
            else:
                print("WARNING: Primary LLM returned an invalid result. Falling back.")

        except Exception as e:
            print(
                f"WARNING: Primary LLM failed with an exception: {e}. Falling back.")

        # 2. If primary fails or result is invalid, use the backup model
        print("--- Fallback Triggered ---")
        backup_result = self._call_backup_llm(user_prompt)
        return backup_result


# --- Simulation ---

agent = FallbackModelAgent()

for i in range(3):
    print(f"\n--- Processing Request #{i+1} ---")
    result = agent.get_analysis("What are the quarterly earnings?")
    print(f"Final Response: {result}")
