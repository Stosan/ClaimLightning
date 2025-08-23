# Import necessary modules

import os, secrets, uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from src.infrastructure.database.mongo import MongoDBClientConfig
from src.config.app_settings import Settings, get_settings
from contextlib import asynccontextmanager
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from src.utilities.Printer import printer
from src.config.appconfig import env_config
from src.application.api_route import claim_router

# Get application settings from the settings module
settings = get_settings()

# Description for API documentation
description = f"""
{settings.API_V1_STR} helps you do awesome stuff. 🚀
"""

# Define a context manager for the application lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for application lifespan.
    This function initializes and cleans up resources during the application's lifecycle.
    """
    # STARTUP Call Check routine
    mongo_client = MongoDBClientConfig()
    app.state.db_client = mongo_client
    print(running_mode)
    print()
    print()
    printer(" ⚡️🚀 Reinsurance AI Server::Started", "sky_blue")
    print()
    printer(" ⚡️🏎  Reinsurance AI Server::Running", "sky_blue")
    yield
    printer(" 🔴 Reinsurance AI Server::SHUTDOWN", "red")

# Adjust dependency to use warmed db_client
def get_db_client(settings: Settings = Depends(get_settings)):
    return app.state.db_client

# Create FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description=description,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    contact={
        "name": "Sam Ayo",
        "url": "https://www.linkedin.com/in/sam-ayo/",
        "email": "samkehindeayo@gmail.com",
    },
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


templates = Jinja2Templates(directory="src/templates")

# Configure for development or production mode
if env_config.env in ["development", "staging"]:
    running_mode = f"  👩‍💻 🛠️  Running in::{env_config.env} mode"
else:
    # app.add_middleware(HTTPSRedirectMiddleware)
    running_mode = "  🏭 ☁  Running in::production mode"

# Define allowed origins for CORS
origins = [
    "*",
]

# Instantiate basicAuth
security = HTTPBasic()

# Add middleware to allow CORS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request,):
    return templates.TemplateResponse(request=request,name="index.html",context={})

@app.get("/claim-application", response_class=HTMLResponse)
async def claim_application(request: Request,):
    return templates.TemplateResponse(request=request,name="claim.html",context={})

@app.get("/claim-admin-backend", response_class=HTMLResponse)
async def claim_backend_application(request: Request,):
    return templates.TemplateResponse(request=request,name="admin.html",context={})

app.include_router(claim_router,prefix=settings.API_V1_STR,  
                   tags=["AUTH"],dependencies=[  Depends(get_db_client),Depends(get_settings),],)


if __name__ == "__main__":
    # Retrieve environment variables for host, port, and timeout
    timeout_keep_alive = int(os.getenv("TIMEOUT", 6000))

    # Run the application with the specified host, port, and timeout
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(env_config.port),
        timeout_keep_alive=timeout_keep_alive,
    )
