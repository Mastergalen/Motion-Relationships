from database.db import database
from database.models import *

db = database()

db.connect()

db.create_tables([VideoClip, Worker, Assignment, Annotation], safe=True)
