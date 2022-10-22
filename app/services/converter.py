from abc import ABC, abstractmethod
from decimal import Decimal

from app.schemas.converter import ConvertResult


class ConverterService(ABC):
    name: str

    @abstractmethod
    async def convert(self, from_: str, dest: str, value: Decimal) -> ConvertResult:
        ...
