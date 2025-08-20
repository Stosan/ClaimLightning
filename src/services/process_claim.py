
from src.ai_model.memory_context import create_memory
from src.infrastructure.schema import generate_fake_policy_information
from src.infrastructure.database.mongo import MongoDBClientConfig
from src.domain.policyintelligencemodule.conversationmanager import ConversationManager
from src.application.datamodels import ClaimApplicationPayload

from pydantic import BaseModel
from typing import Optional




class ProcessClaim():

    def get_policy_information(self,policy_number:str):
        return generate_fake_policy_information(policy_number)
    
    def save_claim_processing_docs(self,policy_number:str,db_client_config:MongoDBClientConfig=MongoDBClientConfig)->bool:
        try:
            create_memory(db_client_config.get_context_collection(),policy_number,"I have just successfully uploaded a document", "Alright! Document has been recieved, time to proceed to next step.")
        except Exception as e:
            print(f"Error during claim processing file saving: {str(e)}")
            raise

    def run_claim_processing(self,user_input:ClaimApplicationPayload,db_client_config:MongoDBClientConfig=MongoDBClientConfig):
        try:
            if user_input != "":
                policy_data = ""
                print("user_input >>> ", user_input)
                if user_input.message == "I want to make a claim":
                    policy_data = self.get_policy_information(user_input.policyNumber)
                conversationManager = ConversationManager(user_input.message, user_input.policyNumber, policy_data, db_client_config)
                return conversationManager.llm_call()
        except Exception as e:
            print(f"Error during claim processing: {str(e)}")
            raise

