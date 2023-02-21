import uuid
from enum import Enum

from pydantic import BaseModel, Field, root_validator

from config import config


class MedicineType(BaseModel):
    name: str
    category: str = None
    description: str = None
    intake_info: str = None