from transformers import pipeline
from processing.process_LLM_output import process_LLM_output
from utils.logger import log_interaction

class LLM_Transformers:
    def __init__(self, model: str = "your_ollama_model"):
        self.model = model
        self.pipe = pipeline("text-generation", model=self.model)

    def __modify_prompt__(self, prompt):
        transformer_prompt = "Give the entire code for the following task containing the library imports and function definition and body:\n" + prompt
        return transformer_prompt

    def generate_code(self, prompt):
        """
        Generate code based on a single prompt or a list of prompts.

        Args:
            prompt (str or list of str): A single prompt or a list of prompts.
        
        Returns:
            str or list of str: The generated output for a single prompt or a list of outputs for multiple prompts.
            str: The extracted code from the generated.
        """
        print("in generate code")
        try:
            result = self.pipe(prompt, max_length=512)
            output = result[0]['generated_text']
            return output

        except Exception as e:
            print(f"Exception while running model {self.model}: {str(e)}")
            return None
        
    
    def generate_and_log_code(self, prompt, task_id):
        print("in generate and log code")
        modified_prompt = self.__modify_prompt__(prompt)
        llm_output = self.generate_code(modified_prompt)
        print("llm output = ", llm_output)
        code = process_LLM_output(llm_output, prompt)
        log_interaction("Transformers", task_id, modified_prompt, llm_output)
        return code
