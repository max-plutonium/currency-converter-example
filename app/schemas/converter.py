from decimal import Decimal
from typing import Optional

from app.schemas import BaseSchema


class ConvertResult(BaseSchema):
    success: bool
    result: Optional[Decimal] = None
    error: Optional[str] = None
