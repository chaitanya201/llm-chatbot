from contextlib import contextmanager
from collections.abc import Iterator

from langgraph.checkpoint.postgres import PostgresSaver

from config import settings


@contextmanager
def postgres_checkpointer() -> Iterator[PostgresSaver]:
    with PostgresSaver.from_conn_string(settings.settings.DATABASE_URL) as checkpointer:
        checkpointer.setup()
        yield checkpointer