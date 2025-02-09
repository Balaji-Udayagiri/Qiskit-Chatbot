import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Evaluate code generation and refinement")
    parser.add_argument("--task_file", type=str, required=True, help="Path to the JSON file containing task prompts")
    parser.add_argument("--initial", action="store_true", help="Evaluate only initial code")
    parser.add_argument("--refined", action="store_true", help="Evaluate only refined code")
    parser.add_argument("--ollama_model", type=str, default="hf.co/Qiskit/granite-8b-qiskit-GGUF:latest", help="Ollama model name")
    parser.add_argument("--gpt_model", type=str, default="o1-preview", help="GPT model name")
    return parser.parse_args()
