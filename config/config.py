import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    database: str
    user: str
    password: str
    host: str


@dataclass
class TgConfig:
    token: str
    admin_id: int


@dataclass
class Config:
    tgbot: TgConfig
    db: DatabaseConfig


load_dotenv()

config = Config(
    tgbot=TgConfig(
        token=os.getenv("TOKEN"),
        admin_id=int(os.getenv('ADMIN'))),
    db=DatabaseConfig(
        database=os.getenv('DATABASE'),
        user=os.getenv('LOGIN'),
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST')
    )
)
