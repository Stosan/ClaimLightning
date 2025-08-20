from pathlib import Path
from openai import OpenAI
from src.ai_model.memory_context import retrieve_memory_with_k
from src.config.appconfig import env_config
from src.utilities.prompt_loader import load_yaml_file
from src.infrastructure.database.mongo import MongoDBClientConfig

base_url = "https://api.aimlapi.com/v1"

api = OpenAI(api_key=env_config.aimlapi_key, base_url=base_url)

def make_llm_call(messages:list,model:str= "openai/gpt-5-chat-latest")->str:

    completion = api.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
        max_tokens=2048,
    )

    response = completion.choices[0].message.content
    return response
