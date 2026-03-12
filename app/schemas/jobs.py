from typing import Literal, Optional
from pydantic import BaseModel, Field


class ParsedJob(BaseModel):
    client_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    job_description: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=None)
    currency: Optional[Literal["RSD", "EUR"]] = Field(default=None)
    address: Optional[str] = Field(default=None)