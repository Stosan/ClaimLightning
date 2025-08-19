
from src.ai_model.aimlapi import llm_call
from src.application.datamodels import ClaimApplicationPayload


class ProcessClaim():
    def run_claim_processing(self,user_input:ClaimApplicationPayload,document_uploaded:bool):
        if user_input != "":
            return llm_call(user_input)

