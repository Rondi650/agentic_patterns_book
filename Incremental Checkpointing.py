import asyncio
import os
import json

# A simple file-based checkpoint manager
CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)


def save_checkpoint(doc_id: str, step_name: str, data):
    """Saves step data to a file."""
    filepath = os.path.join(CHECKPOINT_DIR, f"{doc_id}_{step_name}.json")
    with open(filepath, 'w') as f:
        json.dump(data, f)
    print(f"CHECKPOINT: Saved '{step_name}' for doc '{doc_id}'.")


def load_checkpoint(doc_id: str, step_name: str):
    """Loads step data from a file if it exists."""
    filepath = os.path.join(CHECKPOINT_DIR, f"{doc_id}_{step_name}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            print(
                f"CHECKPOINT: Found and loaded '{step_name}' for doc '{doc_id}'.")
            return json.load(f)
    return None


# --- Agent Task Simulations ---
async def clean_text_agent(text: str):
    print("TASK: Cleaning text (long process)...")
    # Simulate work
    return text.strip().lower()


async def extract_entities_agent(cleaned_text: str):
    print("TASK: Extracting entities (long process)...")
    # Simulate work
    return {"entities": ["paris", "eiffel tower"]}


async def summarize_agent(entities: dict):
    print("TASK: Summarizing text...")
    # Simulate work
    return "This document is about the Eiffel Tower in Paris."


class DocumentPipelineAgent:
    async def process_document(self, doc_id: str, raw_text: str):
        print(f"\n--- Starting pipeline for doc: {doc_id} ---")

        # Step 1: Clean Text
        cleaned_text = load_checkpoint(doc_id, "cleaned_text")

        if not cleaned_text:
            cleaned_text = await clean_text_agent(raw_text)
            save_checkpoint(doc_id, "cleaned_text", cleaned_text)

        # Step 2: Extract Entities
        entities = load_checkpoint(doc_id, "entities")

        if not entities:
            # This step will fail if "eiffel" is in the text, to simulate a crash
            if "eiffel" in cleaned_text:
                print("ERROR: Entity extraction failed unexpectedly!")
                raise ValueError("Simulated failure during entity extraction")

            entities = await extract_entities_agent(cleaned_text)
            save_checkpoint(doc_id, "entities", entities)

        # Step 3: Summarize
        summary = await summarize_agent(entities)
        print("--- Pipeline finished successfully ---")
        return summary


# Execute the workflow


async def main():
    pipeline = DocumentPipelineAgent()
    doc_id_1 = "doc123"
    raw_text_1 = "  The Eiffel Tower is in Paris. "

    try:
        # This run will fail during step 2
        await pipeline.process_document(doc_id_1, raw_text_1)

    except ValueError as e:
        print(f"\nPipeline run failed: {e}")
        print("--- Attempting to resume pipeline ---")

        # In a real system, you might fix the agent before retrying
        # Here we just run it again; it will resume from the checkpoint
        # To make it succeed this time, let's pretend the bug is fixed
        await pipeline.process_document(
            doc_id_1,
            "  This is a different document. "
        )

asyncio.run(main())
