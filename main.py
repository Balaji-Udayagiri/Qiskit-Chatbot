import csv
from llms.llm_ollama import LLM_Ollama
from llms.llm_gpt import LLM_GPT
from utils.json_handler import load_tasks
from utils.code_helpers import generate_code_with_llm, refine_code_with_gpt, evaluate_and_log
from utils.file_manager import save_generated_code
from utils.logger import log_interaction
from args_parser import parse_arguments

def main():
    # Parse arguments
    args = parse_arguments()

    # Load tasks from JSON
    tasks = load_tasks(args.task_file)
    if not tasks:
        print("No tasks found. Exiting...")
        return

    # Initialize LLMs
    qiskit_code_assistant = LLM_Ollama(model=args.ollama_model)
    gpt = LLM_GPT(model=args.gpt_model)

    output_csv = "outputs/evaluation_results.csv"
    with open(output_csv, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["task_id", "difficulty_Scale", "result", "error_message"])

        for task in tasks:
            task_id = task["task_id"]
            print(f"Processing task {task_id}...")
            ollama_prompt = "Give the entire code for the following task containing the library imports and function definition and body:\n" + task["prompt"]

            if args.initial:
                # Step 1: Generate code with Ollama (only initial code)
                
                #ollama_output, initial_code = generate_code_with_llm(qiskit_code_assistant, task["prompt"])
                ollama_output, initial_code = generate_code_with_llm(qiskit_code_assistant, ollama_prompt)

                log_interaction("Ollama", task["task_id"], ollama_prompt, ollama_output)
                initial_file_path = save_generated_code(task_id, "initial_code", initial_code)

                # Step 2: Evaluate initial code
                print(f"Evaluating initial code for task {task_id}...")
                evaluate_and_log(task_id, initial_file_path, task["difficulty_scale"], task["test"], csv_writer)

            elif args.refined:
                # Step 1: Generate initial code with Ollama
                ollama_output, initial_code = generate_code_with_llm(qiskit_code_assistant, ollama_prompt)
                log_interaction("Ollama", ollama_prompt, ollama_output)
                initial_file_path = save_generated_code(task_id, "initial_code", initial_code)

                # Step 2: Refine code with GPT
                gpt_output, refined_code = refine_code_with_gpt(gpt, task["prompt"], initial_code)
                log_interaction("GPT", task["prompt"], gpt_output)
                refined_file_path = save_generated_code(task_id, "refined_code", refined_code)

                # Step 3: Evaluate refined code
                print(f"Evaluating refined code for task {task_id}...")
                evaluate_and_log(task_id, refined_file_path, task["difficulty_scale"], task["test"], csv_writer)

            else:
                # If neither flag is set, evaluate both codes
                print(f"Evaluating both codes for task {task_id}...")
                ollama_output, initial_code = generate_code_with_llm(qiskit_code_assistant, ollama_prompt)
                log_interaction("Ollama", task["prompt"], ollama_output)
                initial_file_path = save_generated_code(task_id, "initial_code", initial_code)

                # Evaluate initial code
                evaluate_and_log(task_id, initial_file_path, task["difficulty_scale"], task["test"], csv_writer)

                # Refine code with GPT
                gpt_output, refined_code = refine_code_with_gpt(gpt, task["prompt"], initial_code)
                log_interaction("GPT", task["prompt"], gpt_output)
                refined_file_path = save_generated_code(task_id, "refined_code", refined_code)

                # Evaluate refined code
                evaluate_and_log(task_id, refined_file_path, task["difficulty_scale"], task["test"], csv_writer)

            print(f"Task {task_id} complete. Outputs saved to 'outputs/'.")

if __name__ == "__main__":
    main()
