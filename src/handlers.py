from typing import get_args

from models import EmailRequest, EmailResponse, ToneTypes
from llm.llm_service import LLMService

system_prompt = f"""
Constraints:
- The input parameter key-values pairs must have value that relates to the key. Such as "Purpose: Leave Requested, Recipient: Boss, Tone: Professional". Reject if any of these don't match the key.
- Subject max length: 15 words
- Email shouldn't be lengthy, even if specified in the prompt. Max 100 words.
- Tone must be one of the following: {get_args(ToneTypes)}
- Response must follow the defined JSON Schema
"""

class Handlers():
    def __init__(self) -> None:
        self.llm = LLMService()

    async def generate_email(self, request: EmailRequest) -> EmailResponse:
        prompt = f"""
            You're a professional email writer. Based on the following parameters, draft email's subject, body and next actions.
            Purpose: {request.purpose}, Recipient: {request.recipient}, Tone: {request.tone}
        """
        response = await self.llm.write(prompt=prompt, system_prompt=system_prompt, response_schema=EmailResponse)
        return response
