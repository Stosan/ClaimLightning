

from typing import Optional
from pydantic import BaseModel


class UserPolicyInformation(BaseModel):
    policy_number: str
    policy_holder_name: str
    policy_start_date: str
    policy_end_date: str
    premium_amount: float
    coverage_details: str
    policy_type: Optional[str] = None
    beneficiary_name: Optional[str] = None
    contact_information: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    vehicle_vin: Optional[str] = None

def generate_fake_policy_information(policy_number: str) -> UserPolicyInformation:
    # Create a dummy UserPolicyInformation instance
    fake_policy_info = UserPolicyInformation(
        policy_number=policy_number,
        policy_holder_name="Sam Ayo",
        policy_start_date="2025-01-01",
        policy_end_date="2026-01-01",
        premium_amount=1200.50,
        coverage_details="Comprehensive coverage including health, accident, and theft.",
        policy_type="General Insurance",
        beneficiary_name="Jane Ayo",
        contact_information="sam.ayo@gmail.com",
        vehicle_make="Toyota",
        vehicle_model="Camry",
        vehicle_year=2020,
        vehicle_vin="1HGCM82633A123456"
    )
    return fake_policy_info.model_dump()