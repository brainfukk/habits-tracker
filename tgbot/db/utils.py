from tgbot.core.config import TABLES_PREFIX


def create_table_name(name: str) -> str:
    return "{}_{}".format(TABLES_PREFIX, name)


def create_table_reference(name: str, reference: str):
    return "{}.{}".format(create_table_name(name), reference)
