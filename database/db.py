from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from uuid import uuid4

import mysql.connector
from mysql.connector import Error

from config.settings import DatabaseSettings


class DatabaseError(Exception):
    """Raised for database connection or query failures."""


@dataclass(frozen=True)
class HistoryToken:
    token: str
    token_id: int
    embedding: list[float]
    embedding_dimension: int


@dataclass(frozen=True)
class HistoryEntry:
    input_word: str
    created_at: str
    tokens: list[HistoryToken]


class Database:
    def __init__(self, settings: DatabaseSettings) -> None:
        self.settings = settings

    def _server_connection(self):
        return mysql.connector.connect(
            host=self.settings.host,
            port=self.settings.port,
            user=self.settings.user,
            password=self.settings.password,
        )

    def _database_connection(self):
        return mysql.connector.connect(
            host=self.settings.host,
            port=self.settings.port,
            user=self.settings.user,
            password=self.settings.password,
            database=self.settings.database,
        )

    def initialize(self) -> None:
        try:
            with self._server_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"CREATE DATABASE IF NOT EXISTS `{self.settings.database}`"
                    )
                conn.commit()

            with self._database_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            email VARCHAR(255) NOT NULL UNIQUE,
                            password_hash VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS tokenization_history (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            request_id CHAR(36) NOT NULL,
                            input_word VARCHAR(3) NOT NULL,
                            token VARCHAR(255) NOT NULL,
                            token_id INT NOT NULL,
                            embedding JSON NOT NULL,
                            embedding_dimension INT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            INDEX request_id_idx (request_id)
                        )
                        """
                    )
                conn.commit()
        except Error as exc:
            if getattr(exc, "errno", None) == 1045:
                raise DatabaseError(
                    "MySQL login failed. Set MYSQL_USER and MYSQL_PASSWORD in .env."
                ) from exc
            raise DatabaseError("Could not initialize the MySQL database.") from exc

    def create_user(self, email: str, password_hash: str) -> int:
        try:
            with self._database_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                        (email, password_hash),
                    )
                    user_id = cursor.lastrowid
                conn.commit()
            return int(user_id)
        except Error as exc:
            if getattr(exc, "errno", None) == 1062:
                raise DatabaseError("An account with this email already exists.") from exc
            if getattr(exc, "errno", None) == 1045:
                raise DatabaseError(
                    "MySQL login failed. Set MYSQL_USER and MYSQL_PASSWORD in .env."
                ) from exc
            raise DatabaseError("Could not create the account.") from exc

    def get_user(self, email: str):
        try:
            with self._database_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT id, email, password_hash FROM users WHERE email = %s",
                        (email,),
                    )
                    return cursor.fetchone()
        except Error as exc:
            if getattr(exc, "errno", None) == 1045:
                raise DatabaseError(
                    "MySQL login failed. Set MYSQL_USER and MYSQL_PASSWORD in .env."
                ) from exc
            raise DatabaseError("Could not retrieve the account.") from exc

    def save_history(self, input_word: str, embeddings) -> None:
        request_id = str(uuid4())
        query = """
            INSERT INTO tokenization_history
                (request_id, input_word, token, token_id, embedding, embedding_dimension)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = [
            (
                request_id,
                input_word,
                item.token,
                item.token_id,
                json.dumps(item.vector),
                item.dimension,
            )
            for item in embeddings
        ]

        try:
            with self._database_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.executemany(query, values)
                conn.commit()
        except Error as exc:
            raise DatabaseError("Could not save tokenization history.") from exc

    def fetch_history(self) -> list[HistoryEntry]:
        query = """
            SELECT request_id, input_word, token, token_id, embedding, embedding_dimension, created_at
            FROM tokenization_history
            ORDER BY created_at DESC, id ASC
        """

        try:
            with self._database_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
        except Error as exc:
            raise DatabaseError("Could not retrieve tokenization history.") from exc

        grouped = defaultdict(list)
        metadata = {}
        for row in rows:
            key = row["request_id"]
            metadata[key] = (
                row["input_word"],
                row["created_at"].isoformat(sep=" ", timespec="seconds"),
            )
            grouped[key].append(
                HistoryToken(
                    token=row["token"],
                    token_id=int(row["token_id"]),
                    embedding=self._parse_embedding(row["embedding"]),
                    embedding_dimension=int(row["embedding_dimension"]),
                )
            )

        return [
            HistoryEntry(
                input_word=metadata[request_id][0],
                created_at=metadata[request_id][1],
                tokens=tokens,
            )
            for request_id, tokens in grouped.items()
        ]

    def _parse_embedding(self, value) -> list[float]:
        if isinstance(value, list):
            return [float(item) for item in value]
        return [float(item) for item in json.loads(value)]

    def clear_history(self) -> None:
        try:
            with self._database_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM tokenization_history")
                conn.commit()
        except Error as exc:
            raise DatabaseError("Could not clear tokenization history.") from exc
