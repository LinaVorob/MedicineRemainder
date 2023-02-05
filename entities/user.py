from pydantic import BaseModel, Field, root_validator

from config import config


class UserType(BaseModel):
    admin: bool = False
    tg_id: int = Field(alias='id')

    @root_validator
    def is_admin(cls, values):
        if values['tg_id'] == int(config.tgbot.admin_id):
            values['admin'] = True
        return values


