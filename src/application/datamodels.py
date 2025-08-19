
from pydantic import BaseModel, Field

# Model for customer login payload
class CustomerLoginPayload(BaseModel):
    policyNumber: str  # Customer's policy number
    password: str      # Customer's password

# Model for customer login response
class CustomerLoginResponse(BaseModel):
    status: int = Field(default=200)  # HTTP status code
    token:str
    policyNumber: str
    message: str = Field(default="success!")  # Response message

# Model for claim application payload
class ClaimApplicationPayload(BaseModel):
    policyNumber: str  # Customer's policy number
    message: str       # Message or details about the claim

# Model for claim application response
class ClaimApplicationResponse(BaseModel):
    status: int = Field(default=200)  # HTTP status code
    aiMessage: str = Field(default="")  # AI-generated message or response
