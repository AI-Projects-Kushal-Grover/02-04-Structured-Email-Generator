from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ToneTypes = Literal["Formal", "Casual", "Empathetic", "Urgent", "Humorous"]

class EmailRequest(BaseModel):
    model_config=ConfigDict(extra="forbid")
    purpose: str = Field()
    recipient: str = Field()
    tone: ToneTypes = Field()

class EmailResponse(BaseModel):
    model_config=ConfigDict(extra="forbid")
    subject: str = Field()
    body: str = Field()
    suggested_actions: list[str] = Field()
