import time
import random


class Supervisor:
    def __init__(self, agent_ids):
        self.worker_agents = {
            agent_id: self._start_agent(agent_id)
            for agent_id in agent_ids
        }
        print(self.worker_agents)

    def _start_agent(self, agent_id):
        # In a real system, this would start a new process or container
        print(f"SUPERVISOR: Starting process for Agent {agent_id}...")
        return {"status": "healthy", "process_id": random.randint(1000, 9999)}

    def is_agent_healthy(self, agent_id):
        # Simulates a health check (e.g., checking a heartbeat endpoint)
        # We'll simulate a random crash for demonstration
        if random.random() < 0.2:  # 20% chance of appearing unhealthy
            return False
        return True

    def restart_agent_process(self, agent_id):
        # Simulates restarting the agent
        print(f"SUPERVISOR: Restarting Agent {agent_id}...")
        self.worker_agents[agent_id] = self._start_agent(agent_id)
        print()
        print(self.worker_agents[agent_id])
        print()
        print(self._start_agent(agent_id))
        print(f"SUPERVISOR: Agent {agent_id} has been resuscitated.")

    def monitor_agents(self):
        print("Supervisor monitoring loop started...")
        while True:
            for agent_id in list(self.worker_agents.keys()):
                print(agent_id)
                if not self.is_agent_healthy(agent_id):
                    print(
                        f"SUPERVISOR: Agent {agent_id} is unhealthy. "
                        "Attempting resuscitation."
                    )
                    self.restart_agent_process(agent_id)

            time.sleep(10)  # Check every 10 seconds


# Execute the workflow
supervisor = Supervisor(agent_ids=["DataProcessor-1", "DataProcessor-2"])
supervisor.monitor_agents()

# To run this indefinitely, you would call supervisor.monitor_agents()
# For a short demonstration, we'll just show the concept
print("Demonstrating a single monitoring cycle (conceptual).")
print("In a real system, the monitor_agents() loop would run continuously.")
