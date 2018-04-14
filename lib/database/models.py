import datetime
from playhouse.shortcuts import model_to_dict
from peewee import *
from peewee import fn
from lib.database.db import database


class BaseModel(Model):
    class Meta:
        database = database()


class VideoClip(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField(null=True)
    is_static_camera = BooleanField(default=False)
    is_ready_to_annotate = BooleanField(default=False)
    cleanup = CharField(null=True)
    has_interactions = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)

    @classmethod
    def annotations(cls, clip_id, expert_only):
        if expert_only:
            data = VideoClip \
                .select() \
                .join(Assignment) \
                .join(Annotation, JOIN.LEFT_OUTER) \
                .join(Worker, on=(Worker.id == Assignment.worker_id)) \
                .where((VideoClip.id == clip_id) & Worker.is_expert) \
                .get()
        else:
            data = VideoClip \
                .select() \
                .join(Assignment) \
                .join(Annotation, JOIN.LEFT_OUTER) \
                .join(Worker, on=(Worker.id == Assignment.worker_id)) \
                .where((VideoClip.id == clip_id) & ~Worker.is_expert) \
                .get()

        vid_dict = model_to_dict(data, backrefs=True)

        return vid_dict['assignment_set']


class Worker(BaseModel):
    id = CharField(primary_key=True)
    notes = CharField(null=True)
    is_expert = BooleanField(default=False)


class Assignment(BaseModel):
    id = CharField(primary_key=True)
    feedback = CharField(null=True)
    video_clip_id = ForeignKeyField(VideoClip)
    worker_id = ForeignKeyField(Worker)
    assignment_status = CharField()
    accepted_at = DateTimeField()
    submitted_at = DateTimeField()
    reward = DecimalField(decimal_places=2)
    manual_review = CharField(null=True)



    @classmethod
    def approved(cls):
        return Assignment.select(Assignment.video_clip_id, fn.COUNT('*'), fn.MAX(Worker.is_expert.cast('int')).alias('has_expert')) \
            .join(Worker) \
            .where(
                Worker.is_expert |
                (
                    (Assignment.assignment_status == 'Approved') &
                    ((Assignment.manual_review != 'bad') | (Assignment.manual_review.is_null()))
                )  # Not manually dismissed
            ) \
            .group_by(Assignment.video_clip_id) \
            .having((fn.COUNT('*') > 1) | (fn.MAX(Worker.is_expert.cast('int')) > 0))


class Annotation(BaseModel):
    assignment_id = ForeignKeyField(Assignment)
    start = IntegerField()
    end = IntegerField()
    relationship = CharField()
