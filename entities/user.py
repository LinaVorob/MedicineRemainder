from pydantic import BaseModel, Field


class UserType(BaseModel):
    tg_id: int
    admin: bool = False


