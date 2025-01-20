from openai import OpenAI
from dotenv import load_dotenv
import os
from processing.process_LLM_output import process_LLM_output
from utils.logger import log_interaction


class LLM_GPT:
    """
    A class to interact with the GPT model using the OpenAI API.

    Attributes:
        model (str): The GPT model name to use (default is "gpt-4").
        client (OpenAI): The OpenAI client instance for interacting with the API.
    """

    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the LLM_GPT class.

        Args:
            model (str): The name of the GPT model to use.
            api_key (str): The OpenAI API key.
        """
        load_dotenv()
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize the OpenAI client with the provided API key

    def __modify_prompt__(self, prompt, initial_code):
        ollama_prompt = f"From the prompt:\n\n{prompt}\n\nI wrote:\n\n{initial_code}\n\nFix any errors, complete the code with imports, and wrap the function in triple backticks for clarity."
        return ollama_prompt

    def generate_code(self, prompts):
        """
        Generate responses for one or more prompts/questions using GPT.

        Args:
            prompts (str or list): A single prompt (str) or a list of prompts (list of str).

        Returns:
            list: A list of responses, one for each prompt.
        """
        if isinstance(prompts, str):
            prompts = [prompts]  # Convert a single prompt to a list

        responses = []
        for prompt in prompts:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                responses.append(response.choices[0].message.content.strip())
            except Exception as e:
                responses.append(f"Error: {e}")
        return responses

    def generate_and_log_code(self, prompt, task_id, initial_code):
        ollama_prompt = self.__modify_prompt__(prompt, initial_code)
        llm_output = self.generate_code(ollama_prompt)[0]
        code = process_LLM_output(llm_output, prompt)
        log_interaction("Ollama", task_id, ollama_prompt, llm_output)
        return code
