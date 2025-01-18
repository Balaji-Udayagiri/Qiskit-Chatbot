from llms.llm_ollama import LLM_Ollama
from llms.llm_gpt import LLM_GPT
from processing.process_QCA_output import process_ollama_output
from utils.file_manager import save_to_file
from utils.logger import log_interaction
from utils.json_handler import load_tasks
from utils.file_manager import save_generated_code
import os

def main():
    # Load tasks from JSON
    tasks = load_tasks("prompts/dataset_qiskit_test_human_eval1.json")
    if not tasks:
        print("No tasks found. Exiting...")
        return

    # Initialize LLMs
    qiskit_code_assistant = LLM_Ollama(model="hf.co/Qiskit/granite-8b-qiskit-GGUF:latest")
    gpt = LLM_GPT(model="gpt-4")

    for task in tasks:
        # Extract the prompt and prepare for generation
        prompt = task["prompt"]
        task_id = task["task_id"]

        print(f"Processing task {task_id}...")

        # Step 1: Generate code with Ollama
        print("Generating code with Ollama...")
        initial_code = qiskit_code_assistant.generate_code(prompt)
        log_interaction("Ollama", prompt, initial_code)

        # Process the Ollama output to extract the generated code
        initial_code = process_ollama_output(initial_code, prompt)

        # Step 2: Refine code with GPT
        # print("Refining code with GPT...")
        # refinement_prompt = f"The code was given to:\n\n{initial_code}"
        # refined_code = gpt.generate_code(refinement_prompt)
        # log_interaction("GPT", refinement_prompt, refined_code)

        # # Save outputs
        # os.makedirs("outputs/initial_code", exist_ok=True)
        # os.makedirs("outputs/refined_code", exist_ok=True)

        # save_to_file(f"outputs/initial_code/{task_id}.py", initial_code)
        # save_to_file(f"outputs/refined_code/{task_id}.py", refined_code)

        # Save the task metadata along with the generated outputs
        task["generated_initial_code"] = initial_code
        #task["generated_refined_code"] = refined_code
        save_to_file(f"outputs/{task_id}_metadata.json", task)
        save_generated_code(task_id, initial_code)
        

        print(f"Task {task_id} complete. Outputs saved to 'outputs/'.")

if __name__ == "__main__":
    main()
