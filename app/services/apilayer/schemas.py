from decimal import Decimal
from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel


class ErrorDescr(BaseModel):
    code: int
    type_: str = Field(alias='type')
    info: str


class ConvertResp(BaseModel):
    success: bool
    result: Optional[Decimal] = None
    error: Optional[ErrorDescr] = None
