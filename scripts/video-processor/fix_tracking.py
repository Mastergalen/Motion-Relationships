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
parser.add_argument('--delete', type=int, help='IDs to delete', nargs='+')
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


def delete(annotations, delete_ids):
    print("Deleting {}".format(delete_ids))

    for frame in annotations:
        frame[:] = [x for x in frame if x[0] not in delete_ids]


def count_unique(annotations):
    ids = set()

    for frame in annotations:
        for annotation in frame:
            ids.add(annotation[0])

    print("{} unique IDs remaining".format(len(ids)))
    print(ids)


print("Editing {}".format(args.clip_id))

path = os.path.join('test-videos', '{}.json'.format(args.clip_id))
with open(path) as f:
    data = json.load(f)

if args.delete is not None:
    delete(data['annotations'], args.delete)

correct(data['annotations'], args.source_ids, args.target)

count_unique(data['annotations'])

with open(path, 'w') as f:
    json.dump(data, f, indent=4)





