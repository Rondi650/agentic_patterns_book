from collections import Counter
from collections.abc import Callable
from typing import Any, Literal

LiteralDecision = Literal["Approve", "Review", "Reject", "Escalate"]


class LoanOrchestrator:
    def __init__(self):
        # In a real system, these would be different models or services
        self.agents: list[Callable[[dict[str, Any]], LiteralDecision]] = [
            self.call_agent_A,
            self.call_agent_B,
            self.call_agent_C
        ]

    # --- Agent simulation methods ---

    def call_agent_A(self, application) -> LiteralDecision:
        print("Agent A evaluating...")
        return "Approve"

    def call_agent_B(self, application) -> LiteralDecision:
        print("Agent B evaluating...")
        return "Review"

    def call_agent_C(self, application) -> LiteralDecision:
        print("Agent C evaluating...")
        return "Approve"

    def get_final_decision(self, application_data: dict[str, Any]) -> str | LiteralDecision:
        print(
            f"\nGetting final decision for application: {application_data['id']}")

        # In a real system, these calls would be made in parallel
        decisions = [agent(application_data) for agent in self.agents]
        print(f"Collected decisions: {decisions}")

        # Count the votes
        vote_counts = Counter(decisions)
        print(f"Vote counts: {vote_counts}")

        # Determine if there is a clear majority (more than half the votes)
        if vote_counts and vote_counts.most_common(1)[0][1] > len(self.agents) / 2:
            final_decision = vote_counts.most_common(1)[0][0]
            print(f"Majority found. Final decision is: '{final_decision}'")
            return final_decision
        else:
            print("No clear majority. Escalating for human review.")
            return "Escalate"


# Execute the workflow
orchestrator = LoanOrchestrator()
application = {"id": "APP-XYZ-789", "amount": 500000}
final_decision = orchestrator.get_final_decision(application)
print(f"Final decision for application {application['id']}: {final_decision}")
