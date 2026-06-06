# --- 1. Define the Access Control List (ACL) ---
# This defines what each role is allowed to do.
ROLE_PERMISSIONS = {
    "sales_role": ["read_purchase_history", "read_contact_info"],
    "marketing_role": ["read_aggregated_data"]
}

# --- 2. Define the Protected Resource (the Data Agent) ---


class CustomerDataAgent:
    def __init__(self, acl):
        self.acl = acl
        # Mock database of protected data
        self.database = {
            "read_purchase_history": {"items": ["Laptop", "Mouse"]},
            "contact_info": {"email": "j.doe@example.com"},
            "payment_details": {"card": "xxxx-xxxx-xxxx-1234"},
            "read_aggregated_data": {"total_sales": 10000}
        }

    def get_data(self, requested_action: str, agent_token: str):
        """
        Handles a data request, checking auth and authorization.
        'agent_token' is a simple string representing the agent's role.
        """
        print(f"\n--- New Request ---")
        print(f"AGENT (Role: {agent_token}) requests: '{requested_action}'")

        # 1. Authentication (Who is this?)
        # We simply trust the token is the role for this example.
        agent_role = agent_token
        if agent_role not in self.acl:
            print(f"DENIED (401): Role '{agent_role}' does not exist.")
            return "Error: 401 Unauthorized"

        # 2. Authorization (What are they allowed to do?)
        allowed_actions = self.acl.get(agent_role)
        if requested_action not in allowed_actions:
            print(
                f"DENIED (403): Role '{agent_role}' cannot perform '{requested_action}'.")
            return "Error: 403 Forbidden"

        # 3. Grant Access
        data = self.database.get(requested_action)
        print(f"ALLOWED (200): Access granted.")
        return f"Success: {data}"

# --- 3. Execute the Workflow ---


# Initialize the system
data_agent = CustomerDataAgent(acl=ROLE_PERMISSIONS)

# Define the agents' "tokens" (their roles)
SALES_AGENT_TOKEN = "sales_role"
MARKETING_AGENT_TOKEN = "marketing_role"

# --- Scenario 1 (Success) ---
# Sales agent requests allowed data
result_1 = data_agent.get_data("read_purchase_history", SALES_AGENT_TOKEN)
print(result_1)

# --- Scenario 2 (Authorization Failure) ---
# Sales agent requests forbidden data
result_2 = data_agent.get_data("read_payment_details", SALES_AGENT_TOKEN)
print(result_2)

# --- Scenario 3 (Success) ---
# Marketing agent requests allowed data
result_3 = data_agent.get_data(
    "read_aggregated_data", MARKETING_AGENT_TOKEN)
print(result_3)

result4 = data_agent.get_data(
    'xpto', 'xpto_agent'
)
print(result4)