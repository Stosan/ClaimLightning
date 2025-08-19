import asyncio
from typing import Optional
from fastapi import APIRouter, Header, status
from src.application.datamodels import *
from src.config.app_settings import get_setting
from fastapi.responses import JSONResponse
from src.config.appconfig import env_config

# Get application settings from the settings module
settings = get_setting()

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
    if x_api_key != env_config.x_api_key.lower:
        # Return an unauthorized error response
        return JSONResponse(status_code=401, content={"message": "Unauthorized access: Invalid API key"})
    try:
        customerLoginResponse = CustomerLoginResponse()
        return JSONResponse(content=customerLoginResponse.model_dump(),status_code=customerLoginResponse.status)
    except Exception as e:
        # Log the error
        print(f"Error in login endpoint: {str(e)}")
        # Return an error response
        return JSONResponse(status_code=500, content={"message": f"An error occurred {e}"})

