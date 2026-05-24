import subprocess


class SandboxedComputationAgent:

    def run_code_in_sandbox(self, code_string: str):
        """
        Executes a string of Python code in a secure subprocess.
        This is a basic form of sandboxing. More robust solutions use containers (e.g., Docker).
        """
        print(f"--- Attempting to run code in sandbox ---\n{code_string}\n")

        try:
            # Run code in a subprocess with a 5-second timeout.
            # In a real system, you would use containerization with stricter
            # controls over network and file access.
            result = subprocess.run(
                ["python3", "-c", code_string],
                capture_output=True,  # Capture stdout and stderr
                text=True,            # Decode output as text
                timeout=5             # Enforce a timeout
            )

            if result.returncode == 0:
                print(f"--- Execution Succeeded ---\nOutput: {result.stdout.strip()}")
                return result.stdout.strip()
            else:
                print(f"--- Execution Failed ---\nError: {result.stderr.strip()}")
                return f"Error: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            print("--- Execution Failed ---\nError: Execution timed out.")
            return "Error: Execution timed out."


# --- Simulation ---
agent = SandboxedComputationAgent()

# 1. A safe request
safe_code = "print(2 + 2)"
agent.run_code_in_sandbox(safe_code)

print("\n" + "=" * 40 + "\n")

# 2. A malicious request (this will fail because subprocesses
# don't have permission to write to root by default in many environments,
# demonstrating a basic security boundary)
malicious_code = "import os; print(os.listdir('/'))"
agent.run_code_in_sandbox(malicious_code)


malicious_code =  "import time; time.sleep(6)"
agent.run_code_in_sandbox(malicious_code)