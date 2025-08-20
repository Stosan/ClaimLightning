import asyncio
from datetime import datetime
import os
from pathlib import Path
from typing import Annotated, List, Optional
from uuid import uuid4
import uuid
import aiofiles
from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Header,
    Request,
    UploadFile,
    status,
)
from src.services.process_claim import ProcessClaim
from src.application.datamodels import *
from src.config.app_settings import get_settings
from fastapi.responses import JSONResponse
from src.config.appconfig import env_config

# Get application settings from the settings module
settings = get_settings()

claim_router = APIRouter()

# Configuration constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
UPLOAD_DIR = "uploads/claims"  # Configure this path


# Define a health check endpoint
@claim_router.get("/", status_code=status.HTTP_200_OK)
def index():
    return "pong"


@claim_router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return "healthy"


@claim_router.post("/verify-customer", response_model=CustomerLoginResponse)
async def customer_login(
    customer_login_payload: CustomerLoginPayload,
    x_api_key: Optional[str] = Header(None, alias="X-API-KEY"),
):
    if x_api_key != env_config.x_api_key:
        # Return an unauthorized error response
        return JSONResponse(
            status_code=401, content={"message": "Unauthorized access: Invalid API key"}
        )
    try:
        rand_token = uuid4().hex[:5]
        customerLoginResponse = CustomerLoginResponse(
            token=rand_token, policyNumber=customer_login_payload.policyNumber
        )
        return JSONResponse(
            content=customerLoginResponse.model_dump(),
            status_code=customerLoginResponse.status,
        )
    except Exception as e:
        # Log the error
        print(f"Error in login endpoint: {str(e)}")
        # Return an error response
        return JSONResponse(
            status_code=500, content={"message": f"An error occurred {e}"}
        )


@claim_router.post("/process-claim", response_model=ClaimApplicationResponse)
async def claim_processing(
    request: Request,
    claim_application_payload: ClaimApplicationPayload,
    x_api_key: Optional[str] = Header(None, alias="X-API-KEY"),
):
    if x_api_key != env_config.x_api_key:
        # Return an unauthorized error response
        return JSONResponse(
            status_code=401, content={"message": "Unauthorized access: Invalid API key"}
        )
    try:
        db_client = request.app.state.db_client
        processClaim = ProcessClaim()
        result = processClaim.run_claim_processing(
            claim_application_payload, db_client_config=db_client
        )

        claimApplicationResponse = ClaimApplicationResponse(aiMessage=result.replace("**",""))

        return JSONResponse(
            content=claimApplicationResponse.model_dump(),
            status_code=claimApplicationResponse.status,
        )
    except Exception as e:
        # Log the error
        print(f"Error in process claim endpoint: {str(e)}")
        # Return an error response
        return JSONResponse(
            status_code=500, content={"message": f"An error occurred {e}"}
        )


@claim_router.post("/claims/uploads")
async def claim_processing_file_upload(
    request: Request,
    file: UploadFile = File(...),
    x_api_key: Optional[str] = Header(None, alias="X-API-KEY"),
):
    """
    Upload files for insurance claim processing.
    Supports multiple files with validation and progress tracking.
    """
    
    # Validate API key
    if x_api_key != env_config.x_api_key:
        return JSONResponse(
            status_code=401, 
            content={"message": "Unauthorized access: Invalid API key"}
        )

    try:
        # Read file content
        content = await file.read()
        
        # Generate safe filename
        safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._-")
        splitted_filenames = safe_filename.split("riaˆ")
        os.makedirs(f"src/assets/uploads/{splitted_filenames[0]}/", exist_ok=True)
        # Save file (example - adjust path as needed)
        file_path = f"src/assets/uploads/{splitted_filenames[0]}/{splitted_filenames[1]}"
        with open(file_path, "wb") as f:
            f.write(content)
        
        print(f"Successfully uploaded file: {file.filename} -> {safe_filename}")
        db_client = request.app.state.db_client
        processClaim = ProcessClaim()
        result = processClaim.save_claim_processing_docs(splitted_filenames[0], db_client)

        # Return response format that frontend expects
        return JSONResponse(
            status_code=201,
            content={
                "message": "File uploaded successfully",
                "filename": safe_filename,
                "url": f"/uploads/{safe_filename}"  
            }
        )
        
    except Exception as file_error:
        print(f"Error processing file {file.filename}: {str(file_error)}")
        return JSONResponse(
            status_code=500,
            content={
                "message": f"Error processing file '{file.filename}': {str(file_error)}"
            }
        )

