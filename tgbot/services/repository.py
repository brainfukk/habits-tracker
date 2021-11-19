from typing import Any, Dict, List, NoReturn, Optional, Type, Union

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from tgbot.db.models import (
    BaseModel,
    TelegramUser,
    Habit,
    Event
)


class BaseRepo:
    """
    Database abstraction layer
    """

    model: Type[BaseModel]

    def __init__(self, session: Session) -> None:
        self.session = session

    def get(
        self, default: Optional[str] = None, **kwargs
    ) -> Union[BaseModel, NoReturn]:
        """
        Get row from table or raise exception

        :param default: Specific field for lookup
        :param kwargs: Arguments for search
        :return: self.model type object
        """
        check_args = kwargs
        if default is not None:
            check_args = {default: kwargs[default]}
        return self.session.query(self.model).filter_by(**check_args).one()

    def filter(self, kwargs) -> List[BaseModel]:
        """
        Filter data
        :param kwargs: filter expressions
        :return: Filtered data
        """
        expression = self.session.query(self.model)
        for item in kwargs:
            expression = getattr(expression, "filter")(item)

        return expression.all()

    def create(self, instance: Optional[BaseModel] = None, **kwargs) -> BaseModel:
        """
        Create instance in the table

        :param instance: Instance of self.model type
        :param kwargs: Arguments for create instance
        :return: self.model type object
        """
        if instance is None:
            instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, instance: BaseModel, values: Dict[str, Any]) -> BaseModel:
        """
        Update instance in the table

        :param instance: Instance of self.model type
        :param values: Arguments for update instance
        :return: self.model type object
        """
        for key, item in values.items():
            setattr(instance, key, item)
        self.session.commit()
        return instance

    def list(self) -> List[BaseModel]:
        """
        Get all list of instances from table

        :return: List of table records
        """
        return self.session.query(self.model).all()

    def get_or_create(self, default: Optional[str] = None, **kwargs) -> BaseModel:
        """
        Get or create instance from/in table

        :param default: Specific lookup field
        :param kwargs: Arguments for create instance
        :return: self.model type object
        """
        try:
            instance = self.get(default=default, **kwargs)
        except NoResultFound:
            instance = self.create(**kwargs)
        return instance

    def update_or_create(
        self,
        instance: Optional[BaseModel] = None,
        default: Optional[str] = None,
        **kwargs
    ) -> BaseModel:
        """
        Update or create record in/to table

        :param default: Specific lookup field
        :param instance: self.model type object
        :param kwargs: Values for create or update
        :return: self.model type object
        """
        if instance is None:
            instance = self.get(default=default, **kwargs)

        if instance is None:
            instance = self.create(**kwargs)
            return instance
        return self.update(instance=instance, values=kwargs)

    def delete(self, **kwargs):
        self.session.query(self.model).filter_by(**kwargs).delete()
        self.session.commit()

    def truncate(self) -> None:
        """Delete all data from table"""
        self.session.query(self.model).delete()
        self.session.commit()


class TelegramUserRepo(BaseRepo):
    model = TelegramUser

    def get_habits(self, instance):
        return instance.habits

    def get_events(self, instance):
        results = {}
        habits = self.get_habits(instance)

        for habit in habits:
            results[habit] = habit.events
        return results


class HabitRepo(BaseRepo):
    model = Habit

    def get_events(self, instance):
        return instance.events.all()


class EventRepo(BaseRepo):
    model = Event

    def is_today_events_completed(self, user):
        events = self.session.query(self.model).join(
            self.model.habit, aliased=True
        ).filter_by(
            user_telegram_id=user.telegram_id
        ).all()
        for event in events:
            if not event.is_completed:
                return False
        return True

    def complete_event(self, instance):
        instance.is_completed = True
        self.session.commit()
        return instance
