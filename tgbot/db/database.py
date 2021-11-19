import json
import logging
from contextlib import contextmanager

from sqlalchemy import TEXT, TypeDecorator, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import sessionmaker

from tgbot.core.config import DATABASE_URL

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


class JSONEncodedDict(TypeDecorator):  # noqa
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is None:
            return None

        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)


JsonField = MutableDict.as_mutable(JSONEncodedDict)
ListField = MutableList.as_mutable(JSONEncodedDict)


@contextmanager
def session_scope():
    Base.metadata.create_all(engine)
    current_session = _SessionFactory()
    try:
        yield current_session
        current_session.commit()
    except Exception as e:
        logger.error(e)
        current_session.rollback()
    finally:
        current_session.close()