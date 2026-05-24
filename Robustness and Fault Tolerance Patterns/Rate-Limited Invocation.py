import time
from collections import deque


class RateLimitedCreditAgent:
    def __init__(self, limit_per_minute: int):
        self.rate_limit = limit_per_minute
        self.window_seconds = 60
        # Use a deque for efficient popping from the left
        self.request_timestamps = deque()

    def get_score(self, applicant_id: str):
        """Fetches a credit score, applying a rate limit."""
        now = time.time()

        # Remove timestamps that are outside the current time window
        while self.request_timestamps and now - self.request_timestamps[0] > self.window_seconds:
            self.request_timestamps.popleft()

        # Check if the number of recent requests has hit the limit
        if len(self.request_timestamps) >= self.rate_limit:
            print(
                f"RATE LIMITER: Request for {applicant_id} blocked. Limit of {self.rate_limit}/min reached.")
            retry_after = self.window_seconds - \
                (now - self.request_timestamps[0])
            return {"status": "rate_limited", "retry_after": round(retry_after) + 1}

        # If not limited, proceed with the call
        self.request_timestamps.append(now)
        print(
            f"RATE LIMITER: Request for {applicant_id} allowed. ({len(self.request_timestamps)}/{self.rate_limit})")
        return self._call_credit_api(applicant_id)

    def _call_credit_api(self, applicant_id: str):
        # Simulates a successful call to the external API
        return {"status": "success", "score": 750}

# --- Simulation ---


# Create an agent with a low limit for demonstration
agent = RateLimitedCreditAgent(limit_per_minute=3)

for i in range(5):
    print(f"\nProcessing applicant #{i+1}")
    result = agent.get_score(f"applicant-{i+1}")
    print(f"Result: {result}")
    time.sleep(0.5)  # Simulate requests coming in quickly
