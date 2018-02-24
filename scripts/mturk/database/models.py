from peewee import *
from database.db import database

class BaseModel(Model):
    class Meta:
        database = database()

class VideoClip(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField(null=True)
    is_static_camera = BooleanField(default=False)

class Worker(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField(null=True)

class Assignment(BaseModel):
    id = CharField(primary_key=True)
    feedback = CharField(null=True)
    video_clip_id = ForeignKeyField(VideoClip)
    worker_id = ForeignKeyField(Worker)
    accepted_at = DateTimeField()
    submitted_at = DateTimeField()
    reward = DecimalField(decimal_places=2)

class Annotation(BaseModel):
    assignment_id = ForeignKeyField(Assignment)
    start = IntegerField()
    end = IntegerField()
    relationship = CharField()
