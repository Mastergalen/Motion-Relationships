import os

from dotenv import load_dotenv
from peewee import PostgresqlDatabase

load_dotenv('.env')

if os.environ.get('POSTGRES_DB_NAME') is None:
    raise ValueError('Env not set')


def database():
    return PostgresqlDatabase(
        os.environ.get('POSTGRES_DB_NAME'),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=5432
    )
