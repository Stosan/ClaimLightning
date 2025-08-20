from pathlib import Path
from src.ai_model.aimlapi import make_llm_call
from src.ai_model.memory_context import create_memory, retrieve_memory_with_k
from src.utilities.prompt_loader import load_yaml_file
from src.infrastructure.database.mongo import MongoDBClientConfig


class ConversationManager:
    def __init__(self,query:str,policy_number:str,policy_data="",db_client_config:MongoDBClientConfig=MongoDBClientConfig):
        self.query=query
        self.policy_number=policy_number
        self.db_client_config=db_client_config
        self.policy_data=policy_data
        self.chat_history_from_memory=retrieve_memory_with_k(self.db_client_config.get_context_collection(), policy_number,k=3)
        self.prompt_template = self.load_prompt_template()

    def load_prompt_template(self) -> str:
        """Load the instruction prompt template from YAML file."""
        try:
            prompt_path = Path(
                "src/domain/policyintelligencemodule/systemprompt.yaml"
            )
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt template not found at {prompt_path}")
            yaml_data = load_yaml_file(prompt_path)
            return {
                "LLMSYSTEMPROMPT": yaml_data.get("SYSTEMPROMPT", ""),
                       "LLMUSERPROMPT": yaml_data.get("USERPROMPT", ""),
            }
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt template: {str(e)}")


    def llm_call(self)->str:
        response = ""
        try:
            system_prompt = self.load_prompt_template().get("LLMSYSTEMPROMPT")
            if system_prompt is None:
                raise ValueError("Instruction prompt could not be loaded.")
            system_prompt = system_prompt.format(chat_history=self.chat_history_from_memory)

            user_prompt = self.load_prompt_template().get("LLMUSERPROMPT")
            if user_prompt is None:
                raise ValueError("user prompt could not be loaded.")
            
            user_prompt = user_prompt.format(query=self.query, policy_number=self.policy_number,policy_data=self.policy_data if self.policy_data != "" else "")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            try:
                response = make_llm_call(messages)
                create_memory(self.db_client_config.get_context_collection(),self.policy_number,self.query, response)
            except Exception as e:
                print(f"Error during LLM call: {str(e)}")
                raise
            return response
        except Exception as e:
            print(f"Error during LLM call: {str(e)}")
            raise
