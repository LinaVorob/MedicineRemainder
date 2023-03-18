from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from config import config
from db.models import Base, User, Medicine, Intake, Category
from entities import MedicineType, CategoryType, UserType, IntakeType


@dataclass
class DatabaseSettings:
    db_name: str = config.db.database
    host: str = config.db.host
    user: str = config.db.user
    password: str = config.db.password
    dialect: str = 'postgresql'
    driver: str = 'psycopg2'

    def __init__(self):
        self._check_db_exists()
        self._check_tables_exist()

    def get_db_url(self):
        return f'{self.dialect}://{self.user}:{self.password}@{self.host}/{self.db_name}'

    def _check_db_exists(self):
        """Проверяет, есть ли БД. Создает, если нет."""
        engine = create_engine(self.get_db_url())
        if not database_exists(engine.url):
            create_database(engine.url)
            Base.metadata.create_all(engine)
        engine.dispose()

    def _check_tables_exist(self):
        """Проверяет, есть ли в БД таблицы. Создает, если нет."""
        engine = create_engine(self.get_db_url())
        execute_string = 'SELECT * FROM pg_catalog.pg_tables;'
        with engine.connect() as con:
            tbs = con.execute(text(execute_string))
        if not tbs:
            Base.metadata.create_all(engine)
        engine.dispose()


class Database:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.db = DatabaseSettings()
        self.url = self.db.get_db_url()

    def _check_data_exists(self, obj, param, value_check):
        engine = create_engine(self.url)
        try:
            with Session(bind=engine) as session:
                answer_query = session.query(obj).filter(getattr(obj, param) == value_check).all()
                if answer_query:
                    return True
                else:
                    return False
        finally:
            engine.dispose()

    def _add_data(self, obj):
        engine = create_engine(self.url)
        try:
            with Session(bind=engine) as session:
                session.add(obj)
                session.commit()
        finally:
            engine.dispose()

    def add_new_user(self, user: UserType):
        obj_user = User(
            user_id_telegram=user.tg_id,
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

    def check_user(self, param, value_check):
        return self._check_data_exists(User, param, value_check)

    def check_medicine(self, param, value_check):
        return self._check_data_exists(Medicine, param, value_check)

    def check_intake(self, param, value_check):
        return self._check_data_exists(Intake, param, value_check)

    def get_categories(self):
        engine = create_engine(self.url)
        try:
            with Session(engine) as session:
                query = session.query(Category.category_name, Category.category_id).all()
            return query
        finally:
            engine.dispose()
