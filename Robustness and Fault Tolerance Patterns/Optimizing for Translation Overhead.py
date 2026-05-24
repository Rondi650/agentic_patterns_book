# Assume SHARED_CACHE is a globally available, fast key-value store like Redis.
# For this example, we'll simulate it with a simple dictionary.

SHARED_CACHE = {}


def store_in_cache(data: str) -> str:
    """Stores data and returns a unique ID."""
    # In a real system, the key would be a UUID or hash.
    key = f"cache:doc-{hash(data)}"
    SHARED_CACHE[key] = data
    print(f"CACHE: Stored data under key '{key}'.")
    return key


def get_from_cache(key: str) -> str:
    """Retrieves data from the cache using its ID."""
    print(f"CACHE: Retrieving data for key '{key}'.")
    return SHARED_CACHE.get(key)


class SummarizationAgent:
    def summarize_from_reference(self, request: dict):
        print("AGENT: Received lightweight request.")
        document_id = request.get("document_id")

        if not document_id:
            return "Error: No document_id provided."

        # 3. Retrieve the full data from the cache
        document_text = get_from_cache(document_id)

        # 4. Now proceed with summarization...
        print("AGENT: Successfully retrieved document. Starting summarization.")

        # Simulate summarization
        summary = f"This is a summary of the document that starts with: '{document_text[:30]}...'"
        return summary


class Orchestrator:
    def __init__(self):
        self.agent = SummarizationAgent()

    def process_large_document(self, document_text: str):
        print("\n--- Orchestrator: Starting document processing ---")

        # 1. Store the large data in a shared cache first
        document_id = store_in_cache(document_text)
        print(document_id)

        # 2. Send a lightweight reference instead of the full data
        lightweight_request = {"document_id": document_id}
        summary = self.agent.summarize_from_reference(lightweight_request)

        print(f"\n--- Orchestrator: Received final summary ---\n{summary}")
        return summary


# Execute the workflow
orchestrator = Orchestrator()
large_doc = "This is the full text of a very long document that would be too large to fit in a standard prompt..." * 100
orchestrator.process_large_document(large_doc)
