"""
Manually fix lost tracking
"""
import argparse
import os
import json


parser = argparse.ArgumentParser()
parser.add_argument('clip_id', type=str, help='Clip ID')
parser.add_argument('target', type=int, help='Target ID')
parser.add_argument('source_ids', type=int, help='Source IDs', nargs='+')
args = parser.parse_args()


def correct(annotations, replace_ids, target_id):
    print("Replacing {} with {}".format(replace_ids, target_id))
    count = 0
    for frame in annotations:
        for annotation in frame:
            if annotation[0] in replace_ids:
                annotation[0] = target_id
                count += 1

    print("Replaced {} annotations".format(count))
    return annotations


print("Editing {}".format(args.clip_id))

path = os.path.join('test-videos', '{}.json'.format(args.clip_id))
with open(path) as f:
    data = json.load(f)

correct(data['annotations'], args.source_ids, args.target)

with open(path, 'w') as f:
    json.dump(data, f, indent=4)





