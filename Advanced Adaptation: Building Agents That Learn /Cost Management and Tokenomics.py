class CostMonitor:
    def __init__(self, monthly_budget: float):
        self.budget = monthly_budget
        self.current_spend = 0.0
        # A simple cost model: $0.002 per 1000 tokens
        self.cost_per_1k_tokens = 0.002

    def log_usage(self, tokens: int):
        """Logs token usage and updates the current spend."""
        cost = (tokens / 1000) * self.cost_per_1k_tokens
        print(cost)
        self.current_spend += cost
        print(
            f"COST MONITOR: Logged {tokens} tokens. "
            f"Cost: ${cost:.4f}. Total spend: ${self.current_spend:.2f}"
        )

    def is_budget_exceeded(self) -> bool:
        """Checks if the current spend has exceeded the budget."""
        if self.current_spend > self.budget:
            print(f"COST MONITOR: ALERT! Budget of ${self.budget} exceeded.")
            return True
        return False


# --- Orchestration with Cost Control ---
budget = 50.0  # $50 monthly budget
monitor = CostMonitor(monthly_budget=budget)


def run_expensive_training_job():
    print("\nAttempting to run expensive training job...")
    if monitor.is_budget_exceeded():
        print("Action blocked. Budget exceeded.")
        return

    print("Budget OK. Starting training job...")
    # Simulate a job that uses 5 million tokens
    monitor.log_usage(5_000_000)


# Simulate some regular activity

monitor.log_usage(1_000_000)
monitor.log_usage(2_500_000)

# This will succeed
run_expensive_training_job()

# Simulate more activity that pushes it over budget
monitor.log_usage(20_000_000)

# This will be blocked
run_expensive_training_job()