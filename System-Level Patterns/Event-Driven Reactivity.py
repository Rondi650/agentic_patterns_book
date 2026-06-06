import time
import os
from pprint import pprint

os.system('clear')


class MessageBus:
    """A simple mock message bus (like Kafka or Pub/Sub)."""

    def __init__(self):
        # Stores subscribers as: {"topic_name": [list_of_callbacks]}
        self.subscriptions = {}
        print("BUS: Message Bus initialized.")

    def subscribe(self, topic: str, callback_function):
        """Allows a consumer (agent) to subscribe to a topic."""
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.subscriptions[topic].append(callback_function)
        # Get the name of the class that owns the callback
        consumer_name = callback_function.__self__.__class__.__name__
        print(f"BUS: '{consumer_name}' subscribed to topic '{topic}'.")

    def publish(self, topic: str, message: dict):
        """A producer calls this to publish an event."""
        print(f"\nBUS: New message published to topic '{topic}': {message}")
        if topic in self.subscriptions:
            # Push the message to all subscribed consumers
            for callback in self.subscriptions[topic]:
                callback(message)  # Trigger the consumer's method


class TriageAgent:  # Consumer 1
    def __init__(self, bus: MessageBus):
        self.bus = bus
        # Subscribe to the 'new_tickets' topic
        self.bus.subscribe("new_tickets", self.handle_new_ticket)

    def handle_new_ticket(self, ticket_data: dict):
        """This is the callback function triggered by the bus."""
        print("AGENT (Triage): Received new ticket. Classifying...")
        # Simulate LLM classification logic
        priority = "Urgent" if "payment" in ticket_data['content'].lower(
        ) else "Medium"
        category = "Billing" if "payment" in ticket_data['content'].lower(
        ) else "Technical"

        enriched_ticket = {
            **ticket_data,
            "priority": priority,
            "category": category
        }

        # Publish the enriched ticket to a new topic
        self.bus.publish("triaged_tickets", enriched_ticket)


class ArchivingService:  # Consumer 2
    def __init__(self, bus: MessageBus):
        self.bus = bus
        # Subscribe to the same 'new_tickets' topic
        self.bus.subscribe("new_tickets", self.archive_ticket)

    def archive_ticket(self, ticket_data: dict):
        """This callback is also triggered by the 'new_tickets' event."""
        print(
            f"AGENT (Archive): Received ticket {ticket_data['id']}. Writing to data warehouse...")
        # Simulate database write
        time.sleep(0.5)
        print(f"AGENT (Archive): Wrote {ticket_data['id']} to warehouse.")


class WebServer:  # Producer
    def __init__(self, bus: MessageBus):
        self.bus = bus

    def submit_ticket(self, ticket_content: str, user: str):
        ticket_id = f"TKT-{hash(ticket_content)}"
        print(f"\nSERVER: User '{user}' submitted a new ticket.")
        new_ticket = {
            "id": ticket_id,
            "user": user,
            "content": ticket_content
        }
        # Publish the event to the bus
        self.bus.publish("new_tickets", new_ticket)


# --- Execute the Workflow ---
message_bus = MessageBus()
print(message_bus.subscriptions)

# 1. Initialize the Consumers (Agents)
# They automatically subscribe when created
triage_agent = TriageAgent(bus=message_bus)
archiving_service = ArchivingService(bus=message_bus)

pprint(message_bus.subscriptions)

# 2. Initialize the Producer
web_server = WebServer(bus=message_bus)

# 3. Simulate a user submitting a ticket
web_server.submit_ticket(
    ticket_content="I can't access my payment history.",
    user="user@example.com"
)
