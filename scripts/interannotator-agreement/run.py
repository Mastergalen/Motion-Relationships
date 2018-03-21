"""
Print out inter annotator agreement of annotated clips
"""
import argparse
import time
from lib.database.models import *
import lib.mturk.agreement as agreement

parser = argparse.ArgumentParser()
parser.add_argument('--videos_dir', type=str, help='Path to video directory', default='test-videos')
args = parser.parse_args()

query = Assignment.approved()

video_clips = list(query.dicts())

print("Processing {} videos".format(len(video_clips)))

for row in video_clips:
    start = time.time()
    score = agreement.inter_annotator_score(row['video_clip_id'])
    print("{} | Took {}s".format(score, time.time() - start))
