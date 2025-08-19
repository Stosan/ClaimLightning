from pathlib import Path
from openai import OpenAI
from src.config.appconfig import env_config
from src.utilities.prompt_loader import load_yaml_file


base_url = "https://api.aimlapi.com/v1"
user_prompt = "Tell me about San Francisco"

api = OpenAI(api_key=env_config.aimlapi_key, base_url=base_url)

class ConversationManager:
    def __init__(
        self, conversation_store: InMemoryConversationStore = conversation_store
    ):
        self.conversation_store = conversation_store
        self.prompt_template = self.load_prompt_template()

    def load_prompt_template(self) -> str:
        """Load the instruction prompt template from YAML file."""
        try:
            prompt_path = Path(
                "src/ai_model/systemprompt.yaml"
            )
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt template not found at {prompt_path}")
            yaml_data = load_yaml_file(prompt_path)
            return {
                "LLMSYSTEMPROMPT": yaml_data.get("SYSTEMPROMPT", ""),
            }
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt template: {str(e)}")


    def llm_call(self,query:str,policy_number:str,model:str= "gpt-5"):
        system_prompt = self.load_prompt_template().get("LLMSYSTEMPROMPT")
        if system_prompt is None:
            raise ValueError("Instruction prompt could not be loaded.")
        
        user_prompt=user_prompt.format_map(query=query,policy_number=policy_number)
        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        print(messages)
        completion = api.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.4,
            max_tokens=256,
        )

        response = completion.choices[0].message.content
        print("AI:", response)
        return response
