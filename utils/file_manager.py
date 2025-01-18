import os
import json
import unicodedata

def save_to_file(filepath, content):
    """
    Save content to a specified file. Converts dictionaries to JSON format before saving.

    Args:
        filepath (str): Path to the file where content will be saved.
        content (str | dict): The content to write to the file.

    Raises:
        Exception: If there is an error writing to the file.
    """
    try:
        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # If content is a dictionary, convert it to a JSON string
        if isinstance(content, dict):
            content = json.dumps(content, indent=4)  # Format the JSON for readability

        # Write content to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"File saved successfully: {filepath}")

    except Exception as e:
        print(f"Error saving file {filepath}: {e}")
        raise

def normalize_code(code_str):
    """
    Normalize the code to remove problematic characters and ensure compatibility.
    - Convert special Unicode characters to ASCII equivalents where possible.
    - Remove or replace characters that cannot be encoded in UTF-8.
    """
    normalized_code = unicodedata.normalize('NFKD', code_str).encode('ascii', 'ignore').decode('ascii')
    return normalized_code

def sanitize_task_id(task_id):
    """
    Sanitize the task_id to create valid file names by replacing invalid characters.
    """
    return task_id.replace("/", "_")


def save_generated_code(task_id, loc, code_str):
    """
    Save normalized Python code into a Python file.
    """
    sanitized_task_id = sanitize_task_id(task_id)
    file_name = f"outputs/{loc}/generated_code_{sanitized_task_id}.py"
    normalized_code = normalize_code(code_str)  # Normalize the code before saving
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(normalized_code)
    return file_name