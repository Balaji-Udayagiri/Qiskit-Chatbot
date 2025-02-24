from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from processing.process_LLM_output import process_LLM_output
from utils.logger import log_interaction


class LLM_GPT:
    """
    A class to interact with the GPT model using the OpenAI API.

    Attributes:
        model (str): The GPT model name to use (default is "gpt-4").
        client (OpenAI): The OpenAI client instance for interacting with the API.
    """

    def __init__(self, model: str = "deepseek/deepseek-chat:free"):
        """
        Initialize the LLM_GPT class.

        Args:
            model (str): The name of the GPT model to use.
            api_key (str): The OpenAI API key.
        """
        load_dotenv()
        self.model = model
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1", 
            api_key=os.getenv("DEEP_SEEK_V3_KEY")
            )  # Initialize the OpenAI client with the provided API key

    def __modify_prompt__(self, prompt, initial_code):
        ollama_prompt = f"Fix any errors, complete the code with imports, and wrap the function in triple backticks for clarity for the below code.:\n\n{initial_code}\n\n"
        #ollama_prompt = f"From the prompt:\n\n{prompt}\n\nI wrote:\n\n{initial_code}\n\nFix any errors, complete the code with imports, and wrap the function in triple backticks for clarity."
        return ollama_prompt

    def generate_code(self, prompt, max_retries=3, delay=2):
        """
        Generate a response using GPT, retrying if the response is blank or incomplete.

        Args:
            prompt (str): The input prompt.
            max_retries (int): Number of times to retry in case of a blank or incomplete response.
            delay (int): Time (in seconds) to wait before retrying.

        Returns:
            str: The generated response or an error message.
        """
        retries = 0
        while retries < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                generated_text = response.choices[0].message.content.strip()

                if generated_text and "return" in generated_text:  
                    return generated_text  # Valid response
                else:
                    print(f"Incomplete response received. Retrying... ({retries+1}/{max_retries})")

            except Exception as e:
                print(f"Error occurred: {e}. Retrying... ({retries+1}/{max_retries})")

            retries += 1
            time.sleep(delay)  # Wait before retrying

        return "Error: LLM returned blank or incomplete response after multiple attempts."



    def generate_and_log_code(self, prompt, task_id, initial_code):
        ollama_prompt = self.__modify_prompt__(prompt, initial_code)
        llm_output = self.generate_code(ollama_prompt)
        code = process_LLM_output(llm_output, prompt)
        log_interaction("V3", task_id, ollama_prompt, llm_output)
        return code
