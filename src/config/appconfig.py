# Load .env file using:
from dotenv import load_dotenv
load_dotenv(override=True)
import os

class EnvConfig:
    """Class to hold environment configuration variables."""
    
    def __init__(self):
        self.env = os.getenv("ENVIRONMENT")
        self.app_port = os.getenv("PORT")
        self.x_api_key = os.getenv("X-API-KEY")
        self.aimlapi_key = os.getenv("AIMLAPI-KEY")
        
    def __repr__(self):
        return (
            f"EnvConfig(env={self.env}, app_port={self.app_port}, "
        )

# Create an instance of EnvConfig to access the environment variables
env_config = EnvConfig()