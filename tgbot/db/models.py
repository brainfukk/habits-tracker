from datetime import datetime

from sqlalchemy import DateTime, Column, Boolean, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base
from .utils import create_table_name, create_table_reference

UNKNOWN = "Unknown"
USER_TG_ID_FIELD_REFERENCE = create_table_reference("telegram_user", "telegram_id")
HABIT_ID_REFERENCE = create_table_reference("habits", "id")


def updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()


class BaseModel(Base):
    __abstract__ = True

    __created_at_name__ = "created_at"
    __updated_at_name__ = "updated_at"
    __datetime_func__ = datetime.utcnow

    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        __created_at_name__,
        DateTime,
        default=__datetime_func__,
        nullable=False,
    )
    updated_at = Column(
        __updated_at_name__,
        DateTime,
        default=__datetime_func__,
        onupdate=__datetime_func__,
        nullable=False,
    )

    def __repr__(self):
        columns = [col for col in self.__dict__.keys() if not col.startswith("_")]
        values_dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

        repr_string = "<{}({})>"
        attrs_string = ""

        for col_name in columns:
            attrs_string += "{}=".format(col_name) + "{" + col_name + "}, "
        attrs_string = attrs_string.format(**values_dict)
        return repr_string.format(self.__class__.__name__, attrs_string)


class TelegramUser(BaseModel):
    __tablename__ = create_table_name("telegram_user")

    telegram_id = Column(Integer, unique=True)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    user_nickname = Column(String(length=255), unique=True, index=True)

    @property
    def full_name(self):
        f_name = self.first_name if self.first_name else ""
        l_name = self.last_name if self.last_name else ""
        return "{} {}".format(f_name.strip(), l_name.strip()).strip()


class Habit(BaseModel):
    __tablename__ = create_table_name("habits")

    user_telegram_id = Column(Integer, ForeignKey(USER_TG_ID_FIELD_REFERENCE))
    name = Column(String(length=255))

    user = relationship("TelegramUser", backref="habits")


class Event(BaseModel):
    __tablename__ = create_table_name("events")

    habit_id = Column(Integer, ForeignKey(HABIT_ID_REFERENCE))
    content = Column(String(length=500))
    duration = Column(Float, default=0)
    is_completed = Column(Boolean, default=False)

    habit = relationship("Habit", backref="events")
