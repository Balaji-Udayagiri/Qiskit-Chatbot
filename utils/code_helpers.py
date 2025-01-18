# utils/code_helpers.py
from utils.file_manager import save_generated_code
from utils.evaluator import evaluate_code
from utils.logger import log_interaction
from processing.process_LLM_output import process_LLM_output

def generate_code_with_llm(model, prompt):
    print(f"Generating code with {model}...")
    llm_output = model.generate_code(prompt)
    return process_LLM_output(llm_output, prompt)

def refine_code_with_gpt(gpt_model, prompt, initial_code):
    print("Refining code with GPT...")
    refinement_prompt = f"From the prompt:\n\n{prompt}\n\nI wrote:\n\n{initial_code}\n\nFix any errors, complete the code with imports, and wrap the function in triple backticks for clarity."
    return gpt_model.generate_code(refinement_prompt)[0]

def evaluate_and_log(task_id, refined_file_path, difficulty_scale, test_code, csv_writer):
    print(f"Task {task_id}: Evaluating refined code...")
    try:
        result, error_message = evaluate_code(task_id, refined_file_path, test_code)
        print(f"Task {task_id}: {result}")
    except Exception as e:
        result = "FAIL"
        error_message = str(e)
    csv_writer.writerow([task_id, difficulty_scale, result, error_message])
