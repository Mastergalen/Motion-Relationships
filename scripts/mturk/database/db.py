import os
from peewee import PostgresqlDatabase
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../../../.env')
load_dotenv(dotenv_path)

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
