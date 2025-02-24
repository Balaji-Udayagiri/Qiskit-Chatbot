import os
from datetime import datetime
from utils.file_manager import sanitize_task_id

def log_interaction(llm: str, task_id:str, prompt: str, response: str):
    """
        Logs interactions with LLMs.

        Args:
            llm (str): The LLM used (e.g., "Ollama" or "GPT").
            task_id (str): The task ID.
            prompt (str): The prompt sent to the LLM.
            response (str): The response from the LLM.
    """
    log_dir = ".logs/"
    
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #logs_subdir = f".logs_{timestamp}"
    log_file = f"{log_dir}{llm}_log_{sanitize_task_id(task_id)}.txt"
    
    with open(log_file, "w") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"LLM: {llm}\n")
        f.write(f"Prompt:\n{prompt}\n")
        f.write(f"Response:\n{response}\n")
