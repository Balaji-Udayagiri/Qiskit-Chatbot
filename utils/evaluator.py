import subprocess
import os
import ast
from utils.file_manager import sanitize_task_id


def extract_function_name(file_path: str) -> str:
    """
    Extracts the first function name from the given Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        str: The name of the first function defined in the file.
    """
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                return node.name
    raise ValueError("No function definition found in the file.")


def evaluate_code(task_id: str, refined_file_path: str, test_code: str) -> tuple:
    """
    Evaluates the refined code by appending the test function to the file
    and running it. Dynamically extracts the function name and appends
    `check(function_name)` to the test code.

    Args:
        task_id (str): Unique ID for the task being evaluated.
        refined_file_path (str): Path to the refined code file.
        test_code (str): The test code to evaluate the refined output.

    Returns:
        tuple: A tuple containing the result ("PASS" or "FAIL") and an error message (if any).
    """
    temp_eval_file = f"outputs/{sanitize_task_id(task_id)}_eval.py"
    try:
        # Extract the function name from the refined code
        function_name = extract_function_name(refined_file_path)

        # Add `check(function_name)` to the test code
        test_code_with_check = test_code + f"\ncheck({function_name})\n"

        # Combine the refined code and the updated test code into a new file
        with open(refined_file_path, "r") as refined_file, open(temp_eval_file, "w") as eval_file:
            eval_file.write(refined_file.read())       # Write the refined code
            eval_file.write("\n")                     # Add a newline
            eval_file.write(test_code_with_check)     # Append the updated test code

        # Run the evaluation file
        result = subprocess.run(
            ["python", temp_eval_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check if there were errors
        if result.returncode == 0:
            return "PASS", ""  # No errors
        else:
            return "FAIL", result.stderr.strip()  # Capture the error message

    finally:
        # Clean up the temporary evaluation file
        if os.path.exists(temp_eval_file):
            os.remove(temp_eval_file)

def evaluate_and_log(task_id, refined_file_path, difficulty_scale, test_code, csv_writer, code_type):
    print(f"Task {task_id}: Evaluating {code_type} code...")
    try:
        result, error_message = evaluate_code(task_id, refined_file_path, test_code)
        print(f"Task {task_id}: {result}")
    except Exception as e:
        result = "FAIL"
        error_message = str(e)
    csv_writer.writerow([task_id, difficulty_scale, result, error_message, code_type])
