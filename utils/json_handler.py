import json

def load_tasks(json_file):
    """
    Load tasks from a JSON file and return a list of task dictionaries.

    Args:
        json_file (str): Path to the JSON file containing tasks.

    Returns:
        list: A list of task dictionaries.
    """
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tasks from {json_file}: {e}")
        return []
