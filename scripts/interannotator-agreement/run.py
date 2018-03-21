import argparse
import numpy as np
import os
import json
import time
from lib import agreement
from lib.database.models import *
from lib.types import relationship_to_id
from peewee import fn
from playhouse.shortcuts import model_to_dict

parser = argparse.ArgumentParser()
parser.add_argument('--videos_dir', type=str, help='Path to video directory', default='test-videos')
args = parser.parse_args()


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


query = Assignment \
    .select(Assignment.video_clip_id, fn.COUNT('*')) \
    .where(Assignment.assignment_status == 'Approved') \
    .group_by(Assignment.video_clip_id) \
    .having(fn.COUNT('*') > 1)

video_clips = list(query.dicts())

print("Processing {} videos".format(len(video_clips)))

for row in video_clips:
    start = time.time()
    inter_annotator_score(row['video_clip_id'])
    print("Took {}s".format(time.time() - start))
