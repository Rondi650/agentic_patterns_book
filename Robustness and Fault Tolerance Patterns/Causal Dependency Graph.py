import json


class CausalLogger:
    def __init__(self, task_id):
        self.task_id = task_id
        self.graph = {}
        self.step_counter = 0

    def log_step(self, agent_name, action, inputs, output):
        self.step_counter += 1

        step_id = f"step_{self.step_counter}_{agent_name}_{action}"

        # 'inputs' is a list of previous step_ids this step depends on
        self.graph[step_id] = {
            "agent": agent_name,
            "action": action,
            "inputs": inputs,
            "output": output
        }

        print(f"LOGGER: Logged {step_id}")
        return step_id

    def pretty_print_graph(self):
        print(f"\n--- Causal Graph for Task: {self.task_id} ---")
        print(json.dumps(self.graph, indent=2))


# --- Main Orchestration ---
def process_loan_application(task_id, app_data_raw, external_credit_score):
    logger = CausalLogger(task_id)

    # 1. Log initial raw data as the first node
    step1_id = logger.log_step(
        "DataSource",
        "load",
        inputs=[],
        output=app_data_raw
    )

    # 2. Validation step
    validated_data = {"status": "validated",
                      **app_data_raw}  # Simulate validation
    step2_id = logger.log_step(
        "DataValidationAgent",
        "validate",
        inputs=[step1_id],
        output=validated_data
    )

    # 3. Log external data source
    step3_id = logger.log_step(
        "DataSource",
        "fetch_credit_score",
        inputs=[],
        output={"score": external_credit_score}
    )

    # 4. Risk assessment step
    risk_score = 75  # Simulate calculation
    step4_id = logger.log_step(
        "RiskAssessmentAgent",
        "calculate_risk",
        inputs=[step2_id, step3_id],
        output={"risk_score": risk_score}
    )

    # 5. Final decision step
    decision = "Deny" if risk_score > 50 else "Approve"
    step5_id = logger.log_step(
        "FinalDecisionAgent",
        "decide",
        inputs=[step4_id],
        output={"decision": decision}
    )

    logger.pretty_print_graph()


# Execute the workflow
process_loan_application("task-123", {"name": "John Doe"}, 620)
