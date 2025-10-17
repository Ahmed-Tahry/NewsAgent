import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import ROUTER_MODEL_PATH

class ChatTool:
    def __init__(self):
        """
        Initializes the Casual Chat Tool with the Gemma-270m model.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(ROUTER_MODEL_PATH)
            self.model = AutoModelForCausalLM.from_pretrained(
                ROUTER_MODEL_PATH,
                torch_dtype=torch.bfloat16
            )
            print("Chat model (Gemma-270m) loaded successfully.")
        except Exception as e:
            print(f"Error loading chat model: {e}")
            self.model = None
            self.tokenizer = None

    def run(self, user_input: str, history: list) -> str:
        """
        Runs the casual chat model.

        Args:
            user_input (str): The latest message from the user.
            history (list): The conversation history.

        Returns:
            str: The model's response.
        """
        if not self.model or not self.tokenizer:
            return "The chat model is not available."

        # Format the conversation history for the model
        prompt = ""
        for msg in history:
            if msg.type == "human":
                prompt += f"user: {msg.content}\n"
            elif msg.type == "ai":
                prompt += f"assistant: {msg.content}\n"
        
        prompt += f"user: {user_input}\nassistant:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=100, pad_token_id=self.tokenizer.eos_token_id)
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the last assistant message
        last_response = response.split("assistant:")[-1].strip()
        
        return last_response
