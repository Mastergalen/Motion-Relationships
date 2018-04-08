from lib.database.db import database
from lib.database.models import *

db = database()

db.connect()

db.create_tables([VideoClip, Worker, Assignment, Annotation], safe=True)

print('Migration complete')