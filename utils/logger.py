import os
from datetime import datetime

def log_interaction(llm: str, prompt: str, response: str):
    """
    Logs interactions with LLMs.

    Args:
        llm (str): The LLM used (e.g., "Ollama" or "GPT").
        prompt (str): The prompt sent to the LLM.
        response (str): The response from the LLM.
    """
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"{log_dir}{llm}_log_{timestamp}.txt"
    
    with open(log_file, "w") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"LLM: {llm}\n")
        f.write(f"Prompt:\n{prompt}\n")
        f.write(f"Response:\n{response}\n")
