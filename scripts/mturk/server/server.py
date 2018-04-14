"""
Mock MTurk server for handling submissions from annotation-ui
"""
import re
import string
import random
import datetime
from flask import Flask, request

from lib.database.models import *

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)

    assignment_id = 'exp-' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    data = {
        'clip_id': None,
        'feedback': None,
        'annotations': [],
        'worker_id': 'galen'
    }
    pattern = re.compile(r"relationship-(\d+):(\d+)")
    for name, val in request.form.items():
        if name == 'videoId':
            data['clip_id'] = val
        elif name == 'feedback':
            data['feedback'] = val
        elif name.startswith('relationship-'):
            matches = pattern.match(name)
            start = matches.group(1)
            end = matches.group(2)
            data['annotations'].append({
                'assignment_id': assignment_id,
                'start': start,
                'end': end,
                'relationship': val
            })
        elif name == 'assignmentId':
            pass
        else:
            raise Exception('Unknown question identifier')

    clip, _ = VideoClip.get_or_create(id=data['clip_id'])
    worker, _ = Worker.get_or_create(id=data['worker_id'], defaults={'is_expert': True})
    Assignment.get_or_create(
        id=assignment_id,
        defaults={
            'feedback': data['feedback'],
            'video_clip_id': clip.id,
            'worker_id': worker.id,
            'assignment_status': '',
            'accepted_at': datetime.datetime.now(),
            'submitted_at': datetime.datetime.now(),
            'reward': 0
        }
    )
    if len(data['annotations']) > 0:
        Annotation.insert_many(data['annotations']).execute()
    print('Inserted')
    return 'success'
