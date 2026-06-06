# --- Mock Database / Services ---

# Mock database of patient consent records
PATIENT_CONSENT_DB = {
    "Patient-12345": ["billing"],
    "Patient-67890": ["billing", "clinical_research"]
}

# Mock policy engine (can be a simple function or a dedicated service)


def policy_engine_adjudicate(
    action: str, resource_id: str, consent_types: list
) -> bool:
    """
    Checks if an action is compliant.
    Returns True for 'ALLOW' and False for 'DENY'.
    """
    if action == "access_patient_record_for_research":
        # Rule: Must have 'clinical_research' consent
        return "clinical_research" in consent_types
    return False  # Default deny

# --- Agent and Monitor Implementation ---


class HIPAAComplianceMonitor:
    """
    Acts as the compliance agent/monitor.
    It intercepts actions and checks them against the policy engine.
    """

    def __init__(self, consent_db):
        self.consent_db = consent_db

    def intercept_and_adjudicate(
        self, agent_name: str, action: str, patient_id: str
    ) -> dict:
        """
        Intercepts an agent's action, checks policy, and enforces a decision.
        """
        print(
            f"MONITOR: Intercepted action '{action}' from '{agent_name}' for '{patient_id}'.")

        # 1. Get relevant context (patient's consent)
        patient_consent = self.consent_db.get(patient_id, [])
        print(f"MONITOR: Found consent for '{patient_id}': {patient_consent}")

        # 2. Adjudication: Ask the policy engine for a decision
        is_allowed = policy_engine_adjudicate(
            action, patient_id, patient_consent)

        # 3. Enforcement
        if is_allowed:
            print(f"MONITOR: Action ALLOWED.")
            return {"status": "ALLOW"}
        else:
            print(
                f"MONITOR: Action DENIED. (Reason: Missing required consent 'clinical_research')")
            # In a real system, this logs a formal compliance breach alert
            return {"status": "DENY",
                    "reason": "Missing required consent 'clinical_research'"}


class ResearchQueryAgent:
    """
    The agent performing the work. It must send its actions
    through the compliance monitor.
    """

    def __init__(self, monitor: HIPAAComplianceMonitor):
        self.monitor = monitor

    def access_patient_data(self, patient_id: str):
        print(
            f"\nAGENT (ResearchQueryAgent): Attempting to access data for '{patient_id}'...")

        action_to_perform = "access_patient_record_for_research"

        # Send action to the monitor for approval *before* execution
        decision = self.monitor.intercept_and_adjudicate(
            agent_name="ResearchQueryAgent",
            action=action_to_perform,
            patient_id=patient_id
        )

        # Only proceed if the action was allowed
        if decision["status"] == "ALLOW":
            print(f"AGENT: Access granted. Fetching data for {patient_id}...")
            # ... database.query(patient_id) ...
            return f"Successfully retrieved data for {patient_id}."
        else:
            print(f"AGENT: Access denied. Aborting task.")
            return f"Error: Could not access data for {patient_id}. Reason: {decision['reason']}"

# --- Execute the Workflow ---


# 1. Initialize the monitor with the consent database
compliance_monitor = HIPAAComplianceMonitor(consent_db=PATIENT_CONSENT_DB)

# 2. Initialize the agent and pass it the monitor
research_agent = ResearchQueryAgent(monitor=compliance_monitor)

# 3. Run Scenario 1: The Non-Compliant Request (Patient-12345)
# This patient only has 'billing' consent.
result_1 = research_agent.access_patient_data("Patient-12345")
print(f"FINAL RESULT 1: {result_1}")

# 4. Run Scenario 2: The Compliant Request (Patient-67890)
# This patient has 'clinical_research' consent.
result_2 = research_agent.access_patient_data("Patient-67890")
print(f"FINAL RESULT 2: {result_2}")
