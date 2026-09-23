import os
import logging
from typing import TypeVar, Type
import json

from pydantic import BaseModel, ValidationError
from google import genai
from google.genai import types
from json_repair import repair_json

TResponse = TypeVar("TResponse", bound=BaseModel)

class LLMService():
    def __init__(self) -> None:
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY")).aio

    async def write(self, *, prompt: str, system_prompt: str, response_schema: Type[TResponse]) -> TResponse:
        response = await self.client.models.generate_content(
            model=self.model,
            contents=prompt.strip(),
            config=types.GenerateContentConfig(
                system_instruction=system_prompt.strip(),
                response_json_schema=response_schema.model_json_schema(),
                response_mime_type="application/json"
            )
        )
        return self._structure_response(response_text=response.text or "", response_schema=response_schema)

    def _structure_response(self, response_text: str, response_schema: Type[TResponse], repair: bool = True) -> TResponse:
        try:
            return response_schema.model_validate_json(response_text)
        except (json.JSONDecodeError, ValidationError) as e:
            try:
                if repair == False:
                    raise e
                repaired = repair_json(response_text)
                return self._structure_response(repaired, response_schema, False)
            except (json.JSONDecodeError, ValidationError) as repair_error:
                if repair == False:
                    raise e
                
                logging.critical(f"[Critical] Auto-repair also failed: {repair_error}")
                raise ValueError(
                    f"Failed to structure Gemini response into {response_schema.__name__}.\n"
                    f"Raw response was: {response_text}"
                ) from repair_error
