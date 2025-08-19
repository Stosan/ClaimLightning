import asyncio
from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Header, status
from src.ai_model.aimlapi import ConversationManager
from src.application.datamodels import *
from src.config.app_settings import get_settings
from fastapi.responses import JSONResponse
from src.config.appconfig import env_config

# Get application settings from the settings module
settings = get_settings()

claim_router = APIRouter()

# Define a health check endpoint
@claim_router.get("/", status_code=status.HTTP_200_OK)
def index():
    return "pong"


@claim_router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return "healthy"

@claim_router.post("/verify-customer",response_model=CustomerLoginResponse)
async def customer_login(customer_login_payload: CustomerLoginPayload, x_api_key: Optional[str] = Header(None, alias="X-API-KEY")):
    if x_api_key != env_config.x_api_key:
        # Return an unauthorized error response
        return JSONResponse(status_code=401, content={"message": "Unauthorized access: Invalid API key"})
    try:
        rand_token = uuid4().hex[:5]
        customerLoginResponse = CustomerLoginResponse(token=rand_token,policyNumber=customer_login_payload.policyNumber)
        return JSONResponse(content=customerLoginResponse.model_dump(),status_code=customerLoginResponse.status)
    except Exception as e:
        # Log the error
        print(f"Error in login endpoint: {str(e)}")
        # Return an error response
        return JSONResponse(status_code=500, content={"message": f"An error occurred {e}"})


@claim_router.post("/process-claim",response_model=ClaimApplicationResponse)
async def claim_processing(claim_application_payload: ClaimApplicationPayload, x_api_key: Optional[str] = Header(None, alias="X-API-KEY")):
    if x_api_key != env_config.x_api_key:
        # Return an unauthorized error response
        return JSONResponse(status_code=401, content={"message": "Unauthorized access: Invalid API key"})
    try:
        print(claim_application_payload)
        conversationManager = ConversationManager()
        conversationManager.llm_call(claim_application_payload.message,claim_application_payload.policyNumber)
        claimApplicationResponse = ClaimApplicationResponse()
        return JSONResponse(content=claimApplicationResponse.model_dump(),status_code=claimApplicationResponse.status)
    except Exception as e:
        # Log the error
        print(f"Error in process claim endpoint: {str(e)}")
        # Return an error response
        return JSONResponse(status_code=500, content={"message": f"An error occurred {e}"})