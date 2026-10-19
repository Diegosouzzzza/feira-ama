"""Single SQLite connection served by one dedicated thread: every read and write is serialized
there, so the event loop never blocks and there is exactly one writer."""

import asyncio
import logging
import sqlite3
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path

from amazonvision.schemas.errors import ApiError, ErrorCode
from amazonvision.storage.migrator import connect, migrate

log = logging.getLogger("amazonvision.storage")


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    conn.execute("COMMIT")


class Database:
    def __init__(self, path: Path | str) -> None:
        self.path = path
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="av-db")
        self._conn: sqlite3.Connection | None = None
        # Sticky until restart: a storage failure must keep blocking new cycles.
        self.healthy = True
        self.last_error: str | None = None

    def _open(self) -> None:
        self._conn = connect(self.path)
        applied = migrate(self._conn)
        if applied:
            log.info("banco em %s migrado: %s", self.path, applied)

    async def open(self) -> None:
        await asyncio.get_running_loop().run_in_executor(self._executor, self._open)

    async def run[T](self, fn: Callable[[sqlite3.Connection], T]) -> T:
        """Run fn(conn) on the database thread. Storage failures become STORAGE_ERROR."""
        if self._conn is None:
            raise RuntimeError("banco não aberto")
        conn = self._conn
        try:
            result = await asyncio.get_running_loop().run_in_executor(self._executor, fn, conn)
        except sqlite3.IntegrityError:
            raise
        except sqlite3.Error as exc:
            self.healthy = False
            self.last_error = str(exc)
            log.exception("falha no banco de dados")
            raise ApiError(
                ErrorCode.STORAGE_ERROR,
                "Falha ao gravar ou ler o banco de dados.",
                "Verifique o espaço em disco e reinicie o sistema.",
            ) from exc
        return result

    async def close(self) -> None:
        if self._conn is not None:
            conn, self._conn = self._conn, None
            await asyncio.get_running_loop().run_in_executor(self._executor, conn.close)
        self._executor.shutdown(wait=True)
