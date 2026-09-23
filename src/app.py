from pathlib import Path
import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from handlers import Handlers
from models import EmailRequest, EmailResponse

# Load environment variables from .env file
env_file = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_file)

app = FastAPI(title="AI Email Generator", version="0.1.0")
handlers = Handlers()

@app.post("/generate_email")
async def generate_email(request: EmailRequest) -> EmailResponse:
    try:
        logging.info("Received request for email generation")
        return await handlers.generate_email(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
