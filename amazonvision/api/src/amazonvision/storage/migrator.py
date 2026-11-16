"""Numbered SQL migrations tracked with PRAGMA user_version. Each file runs in one transaction."""

import logging
import re
import sqlite3
from pathlib import Path

log = logging.getLogger("amazonvision.storage")

MIGRATIONS_DIR = Path(__file__).with_name("migrations")
_FILENAME = re.compile(r"^(\d{3})_[a-z0-9_]+\.sql$")
# Trigger bodies use BEGIN ... END; only transaction control statements are forbidden.
_FORBIDDEN = re.compile(
    r"^\s*(BEGIN\s*(;|TRANSACTION\b|IMMEDIATE\b|DEFERRED\b|EXCLUSIVE\b)|COMMIT\b|ROLLBACK\b"
    r"|END\s+TRANSACTION\b)",
    re.IGNORECASE | re.MULTILINE,
)


class MigrationError(RuntimeError):
    pass


def discover(directory: Path = MIGRATIONS_DIR) -> list[tuple[int, Path]]:
    found: list[tuple[int, Path]] = []
    for path in sorted(directory.glob("*.sql")):
        match = _FILENAME.match(path.name)
        if not match:
            raise MigrationError(f"nome de migração inválido: {path.name}")
        found.append((int(match.group(1)), path))
    numbers = [n for n, _ in found]
    if numbers != list(range(1, len(numbers) + 1)):
        raise MigrationError(f"migrações devem ser contínuas a partir de 001: {numbers}")
    return found


def connect(db_path: Path | str) -> sqlite3.Connection:
    """Open the database in explicit-transaction mode with the project pragmas."""
    conn = sqlite3.connect(db_path, isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    if str(db_path) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def current_version(conn: sqlite3.Connection) -> int:
    return conn.execute("PRAGMA user_version").fetchone()[0]


def migrate(conn: sqlite3.Connection, directory: Path = MIGRATIONS_DIR) -> list[int]:
    """Apply pending migrations in order. Returns the numbers applied."""
    available = discover(directory)
    latest = available[-1][0] if available else 0
    version = current_version(conn)
    if version > latest:
        raise MigrationError(
            f"banco na versão {version}, mais nova que o código ({latest}); atualize o programa"
        )

    applied: list[int] = []
    for number, path in available:
        if number <= version:
            continue
        sql = path.read_text(encoding="utf-8")
        if _FORBIDDEN.search(sql):
            raise MigrationError(f"{path.name} não pode controlar transações")
        try:
            conn.executescript(f"BEGIN IMMEDIATE;\n{sql}\nPRAGMA user_version = {number};\nCOMMIT;")
        except sqlite3.Error as exc:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise MigrationError(f"falha em {path.name}: {exc}") from exc
        problems = conn.execute("PRAGMA foreign_key_check").fetchall()
        if problems:
            raise MigrationError(f"{path.name} deixou referências inválidas: {len(problems)}")
        log.info("migração %s aplicada", path.name)
        applied.append(number)
    return applied
