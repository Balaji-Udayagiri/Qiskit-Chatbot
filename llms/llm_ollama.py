import subprocess

class LLM_Ollama:
    def __init__(self, model: str = "your_ollama_model"):
        self.model = model

    def generate_code(self, prompt):
        """
        Generate code based on a single prompt or a list of prompts.

        Args:
            prompt (str or list of str): A single prompt or a list of prompts.
        
        Returns:
            str or list of str: The generated output for a single prompt or a list of outputs for multiple prompts.
        """
        try:
            if isinstance(prompt, str):
                # Handle single prompt
                command = ["ollama", "run", self.model, prompt]
                result = subprocess.run(command, capture_output=True, text=True, check=True)

                if result.returncode == 0:
                    return result.stdout.strip()
                else:
                    print(f"Error running model {self.model}: {result.stderr}")
                    return None

            elif isinstance(prompt, list):
                # Handle list of prompts
                outputs = []
                for single_prompt in prompt:
                    command = ["ollama", "run", self.model, single_prompt]
                    result = subprocess.run(command, capture_output=True, text=True, check=True)

                    if result.returncode == 0:
                        outputs.append(result.stdout.strip())
                    else:
                        print(f"Error running model {self.model} for prompt '{single_prompt}': {result.stderr}")
                        outputs.append(None)  # Append None for failed prompts
                return outputs
            else:
                raise ValueError("Prompt must be either a string or a list of strings.")
        except Exception as e:
            print(f"Exception while running model {self.model}: {str(e)}")
            return None
