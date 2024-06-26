from flask import Flask, request

from sample_app.db import connection_context
from sample_app.models import Quote
from sample_app.repositories import MysqlQuoteRepository


app = Flask(__name__)


@app.route("/quotes")
def list_quotes():
    with connection_context() as connection:
        repos = MysqlQuoteRepository(connection)
        quotes = repos.list_quotes()
        data = [i.__dict__ for i in quotes]
    return {"items": data}


@app.route("/quotes/random")
def get_random_quotes():
    with connection_context() as connection:
        repos = MysqlQuoteRepository(connection)
        quote = repos.get_random_quote()
    return quote.__dict__


@app.route("/quotes", methods=["POST"])
def add_quote():
    json_payload = request.json or {}

    author = json_payload.get("author", "")
    text = json_payload.get("text", "")
    quote = Quote(id=-1, author=author, text=text)

    with connection_context() as connection:
        repos = MysqlQuoteRepository(connection)
        repos.insert_quote(quote)

    return {}
