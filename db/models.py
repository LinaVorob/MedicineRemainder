import uuid

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TEXT, INTEGER, BIT
from sqlalchemy import Column, ForeignKey, CheckConstraint

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(UUID, primary_key=True, default=uuid.uuid4, autoincrement=False)
    category_name = Column(VARCHAR(30), nullable=False)
    medicines = relationship("Medicine", back_populates='type_obj')


class Medicine(Base):
    __tablename__ = 'medicines'
    medicine_id = Column(UUID, primary_key=True, default=uuid.uuid4, autoincrement=False)
    medicine_type = Column(UUID, ForeignKey('types.type_id', ondelete='CASCADE'), nullable=True)
    medicine_name = Column(VARCHAR(30), nullable=False, unique=True)
    description = Column(TEXT, nullable=True)
    image_medicine = Column(VARCHAR(200), nullable=True)
    intake_info = Column(TEXT, nullable=True)
    type_obj = relationship("Category", back_populates='medicines')


class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID, primary_key=True, default=uuid.uuid4, autoincrement=False)
    user_id_telegram = Column(INTEGER, nullable=False, unique=True)
    is_admin = Column(BIT, nullable=False, default=0)
    CheckConstraint("user_id_telegram > Field(ge=1000)", name="check_telegram_id")


class Intake(Base):
    __tablename__ = 'users_medicines'
    pair_id = Column(UUID, primary_key=True, default=uuid.uuid4, autoincrement=False)
    user_id = Column(UUID, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    medicine_id = Column(UUID, ForeignKey('medicines.medicine_id', ondelete='CASCADE'), nullable=False)
    time_of_intake = Column(VARCHAR(8), nullable=False, default="00 00 00")
    step_of_intake = Column(VARCHAR(14), nullable=False, default="00 00 00 00 00")
    period_of_intake = Column(VARCHAR(14), nullable=False, default="00 00 00 00 00")
    count_doze = Column(INTEGER, nullable=False, default=0)


