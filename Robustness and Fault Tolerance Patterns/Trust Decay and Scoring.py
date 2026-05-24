import random


class TrustOrchestratorAgent:
    def __init__(self):
        self.trust_scores = {"AgentA": 1.0, "AgentB": 1.0, "AgentC": 1.0}
        self.success_increment = 0.1
        self.failure_decrement = 0.2

    def _call_agent(self, agent_name: str, task_data: dict) -> bool:
        print(agent_name, self.trust_scores[agent_name])
        """Simulates calling a worker agent which may succeed or fail."""
        print(
            f"ORCHESTRATOR: Delegating task to {agent_name} (Score: {self.trust_scores[agent_name]:.2f})")

        # Simulate failure for some agents
        if agent_name == "AgentB" and random.random() < 0.5:  # AgentB is flaky
            print(f"AGENT ({agent_name}): Task Failed.")
            return False

        print(f"AGENT ({agent_name}): Task Succeeded.")
        return True

    def update_trust_score(self, agent_name: str, success: bool):
        """Updates the trust score based on the outcome."""
        if success:
            self.trust_scores[agent_name] += self.success_increment
        else:
            self.trust_scores[agent_name] -= self.failure_decrement

        # Ensure scores don't go below a certain floor
        self.trust_scores[agent_name] = max(0.1, self.trust_scores[agent_name])
        print(f"ORCHESTRATOR: Updated trust scores: {self.trust_scores}")

    def handle_task(self, task_data: dict):
        print(f"\n--- Handling New Task: {task_data['id']} ---")

        # Sort agents by their current trust score in descending order
        sorted_agents = sorted(self.trust_scores.items(),
                               key=lambda item: item[1])
        print(sorted_agents)

        for agent_name, score in sorted_agents:
            success = self._call_agent(agent_name, task_data)
            self.update_trust_score(agent_name, success=success)

            if success:
                print(f"--- Task {task_data['id']} Completed Successfully ---")
                return "Task Complete"

        print(
            f"--- Task {task_data['id']} Failed: All agents were unsuccessful ---")
        # self.escalate_to_human("All agents failed task.")
        return "All Agents Failed"


# --- Simulation ---
orchestrator = TrustOrchestratorAgent()
for i in range(5):
    orchestrator.handle_task({"id": f"task-{i+1}"})
