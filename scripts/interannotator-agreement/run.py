import argparse
import numpy as np
import os
import json
from lib.database.models import *
from lib.types import relationship_to_id
from peewee import fn
from playhouse.shortcuts import model_to_dict

parser = argparse.ArgumentParser()
parser.add_argument('--videos_dir', type=str, help='Path to video directory', default='test-videos')
args = parser.parse_args()


def inter_annotator_score(clip_id):
    res = VideoClip\
        .select()\
        .join(Assignment)\
        .join(Annotation)\
        .where(VideoClip.id == clip_id)

    video_clip = res.get()

    vid_dict = model_to_dict(video_clip, backrefs=True)

    all_ids = all_ids_in_clip(clip_id)
    assignment_count = len(vid_dict['assignment_set'])

    annotations = np.zeros((assignment_count, len(all_ids), len(all_ids)), dtype=np.uint8)
    for i, assignment in enumerate(vid_dict['assignment_set']):
        for annotation in assignment['annotation_set']:
            start_idx = all_ids.index(annotation['start'])
            end_idx = all_ids.index(annotation['end'])
            relationship_id = relationship_to_id[annotation['relationship']]
            annotations[i, start_idx, end_idx] = relationship_id

    pass


def all_ids_in_clip(clip_id):
    """
    Reads all entity IDs in clip from JSON
    :return: Set of IDs in video
    """
    json_path = os.path.join(args.videos_dir, '{}.json'.format(clip_id))
    with open(json_path) as f:
        data = json.load(f)

    ids = set()
    for frame in data['annotations']:
        for annotation in frame:
            ids.add(annotation[0])

    return sorted(ids)


query = Assignment\
    .select(Assignment.video_clip_id, fn.COUNT('*'))\
    .group_by(Assignment.video_clip_id)\
    .having(fn.COUNT('*') > 1)

print(query.sql())

data = list(query.dicts())

print(data)

for row in data:
    inter_annotator_score(row['video_clip_id'])

