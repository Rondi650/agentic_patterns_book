class PlannerAgent:
    def generate_solutions(self, topic: str, count: int = 3):
        """Generates a number of potential solutions for a given topic."""
        print(f"PLANNER: Generating {count} slogans for '{topic}'...")
        # In a real system, this would be an LLM call.
        return [
            f"Unlock your potential with {topic}.",
            f"{topic}: Engineered for excellence.",
            f"Experience the future of {topic} today!"
        ]


class ScorerAgent:
    def evaluate_solutions(self, solutions: list) -> dict:
        """Evaluates and scores a list of solutions."""
        print("SCORER: Evaluating generated solutions...")
        scored_solutions = {}
        for solution in solutions:
            # Simple scoring rubric: score based on length.
            score = len(solution)
            scored_solutions[solution] = score
        return scored_solutions


# --- Orchestration ---
planner = PlannerAgent()
scorer = ScorerAgent()

topic = "Synergy Cloud"
solutions = planner.generate_solutions(topic)
feedback = scorer.evaluate_solutions(solutions)
print(feedback)

print("\n--- Feedback ---")
for solution, score in feedback.items():
    print(f"Score {score}: '{solution}'")

best_solution = max(feedback, key=feedback.get)
print(f"\nBest solution identified: '{best_solution}'")