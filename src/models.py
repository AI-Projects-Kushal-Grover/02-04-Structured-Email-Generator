from typing import Literal

from pydantic import BaseModel, Field

ToneTypes = Literal["Formal", "Casual", "Empathetic", "Urgent", "Humorous"]

class EmailRequest(BaseModel):
    purpose: str = Field()
    recipient: str = Field()
    tone: ToneTypes = Field()

class EmailResponse(BaseModel):
    subject: str = Field()
    body: str = Field()
    suggested_actions: list[str] = Field()
