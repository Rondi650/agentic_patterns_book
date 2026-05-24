import dataclasses


@dataclasses.dataclass
class Message:
    sender: str
    recipient: str
    action: str
    data: dict


class FirewallAgent:
    # Access policies define which agents can talk to which other agents.
    ACCESS_POLICIES = {
        "CustomerDatabaseAgent": {"allowed_senders": ["CustomerServiceAgent"]}
    }

    def validate_message(self, message: Message) -> bool:
        """
        Checks a message against the access policies.
        Returns True if allowed, False if blocked.
        """
        policy = self.ACCESS_POLICIES.get(message.recipient)
        print(policy)
        print(f"FIREWALL: Validating message from '{message.sender}' "
              f"to '{message.recipient}' with action '{message.action}'.")
        if policy:
            print(policy.get("allowed_senders", []))

        # If there's no specific policy, we can default to allow or deny.
        # Here, we default to allow if no policy is found.
        if not policy:
            print(f"FIREWALL: No specific policy for recipient '{message.recipient}'. "
                  f"Defaulting to allow.")
            return True

        if message.sender not in policy["allowed_senders"]:
            print(
                f"FIREWALL: BLOCKED unauthorized message from '{message.sender}' "
                f"to '{message.recipient}'."
            )
            # In a real system, this would trigger a formal security alert.
            return False 

        print(
            f"FIREWALL: Allowed message from '{message.sender}' "
            f"to '{message.recipient}'."
        )
        return True


# --- Simulation ---
firewall = FirewallAgent()

# 1. A legitimate message from an authorized agent
legitimate_message = Message(
    sender="CustomerServiceAgent",
    recipient="CustomerDatabaseAgent",
    action="query",
    data={"customer_id": 123}
)

firewall.validate_message(legitimate_message)  # This will pass

print("-" * 20)

# 2. An attack message from a compromised agent
malicious_message = Message(
    sender="ChatbotAgent",  # Unauthorized sender
    recipient="CustomerDatabaseAgent",
    action="query_all",
    data={}
)

firewall.validate_message(malicious_message)  # This will be blocked

# 3. A message to an agent with no specific policy (defaults to allow)
open_message = Message(
    sender="ChatbotAgent",
    recipient="LoggingAgent",  # No specific policy defined
    action="log",
    data={"event": "user_login"}
)
firewall.validate_message(open_message)  # This will be allowed
