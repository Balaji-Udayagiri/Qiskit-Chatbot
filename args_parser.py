import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Evaluate code generation and refinement")
    parser.add_argument("--initial", action="store_true", help="Evaluate only initial code")
    parser.add_argument("--refined", action="store_true", help="Evaluate only refined code")
    parser.add_argument("--ollama_model", type=str, required=True, help="Ollama model name")
    parser.add_argument("--gpt_model", type=str, required=True, help="GPT model name")
    return parser.parse_args()
