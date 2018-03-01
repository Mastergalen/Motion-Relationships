"""
Imports assignments completed on Amazon Mechnical Turk to database
"""
import re
import xml.etree.ElementTree as ET
from database.models import *
from lib import apiclient
from pdb import set_trace

def import_mturk():
    print('Importing MTurk data')
    client = apiclient.create(is_production=True)

    hits = client.list_hits()['HITs']

    for hit in hits:
        res = client.list_assignments_for_hit(HITId=hit['HITId'])

        for assignment in res['Assignments']:
            print("Processing assignment {}".format(assignment['AssignmentId']))
            answer = assignment['Answer']

            root = ET.fromstring(answer)

            data = {
                'clip_id': None,
                'feedback': None,
                'annotations': [],
                'worker_id': assignment['WorkerId']
            }

            pattern = re.compile(r"relationship-(\d+):(\d+)")

            for field in root:
                name = field[0].text
                value = field[1].text

                if name == 'videoId':
                    data['clip_id'] = value
                elif name == 'feedback':
                    data['feedback'] = value
                elif name.startswith('relationship-'):
                    matches = pattern.match(name)
                    start = matches.group(1)
                    end = matches.group(2)
                    data['annotations'].append({
                        'assignment_id': assignment['AssignmentId'],
                        'start': start, 
                        'end': end, 
                        'relationship': value
                    })
                else:
                    raise Exception('Unknown question identifier')

            clip, _ = VideoClip.get_or_create(id=data['clip_id'])
            worker, _ = Worker.get_or_create(id=data['worker_id'])
            ass, created = Assignment.get_or_create(
                id=assignment['AssignmentId'],
                defaults={
                    'feedback': data['feedback'],
                    'video_clip_id': clip.id,
                    'worker_id': worker.id,
                    'assignment_status': assignment['AssignmentStatus'],
                    'accepted_at': assignment['AcceptTime'],
                    'submitted_at': assignment['SubmitTime'],
                    'reward': hit['Reward']
                }
            )

            # Only insert annotation if assignment was new
            if created:
                Annotation.insert_many(data['annotations']).execute()
            else:
                print("Already imported {}".format(assignment['AssignmentId']))


    print('All done')


import_mturk()
