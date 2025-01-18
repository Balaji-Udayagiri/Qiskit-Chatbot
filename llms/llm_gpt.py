from openai import OpenAI

from dotenv import load_dotenv
import os


class LLM_GPT:
    """
    A class to interact with the GPT model using the OpenAI API.

    Attributes:
        model (str): The GPT model name to use (default is "gpt-4").
        client (OpenAI): The OpenAI client instance for interacting with the API.
    """

    def __init__(self, model: str = "gpt-4", api_key: str = ""):
        """
        Initialize the LLM_GPT class.

        Args:
            model (str): The name of the GPT model to use.
            api_key (str): The OpenAI API key.
        """
        load_dotenv()
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Initialize the OpenAI client with the provided API key

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
