import os
from dotenv import load_dotenv
from peewee import *
from pdb import set_trace

dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

db = PostgresqlDatabase(
    os.environ.get('POSTGRES_DB_NAME'),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'),
    port=5432
)

class BaseModel(Model):
    class Meta:
        database = db

class VideoClip(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField()
    is_static_camera = BooleanField()

class Worker(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField()

class Assignment(BaseModel):
    id = CharField(primary_key=True)
    feedback = CharField()
    video_clip_id = ForeignKeyField(VideoClip)
    worker_id = ForeignKeyField(Worker)
    accepted_at = DateTimeField()
    submitted_at = DateTimeField()
    reward = DecimalField(decimal_places=2)

class Annotations(BaseModel):
    assignment_id = ForeignKeyField(Assignment)
    start = IntegerField()
    end = IntegerField()
    relationship = CharField()

db.connect()

db.create_tables([VideoClip, Worker, Assignment, Annotations])
