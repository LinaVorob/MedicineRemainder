from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from config import config
from db.models import Base, User, Medicine, Intake
from entities.medicine import MedicineType
from entities.user import UserType
from entities.category import CategoryType
from entities.intake import IntakeType


class Database:
    db_name: str = config.db.database
    host: str = config.db.host
    user: str = config.db.user
    password: str = config.db.password
    dialect: str = 'postgresql'
    driver: str = 'psycopg2'

    def get_db_url(self):
        return f'{self.dialect}+{self.dialect}://{self.user}:{self.password}\@{self.host}/{self.db_name}'

    def _check_exists(self):
        """Проверяет, есть ли БД. Создает, если нет."""
        engine = create_engine(self.get_db_url())
        if not database_exists(engine.url):
            create_database(engine.url)
            Base.metadata.create_all(engine)
        engine.dispose()

    def _add_data(self, obj):
        engine = create_engine(self.get_db_url())
        try:
            with Session() as session:
                session.add(obj)
                session.commit()
        finally:
            engine.dispose()

    def add_new_user(self, user: UserType):
        obj_user = User(
            user_id=user.tg_id,
            is_admin=user.admin)
        self._add_data(obj_user)

    def add_new_medicine(self, medicine: MedicineType):
        obj_medicine = Medicine(**medicine)
        self._add_data(obj_medicine)

    def add_new_category(self, category: CategoryType):
        obj_category = Medicine(**category)
        self._add_data(obj_category)

    def add_intake(self, intake: IntakeType):
        ...





