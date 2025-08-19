
from src.infrastructure.database.mongo import MongoDBClientConfig
from src.domain.conversation_manager import ConversationManager
from src.application.datamodels import ClaimApplicationPayload


class ProcessClaim():
    def run_claim_processing(self,user_input:ClaimApplicationPayload,document_uploaded:bool=False,db_client_config:MongoDBClientConfig=MongoDBClientConfig):
        if user_input != "":
            conversationManager = ConversationManager(user_input.message,user_input.policyNumber,db_client_config)
            return conversationManager.llm_call()

