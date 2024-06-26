from contextlib import closing
from mysql.connector.pooling import PooledMySQLConnection

from sample_app.models import Quote


class QuoteRepository:
    def insert_quote(self, quote: Quote): ...

    def get_random_quote(self) -> Quote: ...

    def list_quotes(self) -> list[Quote]: ...


class MysqlQuoteRepository(QuoteRepository):
    def __init__(self, connection: PooledMySQLConnection):
        self._connection = connection

    def insert_quote(self, quote: Quote):
        cursor = self._connection.cursor()
        with closing(self._connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO quotes(author, text) VALUES (%s, %s)",
                (quote.author, quote.text),
            )
            self._connection.commit()

    def get_random_quote(self) -> Quote:
        with closing(self._connection.cursor()) as cursor:
            cursor.execute(
                "SELECT id, author, text FROM quotes ORDER BY RAND() LIMIT 1"
            )
            record = cursor.fetchone()
            return Quote(
                id=record[0],
                author=record[1],
                text=record[2],
            )

    def list_quotes(self) -> list[Quote]:
        with closing(self._connection.cursor()) as cursor:
            cursor.execute("SELECT id, author, text FROM quotes")
            records = cursor.fetchall()
            results = [
                Quote(
                    id=i[0],
                    author=i[1],
                    text=i[2],
                )
                for i in records
            ]
            return results
